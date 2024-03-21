# libs
import asyncio
import aioserial
import struct
import datetime
from scipy.stats import circmean
import pandas as pd
import math
import websockets
import json
import time
import os

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
    baud_rate = 9600
    data_bits = 8
    parity = 'N'
    stop_bits = 1
    aioserial_instance = aioserial.AioSerial(port=os.environ.get('SERIAL_PORT'), baudrate=baud_rate, bytesize=data_bits,parity=parity, stopbits=stop_bits, timeout=1)
    write_data = bytes.fromhex("01040BB8002073D3")
    global started    
    time_to_store = 60                
    stored_list = []

    while True:
        dict_to_stream = {"RTC": None, "WSPD": None, "WDIR": None, "ATMP": None, "HUMD": None, "RAIN": None,
                          "SRAD": None, "BPRS": None, "WDCH": None, "DWPT": None, "P12": None, "P13": None,
                          "P14": None, "P15": None, "P16": None}
        dict_to_store = {"RTC": None, "WSPD": None, "WDIR": None, "ATMP": None, "HUMD": None, "RAIN": None,
                         "SRAD": None, "BPRS": None, "WDCH": None, "DWPT": None, "P12": None, "P13": None,
                         "P14": None, "P15": None, "P16": None}
        await aioserial_instance.write_async(write_data)
        data: bytes = await aioserial_instance.read_async(7 + 2 * 32)        
        response = data[3:-2]
        hex_response = response.hex()
        _8_byte_pairs = []
        FINAL = []
        for i in get_pairs(str(hex_response), 8):
            if i:
                _8_byte_pairs.append(i)
                _2_byte_chars_CDAB = [None, None, None, None]
                CDAB_LIST = [2, 3, 0, 1]
                index = 0
                for j in get_pairs(i, 2):
                    _2_byte_chars_CDAB[CDAB_LIST[index]] = j
                    index += 1
                CDAB_STR = ''.join(_2_byte_chars_CDAB)
                FINAL.append('{:.3f}'.format(struct.unpack('!f', bytes.fromhex(CDAB_STR))[0]))
        if(FINAL):            
            dict_to_stream = update_dict_with_values(dict_to_stream,FINAL)
            if not started:
                timestamp = datetime.datetime.strptime(dict_to_stream['RTC'], "%Y-%m-%dT%H:%M:%S.%f")
                print(f'Starting in {60 - timestamp.second}')
                if timestamp.second == 0:
                    started = True
            if started:
                stored_list.append(dict_to_stream)
                sensors_to_include = ['RTC','WSPD','WDIR','RAIN','SRAD','BPRS','WDCH','HUMD','ATMP']
                filtered_dict = {key: dict_to_stream[key] for key in sensors_to_include if key in dict_to_stream}
                print(filtered_dict)
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


async def main():        
    while True:    
        try:
            async with websockets.connect(f"ws://{os.environ.get('INTERNAL_IP')}/ws/serial_communication/producer/") as websocket:                                
                await websocket.send(json.dumps({'client': 'producer','device': 'rs485','action': 'connection'}))
                await asyncio.gather(read_and_print(websocket),receive_messages(websocket=websocket))                
        except Exception as e:
            print(e)        
            await asyncio.sleep(5)                
            continue

asyncio.run(main())