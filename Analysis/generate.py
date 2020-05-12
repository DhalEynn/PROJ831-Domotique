import sys
sys.path.append('../')
import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData
import Analysis.Analysis as analysis
import Analysis.prediction as prediction
import json
import plotly


def getAllItems():
    logs = connectDB.connectToCollection('logs4')
    categs = getData.getAllExistingCategories(logs)
    items = {}
    for categ in categs:
        items[categ] = getData.getAllIdFromCategory(logs, categ)
    return items

def createGraphLastObjectFreq(items):
    charts = []
    for category in items:
        for Id in items[category]:
            data = analysis.lastObjectFreq(category, Id, 100)
            fig = analysis.graphLastObjectFreq(data[0], data[1])
            chart = {'Category': category,
                    'Id':  Id,
                    'chart_type': 'lastObjectFreq',
                    'jsondumps': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)}
            charts.append(chart)
    return charts

def createPredictions(items):
    charts = []
    for category in items:
        for Id in items[category]:
            data = analysis.action_to_list(category, Id, 5000)
            # prediction 1
            predictions = prediction.prediction(data[0], data[1], 10000)
            fig = analysis.list_to_graph(predictions)
            # prediction 2
            # list_freq = an.frequency_activation_minute(liste_action, 5000, 1440)
            # predictions = periodPrediction(liste_action, 10000, list_freq, 1440)
            # fig = analysis.list_to_graph(predictions)
            chart = {'Category': category,
                    'Id':  Id,
                    'chart_type': 'prediction',
                    'jsondumps': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)}
            charts.append(chart)
    return charts

