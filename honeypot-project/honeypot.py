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