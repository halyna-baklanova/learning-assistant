from rest_framework import serializers
from .models import Task, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text_question", "answer"]


class TaskDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="learn:task-detail")
    questions = QuestionSerializer(many=True)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = ["url", "id", "title", "description", "owner", "questions"]


class TaskListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="learn:task-detail")
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = ["url", "title", "owner"]
