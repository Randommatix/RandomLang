import os
import re
import sys
import json
import shlex
import signal
import atexit
import time

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

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CARPETA_PROGRAMAS = os.path.join(
    BASE_DIR,
    "Programas"
)

CARPETA_ESTADO = os.path.join(
    os.path.expanduser("~"),
    ".randomlang"
)

ARCHIVO_PROCESOS = os.path.join(
    CARPETA_ESTADO,
    "processes.json"
)


# ==========================
# PROCESOS RANDOMLANG
# ==========================

PID_ACTUAL = os.getpid()


def preparar_estado():

    os.makedirs(
        CARPETA_ESTADO,
        exist_ok=True
    )

    if not os.path.isfile(
        ARCHIVO_PROCESOS
    ):
        with open(
            ARCHIVO_PROCESOS,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                [],
                archivo
            )


def leer_procesos():

    preparar_estado()

    try:

        with open(
            ARCHIVO_PROCESOS,
            "r",
            encoding="utf-8"
        ) as archivo:

            procesos = json.load(
                archivo
            )

        if not isinstance(
            procesos,
            list
        ):
            return []

        return procesos

    except Exception:

        return []


def guardar_procesos(
    procesos
):

    preparar_estado()

    temporal = (
        ARCHIVO_PROCESOS
        + ".tmp"
    )

    with open(
        temporal,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            procesos,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    os.replace(
        temporal,
        ARCHIVO_PROCESOS
    )


def proceso_vivo(
    pid
):

    try:

        os.kill(
            pid,
            0
        )

        return True

    except ProcessLookupError:

        return False

    except PermissionError:

        return True

    except Exception:

        return False


def limpiar_procesos():

    procesos = leer_procesos()

    vivos = []

    for proceso in procesos:

        pid = proceso.get(
            "pid"
        )

        if not isinstance(
            pid,
            int
        ):
            continue

        if proceso_vivo(
            pid
        ):
            vivos.append(
                proceso
            )

    guardar_procesos(
        vivos
    )

    return vivos


def registrar_proceso(
    nombre
):

    procesos = limpiar_procesos()

    procesos.append(
        {
            "pid": PID_ACTUAL,
            "programa": nombre,
            "ruta": os.path.join(
                CARPETA_PROGRAMAS,
                nombre + ".rl"
            ),
            "inicio": time.time()
        }
    )

    guardar_procesos(
        procesos
    )


def desregistrar_proceso():

    procesos = leer_procesos()

    procesos = [
        proceso
        for proceso in procesos
        if proceso.get("pid")
        != PID_ACTUAL
    ]

    guardar_procesos(
        procesos
    )


# ==========================
# ARGUMENTOS
# ==========================

def convertir_partes(
    entrada
):

    try:

        return shlex.split(
            entrada
        )

    except ValueError as error:

        print(
            f"Error en los argumentos: "
            f"{error}"
        )

        return None


def separar_argumentos_partes(
    partes
):

    if not partes:

        return None, None

    nombre = partes[0]

    argumentos = []

    i = 1

    while i < len(
        partes
    ):

        parte = partes[i]

        # ==========================
        # --nombre valor
        # ==========================

        if parte.startswith(
            "--"
        ):

            nombre_parametro = (
                parte[2:]
            )

            if (
                nombre_parametro
                == ""
            ):

                print(
                    "Error: parámetro "
                    "vacío."
                )

                return None, None

            # ----------------------
            # --nombre=valor
            # ----------------------

            if "=" in nombre_parametro:

                nombre_parametro, valor = (
                    nombre_parametro.split(
                        "=",
                        1
                    )
                )

                if (
                    nombre_parametro
                    == ""
                ):

                    print(
                        "Error: parámetro "
                        "vacío."
                    )

                    return None, None

                argumentos.append(
                    {
                        nombre_parametro:
                        valor
                    }
                )

                i += 1

                continue

            # ----------------------
            # --nombre valor
            # ----------------------

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

        argumentos.append(
            parte
        )

        i += 1

    return nombre, argumentos


def separar_argumentos(
    entrada
):

    partes = convertir_partes(
        entrada
    )

    if partes is None:

        return None, None

    return separar_argumentos_partes(
        partes
    )


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

        return 1

    registrar_proceso(
        nombre
    )

    codigo = ""

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

        return 0

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

        return 1

    except ErrorEjecucionRandomLang as error:

        print(
            error
        )

        return 1

    except KeyboardInterrupt:

        print(
            f"\nPrograma "
            f"'{nombre}' detenido."
        )

        return 130

    except Exception as error:

        print(
            f"Error al ejecutar "
            f"'{nombre}':"
        )

        print(
            error
        )

        return 1

    finally:

        desregistrar_proceso()


# ==========================
# REPL
# ==========================

def iniciar_repl():

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

        try:

            entrada = input(
                "RandomLang> "
            ).strip()

        except EOFError:

            print()

            break

        except KeyboardInterrupt:

            print(
                "\nHasta luego."
            )

            break

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


# ==========================
# MODO CLI
# ==========================

def iniciar_cli(
    argumentos_cli
):

    nombre, argumentos = (
        separar_argumentos_partes(
            argumentos_cli
        )
    )

    if nombre is None:

        return 1

    return ejecutar_programa(
        nombre,
        argumentos
    )


# ==========================
# MAIN
# ==========================

def main():

    preparar_estado()

    # Sin argumentos:
    # abrir REPL.
    if len(sys.argv) == 1:

        iniciar_repl()

        return 0

    # Con argumentos:
    # ejecutar directamente.
    return iniciar_cli(
        sys.argv[1:]
    )


if __name__ == "__main__":

    sys.exit(
        main()
    )