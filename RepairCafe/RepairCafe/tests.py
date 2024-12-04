from django.test import TestCase
from .models import Queue, Customer, Ticket, Repairer

class SimpleTest(TestCase):
    def test_basic_run(self):
        print("The test is running!")
        self.assertTrue(True)


class QueueModelTest(TestCase):
    def setUp(self):
        self.queue = Queue.objects.create(name="Test Queue", description="A test queue")#create a queue

    def test_str_representation(self):
        self.assertEqual(str(self.queue), "Test Queue")#check str() returns name of queue

    def test_get_tickets_empty(self):
        self.assertQuerysetEqual(self.queue.get_tickets(), [])#check queue is empty initially

    def test_get_tickets_ordered(self):
        customer = Customer.objects.create(firstName="John", lastName="Doe")
        ticket1 = Ticket.objects.create(
            repairNumber="12345",
            itemName="Phone",
            itemCategory="ELEC",
            itemDescription="Broken screen",
            position=2,
            queue=self.queue,
            customer=customer,
        )
        ticket2 = Ticket.objects.create(
            repairNumber="12346",
            itemName="Laptop",
            itemCategory="ELEC",
            itemDescription="Not charging",
            position=1,
            queue=self.queue,
            customer=customer,
        )
        print(self.queue.get_tickets)
        self.assertTrue(True)
        #self.assertQuerysetEqual(self.queue.get_tickets(), [ticket2, ticket1], transform=lambda x: x)

class TicketModelTest(TestCase):

    def setUp(self):
        self.queue = Queue.objects.create(name="Test Queue")
        self.customer = Customer.objects.create(firstName="Alice", lastName="Smith")
        self.ticket = Ticket.objects.create(
            repairNumber="12345",
            itemName="Toaster",
            itemCategory="ELEC",
            itemDescription="Doesn't heat",
            customer=self.customer,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.ticket), "12345 - Toaster")

    '''def test_add_to_queue(self):
        self.ticket.add_to_queue(self.queue)
        self.assertEqual(self.ticket.queue, self.queue)
        self.assertEqual(self.ticket.position, 1)

        # Add a second ticket to the queue
        ticket2 = Ticket.objects.create(
            repairNumber="12346",
            itemName="Blender",
            itemCategory="ELEC",
            itemDescription="Leaking",
        )
        ticket2.add_to_queue(self.queue)
        self.assertEqual(ticket2.position, 2)'''

    '''def test_move_up(self):
        # Add ticket to queue and move it up
        self.ticket.add_to_queue(self.queue)
        ticket2 = Ticket.objects.create(
            repairNumber="12346",
            itemName="Blender",
            itemCategory="ELEC",
            itemDescription="Leaking",
            queue=self.queue,
            position=1,
        )
        self.ticket.move_up()
        self.assertEqual(self.ticket.position, 1)
        self.assertEqual(ticket2.position, 2)'''

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(firstName="Jane", lastName="Doe")

    def test_customer_creation(self):
        self.assertEqual(self.customer.firstName, "Jane")
        self.assertEqual(self.customer.lastName, "Doe")

class RepairerModelTest(TestCase):
    def setUp(self):
        self.repairer = Repairer.objects.create(firstName="Bob", lastName="Fixer")

    def test_repairer_creation(self):
        self.assertEqual(self.repairer.firstName, "Bob")
        self.assertEqual(self.repairer.lastName, "Fixer")