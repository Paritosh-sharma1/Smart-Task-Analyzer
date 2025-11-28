from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # We accept dependencies as a list, simpler for the frontend to send
    dependencies = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=[]
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'estimated_hours', 'importance', 'dependencies']