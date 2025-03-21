from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, redirect
from .models import Ticket, Queue, Customer, UserRoles, Repairer, SharedPassword
from .forms import TicketFilterForm,TicketForm,IncompleteTicketForm,RulesButton, CheckinForm, CheckoutForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import populate_RepairCafe as script
from django.conf import settings
from datetime import date
from django.db.models import Max
from django.http import JsonResponse, Http404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from functools import wraps
import csv
import json
from datetime import datetime

def check_user_password(user_type, provided_password):
    try:
        shared_password = SharedPassword.objects.get(user_type=user_type)
        return shared_password.check_password(provided_password)
    except SharedPassword.DoesNotExist:
        return False


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



def get_queue_position(request, repairNumber):
    try:
        ticket = Ticket.objects.get(repairNumber=repairNumber)
        return JsonResponse({'position': ticket.position})
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)


def reset_data(request): 

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    script.populate()
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
        return HttpResponseRedirect('RepairCafe/main_queue.html')






def main_queue(request):
    

    # Check if the user is authenticated and has an active role
    if not request.user.is_authenticated or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))




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
            ticket_list = ticket_list.filter(repairStatus='WAITING')

        #populate the list of forms used to display all tickets in the queue
        ticketForms = [TicketForm(instance=ticket) for ticket in ticket_list]
        context_dict['TicketForms'] = ticketForms
        context_dict['Queue'] = queue
        context_dict['Tickets'] = ticket_list
        context_dict['FilterForm'] = form
    except Queue.DoesNotExist:
        context_dict['Queue'] = None
    return render(request, 'RepairCafe/main_queue.html', context=context_dict)



def waiting_list(request):

    if not request.user.is_authenticated or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    '''if len(request.user.roles) > 1 and not request.user.activerole: #if user has multiple roles and activerole is not set, redirect to a page where they select the role they use to access this page
       return redirect('RepairCafe:role_selection')
    elif len(request.user.roles) == 1:
        request.user.activerole = request.user.roles[0]
        request.user.save()'''




    context_dict={}
    try:
        queue = Queue.objects.get(name="Waiting List")
        ticket_list = Ticket.objects.filter(queue=queue, repairStatus='WAITING_TO_JOIN').order_by('position')

        form = TicketFilterForm(request.GET or None)
        print("Form is valid:", form.is_valid())  # This will print if the form is valid
        if form.is_valid():
            category_filter = form.cleaned_data.get('itemCategory')
            if category_filter and category_filter != 'ALL':
                ticket_list = ticket_list.filter(itemCategory=category_filter)

        #populate the list of forms used to display all tickets in waiting list
        waitingForms = [TicketForm(instance=ticket) for ticket in ticket_list]
        context_dict['TicketForms'] = waitingForms

        context_dict['Queue'] = queue
        context_dict['Tickets'] = ticket_list
        context_dict['WaitingForm'] = form
        context_dict['Ticket'] = Ticket
    except Queue.DoesNotExist:
        context_dict['Queue'] = None
    return render(request, 'RepairCafe/waiting_list.html', context=context_dict)

def checkout_queue(request, activerole=""):

    '''if len(request.user.roles) > 1 and not request.user.activerole: #if user has multiple roles, redirect to a page where they select the role they use to access this page
        redirect('RepairCafe:role_selection')
    elif len(request.user.roles) == 1:
        request.user.activerole = request.user.roles[0]
        request.user.save()'''

    if not request.user.is_authenticated or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))

    context_dict={}
    try:
        queue = Queue.objects.get(name="Checkout Queue")
        ticket_list = Ticket.objects.filter(isCheckedOut=False,
                                            queue=queue,
                                            repairStatus__in=['COMPLETED', 'INCOMPLETE']).order_by('position')

        form = TicketFilterForm(request.GET or None)
        if form.is_valid():
            category_filter = form.cleaned_data.get('itemCategory')
            if category_filter and category_filter != 'ALL':
                ticket_list = ticket_list.filter(itemCategory=category_filter)

        context_dict['Queue'] = queue
        context_dict['Tickets'] = ticket_list
        context_dict['WaitingForm'] = form
    except Queue.DoesNotExist:
        context_dict['Queue'] = None
    return render(request, 'RepairCafe/checkout_queue.html', context=context_dict)


def basic_stats(request):

    if not request.user.is_authenticated or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))

    checkedin = Ticket.objects.exclude(repairStatus="WAITING").count()
    checkedout = Ticket.objects.filter(isCheckedOut=True).count()
    successful = Ticket.objects.filter(repairStatus="COMPLETED").count()
    unsuccessful = Ticket.objects.filter(repairStatus="INCOMPLETE").count()
    catpercentages = {}

    for category in Ticket.ITEM_CATEGORY_CHOICES:
        catpercentages[category] = round(((Ticket.objects.filter(itemCategory=category[0])
                                           .count()) / (Ticket.objects.count()) * 100), 1)

    context_dict = {"checkedin": checkedin, "checkedout": checkedout,
                    "successful": successful, "unsuccessful": unsuccessful,
                    "catpercentages": catpercentages}

    return render(request, 'RepairCafe/basic_stats.html', context_dict)


