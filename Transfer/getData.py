import os
import copy
import pymongo
from pymongo import MongoClient

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
SERVER = os.getenv('DB_SERVER')

client = MongoClient('mongodb://' + USERNAME + ':' + PASSWORD + '@' + SERVER)

#db domo
db = client.domo

#collection logs
logs = db.logs

#collection analyse
analyse = db.analyse

def getCategory(categ):
    results = []
    for r in logs.find({'Category': categ}):
        results.append(r)
    return results

def getFunction(funct):
    results = []
    for r in logs.find({'Function': funct}):
        results.append(r)
    return results

def getCommand(comm):
    results = []
    for r in logs.find({'Command': funct}):
        results.append(r)
    return results