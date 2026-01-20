import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_registration_success(api_client):
    url = reverse("register")
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "strongpassword123",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED


def test_registration_missing_fields(api_client):
    url = reverse("register")
    payload = {"email": "", "username": ""}  # missing password
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# add codedocs
# i think it is not recognizing the .coveragerc because it is not ignoring the */migrations/*