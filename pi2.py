# Python Code to operate Raspberrypi 2
# Controls the moisture sensor to report on status of EXTERNAL WATER STORAGE TANK
# MQTT protocols

# Import libraries
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# initializes the MQTT client object
client = mqtt.Client()
# connects to the MQTT broker 
client.connect("test.mosquitto.org", 1883, 60)

# Set channels
channel1 = 21 # Channel for sensing high/low for moisture sensor

# set GPIO mode
GPIO.setmode(GPIO.BCM) 
GPIO.setup(channel1, GPIO.IN) # set default IN for moisture sensor

# set infinite loop
try:
    while True:
        # checks the status of high/low from moisture sensor
        if GPIO.input(channel1):
            # prints no water detected on console
            print("No Water Detected!")
            # publishes to MQTT of no water detected encoded
            client.publish("csc1010/randomstring/banksenor/1", payload=("No Water Detected").encode())
        else:
            # prints water detected on console
            print("Water Detected!")
            # publishes to MQTT of water detected encoded
            client.publish("csc1010/randomstring/banksenor/1", payload=("Water Detected").encode())

# CONTROL C exits program, and cleans up the GPIO setups
except KeyboardInterrupt:
    GPIO.cleanup()