from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Dishes)
admin.site.register(Order)
admin.site.register(OrderKitchen)
admin.site.register(Message)