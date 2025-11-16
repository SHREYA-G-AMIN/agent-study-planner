import json
import requests
from config.settings import POLLINATIONS_API_KEY, MODEL_NAME, TEMPERATURE_MOTIVATION
from json_manager import StudentDataManager


class MotivatorAgent:
    def __init__(self, data_manager=None):
        """
        Initialize the Motivator Agent.
        
        Args:
            data_manager: Optional StudentDataManager instance for JSON integration
        """
        # Use direct Pollinations.ai HTTP calls
        self.api_key = POLLINATIONS_API_KEY
        self.model = MODEL_NAME
        self.default_temperature = TEMPERATURE_MOTIVATION
        self.system_prompt = """You are a supportive and encouraging study motivation coach. Your responsibilities:

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

You help students stay motivated and consistent in their study journey."""
        
        # JSON integration (optional)
        self.data_manager = data_manager
    
    def daily_motivation(self, completed_count: int, missed_count: int, streak: int):
        """Generates daily motivational message"""
        human = (
            "Create a motivational message for a student:\n\n"
            f"Completed Tasks: {completed_count}\n"
            f"Missed Tasks: {missed_count}\n"
            f"Current Streak: {streak} days\n\n"
            "Craft a personalized, encouraging message (2-3 sentences) that:\n"
            "- Acknowledges their current progress\n"
            "- Provides genuine encouragement\n"
            "- Inspires them to keep going\n\n"
            "Be warm, supportive, and specific."
        )

        try:
            resp = self._call_openai(self.system_prompt, human, self.default_temperature)
            return {"output": resp, "message": resp}
        except Exception as e:
            return {"error": str(e)}
    
    def weekly_summary(self, completed_count: int, missed_count: int, streak: int):
        """Creates weekly progress summary"""
        human = (
            "Create a comprehensive weekly summary for a student:\n\n"
            f"This Week's Stats:\n- Completed Tasks: {completed_count}\n- Missed Tasks: {missed_count}\n- Study Streak: {streak} days\n\n"
            "Create an engaging weekly report that includes:\n"
            "1. Key achievements this week\n"
            "2. Areas for improvement\n"
            "3. Encouraging next steps\n"
            "4. Overall performance assessment\n\n"
            "Make it motivating, actionable, and celebrate progress!"
        )

        try:
            resp = self._call_openai(self.system_prompt, human, self.default_temperature)
            return {"output": resp, "summary": resp}
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

    def _call_openai(self, system_prompt: str, human_prompt: str, temperature: float = 0.7) -> str:
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
