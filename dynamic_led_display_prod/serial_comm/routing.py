from .consumers import SerialConsumerRS232,SerialConsumerRS485
from django.urls import re_path

serial_urlpatterns = [
    re_path(r"serial_communication_rs232/$", SerialConsumerRS232.as_asgi()),
    re_path(r"serial_communication_rs485/$", SerialConsumerRS485.as_asgi()),
]