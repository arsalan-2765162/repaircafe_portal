import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SH28Project.settings')  # Replace with your project's settings path
import django
django.setup()
from django.contrib.auth.hashers import make_password
from RepairCafe.models import Ticket, Customer, Repairer, Queue, SharedPassword , Carbon_footprint_categories

def populate():
    for each in [Ticket, Customer, Repairer, Queue, Carbon_footprint_categories]:
        x = each.objects.all()
        for entry in x:
            entry.delete()
    def add_queue(name, description):
        queue = Queue.objects.get_or_create(name=name)[0]
        queue.description = description  # Add the description
        queue.save()
        return queue
    def add_carbon_footprint_category(name, carbon_footprint):
        category = Carbon_footprint_categories.objects.get_or_create(name=name)[0]
        category.co2_emission_kg = carbon_footprint
        category.save()
        return category
    




    # Queue descriptions
    queue_data = {
        'Main Queue': "The queue for tickets that have been accepted.",
        'Waiting List': "The queue for tickets to be checked by the check-in person before adding to the Main Queue.",
        'Checkout Queue': "The queue for tickets to be checked out.",
        'PAT Queue': "The queue for items that need PAT testing."  
    }

    password_data = {
        'visitor': 'visitor',
        'repairer': 'repairer',
        'volunteer': 'volunteer'
    }

    carbon_items = [
        "dehumidifier",
        "battery/charger/adaptor",
        "bicycle",
        "clothes/textiles",
        "coffee maker",
        "decorative or safety lights",
        "desktop computer",
        "dslr/video camera",
        "digital compact camera",
        "fan",
        "flat screen",
        "food processor",
        "games console",
        "hair/beauty item",
        "hair dryer",
        "handheld entertainment device",
        "headphones",
        "hi-fi integrated",
        "hi-fi separates",
        "iron",
        "jewellery",
        "kettle",
        "lamp",
        "laptop",
        "large home electrical",
        "miscellaneous item",
        "mobile phone",
        "musical instrument",
        "paper shredder",
        "portable radio",
        "power tool",
        "printer/scanner",
        "projector",
        "sewing machine",
        "small home electrical (eg, baby monitor, doorbell)",
        "small kitchen item (eg, bread maker, rice cooker)",
        "tablet",
        "toaster",
        "toy",
        "tv/gaming related accessory",
        "watch/clock",
        "N/A"
    ]

    carbon_data = {item: 0 for item in carbon_items}

    

    


    # Adding Queue objects
    queue_objects = {queue: add_queue(queue, description) for queue, description in queue_data.items()}
    carbon_objects = {item: add_carbon_footprint_category(item, carbon) for item, carbon in carbon_data.items()}

    #set default password for each user type
    for user_type, password in password_data.items():
        obj, created = SharedPassword.objects.get_or_create(user_type=user_type)
        obj.set_password(password)
   





if __name__ == '__main__':
    print('Starting setup script...')
    populate()
