"""
ASGI config for dynamic_led_display_prod project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from serial_comm.routing import serial_urlpatterns
from controller.routing import programs_and_elements_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dynamic_led_display_prod.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": URLRouter((serial_urlpatterns + programs_and_elements_urlpatterns)) 
})
