from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ModelProperties(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_or_none(cls, **kwargs):
        """
        shortcut for try except not defined record in database
        """
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return None


class BaseModel(ModelProperties):
    """
    basic model contains created at and last updated at to get idea about record last update
    """

    created_at = models.DateTimeField(auto_now=True, blank=True)
    last_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Base Model")
        verbose_name_plural = _("Base model")
        abstract = True


class BoundToUser(models.Model):
    """
    define for a model that belongs to user like token or todo
    """

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    class Meta:
        abstract = True
