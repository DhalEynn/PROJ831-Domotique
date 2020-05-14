import os
import pymongo
from pymongo import MongoClient

def connectToCollection(collection):
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')
    SERVER = os.getenv('DB_SERVER')

    client = MongoClient('mongodb://' + USERNAME + ':' + PASSWORD + '@' + SERVER)
    #db domo
    db = client.domo
    return db[collection]
    