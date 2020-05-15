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

def lastObjectFreq(category,object_id, time):
    """
    calculates the frequency of occurrence of all objects before the action of the given object in the time period.
    category: category of the object
    object_id: id of the object
    time: time period in which we will check the occurence of other objects
    """
    logs = connectDB.connectToCollection('logs4')
    # retrieve all the actions of an object
    action_lists = getData.getItem(logs, category, object_id, ['EDGE RUNNED'])
    dico_frequency = {}
    nb_actions = len(action_lists)
    # go through the actions
    for action in action_lists:
        # we get back all the actions that preceded our action
        previous_action = getData.getDate(logs, 'begin', action['Begin Date'], action['Begin Date'] + time, ['EDGE RUNNED'])
        past_action = []
        # we go through all the previous actions
        for p_action in previous_action:
            
            action_category = p_action['Category']
            action_id = p_action['Id']
            action_command = p_action['Function']
            # if we haven't already added the action to our dictionary, we'll add it.
            if [action_category,action_id] not in past_action:
                past_action.append([action_category,action_id])
                # if the key already exists we increment the counter
                if ( dico_frequency.get(action_category, {}).get(action_id, {}).get(action_command) ):
                    dico_frequency[action_category][action_id][action_command] += 1
                # otherwise we create the key
                elif action_category  not in dico_frequency.keys():
                    dico_frequency[action_category]={action_id:{action_command: 1}}

                elif action_id not in dico_frequency[action_category].keys():
                    dico_frequency[action_category][action_id] = {action_command: 1}
                else:
                    dico_frequency[action_category][action_id][action_command] = 1

    return(dico_frequency , nb_actions)

def graphLastObjectFreq(dict_frequency, nb_actions):
    """
    create the barchart for our lastObjectFreq function
    dict_frequency: trhe dictionnary with the frequency of each object (given by lastObjectFreq())
    nb_actions: number of actions
    """
    list_object=[]
    list_objet_frequency = []
    for key_category in dict_frequency.keys():
        for key_id in dict_frequency[key_category].keys():
            nb_action = 0
            for key_comande in dict_frequency[key_category][key_id].keys():
                nb_action += dict_frequency[key_category][key_id][key_comande]
            list_object += [key_category + str(key_id)]
            list_objet_frequency += [nb_action/nb_actions]
    fig = px.bar(x=list_object, y=list_objet_frequency)
    fig.update_layout(
        yaxis=dict(tickformat=".00%"),
        xaxis_title="State",
        yaxis_title="Activation",
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#7f7f7f"
    ))
    fig.show()
    return fig


def action_to_list(category, object_id, maxTime):
    """
    Create a time-based status list for a given object.
    category: category of the object
    object_id: id of the object
    maxTime: used to limit the amount of data to be processed.
    """
    logs = connectDB.connectToCollection('logs4')
    action_list = getData.getItem(logs, category, object_id, ['EDGE RUNNED']) # retrieves all the actions of an object
    time = [0]
    state = [0]
    i = 0
    for action in action_list:
        if time[-1] > maxTime:
            break
        while len(time)< action['Begin Date']:
            if time[-1] > maxTime:
                break
            time += [i]
            i += 1
            state.append(state[-1])
        if time[-1] <= maxTime:
            time += [i]
            i += 1
            state += [int(action['Ending State'][1])]
    return [time,state] # return a list containing, a time list and a status list.

def list_to_graph(action_list):
    """
    plot the graph of one object (state value according to time)
    """         
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=action_list[0], y=action_list[1],
                    mode='lines+markers',
                    name='lines+markers',))

    fig.update_layout(
        xaxis_title="State",
        yaxis_title="Time",
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#7f7f7f"
    ))
    fig.show()

    
    

def mean_time(state_list, transition):
    """
    calculates the average time a function spends in the on or off state.
    -1 for off. 1 for on.
    state_list:
    transition: 
    """   
    i = 1
    begin_time = -1
    end_time = 0
    nb_action = 0
    total_duration = 0
    while i < len(state_list[1]):
        if state_list[1][i] != state_list[1][i-1]:
            if  transition == state_list[1][i] - state_list[1][i-1]:
                begin_time = state_list[0][i]
                #print("begin_time = ", begin_time)
            elif(begin_time != -1):
                end_time = state_list[0][i]
                #print("duration =  ", end_time - begin_time)
                total_duration += (end_time - begin_time)
                nb_action += 1
        i += 1
    #print(total_duration/nb_action)
    return(total_duration/nb_action) 


def fullPeriodGraph(state_list):
    """ 
    Calculate the period between 2 on state and the period between 2 off state
    state_list: list with all the states
    return: the list of all on period and the list of all off period
    """
    onPeriodList = [] 
    offPeriodList = []
    onPeriod = 0
    offPeriod = 0
    if state_list[1][0] == 1:
        onPeriod = 1
    else :
        offPeriod = 1
    # browse through state_list and increment onPeriod and offPeriod when it is needed
    for i in range (len(state_list[1])):
        if state_list[1][i] == 0:
            # if the state change, save the value of onPeriod and then set it to 0
            if state_list[1][i] != state_list[1][i-1]:
                onPeriodList.append(onPeriod)
                onPeriod = 0

            else:
                onPeriod+=1

        else:
            # if the state change, save the value of offPeriod and then set it to 0
            if state_list[1][i] != state_list[1][i-1]:
                offPeriodList.append(offPeriod)
                offPeriod = 0
            else:
                offPeriod+=1
    on = pd.Series(onPeriodList)
    off = pd.Series(offPeriodList)
    color1 = 'green'
    color2 = 'red'

    trace1 = go.Bar(
        x = on.index,
        y = on.values,
        name='on period',

    )
    trace2 = go.Bar(
        x= off.index,
        y =off.values,
        name='off period',

    )
    data = [trace1, trace2]

    fig = go.Figure(data=data)
    fig.update_layout(
        yaxis_title ="Length",
        xaxis_title ="Period n°",
        barmode='group'
        )
    fig.show()




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

def activation_per_period(state_list, maxSize, period):
    """
    Return a list containing the number of  activation of each state at each periodic time unit
    state_list: list with all the states
    maxSize: the maximum size of the list
    period: length of the period to consider
    """
    # initialise our result array
    list_activation = [list(range(period)), [{}]*period]
    # determine the iteration size 
    itSize = min(maxSize,len(state_list[1]))
    for i in range(itSize):
        # end the for if we can't finish a period with the remaining states
        if i % period == 0 and itSize < i + period :
            break
        # count ,for each time in a period, how many time the state was on

        if state_list[1][i] in list_activation[1][i%period].keys():
            list_activation[1][i%period][state_list[1][i]] += 1 
        else:
            list_activation[1][i%period] = {state_list[1][i]: 1}
    return list_activation

# f1 = action_to_list('ROLLINGSHUTTER',5, 10000)
# f = frequence_activation_minute(f1, 5000, 1440)

# f2 = action_to_list('ROLLINGSHUTTER',25,10000)
# fullPeriodGraph(f2)
# list_to_graph(f2)

# mean_time(f1[0], f1[1], 1)
# print(correlation())