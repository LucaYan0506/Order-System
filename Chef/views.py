from django.shortcuts import render
from django.http import JsonResponse
from Waiter.views import OrderKitchen


# Create your views here.
def index_view(request):
    return render(request,'Chef/index.html',{
    })


def order_info(request):
    order = OrderKitchen.objects.all()
    return JsonResponse({
        'orders':[x.serialize() for x in order],
    },
    safe=False
    )
