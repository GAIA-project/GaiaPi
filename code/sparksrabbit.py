# Name: Dimitrios Amaxilatis
# sparksrabbit.py: a helper that connects to the SparkWorks RabbitMQ service to publish measurements from IoT Devices

import time
import pika
import properties

exchange = properties.client_id + '-send'
routing_key = exchange

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


def close():
    connection.close()
