from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import time

@login_required
def analytics(request):
    return render(request,'dashboard/analytics.html')

@login_required
def controller(request):
    return render(request,'dashboard/controller.html')

def consumer(request):
    return render(request, 'consumer/index.html')

def testing(request):
    response = HttpResponse(content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["Connection"] = "keep-alive"

    for i in range(10):  # Send 10 updates for demonstration purposes
            data = f"data: {i}\n\n"
            response.write(data)
            response.flush()
            time.sleep(1)  # Simulating updates every second

    return response