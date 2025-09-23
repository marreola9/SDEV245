from cryptography.fernet import Fernet
#from cryptography.hazmat.primitives import serialization
import hashlib

user_message = input("The first best time was ten years ago, the second best time is NOW!: ")
#user_shift_key = int(input("Shift Key (integer): "))

sha256_hash = hashlib.sha256(user_message.encode()).hexdigest()
print(sha256_hash)

key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(user_message.encode())
print(token)

plain_text = f.decrypt(token)

print(plain_text)
verify = hashlib.sha256(plain_text).hexdigest()
print(verify)
if verify == sha256_hash:
    print("The hashes match")