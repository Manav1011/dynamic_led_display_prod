from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required
def analytics(request):
    return render(request,'dashboard/analytics.html')

@login_required
def controller(request):
    return render(request,'dashboard/controller.html')

def consumer(request):
    return render(request, 'consumer/index.html')

def testing(request):
    a = 10
    context = {'request':dir(request)}
    print(request)
    return render(request, 'consumer/testing.html',context=context)