class Memory:
    def __init__(self):
        self.variables = {}

    def get(self, name):
        return self.variables.get(name, None)

    def put(self, name, value):
        self.variables[name] = value
