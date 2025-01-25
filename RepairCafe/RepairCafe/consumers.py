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