from django.urls import path
from .views import *
urlpatterns = [
    path('chef/',index_view,name='chef'),
    path('chef/order_info/',order_info,name='order_info')
]
