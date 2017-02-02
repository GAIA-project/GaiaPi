# Name: Dimitrios Amaxilatis
# sparksrabbit.py: a helper that connects to the SparkWorks RabbitMQ service to publish measurements from IoT Devices

import time

from influxdb import InfluxDBClient
client = InfluxDBClient("localhost",8086,"gaia","gaia","sensors")



def publish(sensorName, value, timestamp=None):
    try:
        dopublish(sensorName,value,timestamp)
    except:
        pass

def dopublish(sensorName, value, timestamp=None):
    if timestamp is None:
        ts = int(time.time())
        ts *= 1000
        timestamp = ts
    client.write_points([{"time": time.ctime(),"measurement":"sensors","fields": {sensorName : value},"tags":{"hostname":"local"}}])


