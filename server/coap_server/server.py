# reference: https://www.youtube.com/watch?v=Jd2fIFoRnNE&list=PLoVvAgF6geYMb029jpxqMuz5dRDtO0ydM&index=5

import logging
import json
import asyncio
from aiocoap import *

import aiocoap.resource as resource
import aiocoap

from database import send_influxdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("coap-server")
logger.setLevel(logging.DEBUG)

from configuration import CoAP_PORT

class temperature(resource.Resource):
    async def render_post(self, request):
        if request.code.is_request() and request.code == POST:
            payload = request.payload.decode('utf8')
            await sendInfluxdb(payload)
            return Message(code=CONTENT, payload=b'Data added to InfluxDB')
        return Message(code=BAD_REQUEST)

async def main():
    root = resource.Site()
    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['temperature'], temperature())
    await aiocoap.Context.create_server_context(root, bind=('::', CoAP_PORT))
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")