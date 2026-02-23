import pandas as pd
import time
import json
import os

num_partitions = 4
user_events = {}
last_positions = {i: 0 for i in range(num_partitions)}

while True:
    try:
        for p in range(num_partitions):
            filepath = f"streaming/partitions/topic_{p}.log"

            if not os.path.exists(filepath):
                continue

            with open(filepath, "r") as f:
                lines = f.readlines()

            total_messages = len(lines)
            consumed_messages = last_positions[p]

            new_lines = lines[consumed_messages:]
            last_positions[p] = total_messages

            for line in new_lines:
                event = json.loads(line)
                uid = event["user_id"]

                if uid not in user_events:
                    user_events[uid] = []

                user_events[uid].append(event)

                if len(user_events[uid]) > 20:
                    user_events[uid].pop(0)

        with open("streaming/consumer_metrics.json", "w") as m:
            json.dump(last_positions, m)

        rows = []

        for uid, events in user_events.items():
            sessions = len(events) * 3
            watchtime = sum(e["watchtime"] for e in events) * 2

            half = len(events) // 2 if len(events) > 1 else 1

            sessions_roll2 = len(events[-half:])
            watchtime_roll2 = sum(e["watchtime"] for e in events[-half:])

            sessions_lag1 = len(events[:-1]) if len(events) > 1 else sessions
            watchtime_lag1 = sum(e["watchtime"] for e in events[:-1]) if len(events) > 1 else watchtime

            sessions_trend = sessions - sessions_roll2
            watchtime_trend = watchtime - watchtime_roll2

            rows.append({
                "user_id": uid,
                "month": 6,
                "tenure_months": int(6 + (uid % 12)),
                "sessions": sessions,
                "watchtime": watchtime,
                "failed_payments": 1 if uid % 25 == 0 else 0,
                "plan_price": 12,
                "sessions_lag1": sessions_lag1,
                "watchtime_lag1": watchtime_lag1,
                "sessions_roll2": sessions_roll2,
                "watchtime_roll2": watchtime_roll2,
                "sessions_trend": sessions_trend,
                "watchtime_trend": watchtime_trend
            })

        df = pd.DataFrame(rows)

        if len(df) > 0:
            df.to_csv("streaming/features.csv", index=False)
            print("Features updated. Users:", len(df))

    except Exception as e:
        print("Consumer error:", e)

    time.sleep(2)