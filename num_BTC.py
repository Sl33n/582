import math

def num_BTC(b):
    q = int(0)
    c = float(0)
    sum = float(0)
    t = float(0)
    q = b//210000
    m = b%210000
    t = m*(50/(2**q))

    while q > 0:
        sum = sum + (50 / (2**(q-1))) * 210000
        q = q-1

    c = sum + t
    return c