def accept_ticket(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    repairNumber = repairNumber

    if ticket.repairStatus == 'WAITING_TO_JOIN':
        ticket.accept_ticket()

        send_ticket_update("ticket_updates",repairNumber, "ACCEPTED")
        send_queue_update("main_queue_updates", "Main Queue", "ticket_added")
        send_queue_update("waiting_queue_updates", "Waiting List", "ticket_removed")

        messages.success(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been accepted.")
    else:
        messages.error(request, f"Error, ticket {ticket.repairNumber}:{ticket.itemName}, not accepted.")
    return redirect(reverse('RepairCafe:waiting_list'))


def repair_ticket(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
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


def mark_incomplete_ticket(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
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
        incompleteForm = IncompleteTicketForm()
    context_dict = {'ticket': ticket, 'form': incompleteForm}
    return render(request, 'RepairCafe/mark_incomplete_ticket.html', context_dict)


def repair_item(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    context_dict = {}
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    incompleteForm = IncompleteTicketForm()

    send_ticket_update("ticket_updates", repairNumber, "REPAIRING")
    send_queue_update("main_queue_updates", "Main Queue", "ticket_being_repaired")

    context_dict['incompleteForm'] = incompleteForm
    context_dict['ticket'] = ticket
    return render(request, 'RepairCafe/repair_item.html', context_dict)


def complete_ticket(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    if ticket.repairStatus == 'BEING_REPAIRED' and ticket.itemCategory == "ELECM":
        ticket.complete_ticket()
        send_ticket_update("ticket_updates", repairNumber, "WAIT_FOR_PAT")
        send_queue_update("main_queue_updates", "Main Queue", "ticket_updated")

        messages.success(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been sent to PAT Testing.")
    elif (ticket.repairStatus == 'BEING_REPAIRED'):
        ticket.complete_ticket()

        send_ticket_update("ticket_updates", repairNumber, "WAIT_FOR_CHECKOUT")
        send_queue_update("main_queue_updates", "Main Queue", "ticket_removed")
        send_queue_update("checkout_queue_updates", "Checkout Queue", "ticket_removed")

        messages.success(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been marked as completed.")
    else:
        messages.error(request, f"Error, ticket {ticket.repairNumber} - {ticket.itemName}, not completed")

    return redirect(reverse('RepairCafe:main_queue'))


def pat_test(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
        action = request.POST.get('action')

        if action == 'accept':
            ticket.add_to_checkout()  
            ticket.repairStatus = 'COMPLETED'
            ticket.save()

            send_ticket_update("ticket_updates", repairNumber, "WAIT_FOR_CHECKOUT")
            send_queue_update("main_queue_updates", "Main Queue", "ticket_removed")
            send_queue_update("checkout_queue_updates", "Checkout Queue", "ticket_added")

            messages.success(request, f'PAT Test completed for Repair #{repairNumber}. Ticket moved to checkout queue.')

        elif action == 'reject':
            ticket.add_to_checkout()  
            ticket.repairStatus = 'COMPLETED'
            ticket.save()

            send_ticket_update("ticket_updates", repairNumber, "WAIT_FOR_CHECKOUT")
            send_queue_update("main_queue_updates", "Main Queue", "ticket_removed")
            send_queue_update("checkout_queue_updates", "Checkout Queue", "ticket_added")

            messages.warning(request, f'PAT Test rejected for Repair #{repairNumber}. Ticket moved to checkout queue.')

        return redirect('RepairCafe:main_queue')

    return HttpResponseBadRequest("Invalid request method")


def delete_ticket(request,repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    ticket = Ticket.objects.get(repairNumber=repairNumber)
    ticket.delete_ticket()
    messages.success(request, f"Ticket: {ticket.itemName}, has been removed")
    send_queue_update("waiting_queue_updates", "Waiting List", "ticket_removed")
    return redirect('RepairCafe:waiting_list')


def checkout_ticket(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus == 'COMPLETED' or ticket.repairStatus == 'INCOMPLETE':
        ticket.checkout()
        send_ticket_update("ticket_updates", repairNumber, "CHECKOUT")
        send_queue_update("checkout_queue_updates", "Checkout Queue", "ticket_removed")

        messages.success(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been checked out.")
        messages.success(request, f"Ticket {ticket.repairNumber} - {ticket.itemName}, has been checked out.")
    else:
        messages.error(request,f"Error checking out Ticket {ticket.repairNumber} - {ticket.itemName}")
    if (ticket.isVolunteerCreated):
        return redirect('RepairCafe:volunteer_checkout', repairNumber=repairNumber)
    return redirect(reverse('RepairCafe:checkout_queue'))


def change_category(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
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


def authenticate_roles(request):

    new_roles = UserRoles.objects.create()
    login(request, new_roles,backend='django.contrib.auth.backends.ModelBackend')
    
    return new_roles

def enter_password(request):
      
    
    if not request.user.is_authenticated:
     user = authenticate_roles(request)  
        
    #if user is None:  
     #      return render(request, 'RepairCafe/enter_password.html', {'error': 'Authentication failed'})
        
          

    if request.method == 'POST':
        entered_password = request.POST.get('password')
        if check_user_password("visitor", entered_password):
            role = "visitor"
        elif check_user_password("repairer", entered_password):
            role = "repairer"
            request.user.activerole = role
            request.user.save()
            return redirect('RepairCafe:repairer_login')
        elif check_user_password("volunteer", entered_password):
            role = "volunteer"
            request.session['preset_password_verified'] = True
        else:
            return render(request, 'RepairCafe/enter_password.html', {'error': 'Incorrect Password'})        
         
        
        print("assigning role")
        request.user.activerole = role
        request.user.save()

        
        if role == "visitor":
            return redirect('RepairCafe:house_rules')
        elif role == "volunteer":
            return redirect('RepairCafe:waiting_list')
        elif role == "repairer":
            return redirect('RepairCafe:repairer_login')
        

        
    
    return render(request, 'RepairCafe/enter_password.html')

def repairer_login(request):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    
    context_dict = {}
    repairers = Repairer.objects.all()
    if request.method == "POST":
        selected_repairer_name = request.POST.get('selected_repairer')
        user = authenticate_roles(request)
        request.user.activerole = "repairer"
        #request.user.roles.append("repairer")
        request.user.save()
        if not selected_repairer_name:
            context_dict['errors'] = "Error: Please select a repairer before confirming."
        else:
            repairer = Repairer.objects.filter(name=selected_repairer_name).first()
            if repairer:
                request.session['repairer_name'] = repairer.name
                request.session["repairer_picture"] = (
                    repairer.picture.url if repairer.picture else "/static/images/default.jpg"
                ) 
                return redirect('RepairCafe:main_queue')
    context_dict['repairers'] = repairers

    return render(request, 'RepairCafe/repairer_login.html', context_dict)


def repairer_logout(request):
    request.session.flush()
    return redirect("RepairCafe:enter_password")

def settings_page(request):
    return render(request, 'RepairCafe/settings_page.html')

def volunteer_checkout(request, repairNumber):

    if (not request.user.is_authenticated) or not request.user.activerole:
        return redirect(reverse('RepairCafe:enter_password'))
    
    if request.user.activerole == "visitor":
        return redirect(reverse('RepairCafe:index'))
    


    
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus != "COMPLETED" and ticket.repairStatus != "INCOMPLETE":
        raise Http404("The ticket is not in the desired state.")
    if not ticket.isCheckedOut:
        raise Http404("The ticket is not in the desired state.")
    context_dict = {}
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['event_date'] = date.today()
            print(form_data)
            return redirect('RepairCafe:volunteer_checkout_success')
    else:
        form = CheckoutForm
        context_dict['form'] = form

    return render(request, 'RepairCafe/volunteer_checkout.html', context_dict)


def volunteer_checkout_success(request):
    return render(request, 'RepairCafe/volunteer_checkout_success.html')




def role_selection(request): #OBSOLETE


    if request.method == 'POST':
        selected = request.POST.get('role')
        if selected:
            print(selected)           
            request.user.activerole = selected
            request.user.save()

            redirect_url = request.GET.get('redirect_to', 'RepairCafe:main_queue')
            print(f"Redirecting to: {redirect_url}") 
            
            return redirect(redirect_url)#should redirect to whichever page redirected here, but hardcoded to index for now

    return render(request, 'RepairCafe/role_selection.html', {
        'roles': request.user.roles
    })

def logout(request):

    if request.method == 'POST':
        selected = request.POST.get('role')
        if selected:
            print(selected)      
            #request.user.roles.remove(selected)     
            request.user.activerole = ""
            request.user.delete()

            '''if len(request.user.roles) == 0:
                request.user.delete()
                return redirect('RepairCafe:enter_password')'''
            
            return redirect('RepairCafe:main_queue')
        
    return render(request, 'RepairCafe/logout.html', {'roles': request.user.activerole})

"""
Visitor Flow
"""


def house_rules(request):

    request.user.activerole = "visitor"
    request.user.save()

    
    

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
    context_dict = {}

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
                customer=customer,
                checkinFormData=form_data
            )
            waiting_queue = Queue.objects.get(name='Waiting List')  # Assuming you have this queue
            ticket.add_to_queue(waiting_queue)
            repairNumber = ticket.repairNumber

            send_queue_update("waiting_queue_updates", "Waiting List", "ticket_added")
            
            if request.user.activerole == "volunteer":
                return redirect('RepairCafe:index')
            else:
                return redirect('RepairCafe:wait_for_accept', repairNumber=repairNumber)
        else:  
            context_dict['form'] = form
    else:
        form=CheckinForm()
        context_dict['form']=form

    if request.user.activerole == "visitor":
        return render(request, 'RepairCafe/checkin_form.html', context_dict)
    elif request.user.activerole == "volunteer":
        return render(request, 'RepairCafe/volunteer_checkin.html', context_dict)



def wait_for_accept(request, repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus != "WAITING_TO_JOIN":
        raise Http404("The ticket is not in the desired state.")
    context = {
        'ticket': ticket,
        'repairNumber': repairNumber,  # Adding this explicitly
    }
    return render(request, 'RepairCafe/wait_for_accept.html', context)


def wait_for_repair(request, repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus != "WAITING":
        print(ticket.repairStatus, ticket.repairNumber, "This is the issue for 404")
        raise Http404("The ticket is not in the desired state.")
    context_dict = {'ticket': ticket} 
    return render(request, 'RepairCafe/wait_for_repair.html', context_dict)


def repair_prompt(request, repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    print(ticket.repairStatus, ticket.repairNumber, "This is the issue for 404")
    if ticket.repairStatus != "BEING_REPAIRED":
        raise Http404("The ticket is not in the desired state.")
    repairer = ticket.repairer
    context_dict = {'ticket': ticket, 'repairer': repairer} 
    return render(request,'RepairCafe/repair_prompt.html',context_dict)

def wait_for_checkout(request, repairNumber):
    context_dict = {}
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus != "COMPLETED" and ticket.repairStatus != "INCOMPLETE":
        raise Http404("The ticket is not in the desired state.")
    if ticket.isCheckedOut:
        raise Http404("Ticket is already checked out.")
    context_dict['ticket'] = ticket
    return render(request, 'RepairCafe/wait_for_checkout.html', context_dict)


def wait_for_pat(request, repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    context_dict = {}
    if ticket.repairStatus != "NEED_PAT":
        raise Http404("The ticket is not in the desired state.")
    if ticket.isCheckedOut:
        raise Http404("Ticket is already checked out.")
    context_dict['ticket'] = ticket
    return render(request, 'RepairCafe/wait_for_pat.html', context_dict)
    context_dict = {'ticket': ticket}
    return render(request, 'RepairCafe/wait_for_checkout.html')


def checkout(request, repairNumber):
    ticket = get_object_or_404(Ticket, repairNumber=repairNumber)
    if ticket.repairStatus != "COMPLETED" and ticket.repairStatus != "INCOMPLETE":
        raise Http404("The ticket is not in the desired state.")
    if not ticket.isCheckedOut:
        raise Http404("The ticket is not in the desired state.")
    context_dict = {}
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['event_date'] = date.today().isoformat()
            ticket.checkoutFormData = form_data
            ticket.save()
            return redirect('RepairCafe:checkout_success')
    else:
        form = CheckoutForm
        context_dict['form'] = form

    return render(request, 'RepairCafe/checkout.html', context_dict)


def checkout_success(request):
    return render(request, 'RepairCafe/checkout_success.html')

def export_to_csv(request):
    #print(request.POST)
    #print("Exporting to CSV")
    
    startDate = request.POST.get('export_start_date')
    endDate = request.POST.get('export_end_date')
    if not startDate:
        startDate = datetime(1889, 1, 1, 0, 0, 0)
    if not endDate:
        endDate = datetime.now()
    print(startDate, endDate)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="repairCafeData.csv"'

    writer = csv.writer(response)
    writer.writerow(['Repair Number', 'Item Name', 'Item Category', 'Repair Status', 'Time Created', 'Repairer', 'Checkin Form Data', 'Checkout Form Data', 'Carbon Footprint Category', 'Created by volunteer', 'Incomplete Reason','position','queue','Visitor'])

    tickets = Ticket.objects.filter(time_created__range=[startDate,endDate])
    for ticket in tickets:
        writer.writerow([ticket.repairNumber, ticket.itemName, ticket.itemCategory, ticket.repairStatus, ticket.time_created, ticket.repairer, ticket.checkinFormData, ticket.checkoutFormData, ticket.carbon_footprint_category,"Yes" if ticket.isVolunteerCreated else "No",ticket.incompleteReason if ticket.incompleteReason else "N/A", ticket.position, ticket.queue, ticket.customer])

    return response
