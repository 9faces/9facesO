class LuauLexer:
    def __init__(self, c): self.code = c
    def strip_whitespace(self): return self.code.replace('\r\n', '\n')
