import os



# ------------------------------  from database.py file ------------------------------ # 
# InfluxDB credentials
#HOST      = os.environ.get('INFLUXDB_HOST', '192.168.1.172')
HOST      = os.environ.get('INFLUXDB_HOST', '127.0.0.1')
PORT      = os.environ.get('INFLUXDB_PORT', 8086)
USERNAME  = os.environ.get('INFLUXDB_USER', 'miniproject1_user')
PASSWORD  = os.environ.get('INFLUXDB_USER_PASSWORD', 'miniproject1_pass')
DATABASE  = os.environ.get('INFLUXDB_DB', 'iotdb')

# measurements/tables
TEMPERATURE = 'temperature'

# tags/indices
PLACE  = 'testbed_sensor1'

CoAP_HOST = os.environ.get("CoAP_HOST", "127.0.0.1")      # CoAP host
CoAP_PORT = int(os.environ.get("CoAP_PORT", 5683))      # CoAP port