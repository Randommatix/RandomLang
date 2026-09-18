import os
import re

from tokenizer import tokenize
from parser import Parser
from interpreter import (
    Interpreter,
    ErrorEjecucionRandomLang,
    ErrorRandomLang
)


# ==========================
# CONFIGURACIÓN
# ==========================

CARPETA_PROGRAMAS = "Programas"


# ==========================
# ARGUMENTOS
# ==========================

def separar_argumentos(
    entrada
):

    # Permite cosas como:
    #
    # programa --"hola"
    #
    # programa --nombre "Randommatix"
    #
    # programa --nombre "Randommatix" --edad 20

    patron = (
        r'--"[^"]*"'
        r'|"[^"]*"'
        r'|\S+'
    )

    partes = re.findall(
        patron,
        entrada
    )

    if not partes:

        return None, None

    nombre = partes[0]

    argumentos = []

    i = 1

    while i < len(partes):

        parte = partes[i]

        # ==========================
        # --"valor"
        # ==========================

        if (
            parte.startswith(
                '--"'
            )
            and parte.endswith(
                '"'
            )
        ):

            valor = parte[
                3:-1
            ]

            argumentos.append(
                valor
            )

            i += 1

            continue

        # ==========================
        # --nombre "valor"
        # ==========================

        if parte.startswith(
            "--"
        ):

            nombre_parametro = (
                parte[2:]
            )

            if nombre_parametro == "":

                print(
                    "Error: parámetro "
                    "vacío."
                )

                return None, None

            if i + 1 >= len(
                partes
            ):

                print(
                    f"Error: el parámetro "
                    f"'--{nombre_parametro}' "
                    "necesita un valor."
                )

                return None, None

            valor = partes[
                i + 1
            ]

            if (
                valor.startswith(
                    '"'
                )
                and valor.endswith(
                    '"'
                )
            ):

                valor = valor[
                    1:-1
                ]

            argumentos.append(
                {
                    nombre_parametro:
                    valor
                }
            )

            i += 2

            continue

        # ==========================
        # ARGUMENTO NORMAL
        # ==========================

        if (
            parte.startswith(
                '"'
            )
            and parte.endswith(
                '"'
            )
        ):

            parte = parte[
                1:-1
            ]

        argumentos.append(
            parte
        )

        i += 1

    return nombre, argumentos


# ==========================
# EJECUTAR PROGRAMA
# ==========================

def ejecutar_programa(
    nombre,
    argumentos=None
):

    if argumentos is None:

        argumentos = []

    if nombre.endswith(
        ".rl"
    ):

        nombre = nombre[:-3]

    ruta = os.path.join(
        CARPETA_PROGRAMAS,
        nombre + ".rl"
    )

    if not os.path.isfile(
        ruta
    ):

        print(
            f"No existe el programa "
            f"'{nombre}'."
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

        tokens = tokenize(
            codigo
        )

        # ==========================
        # PARSER
        # ==========================

        parser = Parser(
            tokens
        )

        ast = parser.parsear()

        # ==========================
        # INTERPRETE
        # ==========================

        interpreter = Interpreter(
            carpeta_programas=
            CARPETA_PROGRAMAS,

            argumentos=
            argumentos,

            archivo_actual=
            ruta,

            codigo_actual=
            codigo
        )

        interpreter.ejecutar(
            ast
        )

    except ErrorRandomLang as error:

        print(
            f"Error en '{nombre}':"
        )

        print(
            ErrorEjecucionRandomLang(
                error.mensaje,
                ruta,
                error.linea,
                codigo
            )
        )

    except ErrorEjecucionRandomLang as error:

        print(
            error
        )

    except Exception as error:

        print(
            f"Error al ejecutar "
            f"'{nombre}':"
        )

        print(
            error
        )


# ==========================
# CONSOLA RANDOMLANG
# ==========================

print(
    "=== RANDOMLANG ==="
)

print(
    "Escribe el nombre de un "
    "programa para ejecutarlo."
)

print(
    "Los programas se encuentran "
    "en la carpeta 'Programas/'."
)

print(
    "Puedes pasar parámetros al programa."
)

print(
    "Escribe 'salir' para cerrar."
)

print()


while True:

    entrada = input(
        "RandomLang> "
    ).strip()

    if (
        entrada.lower()
        == "salir"
    ):

        print(
            "Hasta luego."
        )

        break

    if entrada == "":

        continue

    nombre, argumentos = (
        separar_argumentos(
            entrada
        )
    )

    if nombre is None:

        continue

    ejecutar_programa(
        nombre,
        argumentos
    )