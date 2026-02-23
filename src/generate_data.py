import numpy as np
import pandas as pd

np.random.seed(42)

n_users = 20000
months = 6

rows = []

for user in range(n_users):
    tenure = np.random.randint(1, 24)
    base_sessions = np.random.poisson(5)
    base_watch = np.random.normal(800, 200)
    failed_payment = np.random.binomial(1, 0.1)
    plan_price = np.random.choice([8, 12, 16])

    churn_month = None

    if np.random.rand() < 0.15:
        churn_month = np.random.randint(3, months + 1)

    for m in range(1, months + 1):

        decay = 1

        if churn_month and m >= churn_month - 2:
            decay = 0.5

        sessions = max(0, int(np.random.poisson(base_sessions * decay)))
        watchtime = max(0, np.random.normal(base_watch * decay, 100))

        churned = 1 if churn_month and m == churn_month else 0

        rows.append([
            user,
            m,
            tenure + m,
            sessions,
            watchtime,
            failed_payment,
            plan_price,
            churned
        ])

data = pd.DataFrame(rows, columns=[
    "user_id",
    "month",
    "tenure_months",
    "sessions",
    "watchtime",
    "failed_payments",
    "plan_price",
    "churn"
])

data.to_csv("data/raw.csv", index=False)

print("Temporal dataset created.")
print("Shape:", data.shape)
print("Churn rate:", data["churn"].mean())
