from pandas import DataFrame
import pandas as pd
import Analysis as analysis


def prediction(time, list_state, duration):
    """
    Takes the time for a function to go on or off.
    Then continues the function, as soon as the time spent in a state exceeds the average time, the state changes and so on.
    Duration Defines the period of time over which we will make predictions.
    """
    periode_off = analysis.mean_time([time,list_state], -1)
    periode_on = analysis.mean_time([time,list_state], 1)
    i = 1
    # we retrieve the last state change and the time at which it occurred.
    while i<len(list_state):
        if list_state[i] != list_state[i-1]:
            last_transition = list_state[i] - list_state[i-1]
            last_time = time[i]
        i += 1
    next_state=list_state[-1]
    # we calculate how much time is left in the current state.
    if last_transition == 1:
        time_to_transition = periode_on - (time[-1] - last_time)
    else:
        time_to_transition = periode_off - (time[-1] - last_time) 
    i=0 
    while i < duration:
        time += [time[-1] + 1]
        list_state += [next_state]
        time_to_transition = time_to_transition -1
        #  we change the next state and recalculate the average time to the next transition.
        if time_to_transition <= 0:
            if next_state == 1:
                next_state = 0
                time_to_transition = periode_off
            elif next_state == 0:
                next_state = 1
                time_to_transition = periode_on
        i += 1
    return ([time, list_state])

def periodPrediction(list_state, duration, list_activation, period):
    """
    Predict the n next states of a periodic function according to the most used state on the lasts periods
    the number of times a state was resenced for each time unit
    list_state: the list of previous states, used as training data
    duration: n next states to predict
    list_activation: list containing the number of  activation of each state at each periodic time unit
    period: length of a period
    """
    time_start = list_state[0][-1]
    # print(len(list_activation[1]))
    for i in range(1, duration):
        list_state[0] += [time_start + i]
        hours = (time_start + i) % period
        # print(hours)
        max_value = 0
        state_id = -1
        # we're looking for the most used state at the given time.
        for state in list_activation[1][hours].keys():
            if list_activation[1][hours][state] > max_value:
                max_value = list_activation[1][hours][state]
                state_id = state
        if state_id == -1:
            print('error unexpected state id')
            return None
        # we predict the most common state.
        list_state[1] += [state_id]
    return list_state


# Prediction exemple with 5000 training data and 10 000 predicted data
# liste_action = analysis.action_to_list('LIGHT',1, 5000)
# list_activation = analysis.activation_per_period(liste_action, 5000, 1440)

# choose the prediction method you want to use
# predictions = periodPrediction(liste_action, 10000, list_activation, 1440)
# predictions = prediction(liste_action[0], liste_action[1], 10000)

# analysis.list_to_graph(predictions)
# liste_action = analysis.action_to_list('LIGHT',1, 15000)
# analysis.list_to_graph(liste_action)

# liste_action = analysis.action_to_list('LIGHT',1, 15000)
# analysis.list_to_graph(liste_action)
# mean_squared_error(liste_action, predictions)

# # real data
# liste_action = analysis.action_to_list('LIGHT',1, 15000)
# analysis.list_to_graph(liste_action)
