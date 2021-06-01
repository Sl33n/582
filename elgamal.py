import random

from params import p
from params import g


def keygen():
    sk = 0
    pk = 0
    sk = random.randint(1, p)
    pk = pow(g, sk, p)
    return pk, sk


def encrypt(pk, m):
    c1 = 0
    c2 = 0
    r = random.randint(1, p)
    c1 = pow(g, r, p)
    x = pow(pk,r,p)
    y = pow(m,1,p)
    c2 = pow(x*y,1,p)
    return [c1, c2]


def decrypt(sk, c):
    m = 0
    (c1, c2) = c
    inv = pow(c1, -1*sk, p)
    m = pow(c2*inv, 1, p)

    return m
