import os

import pymongo
from pymongo import MongoClient

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
SERVER = os.getenv('DB_SERVER')

client = MongoClient('mongodb://' + USERNAME + ':' + PASSWORD + '@' + SERVER)

db = client.domo

logs = db.logs

analyse = db.analyse

data = {
    '_id': 1,
    'string': 'Python and MongoDB',
    'list': [1, 2, 3],
    'int': 3
}

result = logs.insert_one(data)
print('One logs: {0}'.format(result.inserted_id))