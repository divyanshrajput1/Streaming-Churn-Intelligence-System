import pandas as pd
import time

window_size = 2

while True:
    try:
        df = pd.read_csv("streaming/events.csv", names=[
            "user_id", "event_type", "watchtime", "timestamp"
        ])

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        df = df.sort_values(["user_id", "timestamp"])

        agg = df.groupby("user_id").agg({
            "watchtime": "sum",
            "event_type": "count"
        }).reset_index()

        agg.rename(columns={"event_type": "sessions"}, inplace=True)

        df["period"] = df.groupby("user_id").cumcount() // 5

        roll = df.groupby(["user_id", "period"]).agg({
            "watchtime": "sum",
            "event_type": "count"
        }).reset_index()

        roll.rename(columns={"event_type": "sessions"}, inplace=True)

        roll = roll.sort_values(["user_id", "period"])

        roll["sessions_roll2"] = roll.groupby("user_id")["sessions"].rolling(window_size).mean().reset_index(level=0, drop=True)
        roll["watchtime_roll2"] = roll.groupby("user_id")["watchtime"].rolling(window_size).mean().reset_index(level=0, drop=True)

        latest = roll.groupby("user_id").tail(1)

        latest.to_csv("streaming/features.csv", index=False)

        print("Sliding window features updated.")

    except Exception as e:
        print("Processor error:", e)

    time.sleep(5)
