# import python libraries
import flask
from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import time
import json

# define flask
app = Flask(__name__)

# set up variables to get latest messages
messages1 = ["-"] # for light controls status 
messages2 = ["-"] # for auto watering system status
messages3 = ["-"] # for external tank status

# define client message functions for MQTT

# client 1 message function
def on_message1(client, userdata, msg):
    messages1[0] = msg.payload.decode("utf-8")
# client 2 message function
def on_message2(client, userdata, msg):
    messages2[0] = msg.payload.decode("utf-8")
# client 3 message function
def on_message3(client, userdata, msg):
    messages3[0] = msg.payload.decode("utf-8")

# define clients

# client 1 for light controls
# define client entry
client1 = mqtt.Client()
# connect to MQTT broker
client1.connect("test.mosquitto.org", 1883, 60)
# assign message function to client
client1.on_message = on_message1
# subscribe to topic
client1.subscribe("csc1010/randomstring/1/0x00178801047ee3b6")
# starts thread
client1.loop_start()

#client 2 for auto watering system
# define client entry
client2 = mqtt.Client()
# connect to MQTT broker
client2.connect("test.mosquitto.org", 1883, 60)
# assign message function to client
client2.on_message = on_message2
# subscribe to topic
client2.subscribe("csc1010/randomstring/pump/1")
# starts thread
client2.loop_start()

#client 3 for external water tank sensor
# define client entry
client3 = mqtt.Client()
# connect to MQTT broker
client3.connect("test.mosquitto.org", 1883, 60)
# assign message function to client
client3.on_message = on_message3
# subscribe to topic
client3.subscribe("csc1010/randomstring/banksensor/1")
# starts thread
client3.loop_start()

#brightness down
def light_dim(client):
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(brightness="1", transition="3")))

#brightness up
def light_bright(client):
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(brightness="150", transition="3")))
#light off
def light_off(client):
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(state="off")))
#light on
def light_on(client):
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(state="on")))

#system on
def sys_on(client):
    client.publish("csc1010/randomstring/pump/1/set", payload="on")

#system off
def sys_off(client):
    client.publish("csc1010/randomstring/pump/1/set", payload="off")

# define index for flask http call
@app.route('/')
def index():
    return render_template("index.html")

# define farm1 for flask http call
@app.route('/farm1', methods=['GET', 'POST'])
def farm1():

    # initialize status messages
    status1 = ""
    status2 = ""
    
    # if http method is post
    if request.method == 'POST':

        # get light return status
        light_status = request.form.get('light')
        # get auto=watering system status
        system_status = request.form.get('system')

        # auto-watering system
        # if user sends on
        if system_status == "on":
            # sends message to MQTT broker to send message to system to on
            sys_on(client2)
        # if user sends off
        if system_status == "off":
            # sends message to MQTT broker to send message to system to off
            sys_off(client2)

        # light controls
        # if user sends on
        if light_status == "on":
            # sends message to MQTT broker to send message to lights to on settings
            light_on(client1)
        # if user sends off
        if light_status == "off":
            # sends message to MQTT broker to send message to lights to off settings
            light_off(client1)
        # if user sends dim
        if light_status == "dim":
            # sends message to MQTT broker to send message to lights to dim settings
            light_dim(client1)
        # if user sends bright
        if light_status == "bright":
            # sends message to MQTT broker to send message to lights to bright settings
            light_bright(client1)
        # delay for status return
        time.sleep(1)
        # publish status to app interface if there is status message for lights from MQTT
        if len(messages2) > 0:
            status2 = messages2[0]
        # publish status to app interface is there is status message for autowatering system from MQTT
        if len(messages1) > 0:
            status1 = messages1[0]

    # renders the template
    return render_template("farm1.html", l_status=status1, s_status=status2)

# water tank status route
@app.route('/watertank', methods=['GET'])
def farm2():

    # initialize status message
    status3 = ""

    # if message from MQTT is more than 1
    if len(messages3) > 0:
        # display latest message to user interface
        status3 = messages3[0]
    # render template
    return render_template("watertank.html", w_status=status3)

# runs the program
if __name__ == "__main__":
    app.run()
