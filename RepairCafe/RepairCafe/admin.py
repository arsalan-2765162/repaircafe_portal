from django.contrib import admin
from .models import Ticket, Customer, Repairer, Queue

# Register your models here
admin.site.register(Ticket)
admin.site.register(Customer)
admin.site.register(Repairer)
admin.site.register(Queue)
