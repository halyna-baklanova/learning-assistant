from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255, default="Untitled")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    task = models.ForeignKey(Task, related_name="questions", on_delete=models.CASCADE)
    text_question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.text_question
