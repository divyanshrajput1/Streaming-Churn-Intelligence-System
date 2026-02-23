import pandas as pd

df = pd.read_csv("data/raw.csv")

df = df.sort_values(["user_id", "month"])

df["sessions_lag1"] = df.groupby("user_id")["sessions"].shift(1)
df["watchtime_lag1"] = df.groupby("user_id")["watchtime"].shift(1)

df["sessions_roll2"] = df.groupby("user_id")["sessions"].rolling(2).mean().reset_index(level=0, drop=True)
df["watchtime_roll2"] = df.groupby("user_id")["watchtime"].rolling(2).mean().reset_index(level=0, drop=True)

df["sessions_trend"] = df["sessions"] - df["sessions_lag1"]
df["watchtime_trend"] = df["watchtime"] - df["watchtime_lag1"]

df["churn_next_month"] = df.groupby("user_id")["churn"].shift(-1)

df = df.dropna()

df = df[df["month"] < df["month"].max()]

df.to_csv("data/processed.csv", index=False)

print("Rolling snapshot dataset created.")
print("Shape:", df.shape)
print("Next-month churn rate:", df["churn_next_month"].mean())
