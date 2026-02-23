import numpy as np
import time
import json
from datetime import datetime
import os

np.random.seed(42)

users = 1000
events = ["play", "pause", "stop", "cancel"]
num_partitions = 4

os.makedirs("streaming/partitions", exist_ok=True)

produced_offsets = {i: 0 for i in range(num_partitions)}

def generate_event():
    return {
        "user_id": int(np.random.randint(0, users)),
        "event_type": str(np.random.choice(events, p=[0.6, 0.2, 0.15, 0.05])),
        "watchtime": float(max(0, np.random.normal(120, 40))),
        "timestamp": str(datetime.now())
    }

while True:
    event = generate_event()

    partition = event["user_id"] % num_partitions
    filepath = f"streaming/partitions/topic_{partition}.log"

    with open(filepath, "a") as f:
        f.write(json.dumps(event) + "\n")

    produced_offsets[partition] += 1

    with open("streaming/producer_metrics.json", "w") as m:
        json.dump(produced_offsets, m)

    print(f"Produced → Partition {partition}")
    time.sleep(0.1)