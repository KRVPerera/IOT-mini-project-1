import os

# ------------------------------  from database.py file ------------------------------ # 
# InfluxDB credentials
#HOST      = os.environ.get('INFLUXDB_HOST', '192.168.1.172')
HOST      = os.environ.get('INFLUXDB_HOST', 'influxdb')
PORT      = os.environ.get('INFLUXDB_PORT', 8086)
USERNAME  = os.environ.get('INFLUXDB_USER', 'miniproject1_user')
PASSWORD  = os.environ.get('INFLUXDB_USER_PASSWORD', 'miniproject1_pass')
DATABASE  = os.environ.get('INFLUXDB_DB', 'iotdb')

# tags/indices
PLACE  = 'testbed_sensor1'