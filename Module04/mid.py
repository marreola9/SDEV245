from cryptography.fernet import Fernet
#from cryptography.hazmat.primitives import serialization
import hashlib

# Request user input
user_message = input("The first best time was ten years ago, the second best time is NOW!: ")
#user_shift_key = int(input("Shift Key (integer): "))

# Take user input to create the hash and print it
sha256_hash = hashlib.sha256(user_message.encode()).hexdigest()
print(sha256_hash)

# Generate a key and create a instance of Fernet of it to encrypt the message - and store it in 'f' variable
key = Fernet.generate_key()
f = Fernet(key)
# use the Fernet instance to encrypt the message - and store it in 'token' variable
token = f.encrypt(user_message.encode())
print(token)

# Using the Fernet instance, decrypt the message (token) and store it in 'plain_text' variable
plain_text = f.decrypt(token)

print(plain_text)

# Hash user input again and compare it to the hash stored in variable sha256_hash
verify = hashlib.sha256(plain_text).hexdigest()
print(verify)
if verify == sha256_hash:
    print("The hashes match")
    
# If the hashes match, print "The hashes match"