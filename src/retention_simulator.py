import pandas as pd
import xgboost as xgb
import numpy as np

df = pd.read_csv("data/processed.csv")

last_month = df["month"].max()
test = df[df["month"] == last_month].copy()

X_test = test.drop(["user_id", "churn", "churn_next_month"], axis=1)
y_test = test["churn_next_month"]

model = xgb.XGBClassifier()
model.load_model("models/xgb_model.json")

test["prob"] = model.predict_proba(X_test)[:, 1]

baseline_churners = y_test.sum()

avg_revenue = test["plan_price"].mean()

baseline_loss = baseline_churners * avg_revenue

top_10 = test.sort_values("prob", ascending=False).head(int(len(test) * 0.1))

intervention_effectiveness = 0.30

prevented_churn = top_10["churn_next_month"].sum() * intervention_effectiveness

saved_revenue = prevented_churn * avg_revenue

print("Baseline churners:", baseline_churners)
print("Baseline revenue loss:", baseline_loss)
print("Churn prevented (30% effectiveness):", prevented_churn)
print("Revenue saved:", saved_revenue)
