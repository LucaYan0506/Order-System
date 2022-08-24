from dataclasses import field
from datetime import datetime
from django.db import models
from django.forms import ModelForm
from ckeditor.fields import RichTextField 


# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=256)
    available = models.BooleanField(default=True)
    occupied = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    priority = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='dish',blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    date = models.DateTimeField(default=datetime.now)
    #if it's no ordered means that it is in the basket
    ordered = models.BooleanField()
    #if it's paid, it should be archived 
    paid = models.BooleanField()

    #actually price
    actually_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def serialize(self):
        dishes = []
        tot_price = 0
        for x in self.dishes_set.all():
            tot_price += x.quantity * x.dish.price
            dish = {
                'name':x.dish.name,
                'quantity':x.quantity,
                'price':x.quantity * x.dish.price,
                }
            dishes.append(dish)
            
        return {
            'pk':self.pk,
            'dishes':dishes,
            'total_price':tot_price,
        }

class Dishes(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish.name
        
class OrderKitchen(models.Model):
    STASUS = (
        ('new','new'),
        ('in progress','in progress'),
        ('done','done'),
    )
    status = models.CharField(max_length=256, choices=STASUS, default='new')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    dishes = RichTextField()

    def serialize(self):
        return {
            'pk':self.pk,
            'status':self.status,
            'table':self.table.name,
            'dishes':self.dishes,
        }

class Message(models.Model):
    mail= models.CharField(max_length=256)
    subject= models.CharField(max_length=256)
    message= models.TextField()