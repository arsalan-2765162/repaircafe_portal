from django.db import models


class Queue(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, default="This is a Queue")

    def __str__(self):
        return self.name

    def get_tickets(self):
        return self.ticket_set.order_by('position')


class Customer(models.Model):
    NAME_MAX_LENGTH = 128
    firstName = models.CharField(max_length=NAME_MAX_LENGTH)
    lastName = models.CharField(max_length=NAME_MAX_LENGTH)

    def __str__(self):
        return f"{self.firstName}  {self.lastName}"


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


class Repairer(models.Model):
    NAME_MAX_LENGTH = 128
    firstName = models.CharField(max_length=NAME_MAX_LENGTH)
    lastName = models.CharField(max_length=NAME_MAX_LENGTH)
