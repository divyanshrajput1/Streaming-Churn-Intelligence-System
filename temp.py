import pandas as pd

df = pd.read_csv("data/processed.csv")
features = df.drop(["user_id", "churn", "churn_next_month"], axis=1).columns
print(list(features))
