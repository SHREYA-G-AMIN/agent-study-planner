from agents.planner_agent import PlannerAgent
from agents.tracker_agent import TrackerAgent
from agents.motivator_agent import MotivatorAgent
from datetime import datetime
import json

class StudyPlannerSystem:
    def __init__(self):
        print("🚀 Initializing Adaptive Study Planner System...")
        self.planner = PlannerAgent()
        self.tracker = TrackerAgent()
        self.motivator = MotivatorAgent()
        print("✅ All agents initialized successfully!\n")
    
    def create_new_plan(self, syllabus: dict, exam_date: str, available_hours: int):
        """Creates initial study plan for a new student"""
        print("📚 Creating your personalized study plan...")
        
        # Create schedule
        schedule_result = self.planner.create_schedule(syllabus, exam_date, available_hours)
        
        # Get initial motivation
        motivation_result = self.motivator.daily_motivation(0, 0, 0)
        
        return {
            "schedule": schedule_result,
            "motivation": motivation_result,
            "created_at": datetime.now().isoformat()
        }
    
    def daily_check_in(self, schedule: dict, completed_topics: list, current_streak: int):
        """Daily progress tracking and adjustment"""
        print("📊 Checking your daily progress...")
        
        # Track progress
        progress_result = self.tracker.track_progress(schedule, completed_topics)
        
        # Get analytics
        completed_count = len(completed_topics)
        missed_count = len(schedule.get("schedule", [])) - completed_count
        
        analytics_result = self.tracker.get_analytics(completed_count, missed_count, current_streak)
        
        # Get motivation
        motivation_result = self.motivator.daily_motivation(completed_count, missed_count, current_streak)
        
        # Check if replanning needed
        needs_replan = missed_count > 2  # If more than 2 tasks missed
        
        adjusted_schedule = None
        if needs_replan:
            print("⚠️ Detected delays. Adjusting your schedule...")
            # Extract missed tasks from progress result
            adjusted_schedule = self.planner.adjust_schedule(
                schedule, 
                [],  # You'd extract this from progress_result
                schedule.get("available_hours", 3)
            )
        
        return {
            "progress": progress_result,
            "analytics": analytics_result,
            "motivation": motivation_result,
            "needs_replan": needs_replan,
            "adjusted_schedule": adjusted_schedule
        }
    
    def get_weekly_summary(self, completed_count: int, missed_count: int, streak: int):
        """Generates weekly progress summary"""
        print("📈 Generating your weekly summary...")
        
        summary_result = self.motivator.weekly_summary(completed_count, missed_count, streak)
        
        return {
            "summary": summary_result,
            "generated_at": datetime.now().isoformat()
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize system
    system = StudyPlannerSystem()
    
    # Test data
    test_syllabus = {
        "Data Structures": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees"],
        "Algorithms": ["Sorting", "Searching", "Dynamic Programming"],
        "Databases": ["SQL Basics", "Normalization", "Transactions"]
    }
    
    test_exam_date = "2025-11-15"
    test_available_hours = 3
    
    print("="*60)
    print("TEST 1: Creating New Study Plan")
    print("="*60)
    
    result = system.create_new_plan(
        syllabus=test_syllabus,
        exam_date=test_exam_date,
        available_hours=test_available_hours
    )
    
    print("\n📋 RESULT:")
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*60)
    print("TEST 2: Daily Check-in")
    print("="*60)
    
    # Simulate some progress
    test_schedule = result.get("schedule", {})
    test_completed = ["Arrays", "Linked Lists"]
    test_streak = 2
    
    daily_result = system.daily_check_in(
        schedule=test_schedule,
        completed_topics=test_completed,
        current_streak=test_streak
    )
    
    print("\n📋 RESULT:")
    print(json.dumps(daily_result, indent=2))
    
    print("\n" + "="*60)
    print("TEST 3: Weekly Summary")
    print("="*60)
    
    weekly_result = system.get_weekly_summary(
        completed_count=5,
        missed_count=1,
        streak=4
    )
    
    print("\n📋 RESULT:")
    print(json.dumps(weekly_result, indent=2))
    
    print("\n✅ All tests completed!")
    