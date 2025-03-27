import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SH28Project.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from RepairCafe.models import Ticket, Customer, Repairer, Queue, SharedPassword


def setup():
    for each in [Ticket, Customer, Repairer, Queue]:
        x = each.objects.all()
        for entry in x:
            entry.delete()

    def add_queue(name, description):
        queue = Queue.objects.get_or_create(name=name)[0]
        queue.description = description  # Add the description
        queue.save()
        return queue
    
    def add_repairer(name, picture_filename=None):
        repairer, created = Repairer.objects.get_or_create(name=name)

        if picture_filename:  # Assign image if provided
            repairer.picture = f'repairer_pictures/{picture_filename}'
            repairer.save()

        return repairer

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

    repairers_data = [
        {'name': 'Guest Repairer'}
    ]

    # Adding Queue objects
    queue_objects = {queue: add_queue(queue, description) for queue, description in queue_data.items()}

    # Adding Repairer objects
    for repairer_data in repairers_data:
        add_repairer(repairer_data['name'], repairer_data.get('picture'))

    for user_type, password in password_data.items():
        obj, created = SharedPassword.objects.get_or_create(user_type=user_type)
        print(password)
        obj.set_password(password)
        print(obj.check_password(password))
        print(obj.hashed_password)

    # Printing the results
    for queue in Queue.objects.all():
        print(f'Queue: {queue.name} - {queue.description}')
        print()


def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "securepassword123")
        print("Superuser created successfully!")
    else:
        print("Superuser already exists.")


if __name__ == '__main__':
    print('Starting setup script...')
    setup()
    create_superuser()
