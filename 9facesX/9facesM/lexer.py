from luau_tokenizer import tokenize

class LuauLexer:
    def __init__(self, source_code: str):
        self.source_code = source_code

    def tokenize(self):
        try:
            return tokenize(self.source_code)
        except Exception as e:
            raise SyntaxError(f"Lexer Error: {e}")
