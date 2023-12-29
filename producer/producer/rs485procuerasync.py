import asyncio
import aioserial
import struct
import datetime
import math
import websockets
import json

minutes_data = []


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


def update_dict_with_values(dict_to_stream, values_list):
    dict_to_stream["RTC"] = datetime.datetime.now().isoformat()
    for key, value in dict_to_stream.items():
        if key != "RTC":
            value = float(values_list.pop(0)) if values_list else None
            if value is None or math.isnan(value):
                value = 0.0
            dict_to_stream[key] = value
    return dict_to_stream


async def read_and_print(aioserial_instance: aioserial.AioSerial, write_data: bytes, websocket):
    global minutes_data
    time_to_send = 5
    time_to_store = 60
    baud_rate = 9600
    data_bits = 8
    parity = 'N'
    stop_bits = 1
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
        if FINAL:
            dict_to_stream = update_dict_with_values(dict_to_stream, FINAL)
            print(dict_to_stream)
            await send_messages(websocket,
                                data={'client': 'producer', 'device': 'rs485', 'action': 'stream',
                                      'frame': dict_to_stream})


async def main():
    baud_rate = 9600
    data_bits = 8
    parity = 'N'
    stop_bits = 1
    aioserial_instance: aioserial.AioSerial = aioserial.AioSerial(port='COM3', baudrate=baud_rate, bytesize=data_bits,
                                                                    parity=parity, stopbits=stop_bits, timeout=1)

    # Specify the data you want to write
    write_data = bytes.fromhex("01040BB8002073D3")

    async with websockets.connect(f"ws://192.168.1.3:8000/ws/serial_communication/producer/") as websocket:
        print("WebSocket connection established")
        await websocket.send(json.dumps({
            'client': 'producer',
            'device': 'rs485',
            'action': 'connection'
        }))

        # Create a task for read_and_print
        read_task = asyncio.create_task(read_and_print(aioserial_instance, write_data, websocket))

        # Wait for the read task to complete
        await read_task


# Run the event loop
asyncio.run(main())
