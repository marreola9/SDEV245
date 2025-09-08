from cryptography.fernet import Fernet

# Put your key here. In a real application, keep this secret!
key = Fernet.generate_key()
print(key)
f = Fernet(key)
print(f)
token = f.encrypt(b"A really secret message.")
print(token)   
print(f.decrypt(token))