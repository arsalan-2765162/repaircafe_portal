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
        excluded_statuses = ['WAITING_TO_JOIN', 'INCOMPLETE', 'COMPLETED']
        status_choices = [
            choice for choice in Ticket.REPAIR_STATUS_CHOICES
            if choice[0] not in excluded_statuses
        ]
        self.fields['repairStatus'].choices = [('ALL', 'All')] + status_choices
    class Meta:
        model = Ticket
        fields = ()

class IncompleteTicketForm(forms.Form):
    incompleteReason = forms.ChoiceField(
        choices=Ticket.REPAIR_INCOMPLETE_CHOICES,
        widget=forms.RadioSelect,
        label="Reason for Incompletion",
        required=True,
    )
    class Meta:
        model=Ticket
        fields=["incompleteReason"]

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['repairNumber', 'itemName', 'itemCategory', 'position', 'repairStatus', 'itemDescription']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True

class CheckoutForm(forms.Form):
    Q1 = forms.CharField(
        label="Q1 How did you find out about the repair cafe?",
        max_length=256,
        required=True
    )
    Q2 = forms.CharField(
        label="Q2",
        max_length=256,
        required=True
    )

    Q3 = forms.CharField(
        label="Q3",
        max_length=256,
        required=True
    )

    Q4 = forms.CharField(
        label="Q4",
        max_length=256,
        required=True
    )

    Q5 = forms.CharField(
        label="Q5",
        max_length=256,
        required=True
    )

    Q6 = forms.CharField(
        label="Q6",
        max_length=256,
        required=True
    )

    Q7 = forms.CharField(
        label="Q7",
        max_length=256,
        required=True
    )

    Q8 = forms.CharField(
        label="Q8",
        max_length=256,
        required=True
    )

    Q9 = forms.CharField(
        label="Q9",
        max_length=256,
        required=True
    )

    Q10 = forms.CharField(
        label="Q10",
        max_length=256,
        required=True
    )

    Q11 = forms.CharField(
        label="Q11",
        max_length=256,
        required=True
    )

    Q12 = forms.CharField(
        label="Q12",
        max_length=256,
        required=True
    )


    Q13 = forms.CharField(
        label="Q13",
        max_length=256,
        required=True
    )

    Q14 = forms.CharField(
        label="Q14",
        max_length=256,
        required=True
    )

    Q15 = forms.CharField(
        label="Q15",
        max_length=256,
        required=True
    )

    Q16 = forms.CharField(
        label="Q16",
        max_length=256,
        required=True
    )

    Q17 = forms.CharField(
        label="Q17",
        max_length=256,
        required=True
    )

    Q18 = forms.CharField(
        label="Q18",
        max_length=256,
        required=True
    )

    Q19 = forms.CharField(
        label="Q19",
        max_length=256,
        required=True
    )


