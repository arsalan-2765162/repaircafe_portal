from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from django.core.asgi import get_asgi_application
from . import consumers
# ASGI routing configuration for WebSocket consumers.

# This file defines the URL routing for WebSocket connections.
# Each WebSocket connection is routed to a specific consumer based on the URL pattern.

websocket_urlpatterns = [
    re_path(r'ws/ticket_status/(?P<repairNumber>\w+)/$', consumers.TicketStatusConsumer.as_asgi()),
    re_path(r'ws/main_queue/$', consumers.MainQueueConsumer.as_asgi()),
    re_path(r'ws/waiting_queue/$', consumers.WaitingQueueConsumer.as_asgi()),
    re_path(r'ws/checkout_queue/$', consumers.CheckoutQueueConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
