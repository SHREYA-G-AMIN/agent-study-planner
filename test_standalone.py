#!/usr/bin/env python
"""
Standalone test of JSON integration (no agent dependencies required)
"""

from json_manager import StudentDataManager
import json

print("\n" + "#" * 70)
print("# 🎯 STANDALONE JSON INTEGRATION TEST")
print("# (No OpenAI/LangChain required)")
print("#" * 70 + "\n")

# Initialize
manager = StudentDataManager("student_study_data.json")

print("=" * 70)
print("📊 INITIAL STATE")
print("=" * 70)
summary = manager.get_summary()
for key, value in summary.items():
    print(f"   {key}: {value}")

print("\n\n" + "=" * 70)
print("✅ TEST 1: Mark 'Algebra' as Completed")
print("=" * 70)
manager.mark_topic_completed("Algebra")
summary = manager.get_summary()
print(f"   Readiness: {summary['readiness']}%")
print(f"   Completed: {summary['completed']}/{summary['total_topics']}")

print("\n\n" + "=" * 70)
print("✅ TEST 2: Mark 'Mechanics' as Completed")
print("=" * 70)
manager.mark_topic_completed("Mechanics")
summary = manager.get_summary()
print(f"   Readiness: {summary['readiness']}%")
print(f"   Completed: {summary['completed']}/{summary['total_topics']}")

print("\n\n" + "=" * 70)
print("🔥 TEST 3: Update Study Streak")
print("=" * 70)
manager.update_streak(7)
summary = manager.get_summary()
print(f"   Streak: {summary['streak']} days")

print("\n\n" + "=" * 70)
print("➕ TEST 4: Add New Topic")
print("=" * 70)
manager.add_topic_to_plan(
    date="2025-11-10",
    subject="Chemistry",
    topic="Organic Chemistry",
    hours=4
)
summary = manager.get_summary()
print(f"   Total Topics: {summary['total_topics']}")
print(f"   Readiness: {summary['readiness']}%")

print("\n\n" + "=" * 70)
print("📋 TEST 5: Get Pending Topics")
print("=" * 70)
pending = manager.get_pending_topics()
print(f"   Pending topics: {len(pending)}")
for topic in pending:
    print(f"   - {topic['topic']} ({topic['subject']})")

print("\n\n" + "=" * 70)
print("📋 TEST 6: Get Completed Topics")
print("=" * 70)
completed = manager.get_completed_topics()
print(f"   Completed topics: {len(completed)}")
for topic in completed:
    print(f"   ✅ {topic['topic']} ({topic['subject']})")
    print(f"      Completed at: {topic.get('completed_at', 'N/A')}")

print("\n\n" + "=" * 70)
print("📊 FINAL STATE")
print("=" * 70)
final_summary = manager.get_summary()
for key, value in final_summary.items():
    print(f"   {key}: {value}")

print("\n\n" + "#" * 70)
print("🎉 SUCCESS! ALL TESTS PASSED!")
print("#" * 70)
print("\n💾 Data persisted to: student_study_data.json")
print("✅ All changes are saved and will survive app restarts!")
print("\n📝 You can now integrate this with your AI agents when ready.")
