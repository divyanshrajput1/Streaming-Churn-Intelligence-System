# 🚀 Streaming Churn Intelligence System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-purple)
![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-darkgreen)
![Status](https://img.shields.io/badge/Status-Production--Style-success)

An end-to-end distributed streaming + machine learning system that simulates how a platform predicts churn in real-time using event-driven architecture.

This project includes:

- Time-based churn modeling (XGBoost, 0.92 ROC-AUC)
- SHAP explainability
- Revenue impact simulator
- Kafka-style partitioned streaming simulation
- Consumer lag monitoring
- Auto-scaling simulation
- Real-time monitoring dashboard

---

# Architecture Overview

Producer → Partitioned Topic Logs → Consumer → Feature Store → ML Model → Dashboard

Key components:

- Event Producer (simulated user activity)
- Kafka-style partitions (log files)
- Consumer with sliding window feature engineering
- Online XGBoost churn scoring
- Lag & throughput monitoring
- Auto-scaling decision engine
- Dark Neon Dashboard

---

# Model Performance

- Model: XGBoost
- ROC-AUC: **0.92**
- Lift @ Top 10%: ~6x
- Time-based forward labeling
- Leakage-free temporal split

---

# Features Engineered

- Rolling session averages
- Watchtime rolling averages
- Trend detection
- Lag features
- Payment behavior
- Tenure modeling

---

# Revenue Impact Simulation

Simulated retention campaign:

- Baseline churners: 790
- Revenue loss: ~$9,461
- Prevented churn (30% effectiveness): 143 users
- Revenue saved: ~$1,714

---

# Streaming Simulation

Simulates Kafka-style architecture:

- 4 partitioned topic logs
- Hash-based partition routing
- Offset tracking
- True consumer lag calculation
- Throughput (events/sec) tracking

---

# Auto Scaling Logic

Auto-scaler dynamically adjusts consumers based on lag:

- Scale up when lag > threshold
- Scale down when lag stabilizes
- Cooldown protection
- Min/max consumer bounds

---

# Dark Neon Dashboard

Features:

- Real-time throughput graph
- Real-time lag trend
- Partition lag distribution
- Churn risk histogram
- Revenue at risk metrics
- Alert banners (Healthy / Warning / Critical)

Run with: streamlit run streaming/dashboard.py

---

# How To Run The System

### 1️⃣ Train Model (optional)
python src/train.py

---

### 2️⃣ Start Streaming Simulation

Terminal 1: python streaming/producer.py
Terminal 2: python streaming/consumer.py

---

### 3️⃣ Launch Dashboard
streamlit run streaming/dashboard.py

Open:
http://localhost:8501

---

# What This Project Demonstrates

- Real-time ML inference
- Distributed systems simulation
- Event-driven architecture
- Feature drift awareness
- Production ML constraints
- Lag-based scaling logic
- Observability engineering

---

# Technologies Used

- Python
- XGBoost
- Pandas
- Plotly
- Streamlit
- JSON-based offset tracking
- Simulated Kafka partitions

---

# Future Improvements

- Dockerized microservices
- Kubernetes-style scaling simulation
- Redis message broker
- Real Kafka integration
- Feature store versioning
- Drift detection alerts
- Reinforcement-learning auto-scaler

---

# Author :
Divyansh Rajput (ML Engineer)

---

# Final Note :

This is not just a churn model.

This is a full distributed streaming ML intelligence system.
