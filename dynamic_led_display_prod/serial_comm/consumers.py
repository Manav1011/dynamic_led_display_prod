from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import numpy as np
import pandas as pd

class SerialConsumerRS485(AsyncWebsocketConsumer):
    entities_rs485 = {
        'dashboard':{},
        'producer':None,    
    }
    async def connect(self):
        await self.accept()
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))

    async def receive(self,text_data):
        text_data = json.loads(text_data)  
        if text_data['client'] == 'dashboard':
            if text_data['page'] == 'analytics':
                SerialConsumerRS485.entities_rs485['dashboard']['analytics'] = self
            if text_data['page'] == 'controller':
                SerialConsumerRS485.entities_rs485['dashboard']['controller'] = self
        if text_data['client'] == 'producer':
            if text_data['action'] == 'connection':
                SerialConsumerRS485.entities_rs485['producer'] = self
            if text_data['action'] == 'stream' and text_data['data']:
                try:
                    if SerialConsumerRS485.entities_rs485['dashboard']['analytics']:
                        await SerialConsumerRS485.entities_rs485['dashboard']['analytics'].send(json.dumps(text_data))
                    if SerialConsumerRS485.entities_rs485['dashboard']['controller']:
                        await SerialConsumerRS485.entities_rs485['dashboard']['controller'].send(json.dumps(text_data))
                except Exception as e:
                    print(e)
            print('rs485')
            print(SerialConsumerRS485.entities_rs485)
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
            if text_data['page'] == 'controller':
                SerialConsumerRS232.entities_rs232['dashboard']['controller'] = self        
        if text_data['client'] == 'producer':
            if text_data['action'] == 'connection':
                SerialConsumerRS232.entities_rs232['producer'] = self
            if text_data['action'] == 'stream' and text_data['data']:
                try:
                    if SerialConsumerRS232.entities_rs232['dashboard']['analytics']:
                        await SerialConsumerRS232.entities_rs232['dashboard']['analytics'].send(json.dumps(text_data))
                    if SerialConsumerRS232.entities_rs232['dashboard']['controller']:
                        await SerialConsumerRS232.entities_rs232['dashboard']['controller'].send(json.dumps(text_data))
                except Exception as e:
                    print(e)
            print('rs232')
            print(SerialConsumerRS232.entities_rs232)