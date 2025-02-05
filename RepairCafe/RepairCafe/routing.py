from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ticket_status/(?P<repairNumber>\w+)/$', consumers.TicketStatusConsumer.as_asgi()),
    re_path(r'ws/main_queue/$', consumers.MainQueueConsumer.as_asgi()),
    re_path(r'ws/waiting_queue/$', consumers.WaitingQueueConsumer.as_asgi()),
    re_path(r'ws/checkout_queue/$', consumers.CheckoutQueueConsumer.as_asgi()),
]