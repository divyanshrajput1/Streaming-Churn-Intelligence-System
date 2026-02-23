import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score

df = pd.read_csv("data/processed.csv")

last_month = df["month"].max()

test = df[df["month"] == last_month]

X_test = test.drop(["user_id", "churn", "churn_next_month"], axis=1)
y_test = test["churn_next_month"]

model = xgb.XGBClassifier()
model.load_model("models/xgb_model.json")

test = test.copy()
test.loc[:, "prob"] = model.predict_proba(X_test)[:, 1]

roc = roc_auc_score(y_test, test["prob"])

overall_rate = y_test.mean()

top_10 = test.sort_values("prob", ascending=False).head(int(len(test) * 0.1))
lift_10 = top_10["churn_next_month"].mean() / overall_rate

top_5 = test.sort_values("prob", ascending=False).head(int(len(test) * 0.05))
lift_5 = top_5["churn_next_month"].mean() / overall_rate

print("ROC-AUC:", roc)
print("Overall churn rate:", overall_rate)
print("Lift @ Top 10%:", lift_10)
print("Lift @ Top 5%:", lift_5)
