from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Queue(models.Model):
    name = models.CharField(max_length=128)

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
    customer = models.OneToOneField(Customer, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.repairNumber} - {self.itemName}"



class Repairer(models.Model):
    NAME_MAX_LENGTH = 128
    firstName = models.CharField(max_length=NAME_MAX_LENGTH)
    lastName = models.CharField(max_length=NAME_MAX_LENGTH)



