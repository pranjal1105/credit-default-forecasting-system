import pandas as pd
import numpy as np
def calculate_prediction_interval(forecast_value, residuals):
    predicted_intervals=residuals+forecast_value
    lower_bound=predicted_intervals.quantile(0.05)
    upper_bound=predicted_intervals.quantile(0.95)

    return lower_bound, upper_bound