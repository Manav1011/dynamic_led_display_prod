# import serial
# import re
# import asyncio
# import websockets
# import json

# logs = {
#     'client':'provider',
#     'RTC':'',
#     'AvgeSpeed':'',
#     'AvgeTemp':'',
#     'AvgeHum':'',
#     'AvgeSr':''
# }
# data = []
# RTCpattern = r"RTCTime:\s+(\d+:\d+:\d+)\s+(\d+/\d+/\d+)"

async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()       
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")

async def send_messages(websocket,data=None):
    try:        
        if data is not None:
            await websocket.send(json.dumps(data))
    except websockets.ConnectionClosed as e:
        exit(e)        

async def read_serial_port(port_name, baud_rate=115200,websocket = None):
    ser = None  # Initialize ser outside the try block
    
    try:
        # Open the serial port
        ser = serial.Serial(port_name, baudrate=baud_rate)
        # Read and print incoming data indefinitely
        while True:
                try:
                    data = ser.readline()  # Read one line of data (until a newline character is encountered)            
                    data = data.decode('utf-8').strip()            
                    if 'RTCTime' in data:   
                        match = re.search(RTCpattern, data)
                        time_str, date_str = match.groups()                                                                    
                        logs['RTC'] = [f'{date_str} - {time_str}']
                    elif 'AvgeSpeed' in data and 'AvgeTemp' in data and 'AvgeHum' in data and 'AvgeSr' in data:
                        data = data.split(',')
                        for i in data:
                            key,value = i.split(':')
                            logs[key] = [value]
                        print(logs)
                        await send_messages(websocket,logs)
                except Exception as e:
                    print(e)

    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser is not None and ser.is_open:
            ser.close()

if __name__ == "__main__":
    async def connect_to_websocket():
        async with websockets.connect(f"ws://192.168.43.106:8000/serial_communication/123/") as websocket:
            print("WebSocket connection established")

            receive_task = asyncio.ensure_future(receive_messages(websocket))
            send_task = asyncio.ensure_future(send_messages(websocket))
            serial_task = asyncio.ensure_future(read_serial_port("/dev/ttyUSB0",websocket=websocket))
            await asyncio.gather(receive_task, send_task,serial_task)
    asyncio.get_event_loop().run_until_complete(connect_to_websocket())
    # serial_port = "/dev/ttyUSB0"
    # read_serial_port(serial_port)

import serial
RTCpattern = r"RTCTime:\s+(\d+:\d+:\d+)\s+(\d+/\d+/\d+)"
logs = {
    'client':'provider',
    'RTC':'',
    'AvgeSpeed':'',
    'AvgeTemp':'',
    'AvgeHum':'',
    'AvgeSr':''
}
import re
def read_serial_port(port_name, baud_rate=115200,websocket = None):
    ser = None  # Initialize ser outside the try block
    try:
        # Open the serial port
        ser = serial.Serial(port_name, baudrate=baud_rate)
        # Read and print incoming data indefinitely
        while True:
                try:
                    data = ser.readline()  # Read one line of data (until a newline character is encountered)            
                    data = data.decode('utf-8').strip() 
                    print(data)
                    if 'RTCTime' in data:   
                        match = re.search(RTCpattern, data)
                        time_str, date_str = match.groups()                                                                    
                        logs['RTC'] = [f'{date_str} - {time_str}']
                    elif 'AvgeSpeed' in data and 'AvgeTemp' in data and 'AvgeHum' in data and 'AvgeSr' in data:
                        data = data.split(',')
                        for i in data:
                            key,value = i.split(':')
                            logs[key] = [value]
                        print(logs)                    
                except Exception as e:
                    print(e)
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser is not None and ser.is_open:
            ser.close()
read_serial_port(port_name="/dev/ttyUSB0")