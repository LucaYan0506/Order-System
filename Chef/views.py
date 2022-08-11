from django.shortcuts import render
from django.urls.base import reverse
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from Waiter.views import OrderKitchen
from django.db.models import Q

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('chef'))
        else:
            return render(request, "Chef/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Chef/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def index_view(request):
    if request.user.is_authenticated:
            return render(request,'Chef/index.html',{
        })
    return HttpResponseRedirect(reverse('login'))


def order_info(request):
    if request.user.is_authenticated:
        order = OrderKitchen.objects.filter(Q(status='in progress') | Q(status='new')) 

        return JsonResponse({
            'orders':[x.serialize() for x in order],
        },
        safe=False
        )

    return HttpResponseRedirect(reverse('login'))
   
def order_in_progress(request):
    if request.user.is_authenticated:
    
        if request.method == 'POST':
            order = OrderKitchen.objects.get(pk=request.POST['pk'])
            order.status = 'in progress'
            order.save()
            
            return JsonResponse({'message':'success'},safe=False)

        return HttpResponse('You are in the wrong page')
    return HttpResponseRedirect(reverse('login'))

def order_done(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            order = OrderKitchen.objects.get(pk=request.POST['pk'])
            order.status = 'done'
            order.save()
            
            return JsonResponse({'message':'success'},safe=False)

        return HttpResponse('You are in the wrong page')
    return HttpResponseRedirect(reverse('login'))
