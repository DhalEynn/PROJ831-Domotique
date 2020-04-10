import sys
sys.path.append('../')

import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData

from flask import Flask
from flask import render_template
from flask import request

import plotly
import plotly.graph_objs as go
import numpy as np
import json


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
    # selection with button
    if request.method == 'POST':
        req = request.form['item']
        # all

        if req == 'all':
            events = getData.getAll(logs, 100,True)
            bar = None
        # item
        else: 
            item = req.split()
            if len(item)==1:
                events = getData.getCategory(logs, item[0],actions,100,True)
            else:
                item[1] = int(item[1])
                events = getData.getItem(logs, item[0], item[1] , actions, 100,True)

            # create plot
            x = []
            y = []
            for event in events:
                if event['Action'] == 'EDGE RUNNED':
                    x.append(event['Begin Date'])
                    if event['Command'] in ['ON', 'UP']:
                        y.append(1)
                    elif event['Command'] in ['OFF', 'DOWN']:
                        y.append(0)
                    else:
                        y.append(-1)
            data = [go.Bar(x=x, y=y)]
            bar = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    # default page
    else:
        events = getData.getAll(logs, 100,True)
        bar = None

    return render_template("logs.html", items=items, nb_line=nb_line, events=events, plot=bar)

@app.route("/analyses")
def analyse():
    return render_template("analyses.html")