from rest_framework import serializers
from learn.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "question", "answer"]
