from .consumers import PorgramsAndElements,PanelChangedConsumer
from django.urls import re_path

programs_and_elements_urlpatterns = [
    re_path(r"ws/programs_and_elements/$", PorgramsAndElements.as_asgi()),    
    re_path(r"ws/panel_changed_events/$", PanelChangedConsumer.as_asgi()),    
]