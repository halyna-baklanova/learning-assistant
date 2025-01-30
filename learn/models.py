from django.db import models

class Task(models.Model):
    question = models.TextField()
    answer = models.TextField()
