from channels.generic.websocket import AsyncWebsocketConsumer
import json
from Waiter.models import OrderKitchen

class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = 'chef_orders'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )    

    async def receive(self, text_data):
        order = json.loads(text_data)['order']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send_message',
                'order' : order,
            }
        )  
        
    async def send_message(self,event):
        await self.send(text_data=json.dumps({
            'order' : event['order'],
        }))