from luaparser import ast

class LuauParser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        try:
            source_str = " ".join([str(t) for t in self.tokens])
            return ast.parse(source_str)
        except Exception as e:
            raise ValueError(f"Parser Error: {e}")

    def generate(self, tree):
        try:
            return ast.to_lua_source(tree)
        except Exception as e:
            raise ValueError(f"Code Generation Error: {e}")
