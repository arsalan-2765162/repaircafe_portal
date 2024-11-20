from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Queue

def index(request):
    return render(request, 'RepairCafe/index.html', context={})


def main_queue(request):
    context_dict={}
    try:
        queue = Queue.objects.get(name="Main Queue")
        ticket_list = Ticket.objects.filter(queue=queue).order_by('position')
        context_dict['Queue']=queue
        context_dict['Tickets']=ticket_list
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/main_queue.html', context=context_dict)

def waiting_list(request):
    context_dict={}
    try:
        queue = Queue.objects.get(name="Waiting List")
        ticket_list = Ticket.objects.filter(queue=queue).order_by('position')
        context_dict['Queue']=queue
        context_dict['Tickets']=ticket_list
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/waiting_list.html', context=context_dict)

def move_ticket(request, ticket_id, direction):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if direction == 'up':
        ticket.move_up()
    return redirect('RepairCafe:view_queue', queue_id=ticket.queue.name)

#def show_navbar(request):

