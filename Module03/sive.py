from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

private_key = Ed25519PrivateKey.generate()

pkFile = open("private_key.pem", "wt", encoding="utf-8")
print(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()), file=pkFile)
pkFile.close()

pkBinaryFile = open("private_key.bin", "wb")
pkBinaryFile.write(private_key.private_bytes_raw())
pkBinaryFile.close()

# readPKFile = open("private_key.pem", "rt", encoding="utf-8")
# private_key = readPKFile.read()
# print(private_key)
# readPKFile.close()

signature = private_key.sign(b"my authenticated message")
public_key = private_key.public_key()

pubFile = open("public_key.pem", "wt", encoding="utf-8")
pubBinaryFile = open("public_key.bin", "wb")
pubBinaryFile.write(public_key.public_bytes_raw())
print(public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    ), file=pubFile)
pubFile.close()



# Raises InvalidSignature if verification fails
public_key.verify(signature, b"my authenticated message")