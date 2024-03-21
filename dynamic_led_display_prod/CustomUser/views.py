from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model

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


def RegisterView(request):
    try:               
        if request.method == 'POST':
            if 'email' in request.POST and 'password' in request.POST:
                if request.user.is_superuser:
                    User = get_user_model()
                    user = User(email=request.POST['email'],is_editor=True)
                    if 'superusercheck' in request.POST and request.POST['superusercheck'] == 'on':
                        user.is_superuser = True
                        user.is_staff = True
                    user.set_password(request.POST['password'])
                    user.save()
                    return redirect('analytics')
                else:
                    messages.error(request,"You're not allowed to perform this action")        
    except Exception as e:        
        messages.error(request,str(e))

    return render(request,'auth/register.html')

def LogoutView(request):    
    try:               
        if request.user.is_authenticated:
           logout(request)
           messages.success(request, 'Logged out successfully')
           return redirect('login')
    except Exception as e:
        print(e)
        messages.error(request,str(e))    