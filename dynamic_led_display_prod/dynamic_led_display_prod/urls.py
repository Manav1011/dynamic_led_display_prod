"""
URL configuration for dynamic_led_display_prod project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
import threading
from serial_comm.management.scripts.producer import connect_to_websocket
import asyncio



urlpatterns = [
    path('',views.analytics,name='analytics'),
    path('controller/',views.controller,name='controller'),
    path('admin/', admin.site.urls),
    path('auth/',include('CustomUser.urls')) ,
    path('consumer/',views.consumer,name='consumer'),
    path('testing/',views.testing,name='testing'),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

def run_the_producer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(connect_to_websocket())


thread = threading.Thread(target=run_the_producer)
thread.start()
# thread.join()
# asyncio.get_event_loop().run_until_complete(connect_to_websocket())
