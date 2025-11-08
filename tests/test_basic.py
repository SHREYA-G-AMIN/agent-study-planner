from agents.planner_agent import PlannerAgent
import json

def test_planner():
    print("Testing Planner Agent...")
    planner = PlannerAgent()
    
    syllabus = {
        "Math": ["Algebra", "Calculus"],
        "Physics": ["Mechanics", "Thermodynamics"]
    }
    
    result = planner.create_schedule(syllabus, "2025-11-30", 3)
    print(json.dumps(result, indent=2))
    print("✅ Planner test complete!")

if __name__ == "__main__":
    test_planner()
    