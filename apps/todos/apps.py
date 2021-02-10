from django.apps import AppConfig


class TodosConfig(AppConfig):
    name = "apps.todos"

    def ready(self):
        import apps.todos.signals
