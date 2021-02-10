from channels.generic.websocket import AsyncJsonWebsocketConsumer


class BaseSocketConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.
    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    async def join_to_group(self):
        """
        we group user sockets, so we can easily send notification to a group
        rather than loop user sockets and send manage to send notification
        on each socket
        :return:
        """
        self.group_name = str(self.user.id)
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def connect(self):
        if not self.scope.get("user"):
            await self.close()
            return
        self.user = self.scope.get("user")
        await self.join_to_group()
        await self.accept()

    async def receive_json(self, content, **kwargs):
        pass

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        pass

    async def send_data(self, event):
        await self.send_json({"content": event["data"]})
