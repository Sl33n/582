import hashlib
import os

def hash_collision(k):
    if not isinstance(k, int):
        print("hash_collision expects an integer")
        return (b'\x00', b'\x00')
    if k <= 0:
        print("Specify a positive number of bits")
        return (b'\x00', b'\x00')

    x = b'\x00'
    y = b'\x00'

    while True:
        x = os.urandom(10)
        y = os.urandom(10)
        x_hash = hashlib.sha256(x).hexdigest()
        y_hash = hashlib.sha256(y).hexdigest()
        x_hash_binary = hex2binary(x_hash)
        y_hash_binary = hex2binary(y_hash)

        for i in range(k):
            if x_hash_binary[len(x_hash_binary) - i - 1] == y_hash_binary[len(y_hash_binary) - i - 1] and i == k - 1:
                print(x_hash_binary)
                print(y_hash_binary)
                return (x, y)
            if x_hash_binary[len(x_hash_binary) - i - 1] == y_hash_binary[len(y_hash_binary) - i - 1]:
                continue
            else:
                break

def hex2binary(hex):
    end_length = len(hex) * 4

    hex_as_int = int(hex, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    return padded_binary

(hash_collision(20))
