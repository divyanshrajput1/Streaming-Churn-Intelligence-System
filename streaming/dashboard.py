import streamlit as st
import pandas as pd
import os
import time
import json
import xgboost as xgb
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
<style>
body {
    background-color: #0B0F19;
}
.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(255,0,0,0.4);
}
.glow-red {
    color: #FF2D2D;
    text-shadow: 0 0 10px #FF0000;
}
.glow-green {
    color: #00FF7F;
    text-shadow: 0 0 10px #00FF7F;
}
.glow-yellow {
    color: #FFD700;
    text-shadow: 0 0 10px #FFD700;
}
</style>
""", unsafe_allow_html=True)

num_partitions = 4

if "throughput_history" not in st.session_state:
    st.session_state.throughput_history = []

if "lag_history" not in st.session_state:
    st.session_state.lag_history = []

if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()
    st.session_state.last_total = 0

while True:

    produced = {}
    consumed = {}

    if os.path.exists("streaming/producer_metrics.json"):
        with open("streaming/producer_metrics.json", "r") as f:
            produced = json.load(f)

    if os.path.exists("streaming/consumer_metrics.json"):
        with open("streaming/consumer_metrics.json", "r") as f:
            consumed = json.load(f)

    lag_data = {}
    total_lag = 0

    for p in range(num_partitions):
        prod = produced.get(str(p), 0) or produced.get(p, 0)
        cons = consumed.get(str(p), 0) or consumed.get(p, 0)
        lag = prod - cons
        lag_data[f"P{p}"] = lag
        total_lag += lag

    total_produced = sum(produced.values()) if produced else 0

    current_time = time.time()
    time_diff = current_time - st.session_state.last_time
    events_diff = total_produced - st.session_state.last_total
    throughput = events_diff / time_diff if time_diff > 0 else 0

    st.session_state.last_time = current_time
    st.session_state.last_total = total_produced

    st.session_state.throughput_history.append(throughput)
    st.session_state.lag_history.append(total_lag)

    # ALERT BANNER
    if total_lag > 200:
        st.markdown("<h2 class='glow-red'>🚨 CRITICAL LAG DETECTED 🚨</h2>", unsafe_allow_html=True)
    elif total_lag > 50:
        st.markdown("<h2 class='glow-yellow'>⚠️ Lag Increasing ⚠️</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 class='glow-green'>✅ System Healthy</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("⚡ Throughput", f"{round(throughput,2)} ev/s")
    col2.metric("📊 Total Lag", total_lag)
    col3.metric("📦 Produced", total_produced)
    col4.metric("🎛 Partitions", num_partitions)

    st.divider()

    # NEON TREND GRAPHS
    left, right = st.columns(2)

    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=st.session_state.throughput_history,
            mode="lines",
            line=dict(color="#FF2D2D", width=4)
        ))
        fig.update_layout(
            title="Throughput Trend",
            plot_bgcolor="#0B0F19",
            paper_bgcolor="#0B0F19",
            font_color="white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            y=st.session_state.lag_history,
            mode="lines",
            line=dict(color="#FFD700", width=4)
        ))
        fig2.update_layout(
            title="Lag Trend",
            plot_bgcolor="#0B0F19",
            paper_bgcolor="#0B0F19",
            font_color="white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # DRAMATIC PARTITION BARS
    lag_df = pd.DataFrame(
        list(lag_data.items()),
        columns=["Partition", "Lag"]
    )

    colors = []
    for value in lag_df["Lag"]:
        if value > 200:
            colors.append("#FF2D2D")
        elif value > 100:
            colors.append("#FF6A00")
        elif value > 20:
            colors.append("#FFD700")
        else:
            colors.append("#00FF7F")

    fig3 = go.Figure()

    fig3.add_trace(go.Bar(
        x=lag_df["Partition"],
        y=lag_df["Lag"].replace(0, 0.1),
        marker_color=colors,
        text=lag_df["Lag"],
        textposition="outside"
    ))

    fig3.update_layout(
        title="Partition Lag",
        plot_bgcolor="#0B0F19",
        paper_bgcolor="#0B0F19",
        font_color="white"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # CHURN SECTION
    if os.path.exists("streaming/features.csv"):
        df = pd.read_csv("streaming/features.csv")

        if len(df) > 0:
            model = xgb.XGBClassifier()
            model.load_model("models/xgb_model.json")

            feature_order = [
                "month","tenure_months","sessions","watchtime",
                "failed_payments","plan_price","sessions_lag1",
                "watchtime_lag1","sessions_roll2","watchtime_roll2",
                "sessions_trend","watchtime_trend"
            ]

            X = df[feature_order]
            probs = model.predict_proba(X)[:, 1]
            df["prob"] = probs

            high_risk = df[df["prob"] > 0.8]

            fig4 = px.histogram(df, x="prob", nbins=30)
            fig4.update_layout(
                title="Churn Risk Distribution",
                plot_bgcolor="#0B0F19",
                paper_bgcolor="#0B0F19",
                font_color="white"
            )

            st.plotly_chart(fig4, use_container_width=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("👥 Active Users", len(df))
            c2.metric("⚠️ High Risk Users", len(high_risk))
            c3.metric("💰 Revenue At Risk",
                      round(len(high_risk) * df["plan_price"].mean(), 2))

    time.sleep(2)
    st.rerun()