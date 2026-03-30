from fastapi import FastAPI
from pydantic import BaseModel

from latex_lexer import LatexLexer
from latex_parser import LatexParser
from latex_type_checker import TypeChecker
from latex_interpreter import Interpreter

from utils import print_ast

app = FastAPI()


class RequestModel(BaseModel):
    expression: str
    variables: dict = {}


class ResponseModel(BaseModel):
    result: float | None = None
    errors: list[str] | None = None


@app.post("/calculate", response_model=ResponseModel)
def calculate(req: RequestModel):
    try:
        lexer = LatexLexer()
        tokens = list(lexer.tokenize(req.expression))

        parser = LatexParser()
        ast = parser.parse(iter(tokens))

        print_ast(ast)

        checker = TypeChecker(ast)
        errors = checker.check()

        if errors:
            return ResponseModel(result=None, errors=errors)

        interpreter = Interpreter()

        for name, value in req.variables.items():
            interpreter.memory.put(name, value)

        # interpreter.memory.put("pi", 3.141592653589793)

        result = interpreter.visit(ast)

        return ResponseModel(result=result, errors=None)

    except Exception as e:
        print("Parser error:", e)

        return ResponseModel(result=None, errors=[str(e)])
