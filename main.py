import sys
sys.path.append('../')

import Filtering.filterData as filterData
import Transfer.sendData as sendData
import Transfer.getData as getData
import Transfer.connectDB as connectDB
import Analysis.generate as generate

import os
import env


# Parameters
logs_file = "Files/WOF3.log"
logs_collection = os.getenv('COLLECTION_LOGS')
analysis_collection = os.getenv('COLLECTION_ANALYSIS')


# Send logs to DB
logsDB = connectDB.connectToCollection(logs_collection)
filtered_data = filterData.LineReadingFromFile(logs_file)
sendData.send_items(filtered_data, logsDB)


# Send analysis to DB
analysisDB = connectDB.connectToCollection(analysis_collection)
items = generate.getAllItems()

lastObjectFreq = generate.createGraphLastObjectFreq(items)
sendData.send_items(lastObjectFreq, analysisDB)

fullPeriod = generate.createFullPeriodGraph(items)
sendData.send_items(fullPeriod, analysisDB)

predictions = generate.createPredictions(items)
sendData.send_items(predictions, analysisDB)

correlation = generate.createCorrelation()
sendData.send_items(correlation, analysisDB)
