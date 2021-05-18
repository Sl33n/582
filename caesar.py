def encrypt(key,plaintext):
    ciphertext=""
    for a in plaintext:
       ciphertext = ciphertext + (chr(ord(a) + key))
    return ciphertext

def decrypt(key,ciphertext):
    plaintext=""
    for a in ciphertext:
        plaintext = plaintext + (chr(ord(a) - key))
    return plaintext

