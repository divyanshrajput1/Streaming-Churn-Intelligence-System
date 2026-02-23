import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score

df = pd.read_csv("data/processed.csv")

last_month = df["month"].max()

train = df[df["month"] < last_month]
test = df[df["month"] == last_month]

X_train = train.drop(["user_id", "churn", "churn_next_month"], axis=1)
y_train = train["churn_next_month"]

X_test = test.drop(["user_id", "churn", "churn_next_month"], axis=1)
y_test = test["churn_next_month"]

scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)

model = xgb.XGBClassifier(
    n_estimators=1000,
    max_depth=7,
    learning_rate=0.02,
    subsample=0.85,
    colsample_bytree=0.85,
    min_child_weight=3,
    gamma=0.3,
    reg_lambda=2,
    reg_alpha=0.5,
    scale_pos_weight=scale_pos_weight,
    eval_metric="auc",
    random_state=42
)

model.fit(
    X_train,
    y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

pred_probs = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, pred_probs)

print("Time-Based Test ROC-AUC:", auc)

model.save_model("models/xgb_model.json")
