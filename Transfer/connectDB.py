import os
import pymongo
from pymongo import MongoClient

def connectToCollection(collection):
    """
        Connect to domo database and return a collection
    """
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')
    SERVER = os.getenv('DB_SERVER')

    client = MongoClient('mongodb://' + USERNAME + ':' + PASSWORD + '@' + SERVER)
    db = client.domo
    return db[collection]
