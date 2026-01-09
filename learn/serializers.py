from rest_framework import serializers
from .models import Task, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text_question", "answer"]


class TaskDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="learn:task-detail")
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Task
        fields = ["url", "title", "description", "questions"]


class TaskListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="learn:task-detail")

    class Meta:
        model = Task
        fields = ["url", "title"]
