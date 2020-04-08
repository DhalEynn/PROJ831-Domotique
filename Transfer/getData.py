import pymongo
def getItem(logs, categ, Id,actions,limit=None):
    '''
        Obtenir tous les événements d'un item défini par une Catégorie, un ID et une liste d'action
        si limit est fixé retourne les limi premiers éléments
    '''
    results = []
    if limit ==None:
        req = logs.find({"Category": categ, "Id" : Id,  "Action":{"$in":actions}}).sort({'Ending Date':-1})
    else:
        req = logs.find({"Category": categ, "Id" : Id,  "Action":{"$in":actions}}).limit(limit).sort({'Ending Date':-1})
    for log in req:
        results.append(log)
    return results

def getDate(logs, period, t1, t2,actions):
    '''
        Obtenir tous les événements dans un intervalle [t1, t2] et en fonction d'une liste d'actions

        Si Period = begin(resp. end) -> Renvoie les événements tels que t1 < Begin(resp. Ending) Date < t2
        Si Period = full -> Renvoie les événements tels que t1 < Begin Date et End Date < t2
    '''
    results = []
    if period =='begin':

        for log in logs.find({'Begin Date': {"$gt" : t1 ,"$lt" :t2},"Action":{"$in":actions}}): 
            results.append(log)
        return results
    
    elif period =='end':

        for log in logs.find({'Ending Date': {"$gt" : t1 ,"$lt" :t2},"Action":{"$in":actions}}):
            results.append(log)
        return results
    
    elif period =='full':

        for log in logs.find({'Begin Date': {"$gt" : t1 ,"$lt" :t2},'Ending Date': {"$gt" : t1 ,"$lt" :t2},"Action":{"$in":actions}}):
            results.append(log)
        return results
        
def getCategory(logs, categ,actions):
    '''
        Obtenir tous les événements des items d'une Catégorie et en fonction d'une liste d'actions
    '''
    results = []
    for r in logs.find({'Category': categ,"Action":{"$in":actions}}):
        results.append(r)
    return results

def getFunction(logs, funct,actions):
    '''
        Obtenir tous les événements qui effectuent une Function et en fonction d'une liste d'actions
    '''
    results = []
    for r in logs.find({'Function': funct,"Action":{"$in":actions}}):
        results.append(r)
    return results

def getCommand(logs, comm,actions):
    '''
        Obtenir tous les événements qui effectuent une Commande et en fonction d'une liste d'actions
    '''
    results = []
    for r in logs.find({'Command': comm,"Action":{"$in":actions}}):
        results.append(r)
    return results

def getAllExistingCategories(collection):
    '''
        Obtenir toutes les categories d'une collection
    '''
    results = collection.distinct( "Category" )
    return results

def getAllIdFromCategory(collection,categ):
    '''
        Obtenir tous les Id appartenant à une category
    '''
    results = collection.distinct( "Id",{ "Category": categ })
    return results

def getAllExistingActions(collection):
    '''
        Obtenir toutes les actions d'une collection
    '''
    results = collection.distinct( "Action" )
    return results

def getAll(collection,limit=None):
    '''
        Obtenir tout d'une collection avec un tri sur Ending Date en decroissant
        possibilité d'avoir une quantité limité de résultats
    '''
    if limit==None:
        results = collection.find({}).sort([("Ending Date", pymongo.DESCENDING)])
    else:
        results = collection.find({}).sort([("Ending Date", pymongo.DESCENDING)]).limit(limit)
    return results