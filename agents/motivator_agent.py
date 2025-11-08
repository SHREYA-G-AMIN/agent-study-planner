from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE_MOTIVATION
from tools.study_tools import get_progress_analytics
from json_manager import StudentDataManager


class MotivatorAgent:
    def __init__(self, data_manager=None):
        """
        Initialize the Motivator Agent.
        
        Args:
            data_manager: Optional StudentDataManager instance for JSON integration
        """
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE_MOTIVATION
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a supportive and encouraging study motivation coach. Your responsibilities:

1. Generate personalized motivational messages
2. Celebrate achievements and milestones
3. Provide constructive feedback for setbacks
4. Create engaging weekly summaries
5. Maintain positive but realistic tone

Guidelines:
- Adapt your style based on student's progress
- Be genuinely encouraging, not generic
- Acknowledge challenges while promoting growth
- Use emojis and friendly language appropriately
- Focus on progress, not perfection

You help students stay motivated and consistent in their study journey."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.tools = [get_progress_analytics]
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
    
    def daily_motivation(self, completed_count: int, missed_count: int, streak: int):
        """Generates daily motivational message"""
        input_text = f"""Create a motivational message for a student:

Completed Tasks: {completed_count}
Missed Tasks: {missed_count}
Current Streak: {streak} days

First use get_progress_analytics, then craft a personalized, encouraging message based on their performance.
Keep it concise (2-3 sentences) and genuinely supportive."""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def weekly_summary(self, completed_count: int, missed_count: int, streak: int):
        """Creates weekly progress summary"""
        input_text = f"""Create a comprehensive weekly summary for a student:

This Week's Stats:
- Completed Tasks: {completed_count}
- Missed Tasks: {missed_count}
- Study Streak: {streak} days

Use get_progress_analytics and then create an engaging weekly report that includes:
1. Key achievements
2. Areas for improvement
3. Encouraging next steps
4. Overall performance assessment

Make it motivating and actionable!"""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ========== JSON-Integrated Methods ==========
    
    def motivate_from_json(self):
        """
        Generate motivational message based on JSON data.
        
        Returns:
            Motivational message dict
        """
        if not self.data_manager:
            print("⚠️ No data_manager provided. Cannot use JSON integration.")
            return {"error": "No data_manager configured"}
        
        print("🚀 Generating motivation from JSON...")
        
        # Load data
        data = self.data_manager.load_student_data()
        progress = data.get("progress_summary", {})
        
        # Calculate metrics
        completed_count = progress.get("completed_topics_count", 0)
        total_topics = progress.get("total_topics", 0)
        missed_count = total_topics - completed_count
        streak = data.get("current_streak", 0)
        readiness = progress.get("readiness_percentage", 0)
        
        # Get pending topics for personalization
        pending_topics = self.data_manager.get_pending_topics()
        pending_count = len(pending_topics)
        
        # Generate personalized motivation
        motivation = self.daily_motivation(completed_count, missed_count, streak)
        
        # Add context
        context = {
            "motivation": motivation,
            "readiness": readiness,
            "completed": completed_count,
            "pending": pending_count,
            "streak": streak
        }
        
        print(f"✅ Motivation generated! Readiness: {readiness}%")
        
        return context
    
    def weekly_summary_from_json(self):
        """
        Generate weekly summary based on JSON data.
        
        Returns:
            Weekly summary dict
        """
        if not self.data_manager:
            print("⚠️ No data_manager provided. Cannot use JSON integration.")
            return {"error": "No data_manager configured"}
        
        print("📊 Generating weekly summary from JSON...")
        
        # Load data
        data = self.data_manager.load_student_data()
        progress = data.get("progress_summary", {})
        
        # Calculate metrics
        completed_count = progress.get("completed_topics_count", 0)
        total_topics = progress.get("total_topics", 0)
        missed_count = total_topics - completed_count
        streak = data.get("current_streak", 0)
        
        # Generate summary
        summary = self.weekly_summary(completed_count, missed_count, streak)
        
        print("✅ Weekly summary generated!")
        
        return summary
