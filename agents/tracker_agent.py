from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE_TRACKING
from tools.study_tools import check_completion_status, get_progress_analytics
from json_manager import StudentDataManager


class TrackerAgent:
    def __init__(self, data_manager=None):
        """
        Initialize the Tracker Agent.
        
        Args:
            data_manager: Optional StudentDataManager instance for JSON integration
        """
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE_TRACKING
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a study progress tracking AI assistant. Your responsibilities:

1. Monitor daily task completion accurately
2. Identify patterns in student behavior
3. Calculate readiness and completion percentages
4. Detect when students are falling behind
5. Provide objective progress assessments

Guidelines:
- Be accurate and data-driven
- Identify both strengths and areas for improvement
- Alert when intervention is needed
- Track streaks and consistency

Always use the provided tools to analyze progress data."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.tools = [check_completion_status, get_progress_analytics]
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
        # JSON integration (optional)
        self.data_manager = data_manager
    
    def track_progress(self, schedule: dict, completed_topics: list):
        """Tracks completion status"""
        import json
        
        completed_str = ",".join(completed_topics)
        
        input_text = f"""Analyze the student's progress:

Schedule: {json.dumps(schedule, indent=2)}
Completed Topics: {completed_str}

Use check_completion_status to analyze what's been completed and what's been missed.
Provide a clear assessment of their current standing."""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def get_analytics(self, completed_count: int, missed_count: int, streak: int):
        """Gets performance analytics"""
        input_text = f"""Generate performance analytics:

Completed Tasks: {completed_count}
Missed Tasks: {missed_count}
Current Streak: {streak} days

Use get_progress_analytics to create a comprehensive performance report."""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ========== JSON-Integrated Methods ==========
    
    def track_from_json(self):
        """
        Track progress using data from JSON file.
        Updates progress summary automatically.
        
        Returns:
            Updated progress summary dict
        """
        if not self.data_manager:
            print("⚠️ No data_manager provided. Cannot use JSON integration.")
            return {"error": "No data_manager configured"}
        
        print("📊 Tracking progress from JSON...")
        
        # Update progress calculations
        updated_data = self.data_manager.update_progress()
        
        # Get progress summary
        progress = updated_data.get("progress_summary", {})
        
        # Print summary
        print(f"   Total Topics: {progress.get('total_topics', 0)}")
        print(f"   Completed: {progress.get('completed_topics_count', 0)}")
        print(f"   Readiness: {progress.get('readiness_percentage', 0)}%")
        
        return progress
    
    def get_analytics_from_json(self):
        """
        Generate analytics based on JSON data.
        
        Returns:
            Analytics report dict
        """
        if not self.data_manager:
            print("⚠️ No data_manager provided. Cannot use JSON integration.")
            return {"error": "No data_manager configured"}
        
        print("📊 Generating analytics from JSON...")
        
        # Load data
        data = self.data_manager.load_student_data()
        progress = data.get("progress_summary", {})
        
        # Calculate metrics
        completed_count = progress.get("completed_topics_count", 0)
        total_topics = progress.get("total_topics", 0)
        missed_count = total_topics - completed_count
        streak = data.get("current_streak", 0)
        
        # Get analytics using existing method
        analytics = self.get_analytics(completed_count, missed_count, streak)
        
        return analytics
    
    def mark_topics_completed_from_list(self, topic_names: list):
        """
        Mark multiple topics as completed and update progress.
        
        Args:
            topic_names: List of topic names to mark as completed
            
        Returns:
            Updated progress summary
        """
        if not self.data_manager:
            print("⚠️ No data_manager provided. Cannot use JSON integration.")
            return {"error": "No data_manager configured"}
        
        print(f"✅ Marking {len(topic_names)} topics as completed...")
        
        # Mark each topic
        for topic_name in topic_names:
            self.data_manager.mark_topic_completed(topic_name)
        
        # Return updated progress
        return self.track_from_json()
