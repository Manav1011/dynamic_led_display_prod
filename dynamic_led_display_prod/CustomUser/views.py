from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.

def LoginView(request):
    try:               
        if request.user.is_authenticated:
            return redirect('analytics')
        else:            
            if request.method == 'POST':            
                user = authenticate(username=request.POST['email'],password=request.POST['password'])
                if user:
                    login(request, user)                    
                    return redirect('analytics')
                else:
                    messages.error(request,"User does not exist")
    except Exception as e:
        print(e)
        messages.error(request,str(e))

    return render(request,'auth/login.html')

def LogoutView(request):    
    try:               
        if request.user.is_authenticated:
           logout(request)
           messages.success(request, 'Logged out successfully')
           return redirect('login')
    except Exception as e:
        print(e)
        messages.error(request,str(e))    