import math

def num_BTC(b):
    q = int(0)
    c = float(0)
    sum = float(0)
    t = float(0)
    q = b//210000
    print("q is", q)
    m = b%210000
    print("m is", m)
    t = m*(50/(2**q))
    print("t is", t)

    while q > 0:
        sum = sum + (50 / (2**(q-1))) * 210000
        q = q-1

    c = sum + t
    return c

print(num_BTC(813574))


