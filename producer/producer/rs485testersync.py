import websocket
import json
import threading
import random
import math
from scipy.stats import circmean
import pandas as pd
import datetime
import time

holt = True
websocket_url = 'ws://192.168.29.18:8000/ws/serial_communication/producer/'
retry_interval = 5  # seconds

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    global holt
    holt = True
    print(f"Closed with status code {close_status_code}: {close_msg}")
    retry_websocket(ws)

def on_open(ws):
    global holt
    holt = False
    print("WebSocket connection opened")
    ws.send(json.dumps({
        'client': 'producer',
        'device': 'rs485',
        'action': 'connection'
    }))

ws = None

def connect_websocket():
    global ws
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

def retry_websocket(ws):
    print(f"Retrying WebSocket connection in {retry_interval} seconds...")
    time.sleep(retry_interval)
    connect_websocket()

websocket_thread = threading.Thread(target=connect_websocket)
websocket_thread.start()

def generate_random_values():
    return {
        'RTC': datetime.datetime.now().isoformat(),
        'WSPD': random.uniform(0.0, 10.0),
        'HUMD': random.uniform(0.0, 10.0),
        'WDIR': random.uniform(0.0, 360.0),
        'ATMP': random.uniform(-10.0, 30.0),
        'RAIN': random.uniform(0.0, 5.0),
        'SRAD': random.uniform(0.0, 1000.0),
        'BPRS': random.uniform(900.0, 1100.0),
        'WDCH': random.uniform(0.0, 360.0),
        'DWPT': random.uniform(-10.0, 30.0),
        'P12': random.uniform(0.0, 100.0),
        'P13': random.uniform(0.0, 100.0),
        'P14': random.uniform(0.0, 100.0),
        'P15': random.uniform(0.0, 100.0),
        'P16': random.uniform(0.0, 100.0),
    }

def send_data(ws, action, data):
    ws.send(json.dumps({'client': 'producer', 'device': 'rs485', 'action': action, 'frame': data}))

def find_averages(data_list):
    df = pd.DataFrame(data_list)
    averages = {
        'RTC': data_list[-1]['RTC'],
        'WSPD': df['WSPD'].mean(),
        'WDIR': round(circmean(df['WDIR'], high=360, low=0), 3),
        'ATMP': df['ATMP'].mean(),
        'RAIN': df['RAIN'].sum(),
        'SRAD': df['SRAD'].mean(),
        'BPRS': df['BPRS'].mean(),
        'WDCH': df['WDCH'].mean(),
        'DWPT': df['DWPT'].mean(),
        'P12': df['P12'].mean(),
        'P13': df['P13'].mean(),
        'P14': df['P14'].mean(),
        'P15': df['P15'].mean(),
        'P16': df['P16'].mean(),
    }
    return averages

time_to_send = 5
time_to_store = 60
stored_list = []

try:
    while True:
        if not holt:
            dict_to_stream = generate_random_values()

            if not stored_list:
                timestamp = datetime.datetime.strptime(dict_to_stream['RTC'], "%Y-%m-%dT%H:%M:%S.%f")
                if timestamp.second == 0:
                    stored_list.append(dict_to_stream)

            stored_list.append(dict_to_stream)
            time_to_send -= 1

            if time_to_send == 0:
                print(dict_to_stream)
                send_data(ws, 'stream', dict_to_stream)
                time_to_send = 5

            time_to_store -= 1

            if time_to_store == 0:
                dict_to_store = find_averages(stored_list)
                send_data(ws, 'store', dict_to_store)
                stored_list = []
                time_to_store = 60

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    pass
    # ser.close()
