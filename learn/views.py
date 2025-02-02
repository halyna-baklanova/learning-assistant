from rest_framework import viewsets, mixins

from learn.models import Task
from learn.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
