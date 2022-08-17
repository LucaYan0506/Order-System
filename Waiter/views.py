from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *

# Create your views here.
def selectTableView(request):
    if request.user.is_authenticated:
        return render(request,'Waiter/selectTable.html', {
            'tables': Table.objects.all()
        })
    return HttpResponseRedirect("/login/?link=index")  

def menuView(request):
    if request.user.is_authenticated:
        if request.GET.get('table'):
            table = Table.objects.get(pk = request.GET.get('table')) 
            categories = Category.objects.filter(active=True)
            basket = None
            tot_basket = 0
            basket_price = 0
            order_price = 0
            order = None

            if Order.objects.filter(table=table, ordered=False, paid=False).exists():
                basket = Order.objects.filter(table=table, ordered=False, paid=False).first()
                for dishes in basket.dishes_set.all():
                    tot_basket += dishes.quantity
                    basket_price += dishes.dish.price * dishes.quantity

            custom_categories = []
            for category in categories:
                dishes = []
                for dish in category.dish_set.all():
                    quantity = 0
                    if basket != None and dish.dishes_set.filter(order=basket).exists():
                        quantity = dish.dishes_set.filter(order=basket).first().quantity

                    url = ''
                    if dish.image:
                        url = dish.image.url

                    custom_dish = {
                        'pk':dish.pk,
                        'name':dish.name,
                        'image':url,
                        'description':dish.description,
                        'price':dish.price,
                        'quantity':quantity,
                    }
                    dishes.append(custom_dish)
                custom_categories.append({
                    'name':category.name,
                    'dishes':dishes
                })
        return HttpResponseRedirect("/login/?link=index")

        if Order.objects.filter(table=table, ordered=True, paid=False).exists():
            order = Order.objects.filter(table=table, ordered=True, paid=False).first()
            for dishes in order.dishes_set.all():
                order_price += dishes.dish.price * dishes.quantity

        return render(request,'Waiter/menu.html', {
            'table': table,
            'categories': custom_categories,
            'basket':basket,
            'tot_basket':tot_basket,
            'basket_price':basket_price,
            'order':order,
            'order_price':order_price,
        })
    return HttpResponse('You are in the wrong page')


def updatebasket(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            dish = Dish.objects.get(pk=data['dish_pk'])
            table = Table.objects.get(pk=data['table_pk'])
            if Order.objects.filter(table=table, ordered=False, paid=False).exists():
                order = Order.objects.filter(table=table, ordered=False, paid=False).first()
            else:
                order = Order(table=table,ordered=False, paid=False)
                order.save()


            if Dishes.objects.filter(order=order, dish=dish).exists():
                dishes = Dishes.objects.filter(order=order, dish=dish).first()
                if int(data['n']) == 0:
                    dishes.delete()
                else:
                    dishes.quantity = data['n']
                    dishes.save()
            elif int(data['n']) > 0:
                dishes = Dishes(order=order,dish=dish,quantity=data['n'])
                dishes.save()

            totPrice = 0

            for dishes in order.dishes_set.all():
                totPrice += dishes.quantity * dishes.dish.price
            return JsonResponse({
                'totPrice':totPrice
            },safe=False)
        return HttpResponse('You are in the wrong page')
    return HttpResponseRedirect("/login/?link=index")

def clearBasket(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            Order.objects.get(pk=request.POST['basket_pk']).delete()
            return JsonResponse({'message':'success'},safe=False)

        return HttpResponse('You are in the wrong page')
    return HttpResponseRedirect("/login/?link=index")


def orderFood(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            basket = Order.objects.get(pk=request.POST['basket_pk'])
            orderKitchen= OrderKitchen(table=basket.table)
            temp = ""
            if basket.dishes_set.all().count() == 0:
                basket.delete()
                return JsonResponse({
                    'result':'Error',
                },safe=False)
                
            all_together = False
            if 'all_together' in request.POST:
                all_together = True

            prev = None
            for x in basket.dishes_set.all().order_by('dish__category__priority'):
                temp += f'<h3 style="font-weight:100;"><strong>{x.quantity} x</strong> {x.dish.name}</h3>'
                if x.dish.category != prev and all_together == False:
                    temp+='<hr>'
                prev = x.dish.category

            orderKitchen.dishes = f"""
                <h1>Table {basket.table.name}</h1>
                {temp}
            """
            orderKitchen.save()

            if Order.objects.filter(table=basket.table, ordered=True, paid=False).exists():
                order =  Order.objects.filter(table=basket.table, ordered=True, paid=False).first()
                for dishes in basket.dishes_set.all():
                    if order.dishes_set.filter(dish=dishes.dish).exists():
                        new_dishes = Dishes.objects.filter(dish=dishes.dish,order=order).first()
                        new_dishes.quantity += dishes.quantity
                        new_dishes.save()
                    else:
                        dishes.order = order
                        dishes.save()


                basket.delete()
            else:
                basket.ordered = True
                basket.save()
            return JsonResponse({
                'result':'Success',
                'pk':orderKitchen.pk,
                'dishes':orderKitchen.dishes,
                'status':orderKitchen.status
                },safe=False)

        return HttpResponse('You are in the wrong page')
    return HttpResponseRedirect("/login/?link=index")

def menuCustomerView(request):
    return render(request,'Waiter/menuCustomer.html',{
        'categories':Category.objects.filter(active=True)
    })

    