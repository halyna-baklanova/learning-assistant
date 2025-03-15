from django.urls import path, include
from rest_framework.routers import DefaultRouter
from learn.views import TaskViewSet, RandomQuestionView, random_question_page

router = DefaultRouter()
router.register(r"learn", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("random/", RandomQuestionView.as_view(), name="random-question"),
    path("random/question/", random_question_page, name="random-question-html-page")
]

app_name = "learn"
