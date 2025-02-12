import pytest 
from channels.testing import WebsocketCommunicator
from django.conf import settings 
from channels.layers import get_channel_layer 
from RepairCafe.routing import application


@pytest.mark.asyncio
class TestConsumers: 
    async def test_ticket_status_consumer(self):
        communicator = WebsocketCommunicator(application,"/ws/ticket_status/123/")
        connected, _ = await communicator.connect()
        assert connected 

        """simulating sending a ticket update"""
        channel_layer = get_channel_layer()
        await (channel_layer.group_send)(
            "ticket_updates",
            {
                "type": "ticket_status_update",
                "repairNumber": 123,
                "status": "IN_PROGRESS",
            },
        )

        """receive the message that is sent to the websocket"""
        response = await communicator.receive_json_from()
        assert response == {
            "repairNumber": 123,
            "status": "IN_PROGRESS",
        }
        await communicator.disconnect()

    async def test_main_queue_consumer(self):
        communicator = WebsocketCommunicator(application, "/ws/main_queue/")
        connected, _ = await communicator.connect()
        assert connected

        """simulate sending a main queue update"""
        channel_layer = get_channel_layer()
        await (channel_layer.group_send)(
            "main_queue_updates",
            {
                "type": "queue_update",
                "message": "ticket_added",
            },
        )

        """receive the message that is sent to the websocket"""
        response = await communicator.receive_json_from()
        assert response == {"message": "ticket_added"}
        await communicator.disconnect()

    async def test_waiting_queue_consumer(self):
        communicator = WebsocketCommunicator(application, "/ws/waiting_queue/")
        connected, _ = await communicator.connect()
        assert connected

        channel_layer = get_channel_layer()
        await (channel_layer.group_send)(
            "waiting_queue_updates",
            {
                "type": "queue_update",
                "message": "ticket_removed",
            },
        )

        response = await communicator.receive_json_from()
        assert response == {"message": "ticket_removed"}

        await communicator.disconnect()

    async def test_checkout_queue_consumer(self):
        communicator = WebsocketCommunicator(application, "/ws/checkout_queue/")
        connected, _ = await communicator.connect()
        assert connected

        channel_layer = get_channel_layer()
        await (channel_layer.group_send)(
            "checkout_queue_updates",
            {
                "type": "queue_update",
                "message": "ticket_checked_out",
            },
        )

        response = await communicator.receive_json_from()
        assert response == {"message": "ticket_checked_out"}

        await communicator.disconnect()
