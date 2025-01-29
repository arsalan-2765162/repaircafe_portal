import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TicketStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "ticket_updates",
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            "ticket_updates",
            self.channel_name
        )

    async def ticket_status_update(self,event):
        await self.send(text_data=json.dumps({
            'repair_number': event['repair_number'],
            'status':event['status']
        }

        ))

class MainQueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "main_queue_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "main_queue_updates",
            self.channel_name
        )

    async def queue_update(self, event):
        print(f"Received update: {event}")
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

class WaitingQueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "waiting_queue_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "waiting_queue_updates",
            self.channel_name
        )

    async def queue_update(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

class CheckoutQueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "checkout_queue_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "checkout_queue_updates",
            self.channel_name
        )

    async def queue_update(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))