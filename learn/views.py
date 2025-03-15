from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from django.shortcuts import render

from learn.models import Task
from learn.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class RandomQuestionView(APIView):
    def get(self, request):
        questions = Task.objects.all()
        if not questions.exists():
            return Response(
                {"detail": "Питань немає в базі."}, status=status.HTTP_404_NOT_FOUND
            )

        random_question = random.choice(questions)
        serializer = TaskSerializer(random_question)
        return Response(serializer.data)


def random_question_page(request):
    return render(request, "index.html")
