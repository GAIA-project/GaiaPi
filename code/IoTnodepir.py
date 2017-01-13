# Name: Lidia Pocero
# IoTnode.py: Program a GAIA IoT node python for RaspberryPi over GrovePi bridge with a PIR sensor

import time
# Import grovepi
import grovepi

# Import sparksrabbit library
import sparksrabbit


pir_sensor = 8
motion = 0
new_motion = 0
grovepi.pinMode(pir_sensor, "INPUT")

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
                time.sleep(5.0)
                # if your hold time is less than this, you might not see as many detections
        time.sleep(.2)

    except IOError:
        print ("Error")
