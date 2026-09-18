import re


class Token:
    def __init__(self, tipo, valor=None, linea=1):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return (
            f"Token("
            f"{self.tipo}, "
            f"{self.valor!r}, "
            f"línea={self.linea}"
            f")"
        )


PALABRAS = {
    "guardar": "GUARDAR",
    "mostrar": "MOSTRAR",
    "si": "SI",
    "sino": "SINO",
    "mientras": "MIENTRAS",
    "para": "PARA",
    "cada": "CADA",
    "en": "EN",
    "funcion": "FUNCION",
    "devolver": "DEVOLVER",
    "extraer": "EXTRAER",
    "Verdadero": "VERDADERO",
    "Falso": "FALSO",
    "Nulo": "NULO",
    "romper": "ROMPER",
    "continuar": "CONTINUAR",
}


def tokenize(codigo):
    tokens = []

    lineas = codigo.splitlines()

    niveles_indentacion = [0]
    profundidad = 0

    for numero_linea, linea in enumerate(
        lineas,
        start=1
    ):
        texto = linea.rstrip()

        if texto.strip() == "":
            continue

        espacios = len(linea) - len(linea.lstrip(" "))

        contenido = linea.lstrip(" ")

        # Dentro de listas/diccionarios/paréntesis
        # no se generan INDENT/DEDENT.
        if profundidad == 0:
            if espacios > niveles_indentacion[-1]:
                niveles_indentacion.append(espacios)
                tokens.append(
                    Token(
                        "INDENT",
                        None,
                        numero_linea
                    )
                )

            elif espacios < niveles_indentacion[-1]:
                while (
                    espacios
                    < niveles_indentacion[-1]
                ):
                    niveles_indentacion.pop()

                    tokens.append(
                        Token(
                            "DEDENT",
                            None,
                            numero_linea
                        )
                    )

                if (
                    espacios
                    != niveles_indentacion[-1]
                ):
                    raise Exception(
                        f"Indentación inválida en "
                        f"la línea {numero_linea}"
                    )

        i = 0

        while i < len(contenido):
            caracter = contenido[i]

            if caracter.isspace():
                i += 1
                continue

            # STRING
            if caracter == '"':
                inicio = i
                i += 1

                valor = ""

                while i < len(contenido):
                    if contenido[i] == '"':
                        break

                    valor += contenido[i]
                    i += 1

                if i >= len(contenido):
                    raise Exception(
                        f"Texto sin cerrar en "
                        f"la línea {numero_linea}"
                    )

                i += 1

                tokens.append(
                    Token(
                        "STRING",
                        valor,
                        numero_linea
                    )
                )

                continue

            # NÚMERO
            if caracter.isdigit():
                inicio = i

                while (
                    i < len(contenido)
                    and (
                        contenido[i].isdigit()
                        or contenido[i] == "."
                    )
                ):
                    i += 1

                texto_numero = contenido[
                    inicio:i
                ]

                if "." in texto_numero:
                    valor = float(
                        texto_numero
                    )
                else:
                    valor = int(
                        texto_numero
                    )

                tokens.append(
                    Token(
                        "NUMERO",
                        valor,
                        numero_linea
                    )
                )

                continue

            # IDENTIFICADOR
            if (
                caracter.isalpha()
                or caracter == "_"
            ):
                inicio = i

                while (
                    i < len(contenido)
                    and (
                        contenido[i].isalnum()
                        or contenido[i] == "_"
                    )
                ):
                    i += 1

                palabra = contenido[
                    inicio:i
                ]

                tipo = PALABRAS.get(
                    palabra,
                    "IDENTIFICADOR"
                )

                tokens.append(
                    Token(
                        tipo,
                        palabra,
                        numero_linea
                    )
                )

                continue

            # OPERADORES DE DOS CARACTERES
            if contenido.startswith(
                ">=",
                i
            ):
                tokens.append(
                    Token(
                        "MAYOR_IGUAL",
                        ">=",
                        numero_linea
                    )
                )
                i += 2
                continue

            if contenido.startswith(
                "<=",
                i
            ):
                tokens.append(
                    Token(
                        "MENOR_IGUAL",
                        "<=",
                        numero_linea
                    )
                )
                i += 2
                continue

            if contenido.startswith(
                "==",
                i
            ):
                tokens.append(
                    Token(
                        "IGUAL_IGUAL",
                        "==",
                        numero_linea
                    )
                )
                i += 2
                continue

            if contenido.startswith(
                "!=",
                i
            ):
                tokens.append(
                    Token(
                        "DIFERENTE",
                        "!=",
                        numero_linea
                    )
                )
                i += 2
                continue

            simbolos = {
                "=": "IGUAL",
                "+": "MAS",
                "-": "MENOS",
                "*": "MULTIPLICAR",
                "/": "DIVIDIR",
                ">": "MAYOR",
                "<": "MENOR",
                "(": "PAREN_IZQ",
                ")": "PAREN_DER",
                "[": "CORCHETE_IZQ",
                "]": "CORCHETE_DER",
                "{": "LLAVE_IZQ",
                "}": "LLAVE_DER",
                ",": "COMA",
                ":": "DOS_PUNTOS",
            }

            if caracter in simbolos:
                tipo = simbolos[caracter]

                tokens.append(
                    Token(
                        tipo,
                        caracter,
                        numero_linea
                    )
                )

                if caracter in "([{":
                    profundidad += 1

                elif caracter in ")]}":
                    profundidad -= 1

                    if profundidad < 0:
                        raise Exception(
                            f"Símbolo de cierre "
                            f"inesperado en la línea "
                            f"{numero_linea}"
                        )

                i += 1
                continue

            raise Exception(
                f"Carácter inesperado "
                f"'{caracter}' en la línea "
                f"{numero_linea}"
            )

        if profundidad == 0:
            tokens.append(
                Token(
                    "NUEVA_LINEA",
                    None,
                    numero_linea
                )
            )

    while len(niveles_indentacion) > 1:
        niveles_indentacion.pop()

        tokens.append(
            Token(
                "DEDENT",
                None,
                len(lineas) + 1
            )
        )

    return tokens