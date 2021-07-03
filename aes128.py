# Implementation AES128 with python library

from cryptography.fernet import Fernet



hexSecKey = "2b7e151628aed2a6abf7158809cf4f3c"


msg = "aabbccdd010000000000000000000000"

msg = msg.encode()

f = Fernet(hexSecKey)
ciphertext = f.encrypt(msg)

print(ciphertext)

print("________________________________Decrypt____________________________________")
cleartext = f.decrypt(ciphertext)

cleartext = cleartext.decode()

print(cleartext)
