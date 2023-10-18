from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request,'dashboard/index.html')

def LoginView(request):    
    try:               
        if request.user.is_authenticated:
            return redirect('index')
        else:            
            if request.method == 'POST':            
                user = authenticate(username=request.POST['email'],password=request.POST['password'])
                if user:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                else:
                    messages.error(request,"User does not exist")
    except Exception as e:
        print(e)
        messages.error(request,str(e))

    return render(request,'auth/login.html')