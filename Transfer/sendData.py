def send_items(items, collection):
	for item in items:
		collection.update_one(item, {'$set': item}, upsert=True)