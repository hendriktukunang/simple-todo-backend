from django.urls import path
from .views import CreateTodo, GetTodo, ListTodo, DeleteTodo, UpdateTodo

urlpatterns = [
    path("create/", CreateTodo.as_view(), name="CreateTodo"),
    path("list/", ListTodo.as_view(), name="ListTodo"),
    path("get/<int:pk>/", GetTodo.as_view(), name="GetTodo"),
    path("delete/<int:pk>/", DeleteTodo.as_view(), name="DeleteTodo"),
    path("update/<int:pk>/", UpdateTodo.as_view(), name="UpdateTodo"),
]
