from datetime import date, datetime

def calculate_priority_score(task_data):
    score = 0
    explanation = []

    # Urgency (due date)
    try:
        due_date = datetime.strptime(task_data.get('due_date'), '%Y-%m-%d').date()
    except:
        due_date = date.today()
        
    today = date.today()
    days_left = (due_date - today).days

    if days_left < 0:
        score += 50
        explanation.append("Overdue.")
    elif days_left <= 2:
        score += 30
        explanation.append("Due very soon.")
    elif days_left <= 7:
        score += 15
        explanation.append("Due this week.")

    # Importance (1–10 scale)
    importance = task_data.get('importance', 0)
    score += importance * 3
    if importance > 7:
        explanation.append("High importance.")

    # Effort estimate
    hours = task_data.get('estimated_hours', 0)
    if hours < 2:
        score += 20
        explanation.append("Quick task.")
    elif hours > 10:
        score -= 10
        explanation.append("High effort.")

    # Dependencies
    deps = task_data.get('dependencies', [])
    if not deps:
        score += 10
        explanation.append("No dependencies.")

    return score, " ".join(explanation)
