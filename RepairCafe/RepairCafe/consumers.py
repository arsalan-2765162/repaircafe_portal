import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TicketStatusConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling ticket status updates.

    This consumer listens to the 'ticket_updates' group and sends updates to connected clients
    about the status of repairs.
    """

    async def connect(self):
        """
        Handles the WebSocket connection.

        Adds the connection to the 'ticket_updates' group to listen for ticket status updates.
        """
        await self.channel_layer.group_add(
            "ticket_updates",
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self,close_code):
        """
        Handles the WebSocket disconnection.

        Removes the connection from the 'ticket_updates' group upon disconnection.
        """
        await self.channel_layer.group_discard(
            "ticket_updates",
            self.channel_name
        )

    async def ticket_status_update(self,event):
        """
        Handles ticket status update messages from the channel layer.

        Sends the ticket status update to the WebSocket client.
        """
        await self.send(text_data=json.dumps({
            'repairNumber': event['repairNumber'],
            'status':event['status']
        }))


class MainQueueConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling updates for the main queue.

    This consumer listens to the 'main_queue_updates' group and sends updates to connected clients
    about the main queue status.
    """

    async def connect(self):
        """
        Handles the WebSocket connection.

        Adds the connection to the 'main_queue_updates' group to listen for main queue updates.
        """
        await self.channel_layer.group_add(
            "main_queue_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the WebSocket disconnection.

        Removes the connection from the 'main_queue_updates' group upon disconnection.
        """
        await self.channel_layer.group_discard(
            "main_queue_updates",
            self.channel_name
        )

    async def queue_update(self, event):
        """
        Handles queue update messages from the channel layer.

        Sends the queue update message to the WebSocket client.
        """
        print(f"Received update: {event}")
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


class WaitingQueueConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling updates for the waiting queue.

    This consumer listens to the 'waiting_queue_updates' group and sends updates to connected clients
    about the waiting queue status.
    """

    async def connect(self):
        """
        Handles the WebSocket connection.

        Adds the connection to the 'waiting_queue_updates' group to listen for waiting queue updates.
        """
        await self.channel_layer.group_add(
            "waiting_queue_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the WebSocket disconnection.

        Removes the connection from the 'waiting_queue_updates' group upon disconnection.
        """
        await self.channel_layer.group_discard(
            "waiting_queue_updates",
            self.channel_name
        )

    async def queue_update(self, event):
        """
        Handles queue update messages from the channel layer.

        Sends the queue update message to the WebSocket client.
        """
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


class CheckoutQueueConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling updates for the checkout queue.

    This consumer listens to the 'checkout_queue_updates' group and sends updates to connected clients
    about the checkout queue status.
    """

    async def connect(self):
        """
        Handles the WebSocket connection.

        Adds the connection to the 'checkout_queue_updates' group to listen for checkout queue updates.
        """
        await self.channel_layer.group_add(
            "checkout_queue_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the WebSocket disconnection.

        Removes the connection from the 'checkout_queue_updates' group upon disconnection.
        """
        await self.channel_layer.group_discard(
            "checkout_queue_updates",
            self.channel_name
        )

    async def queue_update(self, event):
        """
        Handles queue update messages from the channel layer.

        Sends the queue update message to the WebSocket client.
        """
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))