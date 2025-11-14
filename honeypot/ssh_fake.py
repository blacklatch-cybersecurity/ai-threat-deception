import socket, threading, datetime
from classifier import classify_command

HOST = "0.0.0.0"
PORT = 2222  # Fake SSH
LOG = "session.log"

def handle_client(conn, addr):
    conn.send(b"SSH-2.0-OpenSSH_9.0\r\n")
    with open(LOG, "a") as f:
        f.write(f"\n\n== NEW CONNECTION {addr} == {datetime.datetime.now()}\n")

    conn.send(b"login: ")
    user = conn.recv(1024).decode(errors="ignore").strip()

    conn.send(b"password: ")
    pwd = conn.recv(1024).decode(errors="ignore").strip()

    with open(LOG, "a") as f:
        f.write(f"[CREDENTIAL] {user}:{pwd}\n")

    conn.send(b"Welcome to Ubuntu 22.04 LTS\n$ ")

    while True:
        cmd = conn.recv(4096).decode(errors="ignore").strip()
        if not cmd:
            break
        
        risk = classify_command(cmd)

        with open(LOG, "a") as f:
            f.write(f"[CMD] {cmd} | RISK={risk}\n")

        conn.send(f"bash: {cmd}: command not found\n$ ".encode())

    conn.close()


def start_honeypot():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(50)
    print(f"🔥 Honeypot running on port {PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_honeypot()
