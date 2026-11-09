import random
import string
from luaparser import astnodes

class ASTTransformer:
    def __init__(self):
        self.var_map = {}

    def transform(self, tree):
        self._rename_variables(tree)
        self._encode_strings(tree)
        return tree

    def _generate_name(self):
        chars = string.ascii_letters + string.digits
        return "_" + "".join(random.choices(chars, k=6))

    def _rename_variables(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, astnodes.Local):
                for target in node.targets:
                    if isinstance(target, astnodes.Name):
                        if target.id not in self.var_map:
                            self.var_map[target.id] = self._generate_name()
                        target.id = self.var_map[target.id]

            elif isinstance(node, astnodes.Name):
                if node.id in self.var_map:
                    node.id = self.var_map[node.id]

    def _encode_strings(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, astnodes.String):
                original = node.s
                encoded = f"string.char({','.join(str(ord(c)) for c in original)})"
                node.s = encoded
