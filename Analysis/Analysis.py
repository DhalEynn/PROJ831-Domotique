import sys
sys.path.append('../')
import env
import Transfer.connectDB as connectDB
import Transfer.getData as getData
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

def action_to_list(category,ID):
    logs = connectDB.connectToCollection('logs2')
    list_action = getData.getItem(logs, category, ID, ['EDGE RUNNED'])
    x = [0]
    y = [0]
    i = 0
    for action in list_action:

        while len(x)*10< action['Begin Date']:
            if x[-1] < 10000:
                break
            x += [i]
            i += 10
            y.append(y[-1])
        x += [i]
        i += 10
        y += [int(action['Ending State'][1])]
    return [x,y]

def list_to_graph(list_action):         
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list_action[0], y=list_action[1],
                    mode='lines+markers',
                    name='lines+markers'))
    fig.show()

