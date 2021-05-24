import hashlib
import os
import secrets


def hash_collision(k):
    if not isinstance(k, int):
        print("hash_collision expects an integer")
        return (b'\x00', b'\x00')
    if k < 0:
        print("Specify a positive number of bits")
        return (b'\x00', b'\x00')

    x = b'\x00'
    y = b'\x00'


    while True:
        x = b"\x00" + secrets.token_bytes(4) + b"\x00"
        y = b"\x00" + secrets.token_bytes(4) + b"\x00"
        x_hash = hashlib.sha256(x).hexdigest()
        y_hash = hashlib.sha256(y).hexdigest()

        for i in range(k):
            if x_hash[63-i] == y_hash[63-i] and i==k-1:
                return (x, y)
            if x_hash[63-i] == y_hash[63-i]:
                continue
            else: break
