Socket Login Demo

A minimal username/password login service over TCP sockets using Python’s standard library (no frameworks).
The server stores passwords with PBKDF2-HMAC-SHA256 and verifies logins from a simple line-based client.

Contents

server.py — TCP server that prompts for username & password, verifies against SQLite.

init_db.py — Initializes userdata.db with sample users and salted PBKDF2 password hashes.

client.py — Simple interactive client for testing the login flow.

userdata.db — SQLite database (created by init_db.py).

Features

🔐 PBKDF2-HMAC-SHA256 with per-user random salt (constant-time compare).

🚫 Basic in-memory rate limiting: 5 attempts per IP per 60s.

🙈 Generic error messages to reduce user enumeration.

🧪 Tiny, dependency-free demo (Python stdlib only).

Requirements

Python 3.9+ (tested on 3.11/3.12)

macOS, Linux, or Windows

Quick Start

# 1) Create and populate the database

python init_db.py

# 2) Start the server (listens on localhost:9999)

python server.py

# -> outputs: Listening on localhost:9999

# 3) In another terminal, run the client

python client.py

# Enter one of the seeded accounts (see below).

Seeded Users (from init_db.py)
mike213 / mikepassword
john / mycatisgreat999
striker999 / IlikeStriking
bob987 / TheConstructor234

How It Works
Wire Protocol (very simple, line-based)

Server sends Username: then a newline.

Client sends the username + newline.

Server sends Password: then a newline.

Client sends the password + newline.

Server responds with Login successful! or Login failed! then closes.

The server trims input with .strip() and ignores undecodable bytes.

Password Storage Format
pbkdf2$<iterations>$<base64_salt>$<base64_derived_key>

Iterations default to 120_000 (can be tuned).

verify_password() recomputes PBKDF2 with the stored salt/iterations and compares using hmac.compare_digest().

Database Schema
CREATE TABLE IF NOT EXISTS userdata (
id INTEGER PRIMARY KEY,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
);

Files Overview

init_db.py

hash_password(password: str) -> str: creates salted PBKDF2 hash.

Inserts/updates four demo users with unique salts.

server.py

TCP listener on localhost:9999 (reuseaddr enabled).

ATTEMPTS dict provides 5-per-minute IP throttling.

verify_password() parses the stored string, runs PBKDF2, constant-time compares.

Equalizes timing for non-existent users by verifying against a fake hash.

Sends generic messages (Login failed!, Server error.).

client.py

Connects to server, reads prompts line-by-line, asks user for input, prints server response.

Configuration

Change host/port in server.py and client.py:

HOST, PORT = "localhost", 9999

Adjust PBKDF2 iterations in both init_db.py and server.py:

ITERATIONS = 120_000 # in init_db.py
ITERATIONS_DEFAULT = 120_000 # in server.py

Testing

Happy path: Use a seeded username/password — expect “Login successful!”

Fail path: Wrong password — expect “Login failed!”

Rate limiting: Rapidly submit >5 attempts within 60s from same IP — expect “Too many attempts. Try again later.”

Tip: You can script the client with printf/nc for quick tests:

{ printf "mike213\n"; printf "mikepassword\n"; } | nc localhost 9999

OWASP Mapping (how this demo relates)

A01 Broken Access Control: Not demonstrated by default (login only). If you add endpoints like /users/<id>, implement strict ownership/role checks.

A02 Cryptographic Failures: Demonstrates correct password hashing (PBKDF2 + random salt + constant-time compare). Add TLS to protect in transit.

A03 Injection: Uses parameterized SQL (?) to avoid SQL injection when selecting by username.

A04 Insecure Design: Keep reset flows tokenized and time-limited if you add them; current design avoids password reset entirely.

A05 Security Misconfiguration: Consider disabling verbose errors, using timeouts, limiting input size, and enabling TLS.

A06 Vulnerable/Outdated Components: Stdlib-only; if you add deps, pin versions and scan for CVEs.

A07 Identification & Authentication Failures: Basic throttling & generic errors are present; consider MFA, password policies, and breach checks.

A08 Software & Data Integrity Failures: No dynamic code loading; if you add CDNs/webhooks, validate signatures/checksums.

A09 Security Logging & Monitoring Failures: Add structured auth logs and alerts for real environments.

A10 SSRF: No outbound user-driven requests; if you add any, enforce strict allowlists and block internal IP ranges.

Troubleshooting

sqlite3.OperationalError: database is locked
Close other processes using the DB; ensure each connection is short-lived (as in server.py).

Client hangs
Ensure the server is running and reachable at the configured host/port; check local firewall.

All logins fail
Recreate DB: delete userdata.db and run python init_db.py again.
