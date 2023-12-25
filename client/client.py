import logging
import asyncio
from aiocoap import *
import aiocoap
from random import randint
import time
import random

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()
    count =0
    while (count < 200):
        random_float = random.uniform(22.0, 45.0)
        randString = str(random_float)
        payload = (randString).encode("utf-8")
        request = Message(code=aiocoap.POST, payload=payload , uri='coap://[2600:1f16:15a8:3b2:804b:8136:56a6:cb5b]:5683/temp')
        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            print('Result: %s\n%r'%(response.code, response.payload))
        time.sleep(1)
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())