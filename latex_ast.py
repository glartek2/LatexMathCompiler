class Node:
    def __init__(self, line=None):
        self.line = line

    def accept(self, visitor):
        method = getattr(visitor, f'visit_{self.__class__.__name__}', None)
        if not method:
            raise Exception(f"No visit method for {self.__class__.__name__}")
        return method(self)



class IntNum(Node):
    def __init__(self, value, line=None):
        super().__init__(line)
        self.value = value


class FloatNum(Node):
    def __init__(self, value, line=None):
        super().__init__(line)
        self.value = value


class Identifier(Node):
    def __init__(self, name, line=None):
        super().__init__(line)
        self.name = name



class BinExpr(Node):
    def __init__(self, op, left, right, line=None):
        super().__init__(line)
        self.op = op
        self.left = left
        self.right = right


class UnaryExpr(Node):
    def __init__(self, op, expr, line=None):
        super().__init__(line)
        self.op = op
        self.expr = expr



class FunctionCall(Node):
    def __init__(self, name, args, line=None):
        super().__init__(line)
        self.name = name
        self.args = args



class Fraction(Node):
    def __init__(self, numerator, denominator, line=None):
        super().__init__(line)
        self.numerator = numerator
        self.denominator = denominator


class Power(Node):
    def __init__(self, base, exponent, line=None):
        super().__init__(line)
        self.base = base
        self.exponent = exponent


class Group(Node):
    def __init__(self, expr, line=None):
        super().__init__(line)
        self.expr = expr



class Program(Node):
    def __init__(self, expr, line=None):
        super().__init__(line)
        self.expr = expr
