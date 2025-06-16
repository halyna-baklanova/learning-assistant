import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from learn.models import Task

@pytest.mark.django_db
def test_random_question_returns_200_if_task_exists():
    # Arrange
    Task.objects.create(question="What is Python?", answer="A programming language.")
    client = APIClient()

    # Act
    response = client.get("/api/random/")

    # Assert
    assert response.status_code == 200
    assert "question" in response.data
    assert "answer" in response.data


@pytest.mark.django_db
def test_random_question_returns_404_if_no_tasks():
    client = APIClient()

    response = client.get("/api/random/")

    assert response.status_code == 404
    assert response.data["detail"] == "There are no questions yet. Would you like to add more questions before continuing?"
