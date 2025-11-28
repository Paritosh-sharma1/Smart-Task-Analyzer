from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from .scoring import calculate_priority_score

class AnalyzeTasksView(APIView):
    def post(self, request):
        tasks_data = request.data.get('tasks', [])
        strategy = request.data.get('strategy', 'smart')

        analyzed_tasks = []

        for task in tasks_data:
            score, explanation = calculate_priority_score(task)
            task['score'] = score
            task['explanation'] = explanation
            analyzed_tasks.append(task)

        # Sorting strategies
        if strategy == 'fastest':
            analyzed_tasks.sort(key=lambda t: t['estimated_hours'])
            for t in analyzed_tasks:
                t['explanation'] = "Sorted by lowest effort."

        elif strategy == 'impact':
            analyzed_tasks.sort(key=lambda t: t['importance'], reverse=True)
            for t in analyzed_tasks:
                t['explanation'] = "Sorted by highest importance."

        elif strategy == 'deadline':
            analyzed_tasks.sort(key=lambda t: t['due_date'])
            for t in analyzed_tasks:
                t['explanation'] = "Sorted by nearest deadline."

        else:
            analyzed_tasks.sort(key=lambda t: t['score'], reverse=True)

        return Response(analyzed_tasks, status=status.HTTP_200_OK)


class SuggestTasksView(APIView):
    def get(self, request):
        suggestions = [
            {
                "title": "Fix Critical Login Bug",
                "explanation": "High importance and due today."
            },
            {
                "title": "Update Documentation",
                "explanation": "Quick task with no dependencies."
            },
            {
                "title": "Email Client",
                "explanation": "High priority client request."
            }
        ]
        return Response(suggestions)
