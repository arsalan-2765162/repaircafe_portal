import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SH28Project.settings')  # Replace with your project's settings path
import django
django.setup()

from RepairCafe.models import Ticket, Customer, Repairer, Queue

def populate():
    for each in [Ticket, Customer, Repairer, Queue]:
        print(each)
        x = each.objects.all()
        for entry in x:
            entry.delete()
    def add_queue(name, description):
        queue = Queue.objects.get_or_create(name=name)[0]
        queue.description = description  # Add the description
        queue.save()
        return queue

    def add_ticket(repair_number, item_name, item_category, item_description, repair_status, position, queue, customer):
        ticket = Ticket.objects.get_or_create(
            repairNumber=repair_number,
            itemName=item_name,
            itemCategory=item_category,
            itemDescription=item_description,
            repairStatus=repair_status,
            position=position,
            queue=queue,
            customer=customer
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
    }

    tickets_data = [
        # Main Queue tickets
        {'repairNumber': '1', 'itemName': 'Vase', 'itemCategory': 'CERA', 'itemDescription': 'Cracked Base', 'repairStatus': 'COMPLETED', 'position': None, 'queue': 'Main Queue'},
        {'repairNumber': '2', 'itemName': 'T-Shirt', 'itemCategory': 'TEXT', 'itemDescription': 'Small tear on sleeve', 'repairStatus': 'COMPLETED', 'position': None, 'queue': 'Main Queue'},
        {'repairNumber': '3', 'itemName': 'Laptop', 'itemCategory': 'ELEC', 'itemDescription': 'Screen flickers intermittently', 'repairStatus': 'WAITING', 'position': 1, 'queue': 'Main Queue'},
        {'repairNumber': '4', 'itemName': 'Blender', 'itemCategory': 'ELECM', 'itemDescription': 'Motor won’t start', 'repairStatus': 'INCOMPLETE', 'position': None, 'queue': 'Main Queue'},
        {'repairNumber': '5', 'itemName': 'Lamp', 'itemCategory': 'ELECM', 'itemDescription': 'Light won’t turn on', 'repairStatus': 'WAITING', 'position': 2, 'queue': 'Main Queue'},
        {'repairNumber': '6', 'itemName': 'Bowl', 'itemCategory': 'CERA', 'itemDescription': 'Chipped edges of bowl', 'repairStatus': 'WAITING', 'position': 3, 'queue': 'Main Queue'},
        {'repairNumber': '7', 'itemName': 'Hair Dryer', 'itemCategory': 'ELEC', 'itemDescription': 'Not turning on', 'repairStatus': 'WAITING', 'position': 4, 'queue': 'Main Queue'},
        {'repairNumber': '8', 'itemName': 'Toaster', 'itemCategory': 'ELEC', 'itemDescription': 'Broken heating element', 'repairStatus': 'NEED_PAT', 'position': 5, 'queue': 'Main Queue'},
        {'repairNumber': '9', 'itemName': 'Jumper', 'itemCategory': 'TEXT', 'itemDescription': 'Tear on sleeve', 'repairStatus': 'WAITING', 'position': 6, 'queue': 'Main Queue'},
        {'repairNumber': '10', 'itemName': 'Coffee Maker', 'itemCategory': 'OTHER', 'itemDescription': 'Water not heating', 'repairStatus': 'WAITING', 'position': 7, 'queue': 'Main Queue'},

        # Waiting List tickets
        {'repairNumber': '11', 'itemName': 'Jacket', 'itemCategory': 'TEXT', 'itemDescription': 'Broken zipper', 'repairStatus': 'WAITING_TO_JOIN', 'position': 1, 'queue': 'Waiting List'},
        {'repairNumber': '12', 'itemName': 'Table Lamp', 'itemCategory': 'ELEC', 'itemDescription': 'Damaged wire', 'repairStatus': 'WAITING_TO_JOIN', 'position': 2, 'queue': 'Waiting List'},
        {'repairNumber': '13', 'itemName': 'Garden Shears', 'itemCategory': 'OTHER', 'itemDescription': 'Rusty blade', 'repairStatus': 'WAITING_TO_JOIN', 'position': 3, 'queue': 'Waiting List'},
        {'repairNumber': '14', 'itemName': 'Curtains', 'itemCategory': 'TEXT', 'itemDescription': 'Stitching torn', 'repairStatus': 'WAITING_TO_JOIN', 'position': 4, 'queue': 'Waiting List'},
        {'repairNumber': '15', 'itemName': 'Sewing Machine', 'itemCategory': 'OTHER', 'itemDescription': 'Needle not moving', 'repairStatus': 'WAITING_TO_JOIN', 'position': 5, 'queue': 'Waiting List'},
    ]

    customers_data = [
        {'firstName': 'John', 'lastName': 'Doe'},
        {'firstName': 'Jane', 'lastName': 'Smith'},
        {'firstName': 'Robert', 'lastName': 'Brown'},
        {'firstName': 'Emily', 'lastName': 'Davis'},
        {'firstName': 'Michael', 'lastName': 'Wilson'},
        {'firstName': 'Sarah', 'lastName': 'Anderson'},
        {'firstName': 'David', 'lastName': 'Taylor'},
        {'firstName': 'Emma', 'lastName': 'Thomas'},
        {'firstName': 'James', 'lastName': 'Martin'},
        {'firstName': 'Laura', 'lastName': 'White'},
        {'firstName': 'Daniel', 'lastName': 'Moore'},
        {'firstName': 'Sophie', 'lastName': 'Jackson'},
        {'firstName': 'Oliver', 'lastName': 'Harris'},
        {'firstName': 'Lucy', 'lastName': 'Clark'},
        {'firstName': 'William', 'lastName': 'Lewis'}
    ]
    repairers_data = [
        {'firstName': 'Alice', 'lastName': 'Johnson'},
        {'firstName': 'Bob', 'lastName': 'Williams'},
        {'firstName': 'Eve', 'lastName': 'Clark'}
    ]

    customers = []
    for customer_data in customers_data:
        customers.append(add_customer(customer_data['firstName'], customer_data['lastName']))


    # Adding Queue objects
    queue_objects = {queue: add_queue(queue, description) for queue, description in queue_data.items()}

    # Adding Ticket objects (ensure the queue is correctly passed)
    for i, ticket_data in enumerate(tickets_data):
        queue = queue_objects[ticket_data['queue']]
        # Use modulo to cycle through customers if there are more tickets than customers
        customer = customers[i]
        add_ticket(
            ticket_data['repairNumber'], 
            ticket_data['itemName'], 
            ticket_data['itemCategory'],
            ticket_data['itemDescription'], 
            ticket_data['repairStatus'], 
            ticket_data['position'], 
            queue,
            customer
        )



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
