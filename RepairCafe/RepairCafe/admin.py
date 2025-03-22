from django.contrib import admin
from .models import Ticket, Customer, Repairer, Queue, Carbon_footprint_categories, SharedPassword, MailingList

class SharedPasswordAdmin(admin.ModelAdmin):
    list_display = ['user_type', 'hashed_password']

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            raw_password = form.cleaned_data['hashed_password']
            obj.set_password(raw_password)
        super().save_model(request, obj, form, change)

# Register your models here
admin.site.register(Ticket)
admin.site.register(Customer)
admin.site.register(Repairer)
admin.site.register(Queue)
admin.site.register(MailingList)
admin.site.register(Carbon_footprint_categories)
admin.site.register(SharedPassword, SharedPasswordAdmin)
