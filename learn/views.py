from rest_framework import viewsets
from django.shortcuts import render

from learn.models import Task
from learn.serializers import TaskSerializer


def home_view(request):
    return render(request, "index.html")

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
