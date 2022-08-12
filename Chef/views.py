from django.shortcuts import render
from django.urls.base import reverse
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from Waiter.models import OrderKitchen,Order, Table
from django.db.models import Q

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        link = None
        if 'link' in request.POST:
            link = request.POST['link']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if link:
                return HttpResponseRedirect(reverse(link))
            return HttpResponseRedirect(reverse('chef'))
        else:
            return render(request, "Chef/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        link = None
        if request.GET.get('link'):
            link = request.GET.get('link')
        return render(request, "Chef/login.html",{
            'link':link
        })

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

def managerView(request):
    if request.user.is_authenticated:
            table = []

            for t in Table.objects.all():
                if t.order_set.filter(ordered=True,paid=False,table=t).exists():
                    order = t.order_set.filter(ordered=True,paid=False,table=t).first()
                    tot_price = 0
                    for dishes in order.dishes_set.all():
                        tot_price += dishes.quantity * dishes.dish.price

                    table.append({
                        'pk':t.pk,
                        'name':t.name,
                        'order':order,
                        'tot_price':tot_price
                    })
                else:
                    table.append({
                        'pk':t.pk,
                        'name':t.name,
                        'order':None
                    })
            return render(request,'Chef/manager.html',{
                'tables': table
        })
    return HttpResponseRedirect("/login/?link=manager")


def payOrder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            order = Order.objects.get(pk = request.POST['pk'])
            order.paid = True
            order.save()
            return JsonResponse({'message':'success'},safe=False)

        return HttpResponse('You are in the wrong page')

    return JsonResponse({'message':'Pls login with the account'},safe=False)
