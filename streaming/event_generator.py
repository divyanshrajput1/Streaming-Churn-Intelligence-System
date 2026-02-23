import pandas as pd
import numpy as np
import time
from datetime import datetime

np.random.seed(42)

users = 1000
events = ["play", "pause", "stop", "cancel"]

def generate_event():
    return {
        "user_id": np.random.randint(0, users),
        "event_type": np.random.choice(events, p=[0.6, 0.2, 0.15, 0.05]),
        "watchtime": max(0, np.random.normal(120, 40)),
        "timestamp": datetime.now()
    }

while True:
    event = generate_event()
    df = pd.DataFrame([event])
    df.to_csv("streaming/events.csv", mode="a", header=False, index=False)
    print("Generated:", event)
    time.sleep(1)
