from django.urls import path, include
from rest_framework import routers

from learn.views import TaskViewSet, home_view

router = routers.DefaultRouter()
router.register("learn", TaskViewSet)

urlpatterns = [
    path("home/", home_view, name="home"),
    path("", include(router.urls)),
]

app_name = "task"