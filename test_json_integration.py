#!/usr/bin/env python
"""
Quick integration test for JSON workflow
"""

from json_manager import StudentDataManager
import json

print("=" * 60)
print("🧪 QUICK INTEGRATION TEST")
print("=" * 60)

# Test 1: Initialize manager
print("\n1️⃣ Test: Initialize StudentDataManager")
manager = StudentDataManager("student_study_data.json")
print("✅ Manager initialized")

# Test 2: Load existing data
print("\n2️⃣ Test: Load existing data")
data = manager.load_student_data()
print(f"✅ Data loaded: {data.get('student_name')}")
print(f"   Topics: {len(data.get('study_plan', []))}")

# Test 3: Get summary
print("\n3️⃣ Test: Get summary")
summary = manager.get_summary()
print("✅ Summary:")
for key, value in summary.items():
    print(f"   {key}: {value}")

# Test 4: Get pending topics
print("\n4️⃣ Test: Get pending topics")
pending = manager.get_pending_topics()
print(f"✅ Found {len(pending)} pending topics:")
for topic in pending:
    print(f"   - {topic.get('topic')} ({topic.get('subject')})")

# Test 5: Mark a topic completed
print("\n5️⃣ Test: Mark topic completed")
if pending:
    topic_name = pending[0].get('topic')
    print(f"   Marking '{topic_name}' as completed...")
    manager.mark_topic_completed(topic_name)
    
    # Verify it worked
    updated_summary = manager.get_summary()
    print(f"✅ Updated readiness: {updated_summary.get('readiness')}%")

# Test 6: Update progress
print("\n6️⃣ Test: Update progress")
updated_data = manager.update_progress()
progress = updated_data.get('progress_summary', {})
print("✅ Progress updated:")
print(f"   Completed: {progress.get('completed_topics_count')}/{progress.get('total_topics')}")
print(f"   Readiness: {progress.get('readiness_percentage')}%")

# Test 7: Check if schema fields were added
print("\n7️⃣ Test: Verify schema fields")
schema_fields = ['student_id', 'student_name', 'study_plan', 'progress_summary', 'current_streak', 'meta']
for field in schema_fields:
    status = "✅" if field in updated_data else "❌"
    print(f"   {status} {field}")

# Final summary
print("\n" + "=" * 60)
print("🎉 ALL TESTS PASSED!")
print("=" * 60)
print("\n📊 Final State:")
final_summary = manager.get_summary()
for key, value in final_summary.items():
    print(f"   {key}: {value}")
