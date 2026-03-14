import pandas as pd
import numpy as np

# def get_rmse(y_actual,y_pred):
#     return np.sqrt(np.mean((y_actual-y_pred)**2))

# def get_mae(y_actual,y_pred):
#     return np.mean(abs(y_actual-y_pred))

# def get_mape(y_actual,y_pred):
#     return np.mean(abs(y_actual-y_pred)/y_actual)

def evaluate_model(y_actual,y_pred):
    print(f"D TYPE OF {y_actual}: {y_actual.dtype}")
    print(f"D TYPE OF {y_pred}: {y_pred.dtype}")
    rmse=np.sqrt(np.mean((y_actual-y_pred)**2))
    mae=np.mean(abs(y_actual-y_pred))
    mape=np.mean(abs(y_actual-y_pred)/y_actual)
    return rmse,mae,mape