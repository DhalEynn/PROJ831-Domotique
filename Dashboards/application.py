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
    print(items)
    nb_line = max(len(value) for key, value in items.items())
    return render_template("logs.html", items=items, nb_line=nb_line)

"""@app.route("/logs<category>")
def logs(category=None):
    graph = categories.temp(category)
    return render_template("logs.html", graphTemp=graph)"""

@app.route("/analyses")
def analyse():
    return render_template("analyses.html")