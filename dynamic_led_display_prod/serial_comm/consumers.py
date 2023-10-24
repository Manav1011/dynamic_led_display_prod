from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import numpy as np
import pandas as pd
from channels.db import database_sync_to_async
from .models import RS232,RS485
import matplotlib.pyplot as plt


class SerialConsumerRS485(AsyncWebsocketConsumer):
    entities_rs485 = {
        'dashboard':{},
        'producer':None,    
    }
    csv_b64 = ''
    async def connect(self):
        await self.accept()
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))

    async def receive(self,text_data):
        text_data = json.loads(text_data)  
        if text_data['client'] == 'dashboard':
            if text_data.get('page') and text_data['page'] == 'analytics':                
                SerialConsumerRS485.entities_rs485['dashboard']['analytics'] = self
                await self.send(json.dumps({'rs485_plot':await self.get_graph()}))
            elif text_data['page'] == 'controller':
                SerialConsumerRS485.entities_rs485['dashboard']['controller'] = self
        if text_data['client'] == 'producer':
            if text_data['action'] == 'connection':
                SerialConsumerRS485.entities_rs485['producer'] = self
            if text_data['action'] == 'stream' and text_data['data']:
                await self.save_obj(text_data['data'])
                try:
                    if SerialConsumerRS485.entities_rs485['dashboard']['analytics']:
                        await SerialConsumerRS485.entities_rs485['dashboard']['analytics'].send(json.dumps(text_data))
                    if SerialConsumerRS485.entities_rs485['dashboard']['controller']:
                        await SerialConsumerRS485.entities_rs485['dashboard']['controller'].send(json.dumps(text_data))
                except Exception as e:
                    print(e)
            print('rs485')
            print(SerialConsumerRS485.entities_rs485)
            
    @database_sync_to_async
    def save_obj(self,data):
        obj = RS485(RTC=data['RTC'],AvgeSpeed=data['AvgeSpeed'],AvgeTemp=data['AvgeTemp'],AvgeHum=data['AvgeHum'],AvgeSr=data['AvgeSr'])
        obj.save()
    
    @database_sync_to_async
    def get_graph(self):
        objs = RS485.objects.values()
        data= {
            'AvgeSpeed':round(np.mean([float(i['AvgeSpeed']) for i in objs]),2),
            'AvgeTemp':round(np.mean([float(i['AvgeTemp']) for i in objs]),2),
            'AvgeHum':round(np.mean([float(i['AvgeHum']) for i in objs]),2),
            'AvgeSr':round(np.mean([float(i['AvgeSr']) for i in objs]),2),
        }
        return data


class SerialConsumerRS232(AsyncWebsocketConsumer):
    entities_rs232 = {
        'dashboard':{},
        'producer':{},
    }
    async def connect(self):
        await self.accept()        
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))

    async def receive(self,text_data):
        text_data = json.loads(text_data)  
        if text_data['client'] == 'dashboard':
            if text_data['page'] == 'analytics':
                SerialConsumerRS232.entities_rs232['dashboard']['analytics'] = self
                await self.send(json.dumps({'rs232_plot':await self.get_graph()}))
            if text_data['page'] == 'controller':
                SerialConsumerRS232.entities_rs232['dashboard']['controller'] = self        
        if text_data['client'] == 'producer':
            if text_data['action'] == 'connection':
                SerialConsumerRS232.entities_rs232['producer'] = self
            if text_data['action'] == 'stream' and text_data['data']:
                await self.save_obj(text_data['data'])
                try:
                    if SerialConsumerRS232.entities_rs232['dashboard']['analytics']:
                        await SerialConsumerRS232.entities_rs232['dashboard']['analytics'].send(json.dumps(text_data))
                    if SerialConsumerRS232.entities_rs232['dashboard']['controller']:
                        await SerialConsumerRS232.entities_rs232['dashboard']['controller'].send(json.dumps(text_data))
                except Exception as e:
                    print(e)
            print('rs232')
            print(SerialConsumerRS232.entities_rs232)
    @database_sync_to_async
    def save_obj(self,data):
        obj = RS232(RTC=data['RTC'],AvgeSpeed=data['AvgeSpeed'],AvgeTemp=data['AvgeTemp'],AvgeHum=data['AvgeHum'],AvgeSr=data['AvgeSr'])
        obj.save()
    @database_sync_to_async
    def get_graph(self):
        objs = RS232.objects.values()
        data= {
            'AvgeSpeed':round(np.mean([float(i['AvgeSpeed']) for i in objs]),2),
            'AvgeTemp':round(np.mean([float(i['AvgeTemp']) for i in objs]),2),
            'AvgeHum':round(np.mean([float(i['AvgeHum']) for i in objs]),2),
            'AvgeSr':round(np.mean([float(i['AvgeSr']) for i in objs]),2),
        }
        return data