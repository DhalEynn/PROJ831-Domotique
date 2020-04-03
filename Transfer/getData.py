def getItem(logs, categ, Id,actions):
    '''
        Obtenir tous les événements d'un item défini par une Catégorie, un ID et une liste d'action
    '''
    results = []
    for log in logs.find({"Category": categ, "Id" : Id,  "Action":{"$in":actions}}):
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
