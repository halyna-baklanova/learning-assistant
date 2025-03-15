from django.urls import path, include
from rest_framework.routers import DefaultRouter
from learn.views import TaskViewSet, RandomQuestionView

router = DefaultRouter()
router.register(r"learn", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("random/", RandomQuestionView.as_view(), name="random-question"),
]

app_name = "learn"
