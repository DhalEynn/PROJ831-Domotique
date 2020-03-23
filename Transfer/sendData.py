
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

def send_items(items, collection):
	for item in items:
		item['_id']=make_hash(item)
		collection.update_one({'_id': item['_id']}, {'$set': item}, upsert=True)