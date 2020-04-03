import sys
sys.path.append('../')

import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def logs():
    logs = connectDB.connectToCollection("logs")

    categs = getData.getAllExistingCategories(logs)
    items = {}
    for categ in categs:
        items[categ] = getData.getAllIdFromCategory(logs, categ)
    nb_line = max(len(value) for key, value in items.items())

    actions = getData.getAllExistingActions(logs)
    events = getData.getItem(logs, "SWITCH", 3 , actions)
    return render_template("logs.html", items=items, nb_line=nb_line, events=events)

@app.route("/analyses")
def analyse():
    return render_template("analyses.html")