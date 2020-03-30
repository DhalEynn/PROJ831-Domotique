def getItem(categ, Id):
    '''
        Obtenir tous les événements d'un item défini par une Catégorie un ID
    '''
    results = []
    for log in logs.find({"Category": categ, "Id" : Id}):
        results.append(log)
    return results

def getDate(period, t1, t2):
    '''
        Obtenir tous les événements dans un intevalle [t1, t2]

        Si Period = begin(resp. end) -> Renvoie les events tel que t1 < Begin(resp. Ending) Date < t2
        Si Period = full -> Renvoie les events tel que t1 < Begin Date et End Date < t2
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
    '''
        Obtenir tous les événements des item d'une Catégorie
    '''
    results = []
    for r in logs.find({'Category': categ}):
        results.append(r)
    return results

def getFunction(funct):
    '''
        Obtenir tous les événements qui effectue une Function
    '''
    results = []
    for r in logs.find({'Function': funct}):
        results.append(r)
    return results

def getCommand(comm):
    '''
        Obtenir tous les événements qui effectue une Commande
    '''
    results = []
    for r in logs.find({'Command': comm}):
        results.append(r)
    return results
