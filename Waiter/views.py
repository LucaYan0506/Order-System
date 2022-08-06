from django.shortcuts import render

# Create your views here.
def selectTableView(request):
    return render(request,'Waiter/selectTable.html')