from django.db import models


class Task(models.Model):
    question = models.TextField(blank=False)
    answer = models.TextField(blank=False)
