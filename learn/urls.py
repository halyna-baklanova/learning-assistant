from django.urls import path, include
from rest_framework.routers import DefaultRouter
from learn.views import (
    RandomQuestionView,
    random_question_page,
    upload_questions_view,
    TaskViewSet,
)

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
    path("random/", RandomQuestionView.as_view(), name="random-question"),
    path("upload/", upload_questions_view, name="upload-questions"),
    path("random/question/", random_question_page, name="random-question-html-page"),
]

app_name = "learn"
