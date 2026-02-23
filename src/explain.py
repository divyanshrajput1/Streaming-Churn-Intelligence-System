import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/processed.csv")

last_month = df["month"].max()
test = df[df["month"] == last_month].copy()

X_test = test.drop(["user_id", "churn", "churn_next_month"], axis=1)

model = xgb.Booster()
model.load_model("models/xgb_model.json")

dtest = xgb.DMatrix(X_test)

shap_values = model.predict(dtest, pred_contribs=True)

shap_values = shap_values[:, :-1]

mean_abs_shap = np.abs(shap_values).mean(axis=0)

importance = pd.DataFrame({
    "feature": X_test.columns,
    "importance": mean_abs_shap
}).sort_values("importance", ascending=False)

print(importance.head(10))

plt.barh(importance["feature"].head(10), importance["importance"].head(10))
plt.gca().invert_yaxis()
plt.title("Top 10 Feature Importance (SHAP)")
plt.show()
