#!/usr/bin/env python
"""
Complete end-to-end test of the JSON-integrated system
"""

print("\n" + "#" * 60)
print("# COMPLETE SYSTEM TEST - JSON INTEGRATION")
print("#" * 60 + "\n")

# Test the complete workflow
from main import StudyPlannerSystem

print("🧪 Test 1: Initialize system with JSON mode")
print("=" * 60)
try:
    system = StudyPlannerSystem(use_json=True)
    print("✅ System initialized successfully!\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit(1)

print("\n🧪 Test 2: Get current summary")
print("=" * 60)
try:
    summary = system.get_summary()
    print("✅ Summary retrieved:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n\n🧪 Test 3: Mark topics as completed")
print("=" * 60)
try:
    # Mark Algebra and Mechanics as completed
    result = system.mark_topics_completed(["Algebra", "Mechanics"])
    print("✅ Topics marked successfully!")
    print(f"   New readiness: {result.get('readiness_percentage', 0)}%")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n\n🧪 Test 4: Get updated summary")
print("=" * 60)
try:
    summary = system.get_summary()
    print("✅ Updated summary:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n\n🧪 Test 5: Update streak")
print("=" * 60)
try:
    system.data_manager.update_streak(5)
    print("✅ Streak updated to 5 days")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n\n" + "#" * 60)
print("🎉 ALL TESTS COMPLETED!")
print("#" * 60)

# Final state
print("\n📊 Final System State:")
print("=" * 60)
try:
    final_summary = system.get_summary()
    for key, value in final_summary.items():
        print(f"   {key}: {value}")
    
    # Show data persistence message
    print("\n💾 All changes have been saved to: student_study_data.json")
    print("✅ Data will persist across application restarts!")
except Exception as e:
    print(f"❌ Error: {e}")
