# Secure Message Hashing and Encryption Script

This simple Python script demonstrates how to:

1. Accept a user input message
2. Generate a **SHA-256 hash** to ensure message integrity
3. **Encrypt** the message using a symmetric key (`Fernet`)
4. **Decrypt** the message
5. Verify the integrity by comparing the original and decrypted hashes

---

## How It Works

1. The user inputs a message.
2. The script calculates its **SHA-256 hash** using `hashlib`.
3. A **Fernet key** is generated (symmetric encryption based on AES).
4. The message is encrypted with that key.
5. The ciphertext is decrypted.
6. The decrypted message is hashed again and compared to the original hash.

---

### Confidentiality, Integrity, and Availability

### Confidentiality: I'm using Fernet in the code to ensure user security isn't compromised. Using Fernet ensures that without the secret key, a hacker can't alter or read the message because it's based on AES (Advanced Encryption Standard) in CBC mode with HMAC authentication.

### Integrity: The original message is encrypted with SHA-256. The hash is stored before encryption, as it's decrypted, re-encrypted, and compared. If the hashes match, it means there was no modification. Using HMAC and hash verification guarantees that the message hasn't been tampered with.

### Availability: Since the program is relatively simple, it doesn't require external services, increasing its availability because it guarantees reliable execution in almost all environments where Python is installed.

### Entropy and Key Generation

### Entropy is essential for generating secure keys. Fernet automatically generates random numbers to generate a 256-bit key. A high-entropy key means it's very difficult to guess or force, protecting your data from unauthorized access.

### The code implemented here means that each time Fernet.generate_key() is called, a new cryptographic key is created, which is completely secure.
