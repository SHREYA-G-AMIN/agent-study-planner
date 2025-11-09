#!/usr/bin/env python
"""
Interactive Study Planner - Takes user input and creates personalized plans
With Firebase sync and auto streak tracking
"""

from json_manager import StudentDataManager
from datetime import datetime, timedelta
import json

# Firebase configuration
STUDENT_ID = "sher_amin"  # Change to your GitHub username or consistent ID
USE_FIREBASE = True  # Set to False to test offline

def welcome():
    """Display welcome message"""
    print("\n" + "="*60)
    print("🎓 INTERACTIVE STUDY PLANNER")
    print("="*60)
    print("Create your personalized study plan!\n")

def get_student_info():
    """Get student information from user"""
    print("📝 Student Information")
    print("-" * 40)
    
    name = input("What's your name? ")
    student_id = input("Student ID (or press Enter for auto): ")
    
    if not student_id:
        student_id = hash(name) % 10000  # Generate simple ID
    
    return {
        "student_id": int(student_id) if student_id.isdigit() else student_id,
        "student_name": name
    }

def get_study_topics():
    """Get study topics from user"""
    print("\n📚 Study Topics")
    print("-" * 40)
    print("Enter your study topics (one at a time)")
    print("Type 'done' when finished\n")
    
    topics = []
    topic_num = 1
    
    while True:
        subject = input(f"Topic {topic_num} - Subject: ")
        if subject.lower() == 'done':
            break
        
        topic = input(f"Topic {topic_num} - Topic name: ")
        if topic.lower() == 'done':
            break
            
        hours = input(f"Topic {topic_num} - Estimated hours (default: 3): ")
        hours = int(hours) if hours.isdigit() else 3
        
        date = input(f"Topic {topic_num} - Start date (YYYY-MM-DD) or press Enter for today: ")
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        topics.append({
            "date": date,
            "subject": subject,
            "topic": topic,
            "hours": hours,
            "completed": False,
            "completed_at": None
        })
        
        topic_num += 1
        print(f"✅ Added: {topic} ({subject})\n")
    
    return topics

def get_exam_date():
    """Get exam date from user"""
    print("\n📅 Exam Schedule")
    print("-" * 40)
    
    exam_date = input("Enter exam date (YYYY-MM-DD): ")
    if not exam_date:
        # Default to 30 days from now
        exam_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        print(f"Using default: {exam_date}")
    
    return exam_date

def create_new_student_plan():
    """Complete workflow to create a new student plan"""
    welcome()
    
    # Get student info
    student_info = get_student_info()
    
    # Get topics
    topics = get_study_topics()
    
    if not topics:
        print("⚠️ No topics added. Exiting...")
        return
    
    # Get exam date
    exam_date = get_exam_date()
    
    # Create the complete data structure
    student_data = {
        "student_id": student_info["student_id"],
        "student_name": student_info["student_name"],
        "study_plan": topics,
        "progress_summary": {
            "total_topics": len(topics),
            "completed_topics_count": 0,
            "readiness_percentage": 0.0
        },
        "exam_date": exam_date,
        "current_streak": 0,
        "meta": {
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    }
    
    # Save to JSON with Firebase sync
    print("\n💾 Saving your study plan...")
    manager = StudentDataManager(use_firebase=USE_FIREBASE, student_id=STUDENT_ID)
    
    # Use manager to save (handles Firebase sync)
    manager.save_student_data(student_data)
    
    print("✅ Data saved successfully!")
    
    # Display summary
    print("\n" + "="*60)
    print("✅ STUDY PLAN CREATED!")
    print("="*60)
    print(f"\n👤 Student: {student_info['student_name']}")
    print(f"📚 Total Topics: {len(topics)}")
    print(f"📅 Exam Date: {exam_date}")
    print(f"\n📋 Topics:")
    for i, topic in enumerate(topics, 1):
        print(f"   {i}. {topic['topic']} ({topic['subject']}) - {topic['hours']}h")
    
    print(f"\n💾 Saved to: student_study_data.json")
    print(f"☁️  Synced to Firebase for student: {STUDENT_ID}")
    print("\n✅ You can now track your progress!")
    
    return student_data

def update_progress():
    """Interactive progress update"""
    print("\n" + "="*60)
    print("📊 UPDATE PROGRESS")
    print("="*60)
    
    manager = StudentDataManager(use_firebase=USE_FIREBASE, student_id=STUDENT_ID)
    
    # Load current data
    data = manager.load_student_data()
    
    print(f"\n👤 Student: {data.get('student_name')}")
    print(f"📚 Total Topics: {len(data.get('study_plan', []))}")
    
    # Show pending topics
    pending = manager.get_pending_topics()
    
    if not pending:
        print("\n🎉 All topics completed!")
        return
    
    print(f"\n📝 Pending Topics:")
    for i, topic in enumerate(pending, 1):
        print(f"   {i}. {topic['topic']} ({topic['subject']})")
    
    # Mark topics as completed
    print("\nMark topics as completed:")
    print("Enter topic numbers (comma-separated) or 'skip':")
    
    choice = input("Topics to mark complete: ")
    
    if choice.lower() != 'skip':
        try:
            indices = [int(x.strip())-1 for x in choice.split(',')]
            for idx in indices:
                if 0 <= idx < len(pending):
                    topic_name = pending[idx]['topic']
                    manager.mark_topic_completed(topic_name)
        except:
            print("⚠️ Invalid input")
    
    # Auto-update streak when studying
    manager.auto_update_streak()
    
    # Show updated summary
    summary = manager.get_summary()
    print("\n" + "="*60)
    print("📊 UPDATED PROGRESS")
    print("="*60)
    print(f"✅ Completed: {summary['completed']}/{summary['total_topics']}")
    print(f"📈 Readiness: {summary['readiness']}%")
    print(f"🔥 Streak: {summary['streak']} days")

def view_summary():
    """View current progress summary"""
    print("\n" + "="*60)
    print("📊 PROGRESS SUMMARY")
    print("="*60)
    
    manager = StudentDataManager(use_firebase=USE_FIREBASE, student_id=STUDENT_ID)
    summary = manager.get_summary()
    
    print(f"\n👤 Student: {summary['student_name']}")
    print(f"📚 Total Topics: {summary['total_topics']}")
    print(f"✅ Completed: {summary['completed']}")
    print(f"⏳ Pending: {summary['pending']}")
    print(f"📈 Readiness: {summary['readiness']}%")
    print(f"🔥 Study Streak: {summary['streak']} days")
    
    # Show completed topics
    completed = manager.get_completed_topics()
    if completed:
        print(f"\n✅ Completed Topics:")
        for topic in completed:
            print(f"   - {topic['topic']} ({topic['subject']})")
    
    # Show pending topics
    pending = manager.get_pending_topics()
    if pending:
        print(f"\n⏳ Pending Topics:")
        for topic in pending:
            print(f"   - {topic['topic']} ({topic['subject']})")

def main_menu():
    """Main menu for interactive planner"""
    while True:
        print("\n" + "="*60)
        print("🎓 STUDY PLANNER MENU")
        print("="*60)
        print("1. Create New Study Plan")
        print("2. Update Progress")
        print("3. View Summary")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == "1":
            create_new_student_plan()
        elif choice == "2":
            update_progress()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            print("\n👋 Goodbye! Keep studying! 📚")
            break
        else:
            print("⚠️ Invalid option")

if __name__ == "__main__":
    main_menu()