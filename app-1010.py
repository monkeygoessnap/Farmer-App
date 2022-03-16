import flask
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/farm1', methods=['GET', 'POST'])
def farm1():

    if request.method == 'POST':
        pass

    return render_template("farm1.html")


@app.route('/farm2', methods=['GET', 'POST'])
def farm2():

    if request.method == 'POST':
        pass
    
    return render_template("farm2.html")

if __name__ == "__main__":
    app.run()
