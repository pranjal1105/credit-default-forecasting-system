import pandas as pd
import numpy as np

def walk_forward_forecast(series, train_end, model_function, forecast_function, model_params=None):

    if model_params is None:
        model_params = {}

    train = series[:train_end]
    test = series[train_end:]

    history = list(train)
    predictions = []

    for i in range(len(test)):

        model = model_function(history, **model_params)

        predicted_value = forecast_function(model, history)

        predictions.append(predicted_value)

        history.append(test.iloc[i])
    predictions=pd.Series(predictions,index=test.index)
    return test, predictions