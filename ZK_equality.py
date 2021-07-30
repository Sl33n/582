from zksk import Secret, DLRep
from zksk import utils


def ZK_equality(G, H):

    r1 = Secret(utils.get_random_num(bits=128))
    r2 = Secret(utils.get_random_num(bits=128))
    m = Secret(utils.get_random_num(bits=2))

    C1 = r1.value * G
    C2 = m.value * G + r1.value * H

    D1 = r2.value * G
    D2 = m.value * G + r2.value * H

    stmt = DLRep(C1,r1.value * G) & DLRep(C2,r1.value * H + m.value * G) & DLRep(D1,r2.value * G) & DLRep(D2,r2.value * H + m.value * G)
    zk_proof = stmt.prove()

    return (C1, C2), (D1, D2), zk_proof

