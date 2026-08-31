class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        if self.valor is None:
            return self.tipo

        return f"{self.tipo}({self.valor})"


def tokenizar_linea(linea, tokens):
    i = 0

    while i < len(linea):

        caracter = linea[i]

        # Espacios dentro de la línea
        if caracter in " \t":
            i += 1
            continue

        # Palabras
        if caracter.isalpha() or caracter == "_":

            palabra = ""

            while (
                i < len(linea)
                and (
                    linea[i].isalnum()
                    or linea[i] == "_"
                )
            ):
                palabra += linea[i]
                i += 1

            palabras_reservadas = {
                "guardar": "GUARDAR",
                "mostrar": "MOSTRAR",
                "si": "SI",
                "sino": "SINO"
            }

            if palabra in palabras_reservadas:
                tokens.append(
                    Token(
                        palabras_reservadas[palabra],
                        palabra
                    )
                )

            else:
                tokens.append(
                    Token("IDENTIFICADOR", palabra)
                )

            continue


        # Números
        if caracter.isdigit():

            numero = ""

            while (
                i < len(linea)
                and linea[i].isdigit()
            ):
                numero += linea[i]
                i += 1

            tokens.append(
                Token("NUMERO", int(numero))
            )

            continue


        # Operadores dobles
        if linea[i:i + 2] == ">=":
            tokens.append(Token("MAYOR_IGUAL", ">="))
            i += 2
            continue

        elif linea[i:i + 2] == "<=":
            tokens.append(Token("MENOR_IGUAL", "<="))
            i += 2
            continue

        elif linea[i:i + 2] == "==":
            tokens.append(Token("IGUAL_IGUAL", "=="))
            i += 2
            continue

        elif linea[i:i + 2] == "!=":
            tokens.append(Token("DIFERENTE", "!="))
            i += 2
            continue


        # Operadores simples
        operadores = {
            "=": "IGUAL",
            "+": "MAS",
            "-": "MENOS",
            "*": "MULTIPLICAR",
            "/": "DIVIDIR",
            "(": "PAREN_IZQ",
            ")": "PAREN_DER",
            ">": "MAYOR",
            "<": "MENOR",
            ":": "DOS_PUNTOS"
        }

        if caracter in operadores:

            tokens.append(
                Token(
                    operadores[caracter],
                    caracter
                )
            )

            i += 1
            continue


        raise Exception(
            f"Carácter desconocido: {caracter}"
        )


def tokenize(codigo):

    tokens = []

    lineas = codigo.splitlines()

    niveles_indentacion = [0]

    for linea in lineas:

        # Ignorar líneas vacías
        if not linea.strip():
            continue

        # Calcular espacios iniciales
        espacios = len(linea) - len(linea.lstrip(" "))

        # INDENT
        if espacios > niveles_indentacion[-1]:

            niveles_indentacion.append(espacios)

            tokens.append(Token("INDENT"))


        # DEDENT
        elif espacios < niveles_indentacion[-1]:

            while espacios < niveles_indentacion[-1]:

                niveles_indentacion.pop()

                tokens.append(Token("DEDENT"))

            if espacios != niveles_indentacion[-1]:
                raise Exception(
                    "Indentación incorrecta"
                )


        # Tokenizar contenido sin espacios iniciales
        contenido = linea.lstrip(" ")

        tokenizar_linea(
            contenido,
            tokens
        )

        # Fin de instrucción
        tokens.append(Token("NUEVA_LINEA"))


    # Cerrar indentaciones pendientes
    while len(niveles_indentacion) > 1:

        niveles_indentacion.pop()

        tokens.append(Token("DEDENT"))

    return tokens