import sys
sys.path.append('../')
import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot

def lastObjectFreq(category,ID, time):
    """
    calcul la frequence d'apparition de tout les objet avant l'action de l'objet donné dans la période time.
    """
    logs = connectDB.connectToCollection('logs')
    # on récupère toute les actions d'un objet
    list_actions = getData.getItem(logs, category, ID, ['EDGE RUNNED'])
    dico_frequency = {}
    nb_actions = len(list_actions)
    # on parcours les actions 
    for action in list_actions:
        # on récupère toute les actions précédents notre action
        previous_action = getData.getDate(logs, 'begin', action['Begin Date'], action['Begin Date'] + time, ['EDGE RUNNED'])
        past_action = []
        # on parcours toutes les actions précédentes
        for p_action in previous_action:
            
            category_action = p_action['Category']
            id_action = p_action['Id']
            comande_action = p_action['Function']
            #si on a pas déjà rajouté l'action à notre dictionnaire on la rajoute
            if [category_action,id_action] not in past_action:
                past_action.append([category_action,id_action])
                #si la clé existe déjà on incrémente le conteur
                if ( dico_frequency.get(category_action, {}).get(id_action, {}).get(comande_action) ):
                    dico_frequency[category_action][id_action][comande_action] += 1
                #sinon on créer la clé
                elif category_action  not in dico_frequency.keys():
                    dico_frequency[category_action]={id_action:{comande_action: 1}}

                elif id_action not in dico_frequency[category_action].keys():
                    dico_frequency[category_action][id_action] = {comande_action: 1}
                else:
                    dico_frequency[category_action][id_action][comande_action] = 1

    return(dico_frequency , nb_actions)

def graphLastObjectFreq(dict_frequency, nb_actions):
    list_object=[]
    list_objet_frequency = []
    for key_category in dict_frequency.keys():
        for key_id in dict_frequency[key_category].keys():
            nb = 0
            for key_comande in dict_frequency[key_category][key_id].keys():
                nb += dict_frequency[key_category][key_id][key_comande]
            list_object += [key_category + str(key_id)]
            list_objet_frequency += [nb/nb_actions]
    fig = px.bar(x=list_object, y=list_objet_frequency)
    fig.show()


def action_to_list(category,ID, maxTime):
    """
    créer une liste des etat en fonction du temps, pour un objet données.
    maxTime sert a limiter la quantité de données à traiter.
    """
    logs = connectDB.connectToCollection('logs')
    list_action = getData.getItem(logs, category, ID, ['EDGE RUNNED']) #récupére tout les action d'un objet
    time = [0]
    etat = [0]
    i = 0
    for action in list_action:
        if time[-1] > maxTime:
            break
        while len(time)< action['Begin Date']:
            if time[-1] > maxTime:
                break
            time += [i]
            i += 1
            etat.append(etat[-1])
        if time[-1] <= maxTime:
            time += [i]
            i += 1
            etat += [int(action['Ending State'][1])]
    return [time,etat] #on retourne une liste contenant, une liste de temps et une liste d'état.

def list_to_graph(list_action):
    """
    plot the graph of one object (state value according to time)
    """         
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list_action[0], y=list_action[1],
                    mode='lines+markers',
                    name='lines+markers'))
    fig.show()

    
    

def mean_time(time,list_etat, transition):
    """
    calcul le temps moyen qu'une fonction passe dans l'etat on ou off.
    -1 pour off. 1 pour on.
    """   
    i = 1
    time_debut = -1
    time_fin = 0
    nb = 0
    somme = 0
    while i < len(list_etat):
        if list_etat[i] != list_etat[i-1]:
            if  transition == list_etat[i] - list_etat[i-1]:
                time_debut = time[i]
                #print("time_debut = ", time_debut)
            elif(time_debut != -1):
                time_fin = time[i]
                #print("duree =  ", time_fin - time_debut)
                somme += (time_fin - time_debut)
                nb += 1
        i += 1
    #print(somme/nb)
    return(somme/nb) 


def period(list_state):
    """ 
    Calculate the period between 2 on state and the period between 2 off state
    list_state: list with all the states
    return: the list of all on period and the list of all off period
    """
    onPeriodList = [] 
    offPeriodList = []
    onPeriod = 0
    offPeriod = 0
    if list_state[0] == 1:
        onPeriod = 1
    else :
        offPeriod = 1
    # browse through list_state and increment onPeriod and offPeriod when it is needed
    for i in range (len(list_state)):
        if list_state[i] == 0:
            # if the state change, save the value of onPeriod and then set it to 0
            if list_state[i] != list_state[i-1]:
                onPeriodList.append(onPeriod)
                onPeriod = 0

            else:
                onPeriod+=1

        else:
            # if the state change, save the value of offPeriod and then set it to 0
            if list_state[i] != list_state[i-1]:
                offPeriodList.append(offPeriod)
                offPeriod = 0
            else:
                offPeriod+=1
    on = pd.Series(onPeriodList)
    off = pd.Series(offPeriodList)
    pyplot.plot(on)
    pyplot.plot(off,color='red')  
    return(onPeriodList, offPeriodList)






def correlation(maxSize):
    """ 
    return the correlation matrix of all the objects
    maxSize: the maximum size of the dataframe, (if it is too high it may create collumns with differents sizes and create a bug) 
    """
    # get the logs
    logs = connectDB.connectToCollection('logs')
    categories = getData.getAllExistingCategories(logs)
    data ={}
    # build a dataframe with each column being a unique category,id couple
    df = pd.DataFrame(data)
    for category in categories:
        ids = getData.getAllIdFromCategory(logs,category)
        for id_c in ids:
            a =action_to_list(category,int(id_c),float('inf'))[1]

            df[category+ ' ' + str(id_c)]= a[0:maxSize]
    # create the correlation matrix
    corr = df.corr()
    # plot it
    ax = sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right'
    );


f1 = action_to_list('ROLLINGSHUTTER',5, 10000)
list_to_graph(f1)
#f2 = action_to_list('HEATER',6,10000)[1]
#mean_time(f1[0], f1[1], 1)
#print(correlation())


