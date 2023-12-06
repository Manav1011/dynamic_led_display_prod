import serial
import asyncio
import websockets
import json
import struct
import datetime
import time
import math
from scipy.stats import circmean
import pandas as pd


minutes_data = []
async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(message)   
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")

async def send_messages(websocket,data=None):
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
    dict_to_store['RTC'] = stored_list[-1]['RTC']
    dict_to_store["WSPD"] = df['WSPD'].mean()
    dict_to_store["WDIR"] = round(circmean(df['WDIR'], high=360, low=0),3)
    dict_to_store["ATMP"] = df['ATMP'].mean()
    dict_to_store["RAIN"] = df['RAIN'].sum()
    dict_to_store["SRAD"] = df['SRAD'].mean()
    dict_to_store["BPRS"] = df['BPRS'].mean()
    dict_to_store["WDCH"] = df['WDCH'].mean()
    dict_to_store["DWPT"] = df['DWPT'].mean()
    dict_to_store["P12"] = df['P12'].mean()
    dict_to_store["P13"] = df['P13'].mean()
    dict_to_store["P14"] = df['P14'].mean()
    dict_to_store["P15"] = df['P15'].mean()
    dict_to_store["P16"] = df['P16'].mean()
    return dict_to_store

def update_dict_with_values(dict_to_stream,values_list):      
    dict_to_stream["RTC"] = datetime.datetime.now().isoformat()    
    for key, value in dict_to_stream.items():        
        if key != "RTC":            
            value = float(values_list.pop(0)) if values_list else None
            if value == None or math.isnan(value):
                value = 0.0            
            dict_to_stream[key] = value
    return dict_to_stream

def send_avgs(data_list):
    print(data_list)

async def read_serial_port(serial_port,websocket = None):
    global minutes_data
    time_to_send = 5
    time_to_store = 60
    baud_rate = 9600
    data_bits = 8
    parity = 'N'
    stop_bits = 1
    stored_list = []
    
    ser = serial.Serial(port=serial_port, baudrate=baud_rate, bytesize=data_bits,parity=parity, stopbits=stop_bits, timeout=1)
    slave_address = 1
    modbus_request = bytes.fromhex("01040BB8002073D3")    
    try:
        while True:
            dict_to_stream = {"RTC":None,"WSPD":None,"WDIR":None,"ATMP":None,"HUMD":None,"RAIN":None,"SRAD":None,"BPRS":None,"WDCH":None,"DWPT":None,"P12":None,"P13":None,"P14":None,"P15":None,"P16":None}
            dict_to_store = {"RTC":None,"WSPD":None,"WDIR":None,"ATMP":None,"HUMD":None,"RAIN":None,"SRAD":None,"BPRS":None,"WDCH":None,"DWPT":None,"P12":None,"P13":None,"P14":None,"P15":None,"P16":None}
            ser.write(modbus_request)
            response = ser.read(7 + 2 * 32)[3:-2]
            hex_response = response.hex()              
            _8_byte_pairs = []
            FINAL = []
            for i in get_pairs(str(hex_response),8):
                if(i):
                    _8_byte_pairs.append(i)                
                    _2_byte_chars_CDAB = [None,None,None,None]
                    CDAB_LIST = [2,3,0,1]
                    index =0
                    for j in get_pairs(i,2):
                        _2_byte_chars_CDAB[CDAB_LIST[index]] = j            
                        index+=1      
                    CDAB_STR = ''.join(_2_byte_chars_CDAB)                                
                    FINAL.append('{:.3f}'.format(struct.unpack('!f', bytes.fromhex(CDAB_STR))[0]))            
            if(FINAL):
                dict_to_stream = update_dict_with_values(dict_to_stream,FINAL)
                stored_list.append(dict_to_stream)
                # minutes_data.append(dict_to_stream)                
                time_to_send-=1
                if(time_to_send == 0):
                    print(dict_to_stream)
                    await send_messages(websocket,data={'client':'producer','device':'rs485','action':'stream','frame':dict_to_stream})
                    time_to_send = 5
                time_to_store-=1                
                if time_to_store == 0:                         
                    dict_to_store = find_averages(dict_to_store=dict_to_store,stored_list=stored_list)
                    # send_avgs(minutes_data)
                    await send_messages(websocket,data={'client':'producer','device':'rs485','action':'store','frame':dict_to_store})
                    stored_list = []
                    time_to_store = 60

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        ser.close()


if __name__ == "__main__":    
    async def connect_to_websocket():
        async with websockets.connect(f"wss://192.168.29.18:8000/ws/serial_communication/producer/") as websocket:
            print("WebSocket connection established")
            await websocket.send(json.dumps({
                'client':'producer',
                'device':'rs485',
                'action':'connection'
            }))
            receive_task = asyncio.ensure_future(receive_messages(websocket))
            send_task = asyncio.ensure_future(send_messages(websocket))
            serial_task = asyncio.ensure_future(read_serial_port("/dev/ttyUSB0",websocket=websocket))
            await asyncio.gather(receive_task, send_task,serial_task)
    asyncio.get_event_loop().run_until_complete(connect_to_websocket())    