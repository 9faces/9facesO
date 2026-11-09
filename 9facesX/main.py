import argparse
import sys
from 9facesM.lexer import LuauLexer
from 9facesM.parser import LuauParser
from 9facesM.transformer import ASTTransformer
from 9facesM.integrity import check_integrity

HEADER = """-- [[ 9faces v1.5.4 ]] --
-- [[ NO SKID~ :0 ]] --

"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--dev", action="store_true")
    
    args = parser.parse_args()

    if not args.dev:
        check_integrity()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            source_code = f.read()

        print("[*] Initializing Lexer...")
        lexer = LuauLexer(source_code)
        tokens = lexer.tokenize()

        print("[*] Parsing to AST...")
        parser = LuauParser(tokens)
        ast_tree = parser.parse()

        print("[*] Applying Obfuscation...")
        transformer = ASTTransformer()
        obfuscated_ast = transformer.transform(ast_tree)

        print("[*] Generating Output...")
        final_code = parser.generate(obfuscated_ast)

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(HEADER + final_code)

        print(f"[+] Success! Obfuscated script saved to: {args.output}")

    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
