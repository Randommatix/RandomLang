import os
from tokenizer import tokenize
from parser import Parser
from interpreter import Interpreter


# ==========================
# CONFIGURACIÓN
# ==========================

CARPETA_PROGRAMAS = "Programas"


# ==========================
# EJECUTAR PROGRAMA
# ==========================

def ejecutar_programa(nombre):

    if nombre.endswith(".rl"):

        nombre = nombre[:-3]


    ruta = os.path.join(
        CARPETA_PROGRAMAS,
        nombre + ".rl"
    )


    if not os.path.isfile(ruta):

        print(
            f"No existe el programa '{nombre}'."
        )

        return


    try:

        # ==========================
        # LEER PROGRAMA
        # ==========================

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:

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


    except Exception as error:

        print(
            f"Error al ejecutar '{nombre}':"
        )

        print(error)


# ==========================
# CONSOLA RANDOMLANG
# ==========================

print("=== RANDOMLANG ===")
print(
    "Escribe el nombre de un programa para ejecutarlo."
)
print(
    "Los programas se encuentran en la carpeta 'Programas/'."
)
print(
    "Escribe 'salir' para cerrar."
)
print()


while True:

    nombre = input("RandomLang> ").strip()


    if nombre.lower() == "salir":

        print("Hasta luego.")

        break


    if nombre == "":

        continue


    ejecutar_programa(nombre)