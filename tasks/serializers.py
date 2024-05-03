from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task's views"""
    class Meta:
        model = Task
        fields = '__all__'
