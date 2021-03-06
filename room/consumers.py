from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Room
from asgiref.sync import async_to_sync
from accounts.models import Profile


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_30_message()
        content = {
            "messages": self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = Profile.objects.get(pk=author)
        room = Room.objects.get_slug(self.room_name)
        message = Message.objects.create(
            sender=author_user,
            text=data['message'],
            room=room[0])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        time = str(message.created_date.strftime("%Y-%m-%d %H:%M:%S"))
        return {
            'author': message.sender.full_name,
            'content': message.text,
            'timestamp': time
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))