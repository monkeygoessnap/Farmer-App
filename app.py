import flask
import os
from flask import Flask

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return

@app.route('/')
def index():
    return 'TestTest'


@app.route('home')
def home():
    return "YourHome"

if __name__ == "__main__":
    app.debug = True
    app.run()
