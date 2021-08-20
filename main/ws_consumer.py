import json

from django.core.cache import cache
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .check_service import get_submission


class SubmissionStatusConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Connect websocket
        """
        self.room_name = self.scope['url_route']['kwargs']['submission_id']
        self.room_group_name = f'room_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Disconnect websocket
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        """
        response = json.loads(text_data)
        submission_status = 'unknown'
        if 'submission_id' in response:
            submission_id = response['submission_id']
            submission_status = cache.get(f'submission_status_{submission_id}')
            if not submission_status:
                _, submission_status = await get_submission(submission_id)
                cache.set(f'submission_status_{submission_id}', submission_status)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_message',
            'status': submission_status,
        })

    async def send_message(self, res):
        """
        Receive message
        """
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
