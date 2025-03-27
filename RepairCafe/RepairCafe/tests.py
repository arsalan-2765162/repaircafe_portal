from django.test import TestCase, Client
from .models import Queue, Customer, Ticket, Repairer, UserRoles
from django.urls import reverse
import time
from unittest.mock import patch


class SimpleTest(TestCase):
    def test_basic_run(self):
        print("The test is running!")
        self.assertTrue(True)


class QueueModelTest(TestCase):
    def setUp(self):
        self.queue = Queue.objects.create(name="Test Queue", description="A test queue")  #create a queue

    def test_str_representation(self):
        self.assertEqual(str(self.queue), "Test Queue")  #check str() returns name of queue

    def test_get_tickets_empty(self):
        self.assertQuerysetEqual(self.queue.get_tickets(), [])  #check queue is empty initially

    def test_get_tickets_ordered(self):
        customer1 = Customer.objects.create(firstName="John", lastName="Doe")
        customer2 = Customer.objects.create(firstName="Joe", lastName="Blogs")
        # can only have one item per customer or get error
        ticket1 = Ticket.objects.create(
            repairNumber=12345,
            itemName="Phone",
            itemCategory="ELEC",
            itemDescription="Broken screen",
            position=2,
            queue=self.queue,
            customer=customer1,
        )

        ticket2 = Ticket.objects.create(
            repairNumber=12346,
            itemName="Laptop",
            itemCategory="ELEC",
            itemDescription="Not charging",
            position=1,
            queue=self.queue,
            customer=customer2,
        )
        self.assertQuerysetEqual(self.queue.get_tickets(), [ticket2, ticket1], transform=lambda x: x)


class TicketModelTest(TestCase):

    def setUp(self):
        self.queue = Queue.objects.create(name="Test Queue")
        self.customer = Customer.objects.create(firstName="Alice", lastName="Smith")
        self.ticket = Ticket.objects.create(
            repairNumber=12345,
            itemName="Toaster",
            itemCategory="ELEC",
            itemDescription="Doesn't heat",
            customer=self.customer,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.ticket), "12345 - Toaster")

    def test_add_to_queue(self):
        self.ticket.add_to_queue(self.queue)
        self.assertEqual(self.ticket.queue, self.queue)
        self.assertEqual(self.ticket.position, 1)

        # Add a second ticket to the queue
        ticket2 = Ticket.objects.create(
            repairNumber=12346,
            itemName="Blender",
            itemCategory="ELEC",
            itemDescription="Leaking",
        )
        ticket2.add_to_queue(self.queue)
        self.assertEqual(ticket2.position, 2)
    #is ability to move up required?
    '''def test_move_up(self):
        # Add ticket to queue and move it up
        self.ticket.add_to_queue(self.queue)
        ticket2 = Ticket.objects.create(
            repairNumber=12346,
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
        self.repairer = Repairer.objects.create(name="Bob")

    def test_repairer_creation(self):
        self.assertEqual(self.repairer.name, "Bob")

    def test_repairer_picture_default(self):
        self.assertFalse(bool(self.repairer.picture), "Expected picture field to be empty by default")


class TestRedirectToEnterPassword(TestCase):
    def setUp(self):
        self.client = Client()


    ''' def test_redirect_to_enter_password_index(self):
        # Simulate an unauthenticated request
        response = self.client.get(reverse('RepairCafe:index'))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(response.url.startswith(reverse('RepairCafe:enter_password')))  # Verify target URL'''

    def test_redirect_to_enter_password_reset_data(self):
        # Simulate an unauthenticated request
        response = self.client.get(reverse('RepairCafe:reset_data'))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(response.url, reverse('RepairCafe:enter_password'))  # Verify target URL

    def test_redirect_to_enter_password_main_queue(self):
        # Simulate an unauthenticated request
        response = self.client.get(reverse('RepairCafe:main_queue'))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(response.url, reverse('RepairCafe:enter_password'))  # Verify target URL

    def test_redirect_to_enter_password_waiting_list(self):
        # Simulate an unauthenticated request
        response = self.client.get(reverse('RepairCafe:waiting_list'))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(response.url, reverse('RepairCafe:enter_password'))  # Verify target URL

    def test_redirect_to_enter_password_checkout_queue(self):
        # Simulate an unauthenticated request
        response = self.client.get(reverse('RepairCafe:checkout_queue'))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(response.url, reverse('RepairCafe:enter_password'))  # Verify target URL

    def test_redirect_to_enter_password_house_rules(self):
        # Simulate an unauthenticated request

        response = self.client.get(reverse('RepairCafe:house_rules'))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(response.url, reverse('RepairCafe:enter_password'))  # Verify target URL


