# GaiaPi

GaiaPi is a set of python scripts and RaspberryPi configuration files designed to supply data from Grove Sensors to the Gaia platform.


## What you need

A RaspberryPi, a Grove Pi and some Grove Sensors. In our case we use:

1. Grove Sound Sensor
1. Grove Temperature and Humidity Sensor
1. Grove Pir Sensor
1. Grove Light Sensor

## How it works

The `IoTnode.py` and `IoTnodepir.py` scripts collect the data from the Grove sensors and transmit them to the Gaia platform for storage and processing.
Both scripts also store the data locally in an `InfluxDB` and prove visualizations via a `Grafana` dashboard.

For the first part the python script contains the following line :

    sparksrabbit.publish('sound', value)

To store the data in the `InfluxDB` the script uses the following:

    influx.publish('sound',value)

Connection settings for both options are configured in the `properties.py` file.

