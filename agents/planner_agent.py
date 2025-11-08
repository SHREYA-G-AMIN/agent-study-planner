from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE_PLANNING
from tools.study_tools import calculate_study_hours, rebalance_schedule
from json_manager import StudentDataManager


class PlannerAgent:
    def __init__(self, data_manager=None):
        """
        Initialize the Planner Agent.
        
        Args:
            data_manager: Optional StudentDataManager instance for JSON integration
        """
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME,
            temperature=TEMPERATURE_PLANNING
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent study planner AI assistant. Your responsibilities:

1. Create realistic, balanced study schedules
2. Break down complex syllabi into manageable daily tasks
3. Ensure even workload distribution
4. Always include revision time before exams
5. Adjust schedules when students fall behind

Guidelines:
- Never overload a single day with too many hours
- Prioritize difficult topics earlier in the schedule
- Leave buffer time for unexpected delays
- Be encouraging and supportive in your responses

Always use the provided tools to calculate and adjust schedules."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.tools = [calculate_study_hours, rebalance_schedule]
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
    
    def create_schedule(self, syllabus: dict, exam_date: str, available_hours: int):
        """Creates a new study schedule"""
        import json
        
        input_text = f"""Create a comprehensive study schedule with these details:

Syllabus: {json.dumps(syllabus, indent=2)}
Exam Date: {exam_date}
Available Hours Per Day: {available_hours}

Use the calculate_study_hours tool to create a detailed daily schedule.
Make sure to include revision days before the exam."""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def adjust_schedule(self, current_schedule: dict, missed_tasks: list, available_hours: int):
        """Adjusts schedule for missed tasks"""
        import json
        
        input_text = f"""A student has fallen behind schedule. Please rebalance their study plan:

Current Schedule: {json.dumps(current_schedule, indent=2)}
Missed Tasks: {json.dumps(missed_tasks, indent=2)}
Available Hours Per Day: {available_hours}

Use the rebalance_schedule tool to create an adjusted schedule that:
1. Prioritizes missed tasks
2. Doesn't overload any single day
3. Maintains realistic goals"""

        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ========== JSON-Integrated Methods ==========
    
    def create_schedule_from_json(self, exam_date: str = "2025-11-20", available_hours: int = 3):
        """
        Create schedule using data from JSON file.
        
        Args:
            exam_date: Target exam date (YYYY-MM-DD)
            available_hours: Hours available per day for study
            
        Returns:
            Generated schedule dict
        """
        if not self.data_manager:
            print("⚠️ No data_manager provided. Cannot use JSON integration.")
            return {"error": "No data_manager configured"}
        
        print("📚 Creating schedule from JSON data...")
        
        # Load current student data
        student_data = self.data_manager.load_student_data()
        
        # Build syllabus from study_plan
        syllabus = {}
        for item in student_data.get("study_plan", []):
            subject = item.get("subject")
            topic = item.get("topic")
            
            if subject not in syllabus:
                syllabus[subject] = []
            if topic not in syllabus[subject]:
                syllabus[subject].append(topic)
        
        if not syllabus:
            print("⚠️ No topics found in study plan")
            return {"error": "No topics in study plan"}
        
        # Generate schedule using existing method
        schedule = self.create_schedule(syllabus, exam_date, available_hours)
        
        # Save schedule back to JSON
        student_data["generated_schedule"] = schedule
        student_data["exam_date"] = exam_date
        student_data["available_hours_per_day"] = available_hours
        self.data_manager.save_student_data(student_data)
        
        print("✅ Schedule created and saved to JSON")
        return schedule
    
    def adjust_schedule_from_json(self):
        """
        Adjust schedule based on pending topics in JSON.
        Automatically detects missed tasks and rebalances.
        
        Returns:
            Adjusted schedule dict
        """
        if not self.data_manager:
            print("⚠️ No data_manager provided. Cannot use JSON integration.")
            return {"error": "No data_manager configured"}
        
        print("🔄 Adjusting schedule based on current progress...")
        
        # Load current data
        student_data = self.data_manager.load_student_data()
        
        # Get pending topics (not completed)
        pending_topics = self.data_manager.get_pending_topics()
        
        if not pending_topics:
            print("🎉 All topics completed! No adjustment needed.")
            return {"message": "All topics completed"}
        
        # Get current schedule
        current_schedule = student_data.get("generated_schedule", {})
        
        # Available hours
        available_hours = student_data.get("available_hours_per_day", 3)
        
        # Adjust schedule
        adjusted = self.adjust_schedule(current_schedule, pending_topics, available_hours)
        
        # Save adjusted schedule
        student_data["generated_schedule"] = adjusted
        self.data_manager.save_student_data(student_data)
        
        print(f"✅ Schedule adjusted for {len(pending_topics)} pending topics")
        return adjusted
