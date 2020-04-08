import sys
sys.path.append('../')

import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs", methods=['GET', 'POST'])
def logs():
    logs = connectDB.connectToCollection("logs")

    # items table
    categs = getData.getAllExistingCategories(logs)
    items = {}
    for categ in categs:
        items[categ] = getData.getAllIdFromCategory(logs, categ)
    nb_line = max(len(value) for key, value in items.items())

    # events table
    actions = getData.getAllExistingActions(logs)
    if request.method == 'POST':
        item = request.form['item'].split()
        item[1] = int(item[1])
        events = getData.getItem(logs, item[0], item[1] , actions, 100)
    else:
        events = getData.getAll(logs)
    return render_template("logs.html", items=items, nb_line=nb_line, events=events)

@app.route("/analyses")
def analyse():
    return render_template("analyses.html")