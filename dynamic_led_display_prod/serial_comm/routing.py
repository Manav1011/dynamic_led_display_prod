from .consumers import SerialConsumer
from django.urls import re_path

serial_urlpatterns = [
    re_path(r"ws/serial_communication/(?P<client>\w+)/$", SerialConsumer.as_asgi()),
]