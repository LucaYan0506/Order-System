from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('',indexView, name="index"),
    path('selectTable/',selectTableView, name="selectTable"),
    path('menuCustomer/',menuCustomerView, name="menuCustomer"),
    path('menu/',menuView, name="menu"),
    path('basket/update/',updatebasket, name="updatebasket"),
    path('basket/clear/',clearBasket, name="clearBasket"),
    path('order/',orderFood, name="orderFood"),
    path('send_message/', send_message, name="send_message")
]
