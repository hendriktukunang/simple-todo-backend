import pytest
from django.urls import reverse
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_auth_with_correct_credentials():
    url = reverse("Auth")
    payload = {
        "username": "hendrik@blankontech.com",
        "password": "123456",
    }
    client = APIClient()
    response = client.post(url, payload)
    assert response.status_code == 200
    assert response.data.get("first_name") == "Hendrik"
    assert response.data.get("last_name") == "Tukunang"
    assert response.data.get("email") == "hendrik@blankontech.com"


@pytest.mark.django_db
def test_auth_with_incorrect_credentials():
    url = reverse("Auth")
    payload = {
        "username": "hendrik@blankontech.com",
        "password": "1234567",
    }
    client = APIClient()
    response = client.post(url, payload)
    assert response.status_code == 400
