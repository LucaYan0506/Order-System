from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('',selectTableView, name="index"),
    path('menu/',menuView, name="menu"),
    path('menuCustomer/',menuCustomerView, name="menuCustomer"),
    path('basket/update/',updatebasket, name="updatebasket"),
    path('basket/clear/',clearBasket, name="clearBasket"),
    path('order/',orderFood, name="orderFood"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
