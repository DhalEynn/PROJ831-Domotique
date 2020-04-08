from matplotlib import pyplot
from pandas import DataFrame
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import Analysis as an



def arimaPrediction():
    series = pd.Series(an.action_to_list('SWITCH',7, 3000)[1])
    X = series.values
    series.plot()
    pyplot.show()
    size = int(len(X) * 0.60)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = [round(output[0][0])]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    # plot
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()

def prevision(time, list_etat, duree):
    periode_off = an.frequence(time,list_etat, -1)
    periode_on = an.frequence(time,list_etat, 1)
    i = 1
    while i<len(list_etat):
        if list_etat[i] != list_etat[i-1]:
            last_transition = list_etat[i] - list_etat[i-1]
            last_time = time[i]
        i += 1
    next_etat=list_etat[-1]
    if last_transition == 1:
        time_to_transition = periode_on - (time[-1] - last_time)
    else:
        time_to_transition = periode_off - (time[-1] - last_time) 
    i=0 
    while i < duree:
        time += [time[-1] + 1]
        list_etat += [next_etat]
        time_to_transition = time_to_transition -1
        if time_to_transition <= 0:
            if next_etat == 1:
                next_etat = 0
                time_to_transition = periode_off
            elif next_etat == 0:
                next_etat = 1
                time_to_transition = periode_on
        i += 1
    return ([time, list_etat])
    liste_action = an.action_to_list('LIGHT',1, 5000)


liste_action = an.action_to_list('LIGHT',1, 5000)
an.list_to_graph(liste_action)
predictions = prevision(liste_action[0], liste_action[1], 10000)
an.list_to_graph(predictions)

liste_action = an.action_to_list('LIGHT',1, 15000)
an.list_to_graph(liste_action)
mean_squared_error(liste_action, predictions)
