from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import numpy as np
import pandas as pd
from channels.db import database_sync_to_async
from .serializers import DailyAverageSerializer
from .models import SerialCommunication,States
import matplotlib.pyplot as plt
import datetime
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import io
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from django.http import HttpResponse
from matplotlib import cm
from scipy.stats import circmean
from matplotlib.colors import ListedColormap
import base64
import matplotlib.dates as mdates


class SerialConsumer(AsyncWebsocketConsumer):
    entities = {
        'rs485':{},
        'rs232':{}
    }    
    async def connect(self):
        self.client = self.scope["url_route"]["kwargs"]["client"]
        if self.client == 'consumer':
            await self.channel_layer.group_add('consumers', self.channel_name)
        await self.accept()
    
    async def disconnect(self,close_code): 
        await self.channel_layer.group_discard('consumers', self.channel_name)       
        self.send(json.dumps(close_code))

    async def receive(self,text_data):
        text_data = json.loads(text_data)        
        # print(text_data)
        if text_data['client'] == 'panel' and text_data.get('device') and text_data.get('action'):
            device = text_data['device']
            action = text_data['action']
            if action == 'connection':
                SerialConsumer.entities[device]['panel'] = self             
                print(SerialConsumer.entities) 

        if text_data['client'] == 'consumer' and text_data.get('device') and text_data.get('action'):
            device = text_data['device']
            action = text_data['action']
            
            if action == 'connection':
                SerialConsumer.entities[device]['consumer'] = self             
                print(SerialConsumer.entities) 

            if action == 'get_windrose':
                values = text_data['values']
                colors = text_data['colors']
                image_base64,df_html = await self.get_windrose(device,values,colors)
                await self.send(json.dumps({
                    'action':'graph_received',
                    'device':'rs485',
                    'image_base64':image_base64,
                    'df_html':df_html
                }))
                
            if action == 'get_line_chart':
                params = text_data['params']
                image_base64,df_html = await self.get_line_chart(device,params)
                await self.send(json.dumps({
                    'action':'graph_received',
                    'device':'rs485',
                    'image_base64':image_base64,
                    'df_html':df_html
                }))
            if action == 'get_area_chart':
                value = text_data['value']
                image_base64,df_html = await self.get_area_chart(device,value)
                await self.send(json.dumps({
                    'action':'graph_received',
                    'device':'rs485',
                    'image_base64':image_base64,
                    'df_html':df_html
                }))
                

        if text_data['client'] == 'producer' and text_data.get('device') and text_data.get('action'):
            device = text_data['device']
            action = text_data['action']

            if action == 'connection':
                SerialConsumer.entities[device]['producer'] = self 
                print(SerialConsumer.entities)

            if action == 'stream' and text_data.get('frame') and text_data.get('device'):
                try:                    
                    if SerialConsumer.entities[device]['consumer'] and SerialConsumer.entities[device]['panel']:                        
                        today = datetime.datetime.today()                                                
                        averages = await self.get_averages(today)
                        await self.channel_layer.group_send(
                            'consumers', {"type": "send.frame.stream", "frame_obj": {'device':text_data['device'],'action':'stream','frame':text_data['frame'],'averages':averages}}
                        )
                        # await SerialConsumer.entities[device]['consumer'].send(json.dumps({
                        #     'device':text_data['device'],
                        #     'action':'stream',
                        #     'frame':text_data['frame']
                        # }))
                except Exception as e:      
                    print(e)                                  
            if action == 'store' and text_data.get('frame') and text_data.get('device'):
                # print(text_data['frame'])
                # Store the stream into database
                await self.store_stream_into_db(text_data['device'],text_data['frame'])
            
    @database_sync_to_async
    def get_averages(self,today):
        Averages = States.objects.filter(date=today).values('param', 'mean')
        average_serialized = DailyAverageSerializer(Averages,many=True)
        return average_serialized.data
    
    async def send_frame_stream(self, event): 
        text_data = event['frame_obj']        
        await self.send(json.dumps(text_data))

    @database_sync_to_async
    def get_windrose(self,device,values=False,colors=False):
        speed_dir_objs = SerialCommunication.objects.filter(device=device).values('WSPD','WDIR')
        df = pd.DataFrame(speed_dir_objs).apply(pd.to_numeric,errors='coerce', downcast='float').round(3)
        wdir_mean = round(circmean(df['WDIR'], high=360, low=0),3)
        summary_df = df.describe().applymap(lambda x: f'{x:.2f}').T
        summary_df.loc['WDIR']['mean'] = wdir_mean
        summary_df = summary_df[['count','min','max','mean']].T
        table_html = summary_df.to_html(classes='table table-bordered table-striped text-center', escape=False, index=True,justify='center').replace('\n','')
        wind_direction = list(df['WDIR'])
        wind_speed = list(df['WSPD'])
        ax = WindroseAxes.from_ax()         
        if(values and colors):
            custom_cmap = ListedColormap(colors)
            custom_bins = np.array(values)    
            ax.contourf(wind_direction, wind_speed, bins=custom_bins, cmap=custom_cmap)
        else:
            ax.contourf(wind_direction, wind_speed, normed=True, cmap=cm.hot)
        # ax.bar(wind_direction, wind_speed, normed=True, opening=1.0, edgecolor='k')
        ax.legend(title="Wind Speed (m/s)")
        ax.set_title("Windrose")
        image_data = io.BytesIO()                
        plt.savefig(image_data, format="png")
        image_data.seek(0)
        image_base64 = base64.b64encode(image_data.read()).decode('utf-8')
        plt.clf()
        return image_base64,table_html

    @database_sync_to_async
    def get_line_chart(self,device,params):
        params.append('RTC')
        line_chart_objs = SerialCommunication.objects.filter(device=device).values(*params)        
        df_params = pd.DataFrame(line_chart_objs)
        RTC_DF = df_params['RTC']
        del df_params['RTC']     
        FLOAT_DF = df_params.apply(pd.to_numeric,errors='coerce', downcast='float').round(3)
        summary_df = FLOAT_DF.describe().applymap(lambda x: f'{x:.2f}')
        table_html = summary_df.to_html(classes='table table-bordered table-striped text-center', escape=False, index=True,justify='center').replace('\n','')
        for i in params:
            if i != 'RTC':
                plt.plot(RTC_DF, FLOAT_DF[i],label=i)
        plt.gcf().autofmt_xdate()
        date_format = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Line Chart of Parameters Over Time')
        plt.legend()
        line_data = io.BytesIO()        
        plt.savefig(line_data, format="png")
        line_data.seek(0)
        image_base64 = base64.b64encode(line_data.read()).decode('utf-8')
        plt.clf()
        return image_base64,table_html
    
    @database_sync_to_async
    def get_area_chart(self,device,value):
        params = [value,'RTC']
        line_chart_objs = SerialCommunication.objects.filter(device=device).values(*params)        
        df_params = pd.DataFrame(line_chart_objs)                
        # del df_params['RTC']     
        FLOAT_DF = df_params[value].apply(pd.to_numeric,errors='coerce', downcast='float').round(3)
        summary_df = pd.DataFrame(FLOAT_DF).describe().applymap(lambda x: f'{x:.2f}')       
        table_html = summary_df.to_html(classes='table table-bordered table-striped text-center', escape=False, index=True,justify='center').replace('\n','')
        df_params.set_index('RTC', inplace=True)
        plt.figure(figsize=(10, 6))
        plt.fill_between(df_params.index, FLOAT_DF, color='skyblue', alpha=0.4, label=f"{value} area")
        plt.plot(df_params.index, FLOAT_DF, color='blue', label=f'{value} Line', marker='o')
        plt.title(f'{value} Over Time')
        plt.xlabel('Time')
        plt.ylabel(f'{value}')
        plt.legend()
        plt.grid(True)
        area_data = io.BytesIO()        
        plt.savefig(area_data, format="png")
        area_data.seek(0)
        image_base64 = base64.b64encode(area_data.read()).decode('utf-8')
        plt.clf()
        return image_base64,table_html


    @database_sync_to_async
    def store_stream_into_db(self,device,frame):
        frame_obj = SerialCommunication(device=device)
        for key, value in frame.items():
            if key != 'RTC':
                 if value == None:
                     value = 0.0
                 setattr(frame_obj, key, float(value))  # Set the attribute using setattr
            else:
                 setattr(frame_obj, key, datetime.datetime.fromisoformat(value))
        frame_obj.save()