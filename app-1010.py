import flask
from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# init mqtt app
client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

#brightness down
def light_dim():
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(brightness="1", transition="3")))
#brightness up
def light_bright():
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(brightness="150", transition="3")))
#light off
def light_off():
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(state="off")))
#light on
def light_on():
    client.publish("csc1010/randomstring/1/0x00178801047ee3b6/set", payload=json.dumps(dict(state="on")))

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/farm1', methods=['GET', 'POST'])
def farm1():

    if request.method == 'POST':

        light_status = request.form.get('light')
        system_status = request.form.get('system')

        if light_status == "on":
            light_on()
        if light_status == "off":
            light_off()
        if light_status == "dim":
            light_dim()
        if light_status == "bright":
            light_bright()

    return render_template("farm1.html")


@app.route('/farm2', methods=['GET', 'POST'])
def farm2():

    if request.method == 'POST':
        pass

    return render_template("farm2.html")

if __name__ == "__main__":
    app.run()
