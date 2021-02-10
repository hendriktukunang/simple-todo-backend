from django.urls import path
from .views import Auth

urlpatterns = [
    path("auth/", Auth.as_view(), name="Auth"),
]
