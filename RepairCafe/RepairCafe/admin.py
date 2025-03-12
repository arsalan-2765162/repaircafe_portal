from django.contrib import admin
from .models import Ticket, Customer, Repairer, Queue, Carbon_footprint_categories

# Register your models here
admin.site.register(Ticket)
admin.site.register(Customer)
admin.site.register(Repairer)
admin.site.register(Queue)
admin.site.register(Carbon_footprint_categories)
