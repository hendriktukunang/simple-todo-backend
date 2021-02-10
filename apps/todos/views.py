from apps.todos.serializers import TodoSerializer
from apps.commons.views import (
    OrderingSupportMixin,
    BaseQuerysetMixin,
    BoundToUserMixin,
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

# Create your views here.


class BaseTodoView:
    serializer_class = TodoSerializer


class ListTodo(
    OrderingSupportMixin,
    BaseQuerysetMixin,
    BoundToUserMixin,
    BaseTodoView,
    ListAPIView,
):

    pagination_class = None


class CreateTodo(
    BaseTodoView,
    OrderingSupportMixin,
    BaseQuerysetMixin,
    BoundToUserMixin,
    CreateAPIView,
):
    pass


class UpdateTodo(
    OrderingSupportMixin,
    BaseQuerysetMixin,
    BoundToUserMixin,
    BaseTodoView,
    UpdateAPIView,
):
    pass


class GetTodo(
    OrderingSupportMixin,
    BaseQuerysetMixin,
    BoundToUserMixin,
    BaseTodoView,
    RetrieveAPIView,
):
    pass


class DeleteTodo(
    OrderingSupportMixin,
    BaseQuerysetMixin,
    BoundToUserMixin,
    BaseTodoView,
    DestroyAPIView,
):
    pass
