import os
import pymongo
from pymongo import MongoClient


def connectToCollection(collectionName):
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')
    SERVER = os.getenv('DB_SERVER')

    client = MongoClient('mongodb://' + USERNAME + ':' + PASSWORD + '@' + SERVER)
    #db domo
    db = client.domo

    
    if (collectionName =='logs'):
        #collection logs
        logs = db.logs
        return logs
    
    elif (collectionName =='analyse'):
        #collection analyse
        analyse = db.analyse
        return analyse

    else:
        print('nope')
