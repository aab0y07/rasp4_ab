# Implementation AES128 with python library

from cryptography.fernet import Fernet


key = Fernet.generate_key()

with open('secret.key', 'wb') as new_key_file:
    new_key_file.write(key)
    
print(key)

msg = "super_secret_key_dias"

msg = msg.encode()

f = Fernet(key)
ciphertext = f.encrypt(msg)

print(ciphertext)

print("________________________________Decrypt____________________________________")
cleartext = f.decrypt(ciphertext)

cleartext = cleartext.decode()

print(cleartext)
