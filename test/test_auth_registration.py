import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_registration_success(api_client):
    url = reverse("Authentication:register")
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123",
        "password2": "Strongpassword123"
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED


# def test_registration_missing_fields(api_client):
#     url = reverse("register")
#     payload = {"email": "", "username": ""}  # missing password
#     response = api_client.post(url, payload, format="json")
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
