import argparse, importlib
L = importlib.import_module('_9facesM.lexer').LuauLexer
C = importlib.import_module('_9facesM.compiler').VMCompiler
p = argparse.ArgumentParser()
p.add_argument("-i", required=True); p.add_argument("-o", required=True); p.add_argument("--dev", action="store_true")
a = p.parse_args()
src = open(a.i, "r", encoding="utf-8-sig").read()
open(a.o, "w", encoding="utf-8").write(C().build(L(src).strip_whitespace()))
print(f"[+] -> {a.o}")
