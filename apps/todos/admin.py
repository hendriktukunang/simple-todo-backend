from django.contrib import admin
from apps.todos.models import Todo

# Register your models here.


@admin.register(Todo)
class AdminUser(admin.ModelAdmin):
    list_display = (
        "id",
        "task",
        "last_updated_at",
        "created_at",
    )
    search_fields = [
        "task",
    ]
