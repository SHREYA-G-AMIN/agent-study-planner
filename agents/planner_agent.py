from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE_PLANNING
from json_manager import StudentDataManager
import json


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
        
        self.system_prompt = """You are an intelligent study planner AI assistant. Your responsibilities:

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
- Respond in clear, structured format"""
        
        # JSON integration (optional)
        self.data_manager = data_manager
    
    def create_schedule(self, syllabus: dict, exam_date: str, available_hours: int):
        """Creates a new study schedule"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """Create a comprehensive study schedule with these details:

Syllabus: {syllabus}
Exam Date: {exam_date}
Available Hours Per Day: {available_hours}

Provide a day-by-day study plan with:
- Date and topics to cover each day
- Estimated hours needed
- Include 2 revision days before exam
- Ensure workload is balanced

Respond with actionable recommendations.""")
        ])
        
        try:
            chain = prompt | self.llm
            result = chain.invoke({
                "syllabus": json.dumps(syllabus, indent=2),
                "exam_date": exam_date,
                "available_hours": available_hours
            })
            return {"output": result.content, "schedule": result.content}
        except Exception as e:
            return {"error": str(e)}
    
    def adjust_schedule(self, current_schedule: dict, missed_tasks: list, available_hours: int):
        """Adjusts schedule for missed tasks"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """A student has fallen behind schedule. Please rebalance their study plan:

Current Schedule: {current_schedule}
Missed/Pending Tasks: {missed_tasks}
Available Hours Per Day: {available_hours}

Create an adjusted schedule that:
1. Prioritizes missed tasks
2. Doesn't overload any single day  
3. Maintains realistic goals
4. Provides encouragement

Give practical recommendations.""")
        ])

        try:
            chain = prompt | self.llm
            result = chain.invoke({
                "current_schedule": json.dumps(current_schedule, indent=2),
                "missed_tasks": json.dumps(missed_tasks, indent=2),
                "available_hours": available_hours
            })
            return {"output": result.content, "adjusted_schedule": result.content}
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
