from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import BaseCommand
from Waiter.models import *

class Command(createsuperuser.Command):
    help = 'Generate an admin'

    def handle(self, *args, **options):
        password = 'admin123'
        username = 'Admin'

        user = self.UserModel(username=username, is_staff =True,is_superuser=True)
        user.set_password(password)
        user.save()  

        self.stdout.write('admin account created')

        for i in range(30):
            table = Table(name=i + 1)
            table.save()
            
        self.stdout.write('30 tables created')
        
        category = Category(name="Starter")
        category.save()
        dish = Dish(category=category,name="Arrancino",description="This is a description",price=5.99)
        dish.save()
        category = Category(name="Soup")
        category.save()
        dish = Dish(category=category,name="Gazpacho",description="This is a description",price=7.99)
        dish.save()
        category = Category(name="Main")
        category.save()
        dish = Dish(category=category,name="Spaghetti Bolognese",description="This is a description",price=10.99)
        dish.save()
        category = Category(name="Dessert")
        category.save()
        dish = Dish(category=category,name="Tiramisu",description="This is a description",price=12.99)
        dish.save()

        self.stdout.write('4 categories + dishes created')
