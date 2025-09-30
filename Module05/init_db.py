import sqlite3, os, base64, hashlib, hmac

DB = "userdata.db"
ITERATIONS = 120_000  # reasonable default

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2${ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(dk).decode()}"

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

users = [
    ("mike213", "mikepassword"),
    ("john", "mycatisgreat999"),
    ("striker999", "IlikeStriking"),
    ("bob987", "TheConstructor234"),
]

for u, p in users:
    cur.execute("INSERT OR REPLACE INTO userdata (username, password) VALUES (?, ?)", (u, hash_password(p)))

conn.commit()
conn.close()
print("DB initialized.")
