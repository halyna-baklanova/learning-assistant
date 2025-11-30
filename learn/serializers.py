from rest_framework import serializers
from .models import Task, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "answer"]

class TaskSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)  # nested questions

    class Meta:
        model = Task
        fields = ["id", "title", "description", "questions"]
