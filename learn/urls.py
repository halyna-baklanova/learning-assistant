from django.urls import path, include
from rest_framework import routers

from learn.views import TaskViewSet

router = routers.DefaultRouter()
router.register("learn", TaskViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "task"
