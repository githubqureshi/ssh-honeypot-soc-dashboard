honeypot.py code:
import socket
import threading
import paramiko
import json
from datetime import datetime
import time
import os
import random

HOST = "0.0.0.0"
PORT = 2222

FAKE_IPS = [
    "8.8.8.8",
    "1.1.1.1",
    "185.143.223.12",
    "45.89.67.23",
    "103.21.244.1"
]

# =========================
# SAFE BLOCK FUNCTION (WINDOWS FRIENDLY)
# =========================
def block_ip(ip):
    print(f"[SIMULATED BLOCK] {ip}")
    # Real blocking only works on Linux VPS
    # os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")

# =========================
# SERVER KEY
# =========================
if not os.path.exists("server.key"):
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file("server.key")

host_key = paramiko.RSAKey(filename="server.key")

# =========================
# SERVER CLASS
# =========================
class Server(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.attempts = 0

    def check_auth_password(self, username, password):
        self.attempts += 1

        fake_ip = random.choice(FAKE_IPS)

        log = {
            "ip": fake_ip,
            "real_ip": self.client_ip,
            "username": username,
            "password": password,
            "time": datetime.utcnow().isoformat(),
            "attack_type": "brute_force"
        }

        print("[ATTACK]", log)

        with open("logs.json", "a") as f:
            f.write(json.dumps(log) + "\n")

        # 🚨 Simulated auto-block
        if self.attempts > 10:
            block_ip(self.client_ip)

        time.sleep(random.uniform(0.2, 1.0))

        return paramiko.AUTH_FAILED

# =========================
# HANDLE CLIENT
# =========================
def handle_client(client, addr):
    transport = paramiko.Transport(client)
    transport.add_server_key(host_key)

    server = Server(addr[0])

    try:
        transport.start_server(server=server)
    except:
        return

    transport.accept(10)
    transport.close()

# =========================
# START SERVER
# =========================
def start():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(100)

    print(f"[+] Honeypot running on port {PORT}")

    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start()




    attack.py code:
    import random
import time
time.sleep(random.uniform(0.1, 1.0))

import paramiko
import time
import random

HOST = " 43.241.129.85"
PORT = 2222

usernames = ["admin", "hamza", "sudo", "amaan"]
passwords = ["tryagain", "1331", "goodone", "ghazanfar", "root"]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

while True:
    username = random.choice(usernames)
    password = random.choice(passwords)

    try:
        print(f"Trying {username}:{password}")

        client.connect(
            HOST,
            port=PORT,
            username=username,
            password=password,
            timeout=2,
            allow_agent=False,
            look_for_keys=False
        )

        client.close()

    except:
        pass

    time.sleep(0.3)



    dashboard.py code:
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
