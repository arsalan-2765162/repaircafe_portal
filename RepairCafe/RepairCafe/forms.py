from django import forms
from RepairCafe.models import Ticket

class TicketFilterForm(forms.Form):
    STATUS_CHOICES = [('ALL', 'All')] + list(Ticket.REPAIR_STATUS_CHOICES)
    CATEGORY_CHOICES = [('ALL', 'All')] + list(Ticket.ITEM_CATEGORY_CHOICES)
    repairStatus = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Repair Status"
                                     ,initial='WAITING')
    itemCategory = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Item Category")

    class Meta:
        model = Ticket
        fields = ()
