import sys
sys.path.append('../')
import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData
import Analysis.Analysis as analysis
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