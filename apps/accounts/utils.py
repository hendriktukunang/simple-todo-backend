from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
import json


class SocketOperationMixin:
    @staticmethod
    @shared_task
    def send_socket_message(group_id, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_id,
            {
                "type": "send_data",
                "data": json.dumps(data),
            },
        )


class TodoSocketOperationMixin:
    def sync_todo_list_to_clients(self):
        SocketOperationMixin.send_socket_message.delay(str(self.id), self.todo_list)
