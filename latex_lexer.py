from sly import Lexer


class LatexLexer(Lexer):


    tokens = {
        'COMMAND',
        'ID', 'INT', 'FLOAT',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'POWER',
        'LBRACE', 'RBRACE',
        'LPAREN', 'RPAREN',
    }


    ignore = ' \t'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    POWER = r'\^'

    LBRACE = r'\{'
    RBRACE = r'\}'
    LPAREN = r'\('
    RPAREN = r'\)'

    COMMAND = r'\\[a-zA-Z]+'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    FLOAT = r'([0-9]+\.[0-9]*|\.[0-9]+)'
    INT = r'\d+'

    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1
        