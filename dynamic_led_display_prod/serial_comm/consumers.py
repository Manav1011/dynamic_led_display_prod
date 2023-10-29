from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import numpy as np
import pandas as pd
from channels.db import database_sync_to_async
from .models import SerialCommunication
import matplotlib.pyplot as plt
import datetime
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import io
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from django.http import HttpResponse


class SerialConsumer(AsyncWebsocketConsumer):
    entities = {
        'rs485':{},
        'rs232':{}
    }    
    async def connect(self):
        await self.accept()
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))

    async def receive(self,text_data):
        text_data = json.loads(text_data)  
        print(text_data)
        if text_data['client'] == 'consumer' and text_data.get('device') and text_data.get('action'):
            device = text_data['device']
            action = text_data['action']
            
            if action == 'connection':
                SerialConsumer.entities[device]['consumer'] = self             
                print(SerialConsumer.entities) 

            if action == 'get_windrose':
                image_link = await self.get_windrose(device)
                await self.send(json.dumps({
                    'action':'windrose_graph_received',
                    'device':'rs485',
                    'graph_link':image_link

                }))

        if text_data['client'] == 'producer' and text_data.get('device') and text_data.get('action'):
            device = text_data['device']
            action = text_data['action']

            if action == 'connection':
                SerialConsumer.entities[device]['producer'] = self 
                print(SerialConsumer.entities)

            if action == 'stream' and text_data.get('frame') and text_data.get('device'):
                try:
                    if SerialConsumer.entities[device]['consumer']:
                        await SerialConsumer.entities[device]['consumer'].send(json.dumps({
                            'device':text_data['device'],
                            'action':'stream',
                            'frame':text_data['frame']
                        }))
                except Exception as e:
                    pass
            if action == 'store' and text_data.get('frame') and text_data.get('device'):
                print(text_data['frame'])
                # Store the stream into database
                await self.store_stream_into_db(text_data['device'],text_data['frame'])

    @database_sync_to_async
    def get_windrose(self,device):
        speed_dir_objs = SerialCommunication.objects.filter(device=device).values('WSPD','WDIR')
        wind_speed = []
        wind_direction = []
        for i in speed_dir_objs:
            wind_speed.append(float(i['WSPD']))
            wind_direction.append(float(i['WDIR']))
        
        ax = WindroseAxes.from_ax()
        ax.bar(wind_direction, wind_speed, normed=True, opening=0.8, edgecolor='k')
        
        ax.set_legend()
        ax.set_title("Windrose")   
        image_data = io.BytesIO()
        plt.savefig(image_data, format="png")
        image_data.seek(0)
        response = HttpResponse(image_data, content_type='image/png')
        response['Content-Disposition'] = 'inline; filename="windrose.png"'
        print(response)
        return response


    @database_sync_to_async
    def store_stream_into_db(self,device,frame):
        frame_obj = SerialCommunication(device=device)
        for key, value in frame.items():
            if key != 'RTC':
                 setattr(frame_obj, key, float(value))  # Set the attribute using setattr
            else:
                 setattr(frame_obj, key, datetime.datetime.fromisoformat(value))
        frame_obj.save()