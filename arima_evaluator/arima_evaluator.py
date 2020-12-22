import statsmodels as sm
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from data import data

import warnings

warnings.filterwarnings("ignore")

oil_data = data()


def eval_arima_model(X, arima_order):
    # prepare training dataset
    train_size = int(len(X) * 0.80)
    train, test = X[0:train_size], X[train_size:]
    history = train
    # make predictions
    predictions = list()
    for t in range(len(test)):
        print(str(t + 1), end=' ')
        model = sm.tsa.arima_model.ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    error = mean_squared_error(test, predictions)
    return error


def eval_models(dataset, p_values, d_values, q_values):
    print()
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p, d, q)
                print("Testing ARIMA " + str(order))
                try:
                    mse = eval_arima_model(dataset, order)
                    if mse < best_score:
                        best_score, best_cfg = mse, order
                    print()
                    print('MSE = ' + str(mse))
                except:
                    continue
    print('Best ARIMA is')
    print(best_cfg)
    print('MSE=%.3f' % best_score)


meow = int(len(oil_data) * 0.8)
meow = len(oil_data[meow:])
print('Testing Predictions for ' + str(meow) + ' days.')
eval_models(oil_data, [1], [1], [9])
