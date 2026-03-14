import pandas as pd
import numpy as np

def create_lag_features(series, lag=12):
    df=pd.DataFrame({"Target":series})

    for i in range(lag):
        df[f"lag_{i+1}"]=df["Target"].shift(i+1)
    df['roll_mean3']=df['Target'].shift(1).rolling(3).mean()
    df['roll_mean6']=df['Target'].shift(1).rolling(6).mean()
    df['roll_std6']=df['Target'].shift(1).rolling(6).std()
    df=df.dropna()
    return df