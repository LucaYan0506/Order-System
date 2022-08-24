from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('manager/',managerView,name='manager'),
    path('manager/order_info',order_detail,name='order_detail'),
    path('pay/',payOrder,name='pay'),
    path('chef/',index_view,name='chef'),
    path('chef/order_info/',order_info,name='order_info'),
    path('chef/order_in_progress/',order_in_progress,name='order_in_progress'),
    path('chef/order_done/',order_done,name='order_done'),
]
