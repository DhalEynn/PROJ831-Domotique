import sys
sys.path.append('../')

import env
import plotly
import json
import Filtering.filterData as filterData
import Transfer.sendData as sendData
import Transfer.getData as getData
import Transfer.connectDB as connectDB
import Analysis.generate as generate
import Analysis.Analysis as analysis

# Send logs to DB
logsDB = connectDB.connectToCollection('logs4')
filtered_data = filterData.LineReadingFromFile('Files/WOF4.log')
sendData.send_items(filtered_data, logsDB)

# Send analysis to DB
analysisDB = connectDB.connectToCollection('analysis')
items = generate.getAllItems()

lastObjectFreq = generate.createGraphLastObjectFreq(items)
sendData.send_items(lastObjectFreq, analysisDB)

fullPeriod = generate.createFullPeriodGraph(items)
sendData.send_items(fullPeriod, analysisDB)

predictions = generate.createPredictions(items)
sendData.send_items(predictions, analysisDB)

correlation = generate.createCorrelation()
sendData.send_items(correlation, analysisDB)