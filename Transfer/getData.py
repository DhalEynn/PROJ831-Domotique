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

def getItem(categ,Id):
    results = []
    for log in logs.find({"Category": categ, "Id" : Id}):
        results.append(log)
    return results

def getDate(period,t1,t2):
    '''
        Si Period = begin(resp. end): Renvoie les events tel que t1 < Begin(resp. Ending) Date < t2
        Si Perdiod = full: Renvoie les events tel que t1 < Begin Date et End Date < t2
    '''
    results = []
    if period =='begin':

        for log in logs.find({'Begin Date': {"$gt" : t1 ,"$lt" :t2}}): 
            results.append(log)
        return results
    
    elif period =='end':

        for log in logs.find({'Ending Date': {"$gt" : t1 ,"$lt" :t2}}):
            results.append(log)
        return results
    
    elif period =='full':

        for log in logs.find({'Begin Date': {"$gt" : t1 ,"$lt" :t2},'Ending Date': {"$gt" : t1 ,"$lt" :t2}}):
            results.append(log)
        return results
        
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
