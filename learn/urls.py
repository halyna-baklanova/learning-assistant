"""
URL configuration for the learning assistant application.

Defines API endpoints for:
- Task management (CRUD operations via ViewSet)
- Question uploads (bulk import)
- Random question selection by task
"""

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from learn.views import (
    TaskViewSet,
    random_question_by_task,
    upload_questions_view,
)

app_name = "learn"

# Router configuration for ViewSet endpoints
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

# URL patterns
urlpatterns = [
    # ViewSet routes (automatically generates list, detail, create, update, delete)
    path("", include(router.urls)),

    # Custom endpoints
    path(
        "upload/",
        upload_questions_view,
        name="upload-questions"
    ),
    path(
        "random/question/<int:task_id>/",
        random_question_by_task,
        name="random-question-by-task"
    ),
]
