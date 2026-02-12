"""
Views for the learning assistant application.
Handles task management, question uploads, and random question selection.
"""

import random

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from learn.models import Task, Question
from learn.permissions import IsOwnerOrReadOnly

from learn.serializers import (
    QuestionSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
    BulkQuestionUploadSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing learning tasks.

    Provides standard CRUD operations and dynamically switches serializers
    based on the action to optimize data transfer.

    Automatically sets the owner to the current user when creating tasks.

    Attributes:
        queryset: Database query that retrieves all Task objects.
        serializer_class: Default serializer for list views (summary view).
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TaskListSerializer

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.

        Returns TaskDetailSerializer for detailed operations to include
        nested questions, otherwise returns TaskListSerializer for brief listing.

        Logic:
            - list -> TaskListSerializer (short summary)
            - others -> TaskDetailSerializer (full data)
        """
        if self.action == "list":
            return TaskListSerializer
        return TaskDetailSerializer

    def perform_create(self, serializer):
        """Set owner to current user when creating a task."""
        serializer.save(owner=self.request.user)

    @action(
        detail=True,
        methods=["get", "post"],
        url_path='upload-questions',
        serializer_class=BulkQuestionUploadSerializer
    )
    def upload_questions(self, request, pk=None):
        """
        Bulk upload questions to a specific task.

        Only the task owner can upload questions.

        Expected JSON format:
        {
            "questions": [
                {
                    "text_question": "Question text",
                    "answer": "Answer text"
                },
                ...
            ]
        }
        """
        task = self.get_object()

        if request.method == "GET":
            existing_questions = task.questions.all()
            return Response({
                "message": f"Upload questions to task: {task.title}",
                "task_id": task.id,
                "task_title": task.title,
                "task_description": task.description,
                "existing_questions_count": existing_questions.count(),
                "existing_questions": QuestionSerializer(existing_questions, many=True).data,
                "instructions": "Send POST request with questions array in JSON format",
            })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        questions_data = serializer.validated_data["questions"]
        questions_to_create = []

        for question_data in questions_data:
            questions_to_create.append(
                Question(
                    task=task,
                    text_question=question_data["text_question"],
                    answer=question_data["answer"]
                )
            )

        created_questions = Question.objects.bulk_create(questions_to_create)

        return Response(
            {
                "message": f"Successfully uploaded {len(created_questions)} questions to task '{task.title}'",
                "task_id": task.id,
                "task_title": task.title,
                "created_count": len(created_questions),
                "questions": QuestionSerializer(created_questions, many=True).data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["get"], url_path="study")
    def study(self, request, pk=None):
        """
        Get a random question from this task for studying.

        Returns a random question from the task's question pool.
        The same question may appear multiple times (fully random).

        GET /learn/tasks/{id}/study/

        Returns:
            200: Random question with answer
            404: Task has no questions

        Response format:
        {
            "question_id": 42,
            "task_id": 5,
            "task_title": "Python Basics",
            "text_question": "What is a list?",
            "answer": "A collection of items",
            "total_questions": 10
        }
        """
        task = self.get_object()
        questions = task.questions.all()

        if not questions.exists():
            return Response(
                {
                    "error": "No questions available for this task",
                    "task_id": task.id,
                    "task_title": task.title,
                    "message": "Please add questions to this task first"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        random_question = questions.order_by("?").first()

        return Response({
            "question_id": random_question.id,
            "task_id": task.id,
            "task_title": task.title,
            "text_question": random_question.text_question,
            "answer": random_question.answer,
            "total_questions": questions.count(),
            "has_ai_answer": False #for AI-Feature
        })
