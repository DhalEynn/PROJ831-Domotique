from matplotlib import pyplot
from pandas import DataFrame
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import Analysis as an

#rip arima
"""
Arima, Arima, Arima, Arima,
Whou ou ou "Arima"
Whou ou ou "Arima"
Whou ou ou "Arima"
Whou ou ou "Arima"

Elle répondait au nom de Arima
L'erreur' ne voulaient pas la cher-lâ
Elle faisait trembler tous les villages
Les gens me disaient : "Méfie toi d'arima"
[x2]

C'était un phénomène, elle n'était pas humaine
Le genre de femme qui change le plus grand délinquant en gentleman

Une beauté sans pareille, tout le monde veut s'en emparer
Sans savoir qu'elle les mène en bateau
Hypnotisés, on pouvait tout donner
Elle n'avait qu'à demander puis aussitôt on démarrait
On cherchait à l'impressionner, à devenir son préféré
Sans savoir qu'elle les mène en bateau
Mais quand je la vois danser le soir
J'aimerais devenir la chaise sur laquelle elle s'assoit
Ou moins que ça, un moins que rien
Juste une pierre sur son chemin

Elle répondait au nom de Bella
Les gens du coin ne voulaient pas la cher-lâ
Elle faisait trembler tous les villages

Les gens me disaient : "Méfie toi d'arima'"
[x2]

Oui, c'est un phénomène qui aime hanter nos rêves
Cette femme était nommée, Bella la peau dorée
Les femmes la haïssaient, d'autres la jalousaient
Mais les hommes ne pouvaient que l'aimer
Elle n'était pas d'ici, ni facile, ni difficile
Synonyme de "magnifique", à ses pieds : que des disciples
Qui devenaient vite indécis, tremblants comme les feuilles
Elle te caressait sans même te toucher
Mais quand je la vois danser le soir
J'aimerai devenir la chaise sur laquelle elle s'assoit

Ou moins que ça, un moins que rien
Juste une pierre sur son chemin

Elle répondait au nom d'arima'
L'erreur ne voulaient pas la cher-lâ
Elle faisait trembler tous les villages
Les gens me disaient : "Méfie toi d'arima"
[x2]

Allez, fais moi tourner la tête (Hé-hé)
Tourner la tête (Héhé)
Rend moi bête comme mes ieds-p (Hé-hé)
Bête comme mes ieds-p (Héhé)
J'suis l'ombre de ton ien-ch (Hé-hé)
L'ombre de ton ien-ch (Héhé)
Fais moi tourner la tête (Hé-hé)
Tourner la tête (Héhé)

Fais moi tourner la tête (Hé-hé)
Tourner la tête (Héhé)
Rend moi bête comme mes ieds-p (Hé-hé)
Bête comme mes ieds-p (Héhé)
J'suis l'ombre de ton ien-ch (Hé-hé)
L'ombre de ton ien-ch (Héhé)
Fais moi tourner la tête (Hé-hé)
Tourner la tête (Héhé)

Elle répondait au nom d'arima
L'erreur ne voulaient pas la cher-lâ
Elle faisait trembler tous les villages
Les gens me disaient : "Méfie toi d'Arima"  
"""

#1440
def prediction(time, list_etat, duree):
    """
    Prend le temps qu'une fonction passe dans l'etat on ou off.
    Puis continue la fonction, des que le temps passé dans un état dépasse le temps moyen on change d'état et ainsi de suite.
    duree définis la periode sur laquelle on va faire des prevision.
    """
    periode_off = an.mean_time([time,list_etat], -1)
    periode_on = an.mean_time([time,list_etat], 1)
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
        # on change le prochain etat et on recalcul le temps moyen avant la transition suivant.
        if time_to_transition <= 0:
            if next_etat == 1:
                next_etat = 0
                time_to_transition = periode_off
            elif next_etat == 0:
                next_etat = 1
                time_to_transition = periode_on
        i += 1
    return ([time, list_etat])

def periodPrediction(list_state, duree, list_freq, period):
    time_start = list_state[0][-1]
    #print(len(list_freq[1]))
    for i in range(1, duree):
        list_state[0] += [time_start + i]
        hours = (time_start + i) % period
        #print(hours)
        list_state[1] += [round(list_freq[1][hours])]
    return list_state



liste_action = an.action_to_list('LIGHT',1, 5000)
#an.list_to_graph(liste_action)
#list_freq = an.frequence_activation_minute(liste_action, 5000, 1440)
#predictions = periodPrediction(liste_action, 10000, list_freq, 1440)
predictions = prediction(liste_action[0], liste_action[1], 10000)
an.list_to_graph(predictions)

liste_action = an.action_to_list('LIGHT',1, 15000)
an.list_to_graph(liste_action)
# mean_squared_error(liste_action, predictions)

