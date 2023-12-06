from .models import Programs,Panel
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

@receiver(post_save,sender=Programs)
def product_updated_receiver(sender,**kwargs):
    panel_obj = Panel.objects.first()
    channel_name = panel_obj.channel_name
    async_to_sync(channel_layer.send)(channel_name, {"type": "program.event"})

