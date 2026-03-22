from latex_lexer import LatexLexer
from latex_parser import LatexParser
from utils import print_ast


def main():
    filename = "examples/ex1"

    try:
        with open(filename, "r") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
        return

    print("Input:")
    print(text)

    lexer = LatexLexer()

    print("\nTokens:")
    tokens = list(lexer.tokenize(text))
    for tok in tokens:
        print(f"{tok.type}: {tok.value}")

    parser = LatexParser()

    print("\nAST:")
    try:
        ast = parser.parse(iter(tokens))
        print_ast(ast)
    except Exception as e:
        print("Parser error:", e)


if __name__ == "__main__":
    main()
    
