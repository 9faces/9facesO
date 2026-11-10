import random
class Opcodes:
    NAMES = ["PUSH","ADD","SUB","MUL","DIV","MOD","BXOR","BAND","BOR","BNOT",
             "CHR","BYTE","CAT","EXEC","DUP","POP","SWAP","JZ","JNZ","JMP",
             "NOP","GLOAD","CALL","ROT","OVER","DROP2",
             "FAKE1","FAKE2","FAKE3","FAKE4","FAKE5"]
    def __init__(self):
        self.ids = {}
        used = set()
        for name in self.NAMES:
            while True:
                v = random.randint(1000000, 9999999)
                if v not in used:
                    used.add(v); self.ids[name] = v; break
    def __getitem__(self, name): return self.ids[name]
