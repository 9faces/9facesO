import random
from _9facesM.opcodes import Opcodes
from _9facesM.encryptor import Encryptor
from _9facesM.emitter import Emitter

class VMCompiler:
    def build(self, payload):
        data = [ord(c) for c in payload]
        op = Opcodes()
        bc = []
        for i, c in enumerate(data):
            pick = i % 3
            if pick == 0:
                off = random.randint(1, 200)
                bc += [op["PUSH"], (c - off) % 256, op["PUSH"], off, op["ADD"]]
            elif pick == 1:
                mask = random.randint(1, 255)
                bc += [op["PUSH"], c ^ mask, op["PUSH"], mask, op["BXOR"]]
            else:
                off = random.randint(1, 200)
                bc += [op["PUSH"], (c + off) % 256, op["PUSH"], off, op["SUB"]]
            for _ in range(random.randint(0, 4)):
                r = random.choice(["NOP","NOP","DUP","FAKE1","FAKE2","FAKE3","FAKE4","FAKE5"])
                bc += [op["DUP"], op["POP"]] if r == "DUP" else [op[r]]
            bc.append(op["CHR"])
        bc += [op["CAT"], op["EXEC"]]
        enc = Encryptor()
        L2 = enc.encode_l2(enc.encode_l1(bc))
        chk1, chk2, seed = enc.checksums(L2)
        return Emitter(op, L2, chk1, chk2, seed).emit()
