from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, redirect
from .models import Ticket, Queue, Customer, Repairer
from .forms import TicketFilterForm,TicketForm,IncompleteTicketForm,RulesButton, CheckinForm, CheckoutForm
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
import populate_RepairCafe as script
from django.conf import settings
from datetime import date
from django.http import JsonResponse, Http404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




def send_ticket_update(group_name, repairNumber, status):
    """
    Sends an update to the ticket status WebSocket channel.

    Args: 
        group_name (str): The group name for the WebSocket channel.
        repairNumber (str): The repair number of the ticket
        status(str): The new status of the ticket.

    Returns:
        None
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "ticket_status_update",
            "repairNumber": repairNumber,
            "status": status,
        },
    )


def send_queue_update(group_name, queue_name, update_type):
    """
    Sends an update to the respective queue WebSocket channel.

    Args: 
        group_name (str): The group name for the WebSocket channel.
        queue_name (str): The queue_name the update is reffering to
        update_type (str): The type of update being sent.

    Returns:
        None
    """
    print(f"Sending update to group {group_name}")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "queue_update",
            "queue_name": queue_name,
            "message": update_type,
        },
    )


def index(request):
    return render(request, 'RepairCafe/index.html', context={})

"""
Repairer/Volunteer Flow
"""

def reset_data(request):
    script.populate()
    referer_url=request.META.get('HTTP_REFERER')
    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
        return HttpResponseRedirect('RepairCafe/main_queue.html')


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

def basic_stats(request):

    checkedin = Ticket.objects.exclude(repairStatus = "WAITING").count()
    checkedout = Ticket.objects.filter(isCheckedOut = True).count()
    successful = Ticket.objects.filter(repairStatus = "COMPLETED").count()
    unsuccessful = Ticket.objects.filter(repairStatus = "INCOMPLETE").count()
    catpercentages = {}

    for category in Ticket.ITEM_CATEGORY_CHOICES:
        catpercentages[category] = round(((Ticket.objects.filter(itemCategory = category[0]).count())/ (Ticket.objects.count()) * 100), 1)

    

    context_dict = {"checkedin":checkedin, "checkedout":checkedout, "successful":successful, "unsuccessful":unsuccessful, "catpercentages":catpercentages}

    return render(request, 'RepairCafe/basic_stats.html', context_dict)



def accept_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    repairNumber=repairNumber
    
    if ticket.repairStatus == 'WAITING_TO_JOIN':
        ticket.accept_ticket()

        send_ticket_update("ticket_updates",repairNumber, "ACCEPTED")
        send_queue_update("main_queue_updates", "Main Queue", "ticket_added")
        send_queue_update("waiting_queue_updates", "Waiting List", "ticket_removed")

        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been accepted.")
    else:
        messages.error(request,f"Error, ticket {ticket.repairNumber}:{ticket.itemName}, not accepted.")
    return redirect(reverse('RepairCafe:waiting_list'))


def repair_ticket(request, repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)

    repairer_name = request.session.get('repairer_name', None)
    if repairer_name:
        repairer = Repairer.objects.filter(name=repairer_name).first()
    else:
        repairer = None

    if repairer and ticket.repairStatus == "WAITING":
        ticket.repairer = repairer
        ticket.repair_ticket()
        ticket.save()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, is now being repaired.")
    elif ticket.repairStatus != "WAITING":
        messages.error(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, cannot be accepted as it is not in WAITING status.")
    else:
        messages.error(request, "No repairer is logged in.")
    return redirect('RepairCafe:repair_item', repairNumber=repairNumber)

def mark_incomplete_ticket(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    if request.method == 'POST':
        incompleteForm = IncompleteTicketForm(request.POST)
        
        if incompleteForm.is_valid():
            ticket.repairStatus = "INCOMPLETE"
            ticket.incompleteReason = incompleteForm.cleaned_data['incompleteReason']
            ticket.add_to_checkout()
            ticket.save()

            send_ticket_update("ticket_updates", repairNumber, "WAIT_FOR_CHECKOUT")
            send_queue_update("main_queue_updates", "Main Queue", "ticket_removed")
            send_queue_update("checkout_queue_updates", "Checkout Queue", "ticket_removed")

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

    send_ticket_update("ticket_updates", repairNumber, "REPAIRING")
    send_queue_update("main_queue_updates", "Main Queue", "ticket_being_repaired")
    
    context_dict['incompleteForm'] = incompleteForm
    context_dict['ticket']=ticket
    return render(request,'RepairCafe/repair_item.html',context_dict)

def complete_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    if ticket.repairStatus == 'BEING_REPAIRED' and ticket.itemCategory == "ELECM":
        ticket.complete_ticket()

        send_ticket_update("ticket_updates", repairNumber, "WAIT_FOR_PAT")
        send_queue_update("main_queue_updates", "Main Queue", "ticket_updated")
        

        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been sent to PAT Testing.")
    elif(ticket.repairStatus == 'BEING_REPAIRED' ):
        ticket.complete_ticket()

        send_ticket_update("ticket_updates", repairNumber, "WAIT_FOR_CHECKOUT")
        send_queue_update("main_queue_updates", "Main Queue", "ticket_removed")
        send_queue_update("checkout_queue_updates", "Checkout Queue", "ticket_removed")


        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been marked as completed.")
    else:
        messages.error(request,f"Error, ticket {ticket.repairNumber} - {ticket.itemName}, not completed")
    
    
    return redirect(reverse('RepairCafe:main_queue'))

def delete_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    ticket.delete_ticket()
    messages.success(request,f"Ticket: {ticket.itemName}, has been removed")
    send_queue_update("waiting_queue_updates", "Waiting List", "ticket_removed")
    return redirect('RepairCafe:waiting_list')

def checkout_ticket(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    if ticket.repairStatus == 'COMPLETED' or ticket.repairStatus =='INCOMPLETE':
        ticket.checkout()

        send_ticket_update("ticket_updates", repairNumber, "CHECKOUT")
        send_queue_update("checkout_queue_updates", "Checkout Queue", "ticket_removed")

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
            send_queue_update("waiting_queue_updates", "Waiting List", "ticket_updated")
        else:
            messages.error(request, f"Invalid category selected for ticket {ticket.repairNumber} - {ticket.itemName}")
    return redirect(request.META.get('HTTP_REFERER', 'RepairCafe:waiting_list'))



def enter_password(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if entered_password == settings.VISITOR_PRESET_PASSWORD:
            request.session['preset_password_verified'] = True
            return redirect('RepairCafe:house_rules')
        elif entered_password == settings.REPAIRER_PRESET_PASSWORD:
            request.session['preset_password_verified'] = True
            return redirect('RepairCafe:repairer_login')
        else:
            return render(request, 'RepairCafe/enter_password.html', {'error': 'Incorrect Password'})
        
    return render(request, 'RepairCafe/enter_password.html')


def repairer_login(request):
    context_dict = {}
    repairers = Repairer.objects.all()
    if request.method == "POST":
        selected_repairer_name = request.POST.get('selected_repairer')
        if not selected_repairer_name:
            context_dict['errors'] = "Error: Please select a repairer before confirming."
        else:
            repairer = Repairer.objects.filter(name=selected_repairer_name).first()
            if repairer:
                request.session['repairer_name'] = repairer.name
                return redirect('RepairCafe:main_queue')
    context_dict['repairers'] = repairers

    return render(request, 'RepairCafe/repairer_login.html', context_dict)





"""
Visitor Flow
"""

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
    context_dict={}

    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            customer = Customer.objects.create(
                firstName=form_data['firstName'],
                lastName=form_data['lastName']
            )
            ticket = Ticket.objects.create(
                repairNumber=Ticket.generate_repair_number(),
                itemName=form_data['itemName'],
                itemCategory=form_data['itemCategory'],
                itemDescription=form_data['itemDescription'],
                customer=customer
            )
            waiting_queue = Queue.objects.get(name='Waiting List')  # Assuming you have this queue
            ticket.add_to_queue(waiting_queue)
            repairNumber=ticket.repairNumber

            send_queue_update("waiting_queue_updates", "Waiting List", "ticket_added")
            
            return redirect('RepairCafe:wait_for_accept', repairNumber=repairNumber)
        else:  
            context_dict['form'] = form
    else:
        form=CheckinForm()
        context_dict['form']=form
    return render(request, 'RepairCafe/checkin_form.html', context_dict)




def wait_for_accept(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    if ticket.repairStatus != "WAITING_TO_JOIN":
        raise Http404("The ticket is not in the desired state.")
    context = {
        'ticket': ticket,
        'repairNumber': repairNumber,  # Adding this explicitly
    }
    return render(request, 'RepairCafe/wait_for_accept.html', context)
                

def wait_for_repair(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    if ticket.repairStatus != "WAITING":
        print(ticket.repairStatus,ticket.repairNumber, "This is the issue for 404")
        raise Http404("The ticket is not in the desired state.")
    context_dict = {'ticket': ticket} 
    return render(request,'RepairCafe/wait_for_repair.html',context_dict)

def repair_prompt(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    print(ticket.repairStatus,ticket.repairNumber, "This is the issue for 404")
    if ticket.repairStatus != "BEING_REPAIRED":
        raise Http404("The ticket is not in the desired state.")
    repairer = ticket.repairer
    context_dict = {'ticket': ticket, 'repairer': repairer} 
    return render(request,'RepairCafe/repair_prompt.html',context_dict)

def wait_for_checkout(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    if ticket.repairStatus != "COMPLETED" and ticket.repairStatus != "INCOMPLETE":
        raise Http404("The ticket is not in the desired state.")
    if ticket.isCheckedOut !=False:
        raise Http404("The ticket is not in the desired state.")
    context_dict = {'ticket': ticket} 
    return render(request,'RepairCafe/wait_for_checkout.html',context_dict)

def checkout(request,repairNumber):
    ticket = get_object_or_404(Ticket,repairNumber=repairNumber)
    if ticket.repairStatus != "COMPLETED" and ticket.repairStatus != "INCOMPLETE":
        raise Http404("The ticket is not in the desired state.")
    if ticket.isCheckedOut != True:
        raise Http404("The ticket is not in the desired state.")
    context_dict={}
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['event_date'] = date.today()
            print(form_data)
            return redirect('RepairCafe:checkout_success')
    else:
        form=CheckoutForm
        context_dict['form']=form

    return render(request,'RepairCafe/checkout.html',context_dict)



def checkout_success(request):
    return render(request,'RepairCafe/checkout_success.html')





        
        


    

