from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Queue

def index(request):
    return render(request, 'RepairCafe/index.html', context={})

def view_queue(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)
    tickets = queue.get_tickets()
    return render(request, 'queue/view_queue.html', {'queue':queue, 'tickets':tickets})

def move_ticket(request, ticket_id, direction):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if direction == 'up':
        ticket.move_up()
    return redirect('view queue', queue_id=ticket.queue.id)
