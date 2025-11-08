from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE_MOTIVATION
from json_manager import StudentDataManager
import json


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
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """Create a motivational message for a student:

Completed Tasks: {completed}
Missed Tasks: {missed}
Current Streak: {streak} days

Craft a personalized, encouraging message (2-3 sentences) that:
- Acknowledges their current progress
- Provides genuine encouragement
- Inspires them to keep going

Be warm, supportive, and specific.""")
        ])

        try:
            chain = prompt | self.llm
            result = chain.invoke({
                "completed": completed_count,
                "missed": missed_count,
                "streak": streak
            })
            return {"output": result.content, "message": result.content}
        except Exception as e:
            return {"error": str(e)}
    
    def weekly_summary(self, completed_count: int, missed_count: int, streak: int):
        """Creates weekly progress summary"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """Create a comprehensive weekly summary for a student:

This Week's Stats:
- Completed Tasks: {completed}
- Missed Tasks: {missed}
- Study Streak: {streak} days

Create an engaging weekly report that includes:
1. Key achievements this week
2. Areas for improvement
3. Encouraging next steps
4. Overall performance assessment

Make it motivating, actionable, and celebrate progress!""")
        ])

        try:
            chain = prompt | self.llm
            result = chain.invoke({
                "completed": completed_count,
                "missed": missed_count,
                "streak": streak
            })
            return {"output": result.content, "summary": result.content}
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
