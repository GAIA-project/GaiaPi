# Name: Lidia Pocero
# IoTnode.py: Program a GAIA IoT node python for RaspberryPi over GrovePi bridge with a PIR sensor

import time
#Import grovepi
import grovepi

#Import rabbit library
import pika
from properties import username
from properties import password
from properties import ip
from properties import port
from properties import exchange
from properties import gateway

pir_sensor = 8
motion=0
grovepi.pinMode(pir_sensor,"INPUT")

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(ip,port,'/',credentials)

connection = pika.BlockingConnection(parameters)
channel =connection.channel()
mo=0
while True:
	try:
	
		# Sense motion, usually human, within the target range
		motion=grovepi.digitalRead(pir_sensor)
		if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
			if motion!=mo:
					mo=motion
					#Send Humidty
					#value = "%.4f" % hum
					value = str(mo)
					ts = int(time.time())
					ts = ts*1000
					timestamp=str(ts)
					sensorName='pir'
					body=(username+'/'+gateway+'/'+sensorName+','+value+','+timestamp)
					channel.basic_publish(exchange=exchange,routing_key='hello',body=body)
					print("send:"+body)	

			# if your hold time is less than this, you might not see as many detections
		time.sleep(.2)

	except IOError:
		print ("Error")
