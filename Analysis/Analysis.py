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

def lastObjectFreq(category,ID, time):
    logs = connectDB.connectToCollection('logs2')
    list_actions = getData.getItem(logs, category, ID, ['EDGE RUNNED'])
    dico_frequency = {}
    nb_actions = len(list_actions)
    for action in list_actions:
        previous_action = getData.getDate(logs, 'begin', action['Begin Date'], action['Begin Date'] + time, ['EDGE RUNNED'])
        past_action = []
        for p_action in previous_action:
            
            category_action = p_action['Category']
            id_action = p_action['Id']
            comande_action = p_action['Function']
            if [category_action,id_action] not in past_action:
                past_action.append([category_action,id_action])
                if ( dico_frequency.get(category_action, {}).get(id_action, {}).get(comande_action) ):
                    dico_frequency[category_action][id_action][comande_action] += 1

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
    logs = connectDB.connectToCollection('logs')
    list_action = getData.getItem(logs, category, ID, ['EDGE RUNNED'])
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
    return [time,etat]

def list_to_graph(list_action):         
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list_action[0], y=list_action[1],
                    mode='lines+markers',
                    name='lines+markers'))
    fig.show()

    
    
    
def frequence(time,list_etat, transition):
    i = 1
    time_debut = 0
    time_fin = 0
    nb = 0
    somme = 0
    while i < len(list_etat):
        if list_etat[i] != list_etat[i-1]:
            if  transition == list_etat[i] - list_etat[i-1]:
                time_debut = time[i]
                #print("time_debut = ", time_debut)
            else:
                time_fin = time[i]
                #print("time_fin = ", time_fin)
                somme += (time_fin - time_debut)
                nb += 1
        i += 1
    #print(somme/nb)
    return(somme/nb) 


def period(list_etat):
    onPeriodList = [] 
    offPeriodList = []
    onPeriod = 0
    offPeriod = 0
    if list_etat[0] == 1:
        onPeriod = 1
    else :
        offPeriod = 1
    for i in range (len(list_etat)):
        while i < len(list_etat):
            if list_etat[i] == 0:
                if list_etat[i] != list_etat[i-1]:
                    onPeriodList.append(onPeriod)
                    onPeriod = 0

                else:
                    onPeriod+=1

            else:
                if list_etat[i] != list_etat[i-1]:
                    offPeriodList.append(offPeriod)
                    offPeriod = 0
                else:
                    offPeriod+=1






def correlation():
    logs = connectDB.connectToCollection('logs')
    categories = getData.getAllExistingCategories(logs)
    data ={}
    df = pd.DataFrame(data)
    maxSize = 240000
    for category in categories:
        ids = getData.getAllIdFromCategory(logs,category)
        for id_c in ids:
            a =action_to_list(category,int(id_c),float('inf'))[1]

            df[category+ ' ' + str(id_c)]= a[0:maxSize]
        print(df)
    corr = df.corr()
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


#f1 = action_to_list('ROLLINGSHUTTER',5, 10000)[1]
#f2 = action_to_list('HEATER',6,10000)[1]

#print(correlation())


