from sly import Parser
from latex_lexer import LatexLexer
import latex_ast as AST


class LatexParser(Parser):
    tokens = LatexLexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'POWER'),
        ('right', 'UMINUS'),
    )

    @_('expr')
    def program(self, p):
        return AST.Program(p.expr)


    @_('expr PLUS term',
       'expr MINUS term')
    def expr(self, p):
        return AST.BinExpr(p[1], p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term


    @_('term TIMES power',
       'term DIVIDE power')
    def term(self, p):
        return AST.BinExpr(p[1], p.term, p.power)

    @_('term power')
    def term(self, p):
        return AST.BinExpr('*', p.term, p.power)

    @_('power')
    def term(self, p):
        return p.power


    @_('power POWER factor')
    def power(self, p):
        return AST.Power(p.power, p.factor)

    @_('factor')
    def power(self, p):
        return p.factor


    @_('MINUS factor %prec UMINUS')
    def factor(self, p):
        return AST.UnaryExpr('-', p.factor)


    @_('COMMAND LBRACE expr RBRACE LBRACE expr RBRACE')
    def factor(self, p):
        if p.COMMAND == r'\frac':
            return AST.Fraction(p.expr0, p.expr1)
        raise SyntaxError(p.COMMAND)


    @_('COMMAND LBRACE expr RBRACE')
    def factor(self, p):
        return AST.FunctionCall(p.COMMAND[1:], [p.expr])


    @_('LBRACE expr RBRACE')
    def factor(self, p):
        return AST.Group(p.expr)


    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr


    @_('ID')
    def factor(self, p):
        return AST.Identifier(p.ID)


    @_('INT')
    def factor(self, p):
        return AST.IntNum(p.INT)


    @_('FLOAT')
    def factor(self, p):
        return AST.FloatNum(p.FLOAT)


    def error(self, p):
        if p:
            print(f"Syntax error at {p.type}, value={p.value}")
        else:
            print("Syntax error at EOF")
