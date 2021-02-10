from apps.commons.serializers import BaseModelSerializer, BoundToUserSerializer
from apps.todos.models import Todo


class TodoSerializer(BoundToUserSerializer, BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        self.Meta.fields = ["id", "task"]
        super(TodoSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Todo
        fields = []
