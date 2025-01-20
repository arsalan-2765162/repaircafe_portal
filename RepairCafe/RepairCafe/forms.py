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
        label="Q1 Why did you come to the repair cafe today? What brought you here?",
        max_length=512,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    Q2 = forms.CharField(
        label="Q2 How did you hear about us?",
        max_length=512,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q3 = forms.CharField(
        label="Q3 How was your experience? What did you get from it? (Learn something new, meet new people etc.)",
        max_length=512,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q4 = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        label="Q4 Would you be interested in learning new repair skills/ attending workshops?",
        required=True
    )

    Q4Extra = forms.CharField(
        label="If yes, what skills/workshops would you be interested in?",
        max_length=256,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Q5 = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        label="Q5 Are you interested in volunteering with us? ",
        required=True
    )

    Q5Extra = forms.CharField(
        label="Q5 If yes please leave your contact details (name and email address)",
        max_length=256,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
        

    Q6 = forms.CharField(
        label="Q6 How did you find out about the repair cafe?",
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Q7 = forms.CharField(
        label="Q7 Item type",
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Q8 = forms.CharField(
        label="Q8 Make of item (if applicable)",
        max_length=256,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Q9 = forms.CharField(
        label="Q9 Model of item (if applicable)",
        max_length=256,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Q10 = forms.CharField(
        label="Q10 What was wrong with the item?",
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Q11 = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        label="Q11 Were we able to repair your item?",
        required=True
    )

    Q11Extra = forms.CharField(
        label="If no, Q11 Why were we unable to repair your item today?",
        max_length=256,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )



    Q12 = forms.ChoiceField(
        label="Q12 Did your item have any sentimental attachment for you?",
        required=True,
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
    )

    Q12Extra = forms.CharField(
        label="Q12 If yes, please tell us more",
        max_length=256,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
        
    )


    Q13 = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        label="Q13 Does having your item repaired make your life happier, healthier or more comfortable?",
        widget=forms.RadioSelect,
        required=True
    )
    Q13Extra = forms.CharField(
        label="Q13 If yes, please tell us more",
        max_length=256,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q14 = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        label="Q14 If you couldn't have had your item repaired today would you have bought a new one?",
        widget=forms.RadioSelect,
        required=True
    )

    Q15 = forms.CharField(
        label="Q15 How much would you have spent on it?",
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Q16 = forms.CharField(
        label="Q16 Do you feel more confident tackling a repair yourself in the future?",
        max_length=256,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q17 = forms.CharField(
        label="Q17 How did you find your experience at the repair cafe?",
        max_length=256,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q18 = forms.CharField(
        label="Q18 What could be improved?",
        max_length=512,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q19 = forms.CharField(
        label="Q19 Did you meet anyone new at the repair cafe?",
        max_length=256,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    Q19Extra = forms.CharField(
        label="Q19 If yes, please tell us more?",
        max_length=256,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    Q20 = forms.CharField(
        label="Q20 Would you come back if you had something else to fix?",
        max_length=256,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )



class RulesButton(forms.Form):

    acceptrules = forms.BooleanField(required=True, 
    label='By ticking you are confirming that you have read and accept the House Rules',
    error_messages={'required':'You must agree to the House Rules to access the site.'})

class CheckinForm(forms.Form):

    confirmbutton = forms.BooleanField(required=True, label='Submit')