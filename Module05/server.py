import base64, hashlib, hmac, os, socket, sqlite3, threading, time

DB = "userdata.db"
HOST, PORT = "localhost", 9999
ITERATIONS_DEFAULT = 120_000

# very simple in-memory rate limit: 5 attempts per IP per 60s
ATTEMPTS = {}
MAX_ATTEMPTS = 5
WINDOW = 60

def within_limit(ip):
    now = time.time()
    window = ATTEMPTS.get(ip, [])
    window = [t for t in window if now - t < WINDOW]
    if len(window) >= MAX_ATTEMPTS:
        ATTEMPTS[ip] = window
        return False
    window.append(now)
    ATTEMPTS[ip] = window
    return True

def recv_line(conn):
    data = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            break
        if chunk in (b"\n",):
            break
        data += chunk
    return data.decode("utf-8", errors="ignore").strip()

def send_line(conn, s):
    conn.sendall((s + "\n").encode("utf-8"))

def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, iters, salt_b64, dk_b64 = stored.split("$", 3)
        if scheme != "pbkdf2":
            return False
        iters = int(iters)
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(dk_b64)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iters)
        return hmac.compare_digest(derived, expected)  # constant-time
    except Exception:
        return False

def handle_connection(conn, addr):
    ip = addr[0]
    try:
        if not within_limit(ip):
            send_line(conn, "Too many attempts. Try again later.")
            return

        send_line(conn, "Username:")
        username = recv_line(conn)
        send_line(conn, "Password:")
        password = recv_line(conn)

        # Generic error messages to reduce user enumeration
        with sqlite3.connect(DB) as cx:
            cx.row_factory = sqlite3.Row
            cur = cx.cursor()
            cur.execute("SELECT id, username, password FROM userdata WHERE username = ?", (username,))
            row = cur.fetchone()

        # Always do a verification step to equalize timing even if no user
        fake_stored = "pbkdf2$120000$" + base64.b64encode(os.urandom(16)).decode() + "$" + base64.b64encode(os.urandom(32)).decode()
        if not row:
            verify_password(password, fake_stored)
            send_line(conn, "Login failed!")
            return

        if verify_password(password, row["password"]):
            send_line(conn, "Login successful!")
        else:
            send_line(conn, "Login failed!")
    except Exception as e:
        # Avoid leaking details to the client
        try:
            send_line(conn, "Server error.")
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse address for quicker restarts
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Listening on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        t = threading.Thread(target=handle_connection, args=(client, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    main()
