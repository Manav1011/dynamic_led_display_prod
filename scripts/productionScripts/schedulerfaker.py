# libs
import asyncio
import random
import struct
import datetime
from scipy.stats import circmean
import pandas as pd
import math
import websockets
import json
import time
import os

directions =   {
   'N': (337.5, 22.5),
   'NE': (22.5, 67.5),
   'E': (67.5, 112.5),
   'SE': (112.5, 157.5),
   'S': (157.5, 202.5),
   'SW': (202.5, 247.5),
   'W': (247.5, 292.5),
   'NW': (292.5, 337.5),   
}


async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(message)
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")


async def send_messages(websocket, data=None):
    try:
        if data is not None:
            await websocket.send(json.dumps(data))
    except websockets.ConnectionClosed as e:
        exit(e)


def get_pairs(s, n):    
    if len(s) % n == 0:
        i = 0
        while i <= len(s) - n:
            yield s[i:i + n]
            i += n
    else:
        yield False

def find_averages(dict_to_store,stored_list):
    df = pd.DataFrame(stored_list)
    # Only include following sesnors data
    sensors_to_include = ['RTC','WSPD','WDIR','RAIN','SRAD','BPRS','WDCH','ATMP','HUMD']
    dict_to_store['RTC'] = stored_list[-1]['RTC']
    dict_to_store["WSPD"] = df['WSPD'].mean()
    dict_to_store["WDIR"] = round(circmean(df['WDIR'], high=360, low=0),3)
    dict_to_store["ATMP"] = df['ATMP'].mean()
    dict_to_store["RAIN"] = df['RAIN'].sum()
    dict_to_store["SRAD"] = df['SRAD'].mean()
    dict_to_store["BPRS"] = df['BPRS'].mean()
    dict_to_store["WDCH"] = df['WDCH'].mean()
    dict_to_store["DWPT"] = df['DWPT'].mean()
    dict_to_store["HUMD"] = df['HUMD'].mean()    
    dict_to_store["P12"] = df['P12'].mean()
    dict_to_store["P13"] = df['P13'].mean()
    dict_to_store["P14"] = df['P14'].mean()
    dict_to_store["P15"] = df['P15'].mean()
    dict_to_store["P16"] = df['P16'].mean()
    filtered_dict = {key: dict_to_store[key] for key in sensors_to_include if key in dict_to_store}
    return filtered_dict

def update_dict_with_values(dict_to_stream,values_list):      
    dict_to_stream["RTC"] = (datetime.datetime.now() - datetime.timedelta(seconds=3)).isoformat()
    for key, value in dict_to_stream.items():        
        if key != "RTC":            
            value = float(values_list.pop(0)) if values_list else None
            if value == None or math.isnan(value):
                value = 0.0            
            dict_to_stream[key] = value
    return dict_to_stream

started = False
async def read_and_print(websocket):
    global directions
    global started    
    time_to_store = 60                
    stored_list = []
    while True:
        dict_to_stream = {"RTC": datetime.datetime.now().isoformat(), "WSPD": random.uniform(0.0, 10.0),
                              "WDIR": random.uniform(0.0, 360.0), "ATMP": random.uniform(-10.0, 30.0),
                              "HUMD": random.uniform(0.0, 100.0), "RAIN": random.uniform(0.0, 5.0),
                              "SRAD": random.uniform(0.0, 1000.0), "BPRS": random.uniform(900.0, 1100.0),
                              "WDCH": random.uniform(0.0, 360.0), "DWPT": random.uniform(-10.0, 30.0),
                              "P12": random.uniform(0.0, 100.0), "P13": random.uniform(0.0, 100.0),
                              "P14": random.uniform(0.0, 100.0), "P15": random.uniform(0.0, 100.0),
                              "P16": random.uniform(0.0, 100.0)}
        dict_to_store = {"RTC": None, "WSPD": None, "WDIR": None, "ATMP": None, "HUMD": None, "RAIN": None,
                             "SRAD": None, "BPRS": None, "WDCH": None, "DWPT": None, "P12": None, "P13": None,
                             "P14": None, "P15": None, "P16": None}        
        if not started:
            timestamp = datetime.datetime.strptime(dict_to_stream['RTC'], "%Y-%m-%dT%H:%M:%S.%f")
            print(f'Starting in {60 - timestamp.second}')
            if timestamp.second == 0:
                started = True
        if started:            
            try:
                direction_found = False                
                for direction, (lower, upper) in directions.items():                    
                    if lower <= float(dict_to_stream['WDIR']) < upper:
                        dict_to_stream['WDIR_MAPPED'] = direction
                        direction_found = True
                        break
                if not direction_found:
                    print('here')
                    dict_to_stream['WDIR_MAPPED'] = 'N'
                                    
            except Exception as e:
                print('here',e)
            stored_list.append(dict_to_stream)
            sensors_to_include = ['RTC','WSPD','WDIR','RAIN','SRAD','BPRS','WDCH','HUMD','ATMP','WDIR_MAPPED']
            filtered_dict = {key: dict_to_stream[key] for key in sensors_to_include if key in dict_to_stream}           
            print(dict_to_stream)
            await send_messages(websocket,
                            data={'client': 'producer', 'device': 'rs485', 'action': 'stream',
                                  'frame': filtered_dict})    
        
            time_to_store-=1                
            if time_to_store == 1:                      
                rain = dict_to_stream['RAIN']                                
                dict_to_store = find_averages(dict_to_store=dict_to_store,stored_list=stored_list)
                await send_messages(websocket,
                            data={'client': 'producer', 'device': 'rs485', 'action': 'store',
                                  'frame': dict_to_store})                    
                stored_list = []
                time_to_store = 60
        time.sleep(1)


async def main():        
    while True:    
        try:
            async with websockets.connect(f"ws://192.168.29.18:8000/ws/serial_communication/producer/") as websocket:                                
                await websocket.send(json.dumps({'client': 'producer','device': 'rs485','action': 'connection'}))
                await asyncio.gather(read_and_print(websocket),receive_messages(websocket=websocket))                
        except Exception as e:
            print(e)        
            await asyncio.sleep(5)                
            continue

asyncio.run(main())