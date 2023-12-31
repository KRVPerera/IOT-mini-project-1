# reference: https://www.youtube.com/watch?v=Jd2fIFoRnNE&list=PLoVvAgF6geYMb029jpxqMuz5dRDtO0ydM&index=5

import logging
import asyncio

from aiocoap import *

import aiocoap.resource as resource
import aiocoap

import logging
import asyncio

from database import send_influxdb

# Set up logging to a file
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from database import send_influxdb

MAX_DATA_POINTS = 100

class temperature(resource.Resource):

    def __init__(self):
        self.site_data = {
            'grenoble': {'values': [0] * MAX_DATA_POINTS, 'index': 0},
            'strasbourg': {'values': [0] * MAX_DATA_POINTS, 'index': 0},
            'saclay': {'values': [0] * MAX_DATA_POINTS, 'index': 0},
            'lillie': {'values': [0] * MAX_DATA_POINTS, 'index': 0}
        }
        self.logger = logging.getLogger("temperature")

    async def render_post(self, request):
        global INDEX
        global MAX_DATA_POINTS
        try:
            if request.code.is_request() and request.code == POST:
                payload = request.payload.decode('utf8')
                site,value_temp = payload.split(',')

                self.logger.debug(f"Site: {site}")
                self.logger.debug(f"Value: {value_temp}")

                try:
                    value = float(value_temp)
                except ValueError:
                    self.logger.error(f"Invalid temperature value received: {value_temp}")
                    return Message(code=BAD_REQUEST)
                
                self.logger.debug(f"Value received: {value}")
                self.site_data[site]['values'][self.site_data[site]['index']] = value

                self.logger.debug(f"Index: {self.site_data[site]['index']}")

                if isinstance(self.site_data[site]['index'], int):
                    self.logger.debug("Index is an integer")
                else:
                    self.logger.debug("Index is not an integer")

                self.site_data[site]['index'] = (self.site_data[site]['index'] + 1) % MAX_DATA_POINTS

                sum_value = 0.0
                sum_value = sum(self.site_data[site])
                self.logger.debug(f"Sum: {sum_value}")
                avg = sum_value*1.0/MAX_DATA_POINTS
                self.logger.debug(f"Avg: {avg}")
                send_influxdb(avg/100.0, site)
                self.logger.debug(f"Data received and sent to InfluxDB: {payload}")
                return Message(code=CONTENT, payload=b'Data added to InfluxDB')
            
            self.logger.warning("Bad request received")
            return Message(code=BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Error in processing request: {e}")
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