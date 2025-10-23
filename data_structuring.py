# data_structuring.py

from datetime import datetime, timedelta
from input_data import input_data

def structure_study_plan(input_data):
    exam_date = datetime.strptime(input_data["exam_date"], "%Y-%m-%d")
    today = datetime.today()
    total_days = max(1, (exam_date - today).days)
    daily_hours = input_data["hours_per_day"]

    topics = input_data["topics"]
    subjects = input_data["subjects"]

    study_plan = []

    for i, topic in enumerate(topics):
        hours_needed = topic["difficulty"]  # difficulty represents hours
        topic_days = max(1, hours_needed // daily_hours)
        
        for day in range(topic_days):
            plan_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
            study_plan.append({
                "date": plan_date,
                "subject": subjects[i],
                "topic": topic["name"],
                "hours": min(daily_hours, hours_needed)
            })
            hours_needed -= daily_hours
            if hours_needed <= 0:
                break

    return study_plan

# Test the function
study_plan = structure_study_plan(input_data)
for item in study_plan:
    print(item)
