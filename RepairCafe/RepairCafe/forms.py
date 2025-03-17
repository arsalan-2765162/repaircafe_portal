from django import forms
from RepairCafe.models import Ticket
from django.core.validators import MinLengthValidator


class TicketFilterForm(forms.Form):
    STATUS_CHOICES = [('ALL', 'All')] + list(Ticket.REPAIR_STATUS_CHOICES)
    CATEGORY_CHOICES = [('ALL', 'All')] + list(Ticket.ITEM_CATEGORY_CHOICES)
    repairStatus = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Repair Status"
                                     , initial='WAITING')
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
        model = Ticket
        fields = ["incompleteReason"]


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
        label="How did you hear about us?",
        max_length=512,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q2 = forms.CharField(
        label="What item did you bring in today and why did you want it to be fixed? (Can you share something more specific)",
        max_length=512,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    Q3 = forms.CharField(
        label="How was your experience? What did you get from it? (Learn something new, meet new people etc.)",
        max_length=512,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


class RulesButton(forms.Form):
    acceptrules = forms.BooleanField(
        required=True,
        label='By ticking you are confirming that you have read and accept the House Rules',
        error_messages={'required': 'You must agree to the House Rules to access the site.'})


class CheckinForm(forms.Form):
    firstName = forms.CharField(
        label="First Name",
        max_length=56,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    lastName = forms.CharField(
        label="Last Name",
        max_length=56,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    emailPhone = forms.CharField(
        label="Email or Phone Number",
        max_length=56,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    postCode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Post Code (First 3 Characters)",
        required=True,
        max_length=3,
        validators=[
            MinLengthValidator(3, 'Must be the first 3 Characters of your Post Code')
        ]

    )

    itemName = forms.CharField(
        label="Item to be repaired *include brand if known",
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    itemDescription = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Short Description of Issue to be Repaired",
        required=True
    )

    itemCategory = forms.ChoiceField(
        label="Category Of item to be Repaired",
        choices=[('', '---Please select a category---')] + list(Ticket.ITEM_CATEGORY_CHOICES),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    photoConsent = forms.BooleanField(
        label="Do you consent to being in photos for social media?",
        required=False,
        widget=forms.CheckboxInput
    )

    mailingConsent = forms.BooleanField(
        label="Would you like to join our Mailing List?",
        required=False,
        widget=forms.CheckboxInput
    )


class CompleteFeedbackForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['fault_cause', 'repair_solution']
        widgets = {
            'fault_cause': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'repair_solution': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fault_cause'].required = True
        self.fields['repair_solution'].required = True
        self.fields['fault_cause'].label = "What was the cause of the fault?"
        self.fields['repair_solution'].label = "How did you fix it?"


class IncompleteFeedbackForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['fault_cause', 'repair_solution', 'incomplete_cause']
        widgets = {
            'fault_cause': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'repair_solution': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'incomplete_cause': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fault_cause'].required = True
        self.fields['repair_solution'].required = True
        self.fields['incomplete_cause'].required = True
        self.fields['fault_cause'].label = "What was the cause of the fault?"
        self.fields['repair_solution'].label = "How was did you try to fix it?"
        self.fields['incomplete_cause'].label = "Why did you not manage to fix it?"
