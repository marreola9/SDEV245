Caesar Cipher (Python)

This is a simple Caesar Cipher CLI app written in Python.  
It allows you to encrypt and decrypt messages using a shift key.
How It Works
The Caesar Cipher is a substitution cipher that shifts each letter of the message by a fixed number of positions in the alphabet.

Encryption: Shifts characters forward by the key.
Decryption: Shifts characters backward by the key (negative shift).

Example with shift 3:
Plaintext: HELLO
Encrypted: KHOOR
Decrypted: HELLO

---

Simulate a digital signature (sign/verify).

Ed25519 Key Generation & Signature Example (Python)

This project demonstrates how to generate Ed25519 keys, save them in PEM and binary formats, and use them for digital signatures and verification using the cryptography library in Python.

Features

- Generate a new Ed25519 private/public key pair.
- Save the private key:
  - In PEM format (`private_key.pem`).
  - In raw binary format (`private_key.bin`).
- Save the public key:
  - In PEM format (`public_key.pem`).
  - In raw binary format (`public_key.bin`).
- Sign a message with the private key.
- Verify the signature with the public key.

Install dependencies:
bash
pip install cryptography

---

SHA-256 hashes for input strings

This is a simple command-line tool written in Python that allows you to generate SHA256 hashes of input strings.  
It uses Python’s built-in `hashlib` and `cmd` modules.

Features

- Compute SHA256 hash of any string.
- Interactive CLI with simple commands.
- Exit gracefully with `exit` or `quit`.
