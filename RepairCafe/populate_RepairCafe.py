import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SH28Project.settings')  # Replace with your project's settings path
import django
django.setup()

from RepairCafe.models import Ticket, Customer, Repairer, Queue

def populate():
    def add_queue(name, description):
        queue = Queue.objects.get_or_create(name=name)[0]
        queue.description = description  # Add the description
        queue.save()
        return queue

    def add_ticket(repair_number, item_name, item_category, item_description, repair_status, position, queue):
        ticket = Ticket.objects.get_or_create(
            repairNumber=repair_number,
            itemName=item_name,
            itemCategory=item_category,
            itemDescription=item_description,
            repairStatus=repair_status,
            position=position,
            queue=queue
        )[0]
        ticket.save()
        return ticket

    def add_customer(first_name, last_name):
        customer = Customer.objects.get_or_create(firstName=first_name, lastName=last_name)[0]
        customer.save()
        return customer

    def add_repairer(first_name, last_name):
        repairer = Repairer.objects.get_or_create(firstName=first_name, lastName=last_name)[0]
        repairer.save()
        return repairer

    # Queue descriptions
    queue_data = {
        'Main Queue': "The queue for tickets that have been accepted.",
        'Waiting List': "The queue for tickets to be checked by the check-in person before adding to the Main Queue.",
        'Repair Completed': "The queue for tickets with completed repairs."
    }

    tickets_data = [
        # Main Queue tickets
        {'repairNumber': '1', 'itemName': 'Washing Machine', 'itemCategory': 'ELEC', 'itemDescription': 'Needs new motor', 'repairStatus': 'WAITING', 'position': 1, 'queue': 'Main Queue'},
        {'repairNumber': '2', 'itemName': 'T-Shirt', 'itemCategory': 'TEXT', 'itemDescription': 'Small tear on sleeve', 'repairStatus': 'WAITING', 'position': 2, 'queue': 'Main Queue'},
        {'repairNumber': '4', 'itemName': 'Laptop', 'itemCategory': 'ELEC', 'itemDescription': 'Screen flickers intermittently', 'repairStatus': 'WAITING', 'position': 3, 'queue': 'Main Queue'},
        {'repairNumber': '5', 'itemName': 'Blender', 'itemCategory': 'ELEC', 'itemDescription': 'Motor won’t start', 'repairStatus': 'WAITING', 'position': 4, 'queue': 'Main Queue'},

        # Waiting List tickets
        {'repairNumber': '6', 'itemName': 'Jacket', 'itemCategory': 'TEXT', 'itemDescription': 'Broken zipper', 'repairStatus': 'WAITING', 'position': 1, 'queue': 'Waiting List'},
        {'repairNumber': '7', 'itemName': 'Table Lamp', 'itemCategory': 'ELEC', 'itemDescription': 'Damaged wire', 'repairStatus': 'WAITING', 'position': 2, 'queue': 'Waiting List'},
        {'repairNumber': '8', 'itemName': 'Garden Shears', 'itemCategory': 'TOOLS', 'itemDescription': 'Rusty blade', 'repairStatus': 'WAITING', 'position': 3, 'queue': 'Waiting List'},

        # Repair Completed queue
        {'repairNumber': '3', 'itemName': 'Hammer', 'itemCategory': 'TOOLS', 'itemDescription': 'Broken handle', 'repairStatus': 'COMPLETED', 'position': 1, 'queue': 'Repair Completed'}
    ]

    customers_data = [
        {'firstName': 'John', 'lastName': 'Doe'},
        {'firstName': 'Jane', 'lastName': 'Smith'}
    ]
    repairers_data = [
        {'firstName': 'Alice', 'lastName': 'Johnson'},
        {'firstName': 'Bob', 'lastName': 'Williams'}
    ]

    # Adding Queue objects
    queue_objects = {queue: add_queue(queue, description) for queue, description in queue_data.items()}

    # Adding Ticket objects (ensure the queue is correctly passed)
    for ticket_data in tickets_data:
        queue = queue_objects[ticket_data['queue']]  # Fetch the corresponding Queue object
        add_ticket(ticket_data['repairNumber'], ticket_data['itemName'], ticket_data['itemCategory'],
                   ticket_data['itemDescription'], ticket_data['repairStatus'], ticket_data['position'], queue)

    # Adding Customer objects
    for customer_data in customers_data:
        add_customer(customer_data['firstName'], customer_data['lastName'])

    # Adding Repairer objects
    for repairer_data in repairers_data:
        add_repairer(repairer_data['firstName'], repairer_data['lastName'])

    # Printing the results
    for queue in Queue.objects.all():
        print(f'Queue: {queue.name} - {queue.description}')
        for ticket in Ticket.objects.filter(queue=queue):
            print(f'  - Ticket: {ticket.repairNumber} - {ticket.itemName}')
        print()

if __name__ == '__main__':
    print('Starting population script...')
    populate()
