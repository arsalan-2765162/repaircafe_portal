from django import forms
from RepairCafe.models import Ticket

class TicketFilterForm(forms.Form):
    STATUS_CHOICES = [('ALL', 'All')] + list(Ticket.REPAIR_STATUS_CHOICES)
    CATEGORY_CHOICES = [('ALL', 'All')] + list(Ticket.ITEM_CATEGORY_CHOICES)
    repairStatus = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Repair Status"
                                     ,initial='WAITING')
    itemCategory = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Item Category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        status_choices = [choice for choice in Ticket.REPAIR_STATUS_CHOICES if choice[0] != 'WAITING_TO_JOIN']
        self.fields['repairStatus'].choices = [('ALL', 'All')] + status_choices
    class Meta:
        model = Ticket
        fields = ()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['repairNumber', 'itemName', 'itemCategory', 'position', 'repairStatus', 'itemDescription']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
