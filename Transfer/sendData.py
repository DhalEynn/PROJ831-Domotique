
import copy


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

def send_items(list,collection):
  for item in list:
    item['_id']=make_hash(item)
    result = collection.insert_one(item)
    print(result.inserted_id)

"""
data = {
    'Category': 'test data', 
    'Id': 9,
    'Function': 'HEAT',
    'Action': 'TRY TO RUN EDGE',
    'Begin State': [1, True],
    'Command': 'OFF',
    'Ending State': [1, False],
    'Begin Date': 455,
    'Ending Date': 486
}

data['_id'] = make_hash(data)

result = logs.insert_one(data)

print(result.inserted_id)
"""