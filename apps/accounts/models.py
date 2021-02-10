from apps.commons.models import BaseModel, ModelProperties, BoundToUser
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token as RestToken
from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.accounts.utils import TodoSocketOperationMixin

# Create your models here.


class User(TodoSocketOperationMixin, BaseModel, AbstractUser):
    """
    user class here, extends additional fields in this class,
    basically it already has appropriate fields from abstract user
    """

    username = None
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def todo_list(self):
        from apps.todos.serializers import TodoSerializer

        return TodoSerializer(
            self.todo_set.all().order_by("id"), many=True, exclude_fields=["user"]
        ).data


class Token(ModelProperties, BoundToUser, RestToken):
    """
    token class here, extends additional fields in this class,
    basically it already has appropriate fields from Rest token
    """

    class Meta:
        verbose_name = _("token")
        verbose_name_plural = _("tokens")
