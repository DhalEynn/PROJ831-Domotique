import pymongo
def getItem(logs, categ, Id,actions,limit=None,sort=False):
    '''
        Obtenir tous les événements d'un item défini par une Catégorie, un ID et une liste d'action
        si limit est fixé retourne les limi premiers éléments
    '''
    results = []
    req = logs.find({"Category": categ, "Id" : Id,  "Action":{"$in":actions}})

    if limit !=None:
        req = req.limit(limit)
    if sort==True:
        req = req.sort([('Ending Date',pymongo.DESCENDING)])

    for log in req:
        results.append(log)
    return results

def getDate(logs, period, t1, t2,actions,limit=None):
    '''
        Obtenir tous les événements dans un intervalle [t1, t2] et en fonction d'une liste d'actions

        Si Period = begin(resp. end) -> Renvoie les événements tels que t1 < Begin(resp. Ending) Date < t2
        Si Period = full -> Renvoie les événements tels que t1 < Begin Date et End Date < t2
    '''
    results = []

    if period =='begin':
        req = logs.find({'Begin Date': {"$gt" : t1 ,"$lt" :t2},"Action":{"$in":actions}})
        if limit !=None:
            req = req.limit(limit)
        for log in req: 
            results.append(log)
        return results
    
    elif period =='end':
        req = logs.find({'Ending Date': {"$gt" : t1 ,"$lt" :t2},"Action":{"$in":actions}})
        if limit !=None:
            req = req.limit(limit)
        for log in req:
            results.append(log)
        return results
    
    elif period =='full':
        req = logs.find({'Begin Date': {"$gt" : t1 ,"$lt" :t2},'Ending Date': {"$gt" : t1 ,"$lt" :t2},"Action":{"$in":actions}})
        if limit !=None:
            req = req.limit(limit)
        for log in req:
            results.append(log)
        return results
        
def getCategory(logs, categ,actions,limit=None,sort=False):
    '''
        Obtenir tous les événements des items d'une Catégorie et en fonction d'une liste d'actions
    '''
    results = []
    req = logs.find({'Category': categ,"Action":{"$in":actions}})

    if limit !=None:
        req = req.limit(limit)
    if sort==True:
        req = req.sort([('Ending Date',pymongo.DESCENDING)])

    for r in req:
        results.append(r)
    return results

def getFunction(logs, funct,actions,limit=None,sort=False):
    '''
        Obtenir tous les événements qui effectuent une Function et en fonction d'une liste d'actions
    '''
    results = []
    req = logs.find({'Function': funct,"Action":{"$in":actions}})

    if limit !=None:
        req = req.limit(limit)
    if sort==True:
        req = req.sort([('Ending Date',pymongo.DESCENDING)])

    for r in req:
        results.append(r)
    return results

def getCommand(logs, comm,actions,limit=None,sort=False):
    '''
        Obtenir tous les événements qui effectuent une Commande et en fonction d'une liste d'actions
    '''
    results = []
    req =logs.find({'Command': comm,"Action":{"$in":actions}})

    if limit !=None:
        req = req.limit(limit)
    if sort==True:
        req = req.sort([('Ending Date',pymongo.DESCENDING)])

    for r in req:
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
        Obtenir toutes les Ids appartenant à une catégorie
    '''
    results = collection.distinct( "Id",{ "Category": categ })
    return results

def getAllExistingActions(collection):
    '''
        Obtenir toutes les actions d'une collection
    '''
    results = collection.distinct( "Action" )
    return results

def getAll(collection,limit=None,sort=False):
    '''
        Obtenir tout d'une collection avec un tri sur Ending Date en decroissant
    '''
    req = collection.find({})
    if limit !=None:
        req = req.limit(limit)
    if sort==True:
        req = req.sort([('Ending Date',pymongo.DESCENDING)])

    results = req
    return results

def getChart(analysis, chart_type, categ, Id):
    req = analysis.find_one({"Category": categ, "Id" : Id,  "chart_type": chart_type})
    return req