import hashlib
import os

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return
    nonce = b'\x00'

    while True:
        x = os.urandom(len(target_string))
        x_hash = hashlib.sha256(x).hexdigest()
        x_hash_binary = hex2binary(x_hash)

        for i in range(len(target_string)):
            if x_hash_binary[len(x_hash_binary) - i - 1] == target_string[len(target_string) - i - 1] and i == len(target_string)-1:
                return (x)
            if x_hash_binary[len(x_hash_binary) - i - 1] == target_string[len(target_string) - i - 1]:
                continue
            else:
                break

def hex2binary(hex):
    end_length = len(hex) * 4

    hex_as_int = int(hex, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    return padded_binary

