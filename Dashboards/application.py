from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def logs():
    return render_template("logs.html")

"""@app.route("/logs<category>")
def logs(category=None):
    graph = categories.temp(category)
    return render_template("logs.html", graphTemp=graph)"""

@app.route("/analyses")
def analyse():
    return render_template("analyses.html")