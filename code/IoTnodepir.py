# Name: Lidia Pocero
# IoTnode.py: Program a GAIA IoT node python for RaspberryPi over GrovePi bridge with a PIR sensor

import os
pidfile="/home/pi/pir.pid"

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def check_running():
    if os.path.isfile(pidfile):
        pid_file = open(pidfile, "r")
        pid = pid_file.read()
        pid_file.close()
        try:
            if check_pid(int(pid)):
                exit()
        except ValueError:
            pass
        save_pid()
    else:
        save_pid()

def save_pid():
    text_file = open(pidfile, "w")
    text_file.write(str(os.getpid()))
    text_file.close()


check_running()

import time
# Import grovepi
import grovepi

# Import sparksrabbit library
import sparksrabbit
import influx



pir_sensor = 8
motion = 0
new_motion = 0
grovepi.pinMode(pir_sensor,"INPUT")

while True:
    try:
        # Sense motion, usually human, within the target range
        new_motion = grovepi.digitalRead(pir_sensor)
        if new_motion == 0 or new_motion == 1:  # check if readings were 0 or 1 it can be 255 also because of IO Errors so remove those values
            if new_motion != motion:
                motion = new_motion
                # Send Motion
                value = str(motion)
                sparksrabbit.publish('pir', value)
	        influx.publish('pir',value)
                time.sleep(5.0)
                # if your hold time is less than this, you might not see as many detections
        time.sleep(.2)

    except IOError:
        print ("Error")


