from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def logs():
    return render_template("index.html")

@app.route("/analyse")
def analyse():
    return render_template("index.html")