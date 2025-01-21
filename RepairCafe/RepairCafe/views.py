from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, redirect
from .models import Ticket, Queue
from .forms import TicketFilterForm,TicketForm,IncompleteTicketForm,RulesButton, CheckinForm, CheckoutForm
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
import populate_RepairCafe as script
from django.conf import settings
from datetime import date


def index(request):
    return render(request, 'RepairCafe/index.html', context={})

def reset_data(request):
	script.populate()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', redirect('RepairCafe/main_queue.html')))

def main_queue(request):
    context_dict={}
    try:
        queue = Queue.objects.get(name="Main Queue")
        ticket_list = Ticket.objects.filter(queue=queue).order_by('position')
        
        #retrive filter paremeters for queue
        form = TicketFilterForm(request.GET or None)
        print("Form is valid:", form.is_valid())  # This will print if the form is valid
        if form.is_valid():
            status_filter = form.cleaned_data.get('repairStatus') or 'WAITING'
            category_filter = form.cleaned_data.get('itemCategory')
            if status_filter and status_filter != 'ALL':
                ticket_list = ticket_list.filter(repairStatus=status_filter)
            if category_filter and category_filter != 'ALL':
                ticket_list = ticket_list.filter(itemCategory=category_filter)
        else:
            ticket_list=ticket_list.filter(repairStatus='WAITING')

        #populate the list of forms used to display all tickets in the queue
        ticketForms = [TicketForm(instance=ticket) for ticket in ticket_list]
        context_dict['TicketForms']=ticketForms
        
        context_dict['Queue']=queue
        context_dict['Tickets']=ticket_list
        context_dict['FilterForm']=form
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/main_queue.html', context=context_dict)

def waiting_list(request):
    context_dict={}
    try:
        queue = Queue.objects.get(name="Waiting List")
        ticket_list = Ticket.objects.filter(queue=queue,repairStatus='WAITING_TO_JOIN').order_by('position')

        form = TicketFilterForm(request.GET or None)
        print("Form is valid:", form.is_valid())  # This will print if the form is valid
        if form.is_valid():
            category_filter = form.cleaned_data.get('itemCategory')
            if category_filter and category_filter != 'ALL':
                ticket_list = ticket_list.filter(itemCategory=category_filter)
        
        #populate the list of forms used to display all tickets in waiting list
        waitingForms = [TicketForm(instance=ticket) for ticket in ticket_list]
        context_dict['TicketForms'] = waitingForms
        
        context_dict['Queue']=queue
        context_dict['Tickets']=ticket_list
        context_dict['WaitingForm']=form
        context_dict['Ticket']=Ticket  
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/waiting_list.html', context=context_dict)

def checkout_queue(request):
    context_dict={}
    try:
        queue = Queue.objects.get(name="Checkout Queue")
        ticket_list = Ticket.objects.filter(isCheckedOut=False,queue=queue, repairStatus__in=['COMPLETED', 'INCOMPLETE']).order_by('position')

        form = TicketFilterForm(request.GET or None)
        print("Form is valid:", form.is_valid())  # This will print if the form is valid
        if form.is_valid():
            category_filter = form.cleaned_data.get('itemCategory')
            if category_filter and category_filter != 'ALL':
                ticket_list = ticket_list.filter(itemCategory=category_filter)
        
        
        context_dict['Queue']=queue
        context_dict['Tickets']=ticket_list
        context_dict['WaitingForm']=form
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/checkout_queue.html', context=context_dict)



def accept_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    if ticket.repairStatus == 'WAITING_TO_JOIN':
        ticket.accept_ticket()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been accepted.")
    else:
        messages.error(request,f"Error, ticket {ticket.repairNumber}:{ticket.itemName}, not accepted.")
    return redirect(reverse('RepairCafe:waiting_list'))

