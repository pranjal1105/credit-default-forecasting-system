import pandas as pd
import numpy as np
import os

# PATHS
forecast_path = r"E:\DV Data Science\credit-default-forecasting-system\data\forecasts\default_rate_forecast.csv"

actual_path = r"E:\DV Data Science\credit-default-forecasting-system\data\processed\monthly_default_rate_cleaned.csv"

monitoring_path = r"E:\DV Data Science\credit-default-forecasting-system\data\monitoring\forecast_monitoring.csv"


# LOAD FORECASTS
forecast_df = pd.read_csv(forecast_path)

# rename interval columns
forecast_df = forecast_df.rename(columns={
    "lower bound 95%": "lower_95",
    "upper bound 95%": "upper_95"
})

forecast_df["forecast_date"] = pd.to_datetime(forecast_df["forecast_date"])


# LOAD ACTUAL DATA
actual_df = pd.read_csv(actual_path)

actual_df["issue_month"] = pd.to_datetime(actual_df["issue_month"])

actual_df = actual_df[["issue_month", "default_rate"]]

actual_df = actual_df.rename(columns={
    "issue_month": "date",
    "default_rate": "actual"
})


# PREPARE FORECAST DATA
forecast_df = forecast_df.rename(columns={
    "forecast_date": "date",
    "forecast_default_rate": "forecast"
})


# MERGE
merged_df = pd.merge(
    forecast_df,
    actual_df,
    on="date",
    how="inner"
)


# CALCULATE ERROR
merged_df["error"] = merged_df["actual"] - merged_df["forecast"]


# CHECK PREDICTION INTERVAL
merged_df["inside_interval"] = (
    (merged_df["actual"] >= merged_df["lower_95"]) &
    (merged_df["actual"] <= merged_df["upper_95"])
)


# SAVE MONITORING DATA
os.makedirs(os.path.dirname(monitoring_path), exist_ok=True)

merged_df.to_csv(monitoring_path, index=False)


# CALCULATE METRICS
mae = np.mean(np.abs(merged_df["error"]))

rmse = np.sqrt(np.mean(merged_df["error"]**2))

bias = np.mean(merged_df["error"])


print("Forecast Monitoring Metrics")
print("---------------------------")
print(f"MAE  : {mae:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"Bias : {bias:.6f}")