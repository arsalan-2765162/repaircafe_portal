from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
from django.contrib.auth.hashers import make_password, check_password

class SharedPassword(models.Model):
    user_type = models.CharField(max_length=50, unique=True)  # e.g., 'visitor', 'repairer'
    hashed_password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.hashed_password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.hashed_password)

    def __str__(self):
        return self.user_type

class UserRoles(AbstractUser):

    #groups = models.ManyToManyField(Group, related_name="user_roles_set", blank=True)
    #user_permissions = models.ManyToManyField(Permission, related_name="user_roles_permissions_set", blank=True)

    
    activerole = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        
        if not self.username:
            self.username = f"user_{uuid.uuid4().hex[:8]}"  
        super().save(*args, **kwargs)


class Queue(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, default="This is a Queue")

    def __str__(self):
        return self.name


    def get_tickets(self):
        return self.ticket_set.order_by('position')


class Repairer(models.Model):
    id = models.BigAutoField(primary_key=True)
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    picture = models.ImageField(upload_to='repairer_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    NAME_MAX_LENGTH = 128
    firstName = models.CharField(max_length=NAME_MAX_LENGTH)
    lastName = models.CharField(max_length=NAME_MAX_LENGTH)

    def __str__(self):
        return f"{self.firstName}  {self.lastName}"


class Carbon_footprint_categories(models.Model):
    NAME_MAX_LENGTH = 123
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    co2_emission_kg = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.co2_emission_kg}kg of co2"


class Ticket(models.Model):
    MAX_ITEM_NAME_LENGTH = 128
    MAX_ITEM_DESC_LENGTH = 256
    REPAIR_STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('WAITING_TO_JOIN', 'Waiting to Join Queue'),
        ('COMPLETED', 'Completed'),
        ('NEED_PAT', 'Needs PAT tested'),
        ('INCOMPLETE', 'Incomplete'),
        ('BEING_REPAIRED', 'Currently being Repaired'),
    ]
    REPAIR_INCOMPLETE_CHOICES = [('NOT_REP', 'Not repairable'),
                                 ('COM_BACK', 'Coming back next time'),
                                 ('TAKEN_HOME', 'Repairer has taken it home')]
    ITEM_CATEGORY_CHOICES = [('ELECM', 'Electrical Mains'),
                             ('ELEC', 'Electrical Low-Voltage/Battery'),
                             ('TEXT', 'Clothing & Textiles'),
                             ('CERA', 'Ceramics'),
                             ('OTHER', 'Other'),]
    
    isVolunteerCreated = models.BooleanField(default=False)
    repairNumber = models.IntegerField(primary_key=True)
    isCheckedOut = models.BooleanField(default=False)
    itemName = models.CharField(max_length=MAX_ITEM_NAME_LENGTH)
    itemCategory = models.CharField(choices=ITEM_CATEGORY_CHOICES, max_length=128)
    itemDescription = models.CharField(max_length=MAX_ITEM_DESC_LENGTH)
    repairStatus = models.CharField(choices=REPAIR_STATUS_CHOICES, default='WAITING_TO_JOIN', max_length=128)
    incompleteReason = models.CharField(choices=REPAIR_INCOMPLETE_CHOICES, max_length=128,
                                        default=None, blank=True, null=True)
    position = models.IntegerField(default=None, null=True, blank=True,)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, default=None, null=True, blank=True,)
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT, null=True, blank=True)
    time_created = models.DateTimeField(default=timezone.now)
    carbon_footprint_category = models.ForeignKey('Carbon_footprint_categories',on_delete=models.SET_DEFAULT,default=None,null=True)
    repairer = models.ForeignKey(Repairer, on_delete=models.SET_NULL, null=True, blank=True)
    checkinFormData = models.JSONField(null=True, blank=True)
    checkoutFormData = models.JSONField(null=True, blank=True)


    def __str__(self):
        return f"{self.repairNumber} - {self.itemName}"

    @classmethod
    def generate_repair_number(cls):
        try:
            all_tickets = cls.objects.all()
            for ticket in all_tickets:
                print(f"Repair Number: {ticket.repairNumber}, Item Name: {ticket.itemName}")
            latest_ticket = all_tickets.order_by('repairNumber').last()
            print(latest_ticket)
            if latest_ticket:
                last_number = latest_ticket.repairNumber
                return str(last_number + 1)
        except Exception as e:
            print(f"Error in generate_repair_number: {e}")

        return "1"

    def add_to_queue(self, queue):
        self.queue = queue
        max_position = Ticket.objects.filter(queue=queue).aggregate(models.Max('position'))['position__max'] or 0
        self.position = max_position + 1
        self.save()

    @staticmethod
    def decrement_positions(queue, position):
        if position is None:
            return
        Ticket.objects.filter(
            queue=queue,
            position__isnull=False,
            position__gt=position).update(position=models.F('position') - 1)

    def accept_ticket(self):
        waiting_list = self.queue
        main_queue = Queue.objects.get(name="Main Queue")
        self.repairStatus = "WAITING"
        self.queue = main_queue
        max_posistion = Ticket.objects.filter(queue=main_queue).aggregate(models.Max('position'))['position__max'] or 0
        old_position = self.position
        self.position = max_posistion + 1
        self.save()

        Ticket.decrement_positions(waiting_list, old_position)

    def complete_ticket(self):
        if self.itemCategory == "ELECM":
            self.repairStatus = "NEED_PAT"
        else:
            self.repairStatus = "COMPLETED"
            self.add_to_checkout()
        self.save()

    def add_to_checkout(self):
        queue = Queue.objects.get(name="Checkout Queue")
        max_position = Ticket.objects.filter(queue=queue).aggregate(models.Max('position'))['position__max'] or 0
        self.queue = queue
        self.position = max_position + 1
        self.save()

    def delete_ticket(self):
        self.decrement_positions(self.queue, self.position)
        self.delete()

    def repair_ticket(self):
        if self.repairStatus == 'WAITING':
            self.repairStatus = 'BEING_REPAIRED'
            old_position = self.position
            self.position = None
            self.save()

            Ticket.decrement_positions(self.queue, old_position)

        else:
            raise ValueError("Ticket cannot be repaired as it is not Waiting for repair")

    def checkout(self):
        if self.repairStatus == 'COMPLETED' or 'INCOMPLETE':
            self.isCheckedOut = True
            self.save()
            self.decrement_positions(self.queue, self.position)

        else:
            raise ValueError("Ticket cannot be checked out as it is not complete or incomplete.")






