import time
from datetime import timedelta

def send_items(items, collection):
	"""
		Send items in the specified collection of the database. 
		Show running time, and percentage of sent items.
	"""
	start_time = time.time()
	print("There are %d items to send." % (len(items)))
	size_percent = int(len(items) * 0.01)
	value = 0
	percent = 0
	temp_time = start_time
	for item in items:
		if (value == size_percent):
			percent += 1
			print("We are now at %d%%" % (percent))
			print("Elapsed real time : %s" % str(timedelta(seconds = (time.time() - temp_time))))
			temp_time = time.time()
			value = 0
		else:
			value += 1
		collection.update_one(item, {'$set': item}, upsert=True)
	print("Elapsed total time : %s." % str(timedelta(seconds = (time.time() - start_time))))
