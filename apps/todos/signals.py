from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from apps.todos.models import Todo


class TodoSignal:
    @staticmethod
    @receiver(post_save, sender=Todo)
    def sync_todo_list_to_clients_post_save(sender, instance, created, **kwargs):
        instance.user.sync_todo_list_to_clients()

    @staticmethod
    @receiver(post_delete, sender=Todo)
    def sync_todo_list_to_clients_post_delete(sender, instance, **kwargs):
        instance.user.sync_todo_list_to_clients()
