from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Queue
from .forms import TicketFilterForm

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
            status_filter = form.cleaned_data.get('repairStatus')
            category_filter = form.cleaned_data.get('itemCategory')
            if status_filter and status_filter != 'ALL':
                ticket_list = ticket_list.filter(repairStatus=status_filter)
            if category_filter and category_filter != 'ALL':
                ticket_list = ticket_list.filter(itemCategory=category_filter)
        else:
            ticket_list=ticket_list.filter(repairStatus='WAITING')

        
        
        context_dict['Queue']=queue
        context_dict['Tickets']=ticket_list
        context_dict['form']=form
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
        
        
        context_dict['Queue']=queue
        context_dict['Tickets']=ticket_list
        context_dict['form']=form
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/waiting_list.html', context=context_dict)

def move_ticket(request, ticket_id, direction):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if direction == 'up':
        ticket.move_up()
    return redirect('RepairCafe:view_queue', queue_id=ticket.queue.name)

#def show_navbar(request):

