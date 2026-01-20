"""
Views for the learning assistant application.
Handles task management, question uploads, and random question selection.
"""

import random

from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from learn.models import Task
from learn.serializers import (
    QuestionSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update"]:
            return TaskDetailSerializer

        return self.serializer_class


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
