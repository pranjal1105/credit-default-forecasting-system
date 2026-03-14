import pandas as pd
import numpy as np

monthly_df=[]

chunk_size=200000
cols=['issue_d',"loan_status"]

for df in pd.read_csv(r"E:\DV Data Science\credit-default-forecasting-system\data\raw\loan.csv",usecols=cols,chunksize=chunk_size):
    df['issue_d']=pd.to_datetime(df['issue_d'],errors="coerce")
    df['default']=0
    df.loc[(df['loan_status'].isin(['Does not meet the credit policy. Status:Charged Off','Default','Charged Off'])),'default']=1
    df['issue_month']=df['issue_d'].dt.to_period("M").dt.to_timestamp()
    df=df.groupby("issue_month",as_index=False).agg(total_loans=('loan_status','count'),total_defaults=('default','sum'))
    
    monthly_df.append(df)

monthly_default_rate=pd.concat(monthly_df,ignore_index=True)
monthly_default_rate=monthly_default_rate.groupby("issue_month",as_index=False).agg(total_loans=('total_loans','sum'),total_defaults=('total_defaults','sum'))
monthly_default_rate["default_rate"]=monthly_default_rate['total_defaults']/monthly_default_rate["total_loans"]

monthly_default_rate.sort_values("issue_month",inplace=True)

monthly_default_rate=monthly_default_rate.set_index("issue_month")

full_range = pd.date_range(
    start=monthly_default_rate.index.min(),
    end=monthly_default_rate.index.max(),
    freq='MS'   # Month Start frequency
)

monthly_default_rate = monthly_default_rate.reindex(full_range)
monthly_default_rate=monthly_default_rate.reset_index()
monthly_default_rate.rename(columns={'index':'issue_month'},inplace=True)

monthly_default_rate[['total_loans','total_defaults','default_rate']]=monthly_default_rate[['total_loans','total_defaults','default_rate']].fillna(0)

monthly_default_rate.to_csv(
    r"E:\DV Data Science\credit-default-forecasting-system\data\processed\monthly_default_rate.csv",
    index=False
)

print(monthly_default_rate.head())
print("\nTotal Months:", len(monthly_default_rate))
print("Average Default Rate:", monthly_default_rate["default_rate"].mean())