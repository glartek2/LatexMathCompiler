from latex_symbols import SymbolTable
from latex_ast import *


class TypeChecker:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTable()
        self.errors = []

    def error(self, message, node):
        self.errors.append(f"Line {getattr(node, 'line', '?')}: {message}")

    def check(self):
        self.visit(self.ast)

        if self.errors:
            print("Semantic errors:")
            for e in self.errors:
                print(e)
        else:
            print("Semantic OK")

        return self.errors

    def visit(self, node):
        method = getattr(self, f"visit_{type(node).__name__}", self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        return None


    def visit_Program(self, node):
        return self.visit(node.expr)


    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"


    def visit_Identifier(self, node):
        t = self.symbol_table.lookup(node.name)

        if t is None:
            return "float"

        return t


    def visit_BinExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left == "float" or right == "float":
            return "float"

        if left == "int" and right == "int":
            return "int"

        self.error(f"Incompatible types: {left} {node.op} {right}", node)
        return None


    def visit_Power(self, node):
        base = self.visit(node.base)
        exp = self.visit(node.exponent)

        if base in ("int", "float") and exp in ("int", "float"):
            return "float"

        self.error("Invalid types for power", node)
        return None


    def visit_Fraction(self, node):
        num = self.visit(node.numerator)
        den = self.visit(node.denominator)

        if num in ("int", "float") and den in ("int", "float"):
            return "float"

        self.error("Invalid types in fraction", node)
        return None


    def visit_FunctionCall(self, node):
        arg_types = [self.visit(arg) for arg in node.args]

        for t in arg_types:
            if t not in ("int", "float"):
                self.error(f"Invalid argument type for function {node.name}", node)
                return None

        return "float"


    def visit_Group(self, node):
        return self.visit(node.expr)


    def visit_UnaryExpr(self, node):
        t = self.visit(node.expr)

        if t in ("int", "float"):
            return t

        self.error("Invalid unary operation", node)
        return None
