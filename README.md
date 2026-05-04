# 🛡️ SSH Honeypot SOC Dashboard

A real-time SSH honeypot system with a SOC-style monitoring dashboard that simulates real-world cybersecurity defense.

---

## 🚀 Features

- 🌍 Real-time global attack visualization  
- 📈 Attack timeline analytics  
- 🚨 Threat detection (Brute-force, Password spray)  
- 💻 Live attack monitoring feed  
- 🧠 SOC-style dashboard  
- 🔐 Simulated attacker blocking  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Paramiko  
- Plotly  
- Pandas  

---

## 🧪 How It Works

1. The honeypot listens for SSH login attempts  
2. Captures attacker credentials (username/password)  
3. Logs all activity in real-time  
4. Dashboard visualizes attack patterns and alerts  

---

## ▶️ Run Locally

```bash
# Start honeypot
python honeypot.py

# Start dashboard
streamlit run dashboard.py
