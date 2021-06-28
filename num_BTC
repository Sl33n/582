import math

def num_BTC(b):
    q = int(0)
    c = float(0)
    sum = 0
    q = b//210000
    m = b%210000
    t = m * 50 / (q + 1)

    for i in range(q):
        sum += (50/(i+1))*210000

    c = sum + t
    return c

print(num_BTC(425000))
