import json
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chat_name = self.scope['url_route']['kwargs']['chat_id']
        self.chat = Chat.objects.get(name=self.chat_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name,
        )

        if self.user not in self.chat.users_online.all():
            self.chat.users_online.add(self.user)
            self.members = self.chat.users_online
            self.online_indicator()

        return self.accept()

    def receive(self, text_data=None, bytes_data=None):
        message_json = json.loads(text_data)
        body = message_json['body']

        message = Message.objects.create(user=self.user, chat=self.chat, body=body)

        event = {
            'type': 'message_hendler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            event,
        )

    def message_hendler(self, event):
        message_id = event['message_id']
        message = Message.objects.get(id=message_id)

        partial = render_to_string(
            'chat/partials/message.html',
            {'message': message, 'user': self.user, 'ws': True},
        )
        self.send(text_data=partial)

    def online_indicator(self):
        event = {
            'type': 'online_indicator_handler',
            'online_count': self.members.count() - 1,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            event,
        )

    def online_indicator_handler(self, event):
        online_count = event['online_count']
        online_indicator = render_to_string(
            'chat/partials/online-indicator.html',
            {'online_count': online_count, 'ws': True, 'request': self.scope},
        )
        self.send(text_data=online_indicator)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name,
            self.channel_name,
        )
        if self.user in self.chat.users_online.all():
            self.chat.users_online.remove(self.user)
            self.members = self.chat.users_online
            self.online_indicator()
