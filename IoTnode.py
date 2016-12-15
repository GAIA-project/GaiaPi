#
# Name: Lidia Pocero	
# IoTnode.py: Program a python GAIA IoT node  for RaspberryPi over GrovePi bridge with: 
# TH02 grove module,Digital Light Grove module and Loudness sensor Grove module 

import time
import math
#Import library for the light sensor
import light_library

#Import temperature humidity sensor library
import grove_i2c_temp_hum_mini

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

#Create the object for humidity and light 
t=grove_i2c_temp_hum_mini.th02()
l=light_library.light()

#digital inputs for PowerOff/On the temperature&humidty sensor
TH02_power = 4
grovepi.pinMode(TH02_power,"OUTPUT")

#values for loudness sensor
ref_SPL = 94 
sensitivity = 3.16
loudness_sensor = 0


def main():
	#Initialize the conection with rabbit server
	credentials = pika.PlainCredentials(username, password)
	parameters = pika.ConnectionParameters(ip,port,'/',credentials)

	connection = pika.BlockingConnection(parameters)
	channel =connection.channel()

	#Power off the temperature&humidity sensor
	grovepi.digitalWrite(TH02_power,1)
	#initialize the light sensor
	l.init()
	#read sensor and udate values on rabbit server

	#Temperature and Humidity
	#while (True):
	#Read temperature and humidty
	grovepi.digitalWrite(TH02_power,0) #Power On the Tem&Hum module
	time.sleep(.1)	#Wait to start I2C comunication  
	tem = t.getTemperature()
	hum = t.getHumidity()
	#print("Temp: %.2fC\tHumidity:%.2f" %(tem,hum),"%") 
	time.sleep(.1)
	grovepi.digitalWrite(TH02_power,1) #Power Off the Tem&Hum module
	time.sleep(.1)
	
	#Send temperature
	value = "%.4f" % tem
	ts = int(time.time())
	ts = ts*1000
	timestamp=str(ts)
	sensorName='temp'
	body=(username+'/'+gateway+'/'+sensorName+','+value+','+timestamp)
	channel.basic_publish(exchange=exchange,routing_key='hello',body=body)
	print("send:"+body)
	
	#Send Humidty
	value = "%.4f" % hum
	ts = int(time.time())
	ts = ts*1000
	timestamp=str(ts)
	sensorName='hum'
	body=(username+'/'+gateway+'/'+sensorName+','+value+','+timestamp)
	channel.basic_publish(exchange=exchange,routing_key='hello',body=body)
	print("send:"+body)
	
	#Read from light module
	lux=l.readVisibleLux()
	time.sleep(0.1)

	#Send lux
	value = "%.4f" % lux
	ts = int(time.time())
	ts = ts*1000
	timestamp=str(ts)
	sensorName='light'
	body=(username+'/'+gateway+'/'+sensorName+','+value+','+timestamp)
	channel.basic_publish(exchange=exchange,routing_key='hello',body=body)
	print("send:"+body)

	#Sound sensor read
	try:
		# Read the sound level
		rms = grovepi.analogRead(loudness_sensor)
		rms = rms*0.0032
		if (rms <=0):
			rms=0.0032
		db_current = (ref_SPL + 20 * math.log10(rms/ sensitivity)); 
		time.sleep(.1)

		#send loudnes
		value = "%.4f" % db_current
		ts = int(time.time())
		ts = ts*1000
		timestamp=str(ts)
		sensorName='sound'
		body=(username+'/'+gateway+'/'+sensorName+','+value+','+timestamp)
		channel.basic_publish(exchange=exchange,routing_key='hello',body=body)
		print("send:"+body)			

   	except IOError:
		print ("Error")	
	#time.sleep(2)
	connection.close()
	
if __name__ == "__main__":
        main()