def repair_ticket(request,repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus == "WAITING":
        ticket.repair_ticket()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, is now being repaired.")
    else:
        messages.error(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, cannot be accepted as it is not in WAITING status.")
    return redirect('RepairCafe:repair_item', repairNumber=repairNumber)

def mark_incomplete_ticket(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    
    if request.method == 'POST':
        incompleteForm = IncompleteTicketForm(request.POST)
        if incompleteForm.is_valid():
            ticket.repairStatus = "INCOMPLETE"
            ticket.incompleteReason = incompleteForm.cleaned_data['incompleteReason']
            ticket.adFd_to_checkout()
            ticket.save()
            messages.success(request, f"Ticket {ticket.repairNumber} - {ticket.itemName} marked as incomplete.")
            return redirect('RepairCafe:main_queue')
    else:
        form = IncompleteTicketForm()
    context_dict = {'ticket': ticket, 'form': incompleteForm}
    return render(request, 'RepairCafe/mark_incomplete_ticket.html', context_dict)

def repair_item(request,repairNumber):
    context_dict={}
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    incompleteForm = IncompleteTicketForm()
    

    context_dict['incompleteForm'] = incompleteForm
    context_dict['ticket']=ticket
    return render(request,'RepairCafe/repair_item.html',context_dict)

def complete_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    if ticket.repairStatus == 'BEING_REPAIRED' and ticket.itemCategory == "ELECM":
        ticket.complete_ticket()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been sent to PAT Testing.")
    elif(ticket.repairStatus == 'BEING_REPAIRED' ):
        ticket.complete_ticket()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been marked as completed.")
    else:
        messages.error(request,f"Error, ticket {ticket.repairNumber} - {ticket.itemName}, not completed")
    return redirect(reverse('RepairCafe:main_queue'))

def delete_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    ticket.delete_ticket()
    messages.success(request,f"Ticket: {ticket.itemName}, has been removed")
    return redirect('RepairCafe:waiting_list')

def checkout_ticket(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    if ticket.repairStatus == 'COMPLETED' or ticket.repairStatus =='INCOMPLETE':
        ticket.checkout()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been checked out.")
    else:
        messages.error(request,f"Error checking out Ticket {ticket.repairNumber} - {ticket.itemName}")
    return redirect(reverse('RepairCafe:checkout_queue'))

def change_category(request, repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if request.method == 'POST':
        new_category = request.POST.get('new_category')
        valid_categories = [choice[0] for choice in Ticket.ITEM_CATEGORY_CHOICES]
        if new_category in valid_categories:
            ticket.itemCategory = new_category
            ticket.save()
            messages.success(request, f"Category for ticket {ticket.repairNumber} - {ticket.itemName} has been updated.")
        else:
            messages.error(request, f"Invalid category selected for ticket {ticket.repairNumber} - {ticket.itemName}")
    return redirect(request.META.get('HTTP_REFERER', 'RepairCafe:waiting_list'))

# visitor flow #

def enter_password(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if entered_password == settings.VISITOR_PRESET_PASSWORD:
            request.session['preset_password_verified'] = True
            return redirect('RepairCafe:house_rules')
        elif entered_password == settings.REPAIRER_PRESET_PASSWORD:
            request.session['preset_password_verified'] = True
            return redirect('RepairCafe:index')
        else:
            return render(request, 'RepairCafe/enter_password.html', {'error': 'Incorrect Password'})
        
    return render(request, 'RepairCafe/enter_password.html')

def house_rules(request):
    if request.method == 'POST':
        form = RulesButton(request.POST)
        if form.is_valid():
            agreed = form.cleaned_data.get('acceptrules')
            if agreed:
                return redirect('RepairCafe:checkin_form')
            else:
                return redirect('RepairCafe:house_rules')
            
    else:
        form = RulesButton()

    
    return render(request, 'RepairCafe/house_rules.html', {'form': form})

def checkin_form(request):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            agreed = form.cleaned_data.get('confirmbutton')

            if agreed:
               return redirect('RepairCafe:index')
        
            else:
               return render(request, 'RepairCafe/checkin_form.html')

    else:
        form = CheckinForm()


    return render(request, 'RepairCafe/checkin_form.html', {'form':form})
    return render(request, 'RepairCafe/house_rules.html')

def checkout(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    context_dict={}
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['event_date'] = date.today()
            print(form_data)
            return render(request,'RepairCafe/checkout_success.html')
    else:
        form=CheckoutForm
        context_dict['form']=form

    return render(request,'RepairCafe/checkout.html',context_dict)

def checkout_success(request):
    return render(request,'RepairCafe/checkout_success.html')
        
        




    

