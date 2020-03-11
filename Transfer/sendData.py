import os
import copy
import pymongo
from pymongo import MongoClient

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
SERVER = os.getenv('DB_SERVER')

client = MongoClient('mongodb://' + USERNAME + ':' + PASSWORD + '@' + SERVER)
db = client.domo
logs = db.logs
analyse = db.analyse


def make_hash(o):

  """
  Makes a hash from a dictionary, list, tuple or set to any level, that contains
  only other hashable types (including any lists, tuples, sets, and
  dictionaries).
  """

  if isinstance(o, (set, tuple, list)):

    return tuple([make_hash(e) for e in o])    

  elif not isinstance(o, dict):

    return hash(o)

  new_o = copy.deepcopy(o)
  for k, v in new_o.items():
    new_o[k] = make_hash(v)

  return hash(tuple(frozenset(sorted(new_o.items()))))


data = {
    'Category': 'switch', 
    'Id': 7,
    'Function': 'HEAT',
    'Action': 'TRY TO RUN EDGE',
    'Begin State': ['1', 'TRUE'],
    'Command': 'OFF',
    'Ending State': ['1', 'OFF'],
    'Begin Date': 485,
    'Ending Date': 486
}

data['_id'] = make_hash(data)

result = logs.insert_one(data)
print(result.inserted_id)