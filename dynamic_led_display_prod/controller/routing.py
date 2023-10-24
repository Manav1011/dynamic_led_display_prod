from .consumers import PorgramsAndElements
from django.urls import re_path

programs_and_elements_urlpatterns = [
    re_path(r"programs_and_elements/$", PorgramsAndElements.as_asgi()),    
]