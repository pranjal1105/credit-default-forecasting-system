import pandas as pd
from src.models import xgboost_model as xm
from dateutil.relativedelta import relativedelta
import os

from src.uncertainity.prediction_intervals import calculate_prediction_interval

# LOAD THE DATASET
monthly_default_rate_cleaned = pd.read_csv(
    r"E:\DV Data Science\credit-default-forecasting-system\data\processed\monthly_default_rate_cleaned.csv"
)

monthly_default_rate_cleaned["issue_month"] = pd.to_datetime(
    monthly_default_rate_cleaned["issue_month"]
)

monthly_default_rate_cleaned = monthly_default_rate_cleaned.set_index("issue_month")

# Take only last 8 years of data for training
last_date = monthly_default_rate_cleaned.index.max()
start_date = last_date - relativedelta(years=8)

training_data = monthly_default_rate_cleaned[
    monthly_default_rate_cleaned.index >= start_date
]

history = training_data["default_rate"]

# Train the model
model = xm.xgb_train(history)

# Forecast
forecast = xm.xgb_forecast(model, history)

forecast_date = history.index[-1] + relativedelta(months=1)

#Import Residuals
residuals=pd.read_csv(r"E:\DV Data Science\credit-default-forecasting-system\data\processed\residuals.csv")

#get lower bound and upper bound for forecasted value
lower_bound, upper_bound=calculate_prediction_interval(forecast,residuals["residuals"])

# Create forecast dataframe
df = pd.DataFrame({
    "forecast_date": [forecast_date.strftime("%Y-%m-%d")],
    "forecast_default_rate": [forecast],
    "lower bound 95%": [lower_bound],
    "upper bound 95%":[upper_bound]
})

print(df)

forecast_path = r"E:\DV Data Science\credit-default-forecasting-system\data\forecasts\default_rate_forecast.csv"

# Ensure folder exists
os.makedirs(os.path.dirname(forecast_path), exist_ok=True)

# Check if forecast file exists
if os.path.exists(forecast_path):

    existing_df = pd.read_csv(forecast_path)

    updated_df = pd.concat([existing_df, df], ignore_index=True)

    updated_df.to_csv(forecast_path, index=False)

else:

    df.to_csv(forecast_path, index=False)