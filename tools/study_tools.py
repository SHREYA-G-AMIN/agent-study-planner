from langchain.tools import tool
from datetime import datetime, timedelta
from typing import Dict, List
import json

@tool
def calculate_study_hours(syllabus_json: str, exam_date: str, available_hours_per_day: int) -> str:
    """
    Calculates daily study schedule based on syllabus and available time.
    
    Args:
        syllabus_json: JSON string of syllabus with subjects and topics
        exam_date: Exam date in YYYY-MM-DD format
        available_hours_per_day: Hours available per day for study
    
    Returns:
        JSON string with daily schedule
    """
    try:
        syllabus = json.loads(syllabus_json)
        exam_dt = datetime.strptime(exam_date, "%Y-%m-%d")
        today = datetime.now()
        days_remaining = (exam_dt - today).days
        
        # Count total topics
        total_topics = sum(len(topics) for topics in syllabus.values())
        
        # Calculate total available hours
        total_hours = days_remaining * available_hours_per_day
        
        # Reserve last 2 days for revision
        study_days = days_remaining - 2
        
        # Hours per topic
        hours_per_topic = total_hours * 0.8 / total_topics  # 80% for learning, 20% buffer
        
        # Create daily schedule
        schedule = []
        current_day = 0
        
        for subject, topics in syllabus.items():
            for topic in topics:
                schedule.append({
                    "day": current_day + 1,
                    "date": (today + timedelta(days=current_day)).strftime("%Y-%m-%d"),
                    "subject": subject,
                    "topic": topic,
                    "hours": round(hours_per_topic, 1),
                    "completed": False
                })
                current_day += 1
                if current_day >= study_days:
                    break
        
        # Add revision days
        for i in range(2):
            schedule.append({
                "day": study_days + i + 1,
                "date": (today + timedelta(days=study_days + i)).strftime("%Y-%m-%d"),
                "subject": "ALL",
                "topic": f"Revision Day {i+1}",
                "hours": available_hours_per_day,
                "completed": False
            })
        
        return json.dumps({
            "total_days": days_remaining,
            "study_days": study_days,
            "revision_days": 2,
            "schedule": schedule
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def check_completion_status(schedule_json: str, completed_topics: str) -> str:
    """
    Checks completion status and identifies missed topics.
    
    Args:
        schedule_json: JSON string of current schedule
        completed_topics: Comma-separated list of completed topics
    
    Returns:
        JSON string with completion analysis
    """
    try:
        schedule = json.loads(schedule_json)
        completed = [t.strip() for t in completed_topics.split(",") if t.strip()]
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        missed_tasks = []
        completed_tasks = []
        upcoming_tasks = []
        
        for task in schedule.get("schedule", []):
            task_date = task["date"]
            topic = task["topic"]
            
            if task_date < today:
                if topic in completed or task["completed"]:
                    completed_tasks.append(task)
                else:
                    missed_tasks.append(task)
            elif task_date == today:
                upcoming_tasks.append(task)
        
        total_past_tasks = len(missed_tasks) + len(completed_tasks)
        completion_rate = (len(completed_tasks) / total_past_tasks * 100) if total_past_tasks > 0 else 0
        
        return json.dumps({
            "completion_rate": round(completion_rate, 1),
            "completed_count": len(completed_tasks),
            "missed_count": len(missed_tasks),
            "today_tasks": upcoming_tasks,
            "missed_tasks": missed_tasks
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def rebalance_schedule(current_schedule_json: str, missed_tasks_json: str, available_hours: int) -> str:
    """
    Redistributes missed topics across remaining days.
    
    Args:
        current_schedule_json: JSON string of current schedule
        missed_tasks_json: JSON string of missed tasks
        available_hours: Hours available per day
    
    Returns:
        JSON string with adjusted schedule
    """
    try:
        schedule = json.loads(current_schedule_json)
        missed_tasks = json.loads(missed_tasks_json)
        
        today = datetime.now()
        
        # Get remaining days
        remaining_schedule = [
            task for task in schedule.get("schedule", [])
            if datetime.strptime(task["date"], "%Y-%m-%d") >= today
        ]
        
        # Add missed tasks to the front of remaining schedule
        new_schedule = []
        day_counter = 0
        
        for missed in missed_tasks:
            new_schedule.append({
                "day": day_counter + 1,
                "date": (today + timedelta(days=day_counter)).strftime("%Y-%m-%d"),
                "subject": missed["subject"],
                "topic": missed["topic"],
                "hours": missed["hours"],
                "completed": False,
                "priority": "HIGH - Missed Task"
            })
            day_counter += 1
        
        # Add remaining tasks
        for task in remaining_schedule:
            if task["topic"] not in [m["topic"] for m in missed_tasks]:
                new_schedule.append({
                    "day": day_counter + 1,
                    "date": (today + timedelta(days=day_counter)).strftime("%Y-%m-%d"),
                    "subject": task["subject"],
                    "topic": task["topic"],
                    "hours": task["hours"],
                    "completed": False,
                    "priority": "NORMAL"
                })
                day_counter += 1
        
        return json.dumps({
            "adjusted": True,
            "schedule": new_schedule,
            "message": f"Redistributed {len(missed_tasks)} missed tasks"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def get_progress_analytics(completed_count: int, missed_count: int, streak_days: int) -> str:
    """
    Calculates progress analytics and performance metrics.
    
    Args:
        completed_count: Number of completed tasks
        missed_count: Number of missed tasks
        streak_days: Current study streak in days
    
    Returns:
        JSON string with analytics
    """
    try:
        total_tasks = completed_count + missed_count
        completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0
        
        # Performance rating
        if completion_rate >= 90:
            rating = "Excellent"
            emoji = "🌟"
        elif completion_rate >= 75:
            rating = "Good"
            emoji = "👍"
        elif completion_rate >= 60:
            rating = "Fair"
            emoji = "📚"
        else:
            rating = "Needs Improvement"
            emoji = "⚠️"
        
        return json.dumps({
            "completion_rate": round(completion_rate, 1),
            "total_completed": completed_count,
            "total_missed": missed_count,
            "current_streak": streak_days,
            "performance_rating": rating,
            "emoji": emoji,
            "insights": [
                f"You've completed {completed_count} out of {total_tasks} tasks",
                f"Current streak: {streak_days} days" if streak_days > 0 else "Start a streak today!",
                f"Performance: {rating}"
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})
    
    