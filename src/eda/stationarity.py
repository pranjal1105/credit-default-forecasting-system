from statsmodels.tsa.stattools import adfuller

def run_adf_test(series):
    result = adfuller(series.dropna())
    return {
        "adf_statistic": result[0],
        "p_value": result[1],
        "critical_values": result[4]
    }