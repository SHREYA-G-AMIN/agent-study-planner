#!/usr/bin/env python
"""
Quick demo: Create a new study plan programmatically
"""

from json_manager import StudentDataManager
from datetime import datetime
import json

print("🎓 DEMO: Creating a New Study Plan")
print("=" * 60)

# Create new student data
student_data = {
    "student_id": 2025,
    "student_name": "Alex",
    "study_plan": [
        {
            "date": "2025-11-10",
            "subject": "Mathematics",
            "topic": "Calculus",
            "hours": 4,
            "completed": False,
            "completed_at": None
        },
        {
            "date": "2025-11-12",
            "subject": "Physics",
            "topic": "Quantum Mechanics",
            "hours": 5,
            "completed": False,
            "completed_at": None
        },
        {
            "date": "2025-11-15",
            "subject": "Chemistry",
            "topic": "Organic Chemistry",
            "hours": 3,
            "completed": False,
            "completed_at": None
        }
    ],
    "progress_summary": {
        "total_topics": 3,
        "completed_topics_count": 0,
        "readiness_percentage": 0.0
    },
    "exam_date": "2025-12-01",
    "current_streak": 0,
    "meta": {
        "version": 1,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
}

# Save it
print("\n💾 Saving new plan for Alex...")

# Direct write to ensure it saves
with open("student_study_data.json", 'w', encoding='utf-8') as f:
    json.dump(student_data, f, indent=4)

print("✅ Saved!")

# Verify by reading back
print("\n📖 Verifying by reading back...")
manager = StudentDataManager()
data = manager.load_student_data()

print("\n" + "=" * 60)
print("📊 VERIFICATION RESULTS")
print("=" * 60)
print(f"👤 Student Name: {data['student_name']}")
print(f"🆔 Student ID: {data['student_id']}")
print(f"📚 Total Topics: {len(data['study_plan'])}")
print(f"📅 Exam Date: {data.get('exam_date', 'N/A')}")

print("\n📋 Topics:")
for i, topic in enumerate(data['study_plan'], 1):
    print(f"   {i}. {topic['topic']} ({topic['subject']}) - {topic['hours']}h")

print("\n" + "=" * 60)
print("✅ Demo Complete!")
print("=" * 60)
print("\nNow run: python interactive_planner.py")
print("Choose option 3 to view Alex's plan!")
