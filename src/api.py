from fastapi import FastAPI
import xgboost as xgb
import pandas as pd

app = FastAPI()

model = xgb.XGBClassifier()
model.load_model("models/xgb_model.json")

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prob = model.predict_proba(df)[0][1]
    return {"churn_probability": float(prob)}
