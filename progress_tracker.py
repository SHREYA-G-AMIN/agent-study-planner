# progress_tracker.py

from data_structuring import structure_study_plan
from input_data import input_data

def track_progress(study_plan, completed_topics):
    """
    Calculates progress metrics based on completed topics.
    
    Args:
        study_plan (list): Output from structure_study_plan()
        completed_topics (list): List of topic names completed by the student
        
    Returns:
        dict: Progress summary including total topics, completed count, readiness %
    """
    total_topics = len(study_plan)
    completed_count = sum(1 for item in study_plan if item["topic"] in completed_topics)
    readiness_percentage = round((completed_count / total_topics) * 100, 2)
    
    return {
        "total_topics": total_topics,
        "completed_topics_count": completed_count,
        "readiness_percentage": readiness_percentage
    }

# Test the tracker
study_plan = structure_study_plan(input_data)
completed_topics = ["Algebra"]  # example: student completed Algebra
progress_summary = track_progress(study_plan, completed_topics)

print("Progress Summary:", progress_summary)
