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

    elif (collectionName =='logs2'):
        #collection analyse
        logs2 = db.logs2
        return logs2

    elif (collectionName =='logs4'):
        #collection analyse
        logs4 = db.logs4
        return logs4

    else:
        print('nope')
