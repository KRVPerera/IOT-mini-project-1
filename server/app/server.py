# reference: https://www.youtube.com/watch?v=Jd2fIFoRnNE&list=PLoVvAgF6geYMb029jpxqMuz5dRDtO0ydM&index=5

import logging
import asyncio

from aiocoap import *

import aiocoap.resource as resource
import aiocoap

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from database import send_influxdb

MAX_DATA_POINTS = 100
INDEX=0
data_values = [0]*MAX_DATA_POINTS

class temperature(resource.Resource):
    async def render_post(self, request):
        global data_values
        try:
            if request.code.is_request() and request.code == POST:
                payload = request.payload.decode('utf8')
                value = float(payload)
                data_values[INDEX] = value
                INDEX = (INDEX+1)%MAX_DATA_POINTS

                sum = sum(data_values)
                avg = sum/MAX_DATA_POINTS

                send_influxdb(float(avg)/100.0)
                logging.debug(f"Data received and sent to InfluxDB: {payload}")
                return Message(code=CONTENT, payload=b'Data added to InfluxDB')
            
            logging.warning("Bad request received")
            return Message(code=BAD_REQUEST)
        except Exception as e:
            logging.error(f"Error in processing request: {e}")
            return Message(code=INTERNAL_SERVER_ERROR)

async def main():
    try:
        root = resource.Site()
        root.add_resource(['.well-known', 'core'],
                resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(['temp'], temperature())
        await aiocoap.Context.create_server_context(site=root, bind=('::', 5683))
        await asyncio.get_running_loop().create_future()

    except Exception as e:
        logging.error(f"Error in starting server: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
        # asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        logging.info("Server stopped by KeyboardInterrupt")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Error: {e}")