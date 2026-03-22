
def print_ast(node, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{node.__class__.__name__}")

    for attr, value in vars(node).items():
        if isinstance(value, list):
            for item in value:
                if hasattr(item, '__dict__'):
                    print_ast(item, indent + 1)
                else:
                    print(f"{prefix}  {item}")
        elif hasattr(value, '__dict__'):
            print_ast(value, indent + 1)
        else:
            print(f"{prefix}  {attr}: {value}")
