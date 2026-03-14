def add_rolling_features(df, column, windows=[3,6]):
    for w in windows:
        df[f"{column}_rolling_mean_{w}"] = df[column].rolling(w).mean()
        df[f"{column}_rolling_std_{w}"] = df[column].rolling(w).std()
    return df