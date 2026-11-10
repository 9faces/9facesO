import random
class Encryptor:
    def __init__(self):
        self.seed = random.randint(1, 9999)
    def encode_l1(self, bc):
        return [bc[i] ^ ((i+1) * 257 + self.seed) % 65536 for i in range(len(bc))]
    def encode_l2(self, L1):
        L2, prev = [], 0
        for v in L1:
            L2.append((v ^ prev) % (2**31))
            prev = v & 0xFF
        return L2
    def checksums(self, L2):
        chk1 = 0
        for b in L2: chk1 = (chk1 * 31 + (b & 0xFF)) % 65536
        return chk1, sum(L2) % 100000, self.seed
