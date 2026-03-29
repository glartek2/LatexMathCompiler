import math
from latex_ast import *
from memory import *
from visit import on, when


class Interpreter:
    def __init__(self):
        self.memory = Memory()

    @on('node')
    def visit(self, node):
        pass


    @when(Program)
    def visit(self, node):
        return self.visit(node.expr)


    @when(IntNum)
    def visit(self, node):
        return node.value

    @when(FloatNum)
    def visit(self, node):
        return node.value


    @when(Identifier)
    def visit(self, node):
        value = self.memory.get(node.name)

        if value is None:
            return 1.0

        return value


    @when(BinExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right

        raise RuntimeError(f"Unknown operator {node.op}")


    @when(Power)
    def visit(self, node):
        base = self.visit(node.base)
        exp = self.visit(node.exponent)
        return base ** exp


    @when(Fraction)
    def visit(self, node):
        num = self.visit(node.numerator)
        den = self.visit(node.denominator)

        if den == 0:
            raise ZeroDivisionError("Division by zero in fraction")

        return num / den


    @when(FunctionCall)
    def visit(self, node):
        arg = self.visit(node.args[0])

        functions = {
            "sin": math.sin,
            "cos": math.cos,
            "log": math.log,
            "sqrt": math.sqrt,
        }

        if node.name not in functions:
            raise RuntimeError(f"Unknown function {node.name}")

        return functions[node.name](arg)


    @when(Group)
    def visit(self, node):
        return self.visit(node.expr)


    @when(UnaryExpr)
    def visit(self, node):
        val = self.visit(node.expr)

        if node.op == '-':
            return -val

        raise RuntimeError(f"Unknown unary operator {node.op}")
