import flask
from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import time
import json

app = Flask(__name__)

messages = []

def on_message(client, userdata, msg):
    messages.append(msg.payload.decode("utf-8"))
    # print(msg.payload.decode("utf-8"))

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)
client.on_message = on_message
client.subscribe("csc1010/randomstring/1/0x00178801047ee3b6")
client.loop_start()

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


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/farm1', methods=['GET', 'POST'])
def farm1():

    status = ""

    if request.method == 'POST':

        light_status = request.form.get('light')
        system_status = request.form.get('system')

        if light_status == "on":
            light_on(client)
        if light_status == "off":
            light_off(client)
        if light_status == "dim":
            light_dim(client)
        if light_status == "bright":
            light_bright(client)
        time.sleep(1)
        if len(messages) > 0:
            status = messages.pop()

    return render_template("farm1.html", l_status=status)


@app.route('/farm2', methods=['GET', 'POST'])
def farm2():

    if request.method == 'POST':
        pass

    return render_template("farm2.html")

if __name__ == "__main__":
    app.run()
    client.loop_forever()
