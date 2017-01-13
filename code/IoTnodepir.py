# Name: Lidia Pocero
# IoTnode.py: Program a GAIA IoT node python for RaspberryPi over GrovePi bridge with a PIR sensor

import time
# Import grovepi
import grovepi

# Import rabbitmq library
import pika
import properties

exchange = properties.client_id + '-send'
routing_key = exchange

pir_sensor = 8
motion = 0
grovepi.pinMode(pir_sensor, "INPUT")

credentials = pika.PlainCredentials(properties.client_id, properties.client_secret)
parameters = pika.ConnectionParameters(properties.ip, properties.port, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()


def publish(sensorName, value, timestamp=None):
    if timestamp is None:
        ts = int(time.time())
        ts *= 1000
        timestamp = str(ts)
    body = (properties.client_id + '/' + properties.gateway + '/' + sensorName + ',' + value + ',' + timestamp)
    channel.basic_publish(exchange=exchange, routing_key=exchange, body=body)
    print("send:" + body)


mo = 0
while True:
    try:
        # Sense motion, usually human, within the target range
        motion = grovepi.digitalRead(pir_sensor)
        if motion == 0 or motion == 1:  # check if readings were 0 or 1 it can be 255 also because of IO Errors so remove those values
            if motion != mo:
                mo = motion
                # Send Motion
                value = str(mo)
                publish('pir', value)

                # if your hold time is less than this, you might not see as many detections
        time.sleep(.2)

    except IOError:
        print ("Error")
