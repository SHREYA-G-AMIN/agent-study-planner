from agents.planner_agent import PlannerAgent
from agents.tracker_agent import TrackerAgent
from agents.motivator_agent import MotivatorAgent
from json_manager import StudentDataManager
from datetime import datetime
import json


class StudyPlannerSystem:
    def __init__(self, use_json=False, json_path="student_study_data.json"):
        """
        Initialize the Study Planner System.
        
        Args:
            use_json: Whether to enable JSON persistence
            json_path: Path to the JSON data file
        """
        print("🚀 Initializing Adaptive Study Planner System...")
        
        # Initialize JSON manager if requested
        self.data_manager = StudentDataManager(json_path) if use_json else None
        
        # Initialize agents (with or without JSON integration)
        self.planner = PlannerAgent(data_manager=self.data_manager)
        self.tracker = TrackerAgent(data_manager=self.data_manager)
        self.motivator = MotivatorAgent(data_manager=self.data_manager)
        
        self.use_json = use_json
        print("✅ All agents initialized successfully!")
        if use_json:
            print(f"💾 JSON persistence enabled: {json_path}\n")
        else:
            print("📝 Running in memory-only mode\n")
    
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
        print("📊 Generating your weekly summary...")
        
        summary_result = self.motivator.weekly_summary(completed_count, missed_count, streak)
        
        return {
            "summary": summary_result,
            "generated_at": datetime.now().isoformat()
        }
    
    # ========== JSON-Driven Workflow Methods ==========
    
    def run_daily_workflow(self, exam_date: str = "2025-11-20", available_hours: int = 3):
        """
        Complete daily workflow using JSON persistence.
        This is the main entry point for JSON-based operations.
        
        Args:
            exam_date: Target exam date
            available_hours: Hours available per day
            
        Returns:
            Dict containing schedule, progress, and motivation
        """
        if not self.use_json:
            print("⚠️ JSON mode not enabled. Initialize with use_json=True")
            return {"error": "JSON mode not enabled"}
        
        print("\n" + "="*60)
        print("📅 DAILY WORKFLOW - JSON Mode")
        print("="*60 + "\n")
        
        # Step 1: Load current data
        print("📂 Step 1: Loading student data...")
        student_data = self.data_manager.load_student_data()
        print(f"   Student: {student_data.get('student_name')}")
        print(f"   Total Topics: {len(student_data.get('study_plan', []))}")
        
        # Step 2: Create or update schedule if needed
        print("\n📚 Step 2: Managing schedule...")
        if "generated_schedule" not in student_data or not student_data.get("generated_schedule"):
            print("   Creating new schedule...")
            schedule = self.planner.create_schedule_from_json(exam_date, available_hours)
        else:
            print("   Schedule exists, checking if adjustment needed...")
            schedule = self.planner.adjust_schedule_from_json()
        
        # Step 3: Update progress
        print("\n📊 Step 3: Tracking progress...")
        progress = self.tracker.track_from_json()
        
        # Step 4: Generate motivation
        print("\n🚀 Step 4: Generating motivation...")
        motivation = self.motivator.motivate_from_json()
        
        # Summary
        print("\n" + "="*60)
        print("🎉 Daily Workflow Complete!")
        print("="*60)
        print(f"\n📊 Progress Summary:")
        print(f"   Readiness: {progress.get('readiness_percentage', 0)}%")
        print(f"   Completed: {progress.get('completed_topics_count', 0)}/{progress.get('total_topics', 0)}")
        print(f"   Streak: {student_data.get('current_streak', 0)} days")
        
        return {
            "schedule": schedule,
            "progress": progress,
            "motivation": motivation,
            "timestamp": datetime.now().isoformat()
        }
    
    def mark_topics_completed(self, topic_names: list):
        """
        Mark topics as completed and update progress.
        
        Args:
            topic_names: List of topic names to mark as completed
            
        Returns:
            Updated progress summary
        """
        if not self.use_json:
            print("⚠️ JSON mode not enabled. Initialize with use_json=True")
            return {"error": "JSON mode not enabled"}
        
        print(f"\n✅ Marking {len(topic_names)} topics as completed...")
        return self.tracker.mark_topics_completed_from_list(topic_names)
    
    def get_summary(self):
        """
        Get a quick summary of student progress from JSON.
        
        Returns:
            Summary dict
        """
        if not self.use_json:
            print("⚠️ JSON mode not enabled. Initialize with use_json=True")
            return {"error": "JSON mode not enabled"}
        
        return self.data_manager.get_summary()


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
    
    # ========== JSON MODE TEST ==========
    print("\n\n" + "#" * 60)
    print("# JSON PERSISTENCE MODE TEST")
    print("#" * 60 + "\n")
    
    # Initialize with JSON mode
    json_system = StudyPlannerSystem(use_json=True)
    
    # Test 1: Run daily workflow
    print("\nTEST 4: JSON Daily Workflow")
    print("="*60)
    result = json_system.run_daily_workflow(
        exam_date="2025-11-20",
        available_hours=3
    )
    
    # Test 2: Mark a topic as completed
    print("\n\nTEST 5: Mark Topics Completed")
    print("="*60)
    json_system.mark_topics_completed(["Algebra"])
    
    # Test 3: Get summary
    print("\n\nTEST 6: Get Summary")
    print("="*60)
    summary = json_system.get_summary()
    print("\n📊 Summary:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    print("\n\n" + "#" * 60)
    print("✅ ALL TESTS COMPLETED (Memory + JSON modes)")
    print("#" * 60)
    