class RepairCafeViewsTestPasswordEntered(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = UserRoles.objects.create_user(username="testuser", password="testpass")
        self.user.activerole = "volunteer"
        self.user.save()
        self.client.login(username="testuser", password="testpass")

        # Simulate a session where the password has been entered
        session = self.client.session
        session['preset_password_verified'] = True
        session.save()

        # Set up common test data
        self.queue = Queue.objects.get_or_create(name="Main Queue")[0]
        self.wait_list=Queue.objects.get_or_create(name="Waiting List")[0]
        self.checkout=Queue.objects.get_or_create(name="Checkout Queue")[0]
        self.customer = Customer.objects.create(firstName="Alice", lastName="Smith")
        self.ticket = Ticket.objects.create(
            repairNumber=12345,
            itemName="Laptop",
            itemCategory="ELEC",
            itemDescription="Battery not charging",
            repairStatus="WAITING",
            queue=self.queue,
            customer=self.customer,
        )

    '''def test_index_view(self):
        response = self.client.get(reverse('RepairCafe:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RepairCafe/index.html')'''

    def test_reset_data_view(self):
        Ticket.objects.all().delete()
        response = self.client.get(reverse('RepairCafe:reset_data'))
        self.assertEqual(response.status_code, 302)
        self.assertGreater(len(Queue.objects.get(name='Main Queue').get_tickets()), 0)
        self.assertGreater(len(Queue.objects.get(name='Waiting List').get_tickets()), 0)
        self.assertGreater(len(Queue.objects.get(name='Checkout Queue').get_tickets()), 0)

    def test_main_queue_view(self):
        response = self.client.get(reverse('RepairCafe:main_queue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RepairCafe/main_queue.html')
        self.assertIn('Tickets', response.context)

    def test_waiting_list(self):
        self.client.get(reverse('RepairCafe:reset_data'))
        response = self.client.get(reverse('RepairCafe:waiting_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tickets', response.context)

    def test_checkout_queue(self):
        self.client.get(reverse('RepairCafe:reset_data'))
        response = self.client.get(reverse('RepairCafe:checkout_queue'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tickets', response.context)

    def test_enter_password_view(self):
        response = self.client.get(reverse('RepairCafe:enter_password'))
        #self.assertEqual(response.status_code, 302) should redirect if password already entered
        #self.assertTemplateUsed(response, 'RepairCafe/enter_password.html')

    def test_house_rules_view(self):
        response = self.client.get(reverse('RepairCafe:house_rules'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RepairCafe/house_rules.html')

    def test_accept_ticket_view(self):
        self.client.get(reverse('RepairCafe:reset_data'))
        self.ticket_to_accept = Queue.objects.get(name="Waiting List").get_tickets()[0]
        self.client.get(reverse('RepairCafe:accept_ticket', args=[self.ticket_to_accept.repairNumber]))
        self.assertIn(self.ticket_to_accept, Queue.objects.get(name="Main Queue").get_tickets())

    def test_repair_ticket_view(self):
        self.client.get(reverse('RepairCafe:reset_data'))
        self.ticket_to_repair = Queue.objects.get(name="Main Queue").get_tickets()[1]
        print(self.ticket_to_repair)
        print(self.ticket_to_repair.repairStatus)
        self.client.get(reverse('RepairCafe:repair_ticket', args=[self.ticket_to_repair.repairNumber]))
        self.ticket_to_repair.repair_ticket()
        self.assertEqual(self.ticket_to_repair.repairStatus, "BEING_REPAIRED")

    '''def test_complete_ticket_mains(self):
        self.client.get(reverse('RepairCafe:reset_data'))
        self.ticket_to_complete=Ticket.objects.filter(queue=Queue.objects.get(name="Main Queue"))[0]
        self.ticket_to_complete.repairStatus="BEING_REPAIRED"
        self.ticket_to_complete.itemCategory="ELECM"

        self.client.get(reverse('RepairCafe:complete_ticket',args=[self.ticket_to_complete.repairNumber]))
        self.assertEqual(self.ticket_to_complete.repairStatus,"NEED_PAT")'''

    def test_complet_ticket_non_mains(self):
        pass

    def test_delete_ticket(self):
        self.ticket_to_delete = Ticket.objects.filter(queue=Queue.objects.get(name="Main Queue"))[0]
        self.client.get(reverse('RepairCafe:delete_ticket', args=[self.ticket_to_delete.repairNumber]))
        self.assertNotIn(self.ticket_to_delete, Ticket.objects.all())

    def test_checkout_ticket(self):
        pass

    def test_change_category(self):
        pass

    def test_enter_password(self):
        pass

    def test_checkin_form(self):
        pass

    def test_checkin_form_incomplete(self):
        pass

    def test_checkout(self):
        pass

    def test_checkout_incomplete(self):
        pass

    def test_checkout_success(self):
        pass

    def test_wait_for_accept(self):
        pass

    def test_wait_for_checkout(self):
        pass


class EnterPasswordViewTest(TestCase):
    def setUp(self):
        self.user = UserRoles.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    @patch('RepairCafe.views.check_user_password')
    def test_enter_password_correct_password(self, mock_check_password):
        # Mock password validation function to return True for visitor role
        mock_check_password.side_effect = lambda role, password: role == "visitor" and password == "visitor123"

        response = self.client.post(reverse('RepairCafe:enter_password'), {'password': 'visitor123'}) 
        self.assertRedirects(response, reverse('RepairCafe:house_rules'))

    def test_enter_password_incorrect_password(self):
        response = self.client.post(reverse('RepairCafe:enter_password'), {'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RepairCafe/enter_password.html')
        self.assertContains(response, 'Incorrect Password')
