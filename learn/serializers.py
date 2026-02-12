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

class BulkQuestionUploadSerializer(serializers.Serializer):
    """
    Serializer for bulk uploading questions to a task.

    Accepts a list of questions with text_question and answer fields.
    """
    questions = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        allow_empty=False
    )

    def validate_questions(self, value):
        """
        Validate that each question has required fields.

        Args:
            value: List of question dictionaries

        Returns:
            Validated list of questions

        Raises:
            ValidationError: If any question is missing required fields
        """
        for i, question in enumerate(value, start=1):
            if "text_question" not in question:
                raise serializers.ValidationError(
                    f"Question at index {i} is missing 'text_question' field"
                )
            if "answer" not in question:
                raise serializers.ValidationError(
                    f"Question at index {i} is missing 'answer' field"
                )

            if question["text_question"].strip() is None:
                raise serializers.ValidationError(
                    f"Question at index {i} has empty 'text_question' field"
                )

            if question["answer"].strip() is None:
                raise serializers.ValidationError(
                    f"Question at index {i} has empty 'answer' field"
                )

            return value
