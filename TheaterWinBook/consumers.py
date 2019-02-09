from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Full_Chatting_Message
from django.contrib.auth.models import User
# from channels_presence.models import Room
# from channels_presence.models import Presence

# class ChatConsumer(AsyncWebsocketConsumer):
#     def fetch_messages(self, data):
#         messages = Full_Chatting_Message.last_30_messages()
#         print('fetch')
#         content = {
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_chat_message(content)
#
#     def new_message(self, data):
#         print("this is new_message :",data)
#         username = data['username']
#         writer = User.objects.get(username=username)
#         # 새로운 메세지는 full_chatting의 가장 오래된 메세지 부터 삭제하자...
#         message = Full_Chatting_Message.objects.create(writer=writer, content=data['message'], timestamp=data['writing_time'])
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         print("this is send_chat_message");
#         return self.send_chat_message(content)
#
#     def messages_to_json(self, messages):
#         print("this is messages_to_json")
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result
#
#     def message_to_json(self, message):
#         print("this is message_to_json",message)
#         return {
#             'writer': message.writer,
#             'content': message.content,
#             'timestamp': str(message.timestamp)
#         }
#
#     commands = {
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }
#
#     async def connect(self):
#         # 처음 들어올 때,
#         print("this is connect")
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         print("this is disconnect")
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         # Receive message from WebSocket
#
#     async def receive(self, text_data):
#         print("this is receive")
#         data = json.loads(text_data)
#         print('data:', data)
#         self.commands[data['command']](self, data)
#
#     async def send_chat_message(self, message):
#         print("this is send_chat_message")
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 # 'username': username,
#                 # 'writing_time': writing_time,
#             }
#         )
#
#     async def send_message(self, message):
#         self.send(text_data=json.dumps(message))
#
#
#         # Receive message from room group
#
#     async def chat_message(self, event):
#         print("this is chat_message")
#         message = event['message']
#         username = event['username']
#         writing_time = event['writing_time']
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps(message))
#


class ChatConsumer(AsyncWebsocketConsumer):
    current_counting = 0;
    async def connect(self):
        # 채널의 전체 명수를 관리하는 함수
        self.user = self.scope["user"]
        # Room.objects.add("everyone",  self.channel_name, self.user)
        # 처음 들어올 때,
        print("this is connect")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print("this is end of connect")
        db_results = reversed(Full_Chatting_Message.objects.order_by('-timestamp').all()[:30])
        for result in db_results:
            writer = result.writer.username
            content = result.content
            timestamp = str(result.timestamp)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': content,
                    'username': writer,
                    'writing_time': timestamp,
                }
            )

    async def disconnect(self, close_code):
        print("this is disconnect")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Room.objects.remove("everyone",self.channel_name)
        print("this is end of disconnect")

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("this is receive")
        text_data_json = json.loads(text_data)
        content = text_data_json['message']
        username = text_data_json['username']
        writing_time = text_data_json['writing_time']
        # 새로운 메세지는 full_chatting 이 100개가 넘었을 시 가장 오래된 메세지 부터 삭제하자...
        writer = User.objects.get(username=username)
        row_count = Full_Chatting_Message.objects.all().count()
        if row_count < 30:
            Full_Chatting_Message.objects.create(writer=writer, content=content,
                                                 timestamp=writing_time)
            print("this is row_count is below 30")
        else:
            modify_row = Full_Chatting_Message.objects.order_by('timestamp').first()
            modify_row.writer = writer
            modify_row.content = content
            modify_row.timestamp = writing_time
            modify_row.save()


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content,
                'username': username,
                'writing_time': writing_time,
            }
        )
        print("this is end of receive")

    # Receive message from room group
    async def chat_message(self, event):
        print("this is chat_message")
        message = event['message']
        username = event['username']
        writing_time = event['writing_time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'writing_time': writing_time,

        }))
        print("this is end of chat_message")
