import sys
sys.path.append('../')
import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns

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
    temps = [0]
    etat = [0]
    i = 0
    for action in list_action:
        if temps[-1] > maxTime:
            break
        while len(temps)< action['Begin Date']:
            if temps[-1] > maxTime:
                break
            temps += [i]
            i += 1
            etat.append(etat[-1])
        temps += [i]
        i += 1
        etat += [int(action['Ending State'][1])]
    return [temps,etat]

def list_to_graph(list_action):         
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list_action[0], y=list_action[1],
                    mode='lines+markers',
                    name='lines+markers'))
    fig.show()

def prevision(time, list_etat, duree):
    periode_off = frequence(time,list_etat, -1)
    periode_on = frequence(time,list_etat, 1)
    i = 1
    while i<len(list_etat):
        if list_etat[i] != list_etat[i-1]:
            last_transition = list_etat[i] - list_etat[i-1]
            last_time = time[i]
        i += 1
    next_etat=etat[i]
    if last_transition == 1:
        time_to_transition = periode_on - (time[i] - last_time)
    else:
        time_to_transition = periode_on - (time[i] - last_time)  
    i=0 
    while i < duree:
        time += [time[-1] + 1]
        etat += next_etat
        time_to_transition += -1
        if time_to_transition <= 0:
            if next_etat == 1:
                next_etat = 0
                time_to_transition = periode_off
            if next_etat == 0:
                next_etat = 1
                time_to_transition = periode_on
        i += 1
    return (time, list_etat)
    
    
    
    def frequence(time,list_etat, transition):
        i = 1
        time_debut = 0
        time_fin = 0
        nb = -1
        somme = 0
        while i < len(list_etat):
            if list_etat[i] != list_etat[i-1]:
                if  transition == list_etat[i] - list_etat[i-1]:
                    time_debut = time[i]
                else:
                    time_fin = time[i]
                    somme += (time_fin - time_debut)
                    nb += 1
            i += 1
        return(somme/nb) 







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


f1 = action_to_list('ROLLINGSHUTTER',5, 10000)[1]
f2 = action_to_list('HEATER',6,10000)[1]

print(correlation())

