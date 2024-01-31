import asyncio
import threading

def start_event_loop(loop,coroutine):
    asyncio.set_event_loop(loop=loop)
    loop.run_until_complete(coroutine())

async def test_coroutine():
    print("Coroutine started")
    asyncio.sleep(10)
    print('Coroutine ended')

new_loop = asyncio.new_event_loop()
newthread = threading.Thread(target=start_event_loop,args=(new_loop,test_coroutine))