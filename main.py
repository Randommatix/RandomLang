from tokenizer import tokenize
from parser import Parser
from interpreter import Interpreter


# ==========================
# LEER PROGRAMA
# ==========================

with open("programa.rl", "r", encoding="utf-8") as archivo:
    codigo = archivo.read()


# ==========================
# TOKENIZER
# ==========================

tokens = tokenize(codigo)


# ==========================
# PARSER
# ==========================

parser = Parser(tokens)

ast = parser.parsear()


# ==========================
# INTÉRPRETE
# ==========================

interpreter = Interpreter()

interpreter.ejecutar(ast)