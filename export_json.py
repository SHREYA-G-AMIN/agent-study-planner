# export_json.py

import json
from data_structuring import structure_study_plan
from progress_tracker import track_progress
from input_data import input_data

# Step 1: Generate study plan
study_plan = structure_study_plan(input_data)

# Step 2: Simulate some completed topics
completed_topics = ["Algebra"]  # Example

# Step 3: Track progress
progress_summary = track_progress(study_plan, completed_topics)

# Step 4: Combine everything
output_data = {
    "student_id": input_data["student_id"],
    "student_name": input_data["student_name"],
    "study_plan": study_plan,
    "progress_summary": progress_summary
}

# Step 5: Export to JSON
with open("student_study_data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("JSON file created successfully!")
