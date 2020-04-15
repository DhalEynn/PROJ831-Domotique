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
import json


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs", methods=['GET', 'POST'])
def logs():
    logs = connectDB.connectToCollection("logs4")

    # items table
    categs = getData.getAllExistingCategories(logs)
    items = {}
    for categ in categs:
        items[categ] = getData.getAllIdFromCategory(logs, categ)
    nb_line = max(len(value) for key, value in items.items())

    # events table
    actions = getData.getAllExistingActions(logs)
    # selection with button
    chart = None
    if request.method == 'POST':
        req = request.form['item']
        # all
        if req == 'all':
            events = getData.getAll(logs, 100,True)
        # item
        else: 
            item = req.split()
            if len(item)==1:
                events = getData.getCategory(logs, item[0],actions,100,True)
            else:
                item[1] = int(item[1])
                events = getData.getItem(logs, item[0], item[1] , actions, 100,True)
                # create plot
                bar_name = ['']
                data = []

                fig = go.Figure()
                for i in range(len(events)):
                    if events[i]['Action'] == 'EDGE RUNNED':
                        y = events[i]['Begin Date']
                        if i>1:
                            y -= events[i-1]['Begin Date']
                        if events[i]['Command'] in ['ON', 'UP']:
                            fig.add_trace(go.Bar(name=events[i]['Command'], y=bar_name, x=[y], marker=dict(color=['green']), orientation='h'))
                        elif events[i]['Command'] in ['OFF', 'DOWN']:
                            fig.add_trace(go.Bar(name=events[i]['Command'], y=bar_name, x=[y], marker=dict(color=['red']), orientation='h'))
                fig.update_layout(width=800,
                                height=50,
                                margin=dict(
                                l=10,
                                r=10,
                                b=10,
                                t=10,),
                                barmode='stack',
                                showlegend=False,
                                )
                chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # default page
    else:
        events = getData.getAll(logs, 100,True)

    return render_template("logs.html", items=items, nb_line=nb_line, events=events, plot=chart)

@app.route("/analyses")
def analyse():
    return render_template("analyses.html")