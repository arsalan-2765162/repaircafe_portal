from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Queue

def index(request):
    return render(request, 'RepairCafe/index.html', context={})

def view_queue(request,name):
    context_dict={}
    try:
        queue = Queue.objects.get(name=name)
        context_dict['Queue']=queue
    except Queue.DoesNotExist:
        context_dict['Queue']=None
    return render(request, 'RepairCafe/queue.html', context=context_dict)

def move_ticket(request, ticket_id, direction):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if direction == 'up':
        ticket.move_up()
    return redirect('RepairCafe:view_queue', queue_id=ticket.queue.name)

