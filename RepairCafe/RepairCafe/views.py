from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Queue
from .forms import TicketFilterForm,TicketForm
from django.urls import reverse
from django.contrib import messages

def index(request):
    return render(request, 'RepairCafe/index.html', context={})


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
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/waiting_list.html', context=context_dict)

def move_ticket(request, ticket_id, direction):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if direction == 'up':
        ticket.move_up()
    return redirect('RepairCafe:view_queue', queue_id=ticket.queue.name)

def accept_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    if ticket.repairStatus == 'WAITING_TO_JOIN':
        ticket.accept_ticket()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been accepted")
    else:
        messages.error(request,f"Error, ticket {ticket.repairNumber}:{ticket.itemName}, not accepted")
    return redirect(reverse('RepairCafe:waiting_list'))

def repair_ticket(request,repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus == "WAITING":
        ticket.repair_ticket()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, is now being repaired")
    else:
        messages.error(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, cannot be accepted as it is not in WAITING status.")
    return redirect('RepairCafe:repair_item', repairNumber=repairNumber)

def repair_item(request,repairNumber):
    ticket=get_object_or_404(Ticket,repairNumber=repairNumber)
    return render(request,'RepairCafe/repair_item.html',{'ticket':ticket})

def complete_ticket(request,repairNumber):
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    if ticket.repairStatus == 'BEING_REPAIRED':
        ticket.complete_ticket()
        messages.success(request,f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been marked complete")
    else:
        messages.error(request,f"Error, ticket {ticket.repairNumber}:{ticket.itemName}, not completed")
    return redirect(reverse('RepairCafe:main_queue'))
        
    

