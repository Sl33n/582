import math

def num_BTC(b):
    q = int(0)
    c = float(0)
    sum = 0
    q = b//210000
    print(q)
    m = b%210000
    print(m)
    t = m * (50 / (q + 1))
    print(t)

    while q > 0:
        sum += (50 / (q)) * 210000
        q = q-1

    c = sum + t
    return c

print(num_BTC(210000))


