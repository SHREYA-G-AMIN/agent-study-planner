import json
import requests
from config.settings import POLLINATIONS_API_KEY, MODEL_NAME, TEMPERATURE_PLANNING
from json_manager import StudentDataManager


class PlannerAgent:
    def __init__(self, data_manager=None):
        """
        Initialize the Planner Agent.
        
        Args:
            data_manager: Optional StudentDataManager instance for JSON integration
        """
        # Use direct Pollinations.ai HTTP calls
        self.api_key = POLLINATIONS_API_KEY
        self.model = MODEL_NAME
        self.default_temperature = TEMPERATURE_PLANNING
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
        human = (
            "Create a comprehensive study schedule with these details:\n\n"
            f"Syllabus: {json.dumps(syllabus, indent=2)}\n"
            f"Exam Date: {exam_date}\n"
            f"Available Hours Per Day: {available_hours}\n\n"
            "Provide a day-by-day study plan with:\n"
            "- Date and topics to cover each day\n"
            "- Estimated hours needed\n"
            "- Include 2 revision days before exam\n"
            "- Ensure workload is balanced\n\n"
            "Respond with actionable recommendations."
        )

        try:
            resp = self._call_openai(self.system_prompt, human, self.default_temperature)
            return {"output": resp, "schedule": resp}
        except Exception as e:
            return {"error": str(e)}
    
    def adjust_schedule(self, current_schedule: dict, missed_tasks: list, available_hours: int):
        """Adjusts schedule for missed tasks"""
        human = (
            "A student has fallen behind schedule. Please rebalance their study plan:\n\n"
            f"Current Schedule: {json.dumps(current_schedule, indent=2)}\n"
            f"Missed/Pending Tasks: {json.dumps(missed_tasks, indent=2)}\n"
            f"Available Hours Per Day: {available_hours}\n\n"
            "Create an adjusted schedule that:\n"
            "1. Prioritizes missed tasks\n"
            "2. Doesn't overload any single day\n"
            "3. Maintains realistic goals\n"
            "4. Provides encouragement\n\n"
            "Give practical recommendations."
        )

        try:
            resp = self._call_openai(self.system_prompt, human, self.default_temperature)
            return {"output": resp, "adjusted_schedule": resp}
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

    def _call_openai(self, system_prompt: str, human_prompt: str, temperature: float = 0.3) -> str:
        """Simple Pollinations.ai ChatCompletions call returning the assistant text."""
        if not self.api_key:
            raise RuntimeError("POLLINATIONS_API_KEY not configured in config.settings")

        url = "https://enter.pollinations.ai/api/generate/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": human_prompt}
            ],
            "temperature": temperature
        }

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            j = r.json()
            # Extract assistant reply
            return j["choices"][0]["message"]["content"].strip()
        except requests.exceptions.HTTPError as e:
            # Try to get error details from response
            error_msg = str(e)
            try:
                error_details = r.json() if hasattr(r, 'json') else {}
                error_msg = f"{error_msg}. Response: {error_details}"
            except:
                error_msg = f"{error_msg}. Response text: {r.text[:200] if hasattr(r, 'text') else 'N/A'}"
            raise RuntimeError(f"Pollinations.ai API error: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Pollinations.ai API request failed: {str(e)}")
