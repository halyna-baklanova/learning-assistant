"""
Views for the learning assistant application.
Handles task management, question uploads, and random question selection.
"""

import random

from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from learn.models import Task
from learn.permissions import IsOwnerOrReadOnly

from learn.serializers import (
    QuestionSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
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


@method_decorator(csrf_exempt, name="dispatch")
def upload_questions_view(request):
    message = None

    if request.method == "POST":
        raw_text = request.POST.get("data", "")
        lines = raw_text.splitlines()
        tasks = []
        question = None

        for line in lines:
            line = line.strip()
            if line.startswith("Q:"):
                question = line[2:].strip()
            elif line.startswith("A:") and question:
                answer = line[2:].strip()
                tasks.append(Task(question=question, answer=answer))
                question = None  # скидаємо після збереження

        Task.objects.bulk_create(tasks)
        message = f"Successfully uploaded {len(tasks)} questions."

    return render(request, "upload.html", {"message": message})


@api_view(["GET"])
def random_question_by_task(request, task_id):
    """
    Get a single random question from a specific task.

    This endpoint retrieves all questions associated with the given task ID
    and returns one of them selected at random. Useful for flashcards or quizzes.

    Parameters:
    task_id (int): The unique ID of the task to pull questions from.

    Returns:
    200 OK: A serialized Question object.
    404 Not Found: If the task doesn't exist or has no questions.
    """
    task = get_object_or_404(Task, id=task_id)
    questions = task.questions.all()

    if not questions:
        return Response({
            "error": "No questions found",
            "task_id": task_id
        }, status=status.HTTP_404_NOT_FOUND)

    random_question = random.choice(list(questions))
    serializer = QuestionSerializer(random_question)

    return Response(serializer.data)
