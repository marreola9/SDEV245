From the code snippets in module 5, I briefly explain why they didn't work. I also created an application with the included fixes, following OWASP guidelines.

1. Broken Access Control (IDOR) — Node/Express
   Returns any user profile by :userId without checking that the requester is the resource owner or has a role allowing access. Anyone who can guess/iterate IDs can read others’ data.

2. Broken Access Control (IDOR) — Flask
   Same flaw: fetches /account/<user_id> directly from the path and returns it with no authorization check. Exposes accounts to unauthorized users.

3. Cryptographic Failures — Java/MD5
   Uses MD5 (fast, broken, no salt). Fast hashes are trivial to brute-force and rainbow-table; there’s no password-hardening (e.g., PBKDF2/Bcrypt/Argon2) or per-user salt.

4. Cryptographic Failures — Python/SHA-1
   Uses SHA-1 with no salt or key-stretching. SHA-1 is obsolete for passwords and, being fast, is susceptible to guessing attacks.

5. Injection — SQL (string concatenation)
   Builds the SQL with untrusted username; an attacker can inject SQL (' OR '1'='1 etc.), leading to data exfiltration or account bypass. No parameterization/prepared statement.

6. Injection — NoSQL/Mongo
   Directly trusts req.query.username in the filter. Attackers can pass crafted objects/operators (e.g., {"$ne": null}) or special types, causing NoSQL injection and unintended matches.

7. Insecure Design — Password reset
   Resets a password solely by providing email + new_password. No proof of mailbox control, no one-time, time-limited token, no verification or logging — a trivial account takeover path.

8. Software & Data Integrity Failures — Untrusted script source
   Loads executable code from a CDN with no integrity guarantees (no subresource integrity, pinning, or signature). If the CDN or path is compromised, you execute attacker code.

9. Server-Side Request Forgery (SSRF)
   Fetches an arbitrary user-supplied URL. Attackers can make your server reach internal services (e.g., cloud metadata, localhost/admin endpoints) or pivot within your network.

10. Identification & Authentication Failures — Plaintext comparison
    Compares input to user.getPassword() directly, implying passwords are stored/retrieved in plaintext (or as reversible/fast hashes). No secure hashing, no constant-time verification, no rate limiting/MFA — easy credential-stuffing and full compromise on data leak.

Socket Login Demo

A minimal username/password login service over TCP sockets using Python’s standard library (no frameworks).
The server stores passwords with PBKDF2-HMAC-SHA256 and verifies logins from a simple line-based client.

Contents

server.py — TCP server that prompts for username & password, verifies against SQLite.

init_db.py — Initializes userdata.db with sample users and salted PBKDF2 password hashes.

client.py — Simple interactive client for testing the login flow.

userdata.db — SQLite database (created by init_db.py).

Features

PBKDF2-HMAC-SHA256 with per-user random salt (constant-time compare).

Basic in-memory rate limiting: 5 attempts per IP per 60s.

Generic error messages to reduce user enumeration.

Tiny, dependency-free demo (Python stdlib only).

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
