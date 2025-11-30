from django.contrib import admin
from .models import Task, Question

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'text', 'answer')
    list_filter = ('task',)
    search_fields = ('text',)
