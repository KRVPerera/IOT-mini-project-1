# ref: https://www.youtube.com/watch?v=O20Y1XR6g0A&list=PLoVvAgF6geYMb029jpxqMuz5dRDtO0ydM&index=4
from influxdb import InfluxDBClient
import time

from config import HOST, PORT, USERNAME, PASSWORD, DATABASE, PLACE

def client():
    client = InfluxDBClient(host=HOST, port=int(PORT), username=USERNAME, password=PASSWORD)
    client.create_database(DATABASE)
    client.switch_database(DATABASE)
    return client

def getInfluxDB(query, measurement='temperature'):
    db_client = client()
    result = db_client.query(query=query)
    output = []
    for key, value in enumerate(result):
        output.append(value)  
    return output

def save(db_client, measurement, fields, tags=None):
    json_body = [{'measurement': measurement, 'tags': tags, 'fields': fields}]
    db_client.write_points(json_body)


def send_influxdb(data, measurement='temperature'):
    db_client = client()
    if measurement == 'temperature' or measurement == 'humidity':
        tags        = { "place": PLACE }
        fields      = { "value" : data }
        save(db_client, measurement, fields, tags=tags)
        # time.sleep(0.1)
        
    else:
        print("Positional argument (measurement) required!")