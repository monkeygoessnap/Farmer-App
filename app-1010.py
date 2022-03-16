import flask
from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import time
import json

app = Flask(__name__)

messages1 = ["-"]
messages2 = ["-"]
messages3 = ["-"]

def on_message1(client, userdata, msg):
    messages1[0] = msg.payload.decode("utf-8")
    # print(msg.payload.decode("utf-8"))

def on_message2(client, userdata, msg):
    messages2[0] = msg.payload.decode("utf-8")
    # print(msg.payload.decode("utf-8"))

def on_message3(client, userdata, msg):
    messages3[0] = msg.payload.decode("utf-8")
    # print(msg.payload.decode("utf-8"))

client1 = mqtt.Client()
client1.connect("test.mosquitto.org", 1883, 60)
client1.on_message = on_message1
client1.subscribe("csc1010/randomstring/1/0x00178801047ee3b6")
client1.loop_start()

client2 = mqtt.Client()
client2.connect("test.mosquitto.org", 1883, 60)
client2.on_message = on_message2
client2.subscribe("csc1010/randomstring/pump/1")
client2.loop_start()

client3 = mqtt.Client()
client3.connect("test.mosquitto.org", 1883, 60)
client3.on_message = on_message3
client3.subscribe("csc1010/randomstring/banksensor/1")
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


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/farm1', methods=['GET', 'POST'])
def farm1():

    status1 = ""
    status2 = ""

    if request.method == 'POST':

        light_status = request.form.get('light')
        system_status = request.form.get('system')

        if system_status == "on":
            sys_on(client2)
        if system_status == "off":
            sys_off(client2)

        if light_status == "on":
            light_on(client1)
        if light_status == "off":
            light_off(client1)
        if light_status == "dim":
            light_dim(client1)
        if light_status == "bright":
            light_bright(client1)
        time.sleep(1)
        if len(messages2) > 0:
            status2 = messages2[0]

        if len(messages1) > 0:
            status1 = messages1[0]

    return render_template("farm1.html", l_status=status1, s_status=status2)


@app.route('/watertank', methods=['GET', 'POST'])
def farm2():

    status3 = ""
    if request.method == 'POST':
        pass

    if len(messages3) > 0:
        status3 = messages3[0]
    return render_template("watertank.html", w_status=status3)

if __name__ == "__main__":
    app.run()
