#!/usr/bin/env python
"""
Test AI agents with actual OpenAI calls
"""

from agents.planner_agent import PlannerAgent
from agents.tracker_agent import TrackerAgent
from agents.motivator_agent import MotivatorAgent

print("🧪 Testing AI Agents with OpenAI")
print("=" * 60)

# Test 1: Motivator (fastest/cheapest)
print("\n1️⃣ Testing MotivatorAgent...")
try:
    motivator = MotivatorAgent()
    result = motivator.daily_motivation(
        completed_count=2,
        missed_count=1,
        streak=3
    )
    print("✅ MotivatorAgent works!")
    print(f"Response: {result.get('message', result.get('output', 'No output'))[:100]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Tracker
print("\n2️⃣ Testing TrackerAgent...")
try:
    tracker = TrackerAgent()
    result = tracker.get_analytics(
        completed_count=5,
        missed_count=2,
        streak=4
    )
    print("✅ TrackerAgent works!")
    print(f"Response: {result.get('analytics', result.get('output', 'No output'))[:100]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Planner (might take longer)
print("\n3️⃣ Testing PlannerAgent...")
try:
    planner = PlannerAgent()
    result = planner.create_schedule(
        syllabus={"Math": ["Algebra"], "Physics": ["Mechanics"]},
        exam_date="2025-12-01",
        available_hours=3
    )
    print("✅ PlannerAgent works!")
    print(f"Response: {result.get('schedule', result.get('output', 'No output'))[:100]}...")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("🎉 AI Agent Testing Complete!")
print("=" * 60)
