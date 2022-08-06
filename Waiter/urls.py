from django.urls import path
from .views import *


urlpatterns = [
    path('',selectTableView, name="index")
]
