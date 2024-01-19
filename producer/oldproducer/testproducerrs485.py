import re
import asyncio
import websockets
import json
import time
from datetime import datetime
import random

logs = {
    'client':None,
    'RTC':None,
    'AvgeSpeed':None,
    'AvgeTemp':None,
    'AvgeHum':None,
    'AvgeSr':None
}

async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()       
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")

async def send_messages(websocket,data=None):
    try:        
        if data is not None:
            await websocket.send(json.dumps({'client':'producer','action':'stream','data':data,'mode':'serial_rs485'}))
        else:
            await websocket.send(json.dumps({'client':'producer','action':'connection','mode':'serial_rs485'}))
    except websockets.ConnectionClosed as e:
        exit(e)      

async def produce_garbage_data(websocket):
    while True:
        for i in logs.keys():
            if i != 'RTC':
                logs[i] = round(random.uniform(-1, 1),2)
            else:
                logs[i] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(logs)
        time.sleep(5)
        await send_messages(websocket,logs)

if __name__ == "__main__":
    async def connect_to_websocket():
        async with websockets.connect(f"ws://192.168.29.18:8000/serial_communication_rs485/") as websocket:
            print("WebSocket connection established")
            receive_task = asyncio.ensure_future(receive_messages(websocket))
            send_task = asyncio.ensure_future(send_messages(websocket))    
            produce_task = asyncio.ensure_future(produce_garbage_data(websocket))        
            await asyncio.gather(receive_task, send_task,produce_task)
    asyncio.get_event_loop().run_until_complete(connect_to_websocket())