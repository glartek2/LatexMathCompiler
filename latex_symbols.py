class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, var_type):
        self.symbols[name] = var_type

    def lookup(self, name):
        return self.symbols.get(name, None)
