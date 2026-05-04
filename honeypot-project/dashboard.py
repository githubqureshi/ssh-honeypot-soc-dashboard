import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.express as px
import requests
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")
st.title("🛡️ SOC Monitoring Dashboard")

# =========================
# UI STYLE
# =========================
st.markdown("""
<style>
body {
    background-color: #0a0f1c;
    color: #e6edf3;
    font-family: monospace;
}
h1, h2, h3 { color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=3000, key="refresh")

# =========================
# LOAD DATA
# =========================
try:
    df = pd.read_json("logs.json", lines=True)
except:
    st.warning("No logs yet")
    st.stop()

df["time"] = pd.to_datetime(df["time"])

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Total Attacks", len(df))
col2.metric("Unique IPs", df["ip"].nunique())
col3.metric("Users", df["username"].nunique())

# =========================
# TIMELINE
# =========================
st.subheader("📈 Attack Timeline")
timeline = df.set_index("time").resample("1min").size()
st.line_chart(timeline)

# =========================
# GEO LOCATION
# =========================
@st.cache_data
def get_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return res.get("lat"), res.get("lon"), res.get("country")
    except:
        return None, None, None

# =========================
# MAP
# =========================
st.subheader("🌍 Attack Map")

map_data = []

for ip in df["ip"].unique():
    lat, lon, country = get_location(ip)
    if lat and lon:
        map_data.append({
            "ip": ip,
            "lat": lat,
            "lon": lon,
            "country": country
        })

if map_data:
    map_df = pd.DataFrame(map_data)

    fig = px.scatter_geo(
        map_df,
        lat="lat",
        lon="lon",
        hover_name="ip",
        projection="natural earth"
    )

    st.plotly_chart(fig, width="stretch")
else:
    st.warning("No valid IP data")

# =========================
# ALERTS
# =========================
st.subheader("🚨 Alerts")

ip_counts = df["ip"].value_counts()

for ip, count in ip_counts.items():
    if count > 5:
        st.error(f"Brute Force → {ip}")

# =========================
# LIVE FEED
# =========================
st.subheader("💻 Live Feed")

latest = df.tail(10)[::-1]

for _, row in latest.iterrows():
    st.code(f"{row['time']} | {row['ip']} | {row['username']}:{row['password']}")

# =========================
# LOGS
# =========================
st.subheader("📜 Logs")
st.dataframe(df, use_container_width=True)