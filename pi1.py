# Python Code to operate Raspberrypi 1
# Control pump and moisture sensor for the auto-watering system to work via
# MQTT protocols

# Import libraries
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Set channels
channel1 = 21 # Channel for sensing high/low for moisture sensor
channel2 = 16 # Channel for operating relay to control motor

# set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel1, GPIO.IN) # set default IN for moisture sensor
GPIO.setup(channel2, GPIO.OUT) # set default OUT for relay

# MQTT topic
mqtt_path = "csc1010/randomstring/pump"

# MQTT subscribe function, on message
def on_message(client, userdata, msg):
	# decode received message
	received = msg.payload.decode("utf-8")
	# if message is on
	if received == "on":
		# add event detect for soil moisture sensor
		GPIO.add_event_detect(channel1, GPIO.BOTH, bouncetime=300)
		# add event callback for controlling relay and printing
		GPIO.add_event_callback(channel1, callback)
		# switch on motor first to trigger event detect
		motor_on(channel2)
		# returns STATUS message by publishing to MQTT topic
		toSend = "System ON"
		# publishes to topic +/1 for status topic
		client.publish(mqtt_path+"/1", payload = toSend)
		# prints ON on console
		print("ON")
	# if message received is off
	if received == "off":
		# remove event detect for soil moisture sensor
		GPIO.remove_event_detect(channel1)
		# switch off motor
		motor_off(channel2)
		# returns STATUS message by publishing to MQTT topic
		toSend = "System OFF"
		# publishes to topic +/1 for status topic
		client.publish(mqtt_path+"/1", payload = toSend)
		# prints OFF on console
		print("OFF")

# initializes the MQTT client object
client = mqtt.Client()
# set on message function to MQTT client message returns
client.on_message = on_message
# connects to the MQTT broker 
client.connect("test.mosquitto.org", 1883, 60)
# subscribes to the topic of setting the system
client.subscribe(mqtt_path+"/1/set")
# starts the multi-threaded loop for the client
client.loop_start()

# defines the callback function for the GPIO
def callback(channel1):
	# soil moisture checks high/low status
	if GPIO.input(channel1):
		# prints no water detected
		print("No Water detected!")
		# and switches on the motor
		motor_on(channel2)
	else:
		# prints water detected
		print("Water Detected!")
		# switches off the motor
		motor_off(channel2)
		
# switches on the motor by switching the relay to on, pin is relay control pin
def motor_on(pin):
	GPIO.output(pin, GPIO.HIGH) #turn motor on
def motor_off(pin):
	GPIO.output(pin, GPIO.LOW) # turns motor off

# loops the main program callback
try:
	while True:
		time.sleep(1)
# keyboard CONTROL C interrupts program and cleans up the GPIO setups
except KeyboardInterrupt:
	GPIO.cleanup()
