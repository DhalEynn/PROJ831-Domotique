from matplotlib import pyplot
from pandas import DataFrame
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import Analysis as an

def arimaPrediction():
    series = pd.Series(an.action_to_list('ROLLINGSHUTTER',5, 10000)[1][:1000])
    X = series.values
    series.plot()
    pyplot.show()
    size = int(len(X) * 0.85)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    # plot
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()