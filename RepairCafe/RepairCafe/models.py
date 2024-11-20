from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Queue(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256,default="This is a Queue")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

    def __str__(self):
        return self.name
    
    def get_tickets(self):
        return self.ticket_set.order_by('position')

class Customer(models.Model):
    NAME_MAX_LENGTH = 128
    firstName = models.CharField(max_length=NAME_MAX_LENGTH)
    lastName = models.CharField(max_length=NAME_MAX_LENGTH)


class Ticket(models.Model):
    MAX_REPAIR_NUM_LENGTH = 8
    MAX_ITEM_NAME_LENGTH = 128
    MAX_ITEM_DESC_LENGTH = 256
    REPAIR_STATUS_CHOICES = [('WAITING','Waiting'),
                      ('COMPLETED','Completed'),
                      ('NEED_PAT','Needs PAT tested'),
                      ('INCOMPLETE','Incomplete')]
    ITEM_CATEGORY_CHOICES = [('ELEC','Electrical'),
                             ('TEXT','Clothing & Textiles'),
                             ('TOOLS','tools & equipment'),]
    
    repairNumber = models.CharField(max_length=MAX_REPAIR_NUM_LENGTH,primary_key=True)
    itemName = models.CharField(max_length=MAX_ITEM_NAME_LENGTH)
    itemCategory = models.CharField(choices=ITEM_CATEGORY_CHOICES,max_length=128)
    itemDescription = models.CharField(max_length=MAX_ITEM_DESC_LENGTH)
    repairStatus = models.CharField(choices=REPAIR_STATUS_CHOICES,default='WAITING',max_length=128)
    position = models.IntegerField(default = 0)
    queue = models.ForeignKey(Queue,on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT,null=True,blank=True)
    
    def __str__(self):
        return f"{self.repairNumber} - {self.itemName}"
    
    def add_to_queue(self, queue):
        self.queue = queue
        max_position = Ticket.objects.filter(queue=queue).aggregate(models.Max('position'))['position_max'] or 0
        self.position = max_position + 1
        self.save()

    def move_up(self):
        if self.position > 1:
            ticket_above = Ticket.objects.filter(queue=self.queue, position=self.position - 1).first()
            if ticket_above:
                ticket_above.position += 1
                ticket_above.save()
            self.position -= 1
            self.save()
            



class Repairer(models.Model):
    NAME_MAX_LENGTH = 128
    firstName = models.CharField(max_length=NAME_MAX_LENGTH)
    lastName = models.CharField(max_length=NAME_MAX_LENGTH)



