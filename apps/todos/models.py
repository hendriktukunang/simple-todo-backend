from django.db import models
from apps.commons.models import BaseModel, ModelProperties, BoundToUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Todo(BaseModel, BoundToUser, ModelProperties):
    task = models.CharField(max_length=150)

    class Meta:
        verbose_name = _("Todo")
        verbose_name_plural = _("Todos")
