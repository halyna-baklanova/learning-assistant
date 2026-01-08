from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from learn.models import Task
from learn.serializers import TaskDetailSerializer, TaskListSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update"]:
            return TaskDetailSerializer

        return self.serializer_class


class RandomQuestionView(APIView):
    def get(self, request):
        questions = Task.objects.all()
        if not questions.exists():
            return Response(
                {
                    "detail": "There are no questions yet. Would you like to add more questions before continuing?"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        random_question = random.choice(questions)
        serializer = TaskDetailSerializer(random_question, context={"request": request})
        return Response(serializer.data)


def random_question_page(request):
    return render(request, "index.html")


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
