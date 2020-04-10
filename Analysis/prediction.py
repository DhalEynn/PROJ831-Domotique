from matplotlib import pyplot
from pandas import DataFrame
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import Analysis as an



#1440
def prevision(time, list_etat, duree):
    """
    Prend le temps qu'une fonction passe dans l'etat on ou off.
    Puis continue la fonction, des que le temps passé dans un état dépasse le temps moyen on change d'état et ainsi de suite.
    duree définis la periode sur laquelle on va faire des prevision.
    """
    periode_off = an.mean_time(time,list_etat, -1)
    periode_on = an.mean_time(time,list_etat, 1)
    i = 1
    #on récupére le dernier changement d'etat et le temps auquel il ce produit.
    while i<len(list_etat):
        if list_etat[i] != list_etat[i-1]:
            last_transition = list_etat[i] - list_etat[i-1]
            last_time = time[i]
        i += 1
    next_etat=list_etat[-1]
    #on calcul le temps qu'il reste dans l'etat en cours.
    if last_transition == 1:
        time_to_transition = periode_on - (time[-1] - last_time)
    else:
        time_to_transition = periode_off - (time[-1] - last_time) 
    i=0 
    while i < duree:
        time += [time[-1] + 1]
        list_etat += [next_etat]
        time_to_transition = time_to_transition -1
        #on change le prochain etat et on recalcul le temps moyen avant la transition suivant.
        if time_to_transition <= 0:
            if next_etat == 1:
                next_etat = 0
                time_to_transition = periode_off
            elif next_etat == 0:
                next_etat = 1
                time_to_transition = periode_on
        i += 1
    return ([time, list_etat])


# liste_action = an.action_to_list('LIGHT',1, 5000)
# an.list_to_graph(liste_action)
# predictions = prevision(liste_action[0], liste_action[1], 10000)
# an.list_to_graph(predictions)

# liste_action = an.action_to_list('LIGHT',1, 15000)
# an.list_to_graph(liste_action)
# mean_squared_error(liste_action, predictions)

