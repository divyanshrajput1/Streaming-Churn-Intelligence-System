import pandas as pd
import xgboost as xgb
import time

model = xgb.XGBClassifier()
model.load_model("models/xgb_model.json")

feature_order = [
    "month",
    "tenure_months",
    "sessions",
    "watchtime",
    "failed_payments",
    "plan_price",
    "sessions_lag1",
    "watchtime_lag1",
    "sessions_roll2",
    "watchtime_roll2",
    "sessions_trend",
    "watchtime_trend"
]

print("Model loaded successfully.")

while True:
    try:
        df = pd.read_csv("streaming/features.csv")

        if len(df) == 0:
            time.sleep(5)
            continue

        df = df.sort_values("user_id")

        df["sessions_lag1"] = df["sessions"]
        df["watchtime_lag1"] = df["watchtime"]

        df["sessions_trend"] = df["sessions"] - df["sessions_roll2"]
        df["watchtime_trend"] = df["watchtime"] - df["watchtime_roll2"]

        df["month"] = 6
        df["tenure_months"] = 12
        df["failed_payments"] = 0
        df["plan_price"] = 12

        X = df[feature_order]

        probs = model.predict_proba(X)[:, 1]

        df["churn_probability"] = probs

        high_risk = df[df["churn_probability"] > 0.8]

        print("High-risk users:", len(high_risk))

    except Exception as e:
        print("Scoring error:", e)

    time.sleep(5)
