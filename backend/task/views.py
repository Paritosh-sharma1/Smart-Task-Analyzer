from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from .scoring import calculate_priority_score
from datetime import date

class AnalyzeTasksView(APIView):
    def post(self, request):
        tasks_data = request.data.get('tasks', [])
        strategy = request.data.get('strategy', 'smart') # Default to smart balance

        analyzed_tasks = []

        for task_input in tasks_data:
            serializer = TaskSerializer(data=task_input)
            if serializer.is_valid():
                serializer.save()
            else:
                print("Validation Error:", serializer.errors)

            # Calculate Smart Score
            score, explain = calculate_priority_score(task_input)
            task_input['score'] = score
            task_input['explanation'] = explain
            analyzed_tasks.append(task_input)

        # Apply Sorting Strategies
        if strategy == 'fastest':
            # Sort by hours (ascending)
            analyzed_tasks.sort(key=lambda x: x['estimated_hours'])
            for t in analyzed_tasks: t['explanation'] = "Sorted by lowest effort."
            
        elif strategy == 'impact':
            # Sort by importance (descending)
            analyzed_tasks.sort(key=lambda x: x['importance'], reverse=True)
            for t in analyzed_tasks: t['explanation'] = "Sorted by highest importance."

        elif strategy == 'deadline':
            # Sort by due_date (ascending)
            analyzed_tasks.sort(key=lambda x: x['due_date'])
            for t in analyzed_tasks: t['explanation'] = "Sorted by nearest deadline."

        else: # 'smart'
            # Sort by calculated score (descending)
            analyzed_tasks.sort(key=lambda x: x['score'], reverse=True)

        return Response(analyzed_tasks, status=status.HTTP_200_OK)

class SuggestTasksView(APIView):
    def get(self, request):
        
        db_tasks = Task.objects.all().order_by('-importance')[:3]
        
        if db_tasks.exists():
            suggestions = []
            for t in db_tasks:
                suggestions.append({
                    "title": t.title,
                    "explanation": f"Fetched from DB: Importance {t.importance}"
                })
            return Response(suggestions)
        
        suggestions = [
            {
                "title": "Fix Critical Login Bug",
                "explanation": "High Importance and Due Today."
            },
            {
                "title": "Update Documentation",
                "explanation": "Quick win (1 hour) and no dependencies."
            },
            {
                "title": "Email Client",
                "explanation": "High priority client request."
            }
        ]
        return Response(suggestions)