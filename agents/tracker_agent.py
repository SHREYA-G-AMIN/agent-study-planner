import json
import requests
from config.settings import POLLINATIONS_API_KEY, MODEL_NAME, TEMPERATURE_TRACKING
from json_manager import StudentDataManager


class TrackerAgent:
    def __init__(self, data_manager=None):
        """
        Initialize the Tracker Agent.
        
        Args:
            data_manager: Optional StudentDataManager instance for JSON integration
        """
        # Use direct Pollinations.ai HTTP calls
        self.api_key = POLLINATIONS_API_KEY
        self.model = MODEL_NAME
        self.default_temperature = TEMPERATURE_TRACKING
        self.system_prompt = """You are a study progress tracking AI assistant. Your responsibilities:

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
- Provide clear, actionable insights"""
        
        # JSON integration (optional)
        self.data_manager = data_manager
    
    def track_progress(self, schedule: dict, completed_topics: list):
        """Tracks completion status"""
        completed_str = ", ".join(completed_topics) if completed_topics else "None yet"
        human = (
            "Analyze the student's progress:\n\n"
            f"Schedule: {json.dumps(schedule, indent=2)}\n"
            f"Completed Topics: {completed_str}\n\n"
            "Provide:\n"
            "1. What's been completed\n"
            "2. What's been missed\n"
            "3. Current readiness assessment\n"
            "4. Specific recommendations\n\n"
            "Be encouraging but honest."
        )

        try:
            resp = self._call_openai(self.system_prompt, human, self.default_temperature)
            return {"output": resp, "analysis": resp}
        except Exception as e:
            return {"error": str(e)}
    
    def get_analytics(self, completed_count: int, missed_count: int, streak: int):
        """Gets performance analytics"""
        
        total = completed_count + missed_count
        completion_rate = (completed_count / total * 100) if total > 0 else 0
        
        human = (
            "Generate performance analytics:\n\n"
            f"Completed Tasks: {completed_count}\n"
            f"Missed Tasks: {missed_count}\n"
            f"Current Streak: {streak} days\n"
            f"Completion Rate: {round(completion_rate,1)}%\n\n"
            "Provide:\n"
            "1. Performance assessment\n"
            "2. Strengths and weaknesses\n"
            "3. Actionable recommendations\n"
            "4. Motivational insights\n\n"
            "Be specific and helpful."
        )

        try:
            resp = self._call_openai(self.system_prompt, human, self.default_temperature)
            return {"output": resp, "analytics": resp}
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

    def _call_openai(self, system_prompt: str, human_prompt: str, temperature: float = 0.2) -> str:
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
