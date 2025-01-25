from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ticket_status/(?P<repair_number>\w+)/$', consumers.TicketStatusConsumer.as_asgi()),
]