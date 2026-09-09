class GuardarVariable:

    def __init__(self, nombre, valor):

        self.nombre = nombre
        self.valor = valor


    def __repr__(self):

        return (
            f"GuardarVariable("
            f"{self.nombre}, "
            f"{self.valor}"
            f")"
        )


class Mostrar:

    def __init__(self, valor):

        self.valor = valor


    def __repr__(self):

        return f"Mostrar({self.valor})"


class Numero:

    def __init__(self, valor):

        self.valor = valor


    def __repr__(self):

        return f"Numero({self.valor})"


class Texto:

    def __init__(self, valor):

        self.valor = valor


    def __repr__(self):

        return f"Texto({self.valor})"


class Variable:

    def __init__(self, nombre):

        self.nombre = nombre


    def __repr__(self):

        return f"Variable({self.nombre})"


class Operacion:

    def __init__(
        self,
        izquierda,
        operador,
        derecha
    ):

        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha


    def __repr__(self):

        return (
            f"Operacion("
            f"{self.izquierda} "
            f"{self.operador} "
            f"{self.derecha}"
            f")"
        )


class Si:

    def __init__(
        self,
        condicion,
        bloque_si,
        bloque_sino=None
    ):

        self.condicion = condicion
        self.bloque_si = bloque_si
        self.bloque_sino = bloque_sino


    def __repr__(self):

        return (
            f"Si("
            f"condicion={self.condicion}, "
            f"bloque_si={self.bloque_si}, "
            f"bloque_sino={self.bloque_sino}"
            f")"
        )


class Mientras:

    def __init__(
        self,
        condicion,
        bloque
    ):

        self.condicion = condicion
        self.bloque = bloque


    def __repr__(self):

        return (
            f"Mientras("
            f"condicion={self.condicion}, "
            f"bloque={self.bloque}"
            f")"
        )


class Comparacion:

    def __init__(
        self,
        izquierda,
        operador,
        derecha
    ):

        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha


    def __repr__(self):

        return (
            f"Comparacion("
            f"{self.izquierda} "
            f"{self.operador} "
            f"{self.derecha}"
            f")"
        )


class LlamadaFuncion:

    def __init__(
        self,
        nombre,
        argumentos
    ):

        self.nombre = nombre
        self.argumentos = argumentos


    def __repr__(self):

        return (
            f"LlamadaFuncion("
            f"{self.nombre}, "
            f"{self.argumentos}"
            f")"
        )


class Funcion:

    def __init__(
        self,
        nombre,
        parametros,
        bloque
    ):

        self.nombre = nombre
        self.parametros = parametros
        self.bloque = bloque


    def __repr__(self):

        return (
            f"Funcion("
            f"{self.nombre}, "
            f"parametros={self.parametros}, "
            f"bloque={self.bloque}"
            f")"
        )


class Devolver:

    def __init__(self, valor):

        self.valor = valor


    def __repr__(self):

        return f"Devolver({self.valor})"


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.posicion = 0


    def actual(self):

        if self.posicion >= len(self.tokens):

            return None

        return self.tokens[
            self.posicion
        ]


    def avanzar(self):

        self.posicion += 1


    def parsear(self):

        instrucciones = []


        while self.actual() is not None:

            if self.actual().tipo == "NUEVA_LINEA":

                self.avanzar()

                continue


            instrucciones.append(
                self.parsear_instruccion()
            )


        return instrucciones


    def parsear_instruccion(self):

        token = self.actual()


        if token.tipo == "GUARDAR":

            return self.parsear_guardar()


        elif token.tipo == "MOSTRAR":

            return self.parsear_mostrar()


        elif token.tipo == "SI":

            return self.parsear_si()


        elif token.tipo == "MIENTRAS":

            return self.parsear_mientras()


        elif token.tipo == "FUNCION":

            return self.parsear_funcion()


        elif token.tipo == "DEVOLVER":

            return self.parsear_devolver()


        elif token.tipo == "IDENTIFICADOR":

            if (
                self.posicion + 1 < len(self.tokens)
                and self.tokens[
                    self.posicion + 1
                ].tipo == "PAREN_IZQ"
            ):

                llamada = self.parsear_llamada_funcion()


                if self.actual().tipo != "NUEVA_LINEA":

                    raise Exception(
                        "Se esperaba NUEVA_LINEA después de "
                        "la llamada a la función"
                    )


                self.avanzar()

                return llamada


        raise Exception(
            f"Instrucción inesperada: {token}"
        )


    def parsear_guardar(self):

        self.avanzar()


        if self.actual().tipo != "IDENTIFICADOR":

            raise Exception(
                "Se esperaba un identificador después de 'guardar'"
            )


        nombre = self.actual().valor

        self.avanzar()


        if self.actual().tipo != "IGUAL":

            raise Exception(
                "Se esperaba '=' después del identificador"
            )


        self.avanzar()


        valor = self.parsear_expresion()


        if self.actual().tipo != "NUEVA_LINEA":

            raise Exception(
                "Se esperaba NUEVA_LINEA después de la expresión"
            )


        self.avanzar()


        return GuardarVariable(
            nombre,
            valor
        )


    def parsear_mostrar(self):

        self.avanzar()


        valor = self.parsear_expresion()


        if self.actual().tipo != "NUEVA_LINEA":

            raise Exception(
                "Se esperaba NUEVA_LINEA después de 'mostrar'"
            )


        self.avanzar()


        return Mostrar(
            valor
        )


    def parsear_devolver(self):

        self.avanzar()


        valor = self.parsear_expresion()


        if self.actual().tipo != "NUEVA_LINEA":

            raise Exception(
                "Se esperaba NUEVA_LINEA después de 'devolver'"
            )


        self.avanzar()


        return Devolver(
            valor
        )


    def parsear_funcion(self):

        self.avanzar()


        if self.actual().tipo != "IDENTIFICADOR":

            raise Exception(
                "Se esperaba un nombre después de 'funcion'"
            )


        nombre = self.actual().valor

        self.avanzar()


        parametros = []


        # ==========================
        # PARÁMETROS
        # ==========================

        if self.actual().tipo == "PAREN_IZQ":

            self.avanzar()


            if self.actual().tipo != "PAREN_DER":

                if self.actual().tipo != "IDENTIFICADOR":

                    raise Exception(
                        "Se esperaba un nombre de parámetro"
                    )


                parametros.append(
                    self.actual().valor
                )

                self.avanzar()


                while self.actual().tipo == "COMA":

                    self.avanzar()


                    if self.actual().tipo != "IDENTIFICADOR":

                        raise Exception(
                            "Se esperaba un nombre de parámetro "
                            "después de ','"
                        )


                    parametros.append(
                        self.actual().valor
                    )

                    self.avanzar()


            if self.actual().tipo != "PAREN_DER":

                raise Exception(
                    "Se esperaba ')' después de los parámetros"
                )


            self.avanzar()


        if self.actual().tipo != "DOS_PUNTOS":

            raise Exception(
                "Se esperaba ':' después de la función"
            )


        self.avanzar()


        if self.actual().tipo != "NUEVA_LINEA":

            raise Exception(
                "Se esperaba NUEVA_LINEA después de ':'"
            )


        self.avanzar()


        if self.actual().tipo != "INDENT":

            raise Exception(
                "Se esperaba INDENT después de 'funcion'"
            )


        self.avanzar()


        bloque = self.parsear_bloque()


        if self.actual().tipo != "DEDENT":

            raise Exception(
                "Se esperaba DEDENT al terminar la función"
            )


        self.avanzar()


        return Funcion(
            nombre,
            parametros,
            bloque
        )


    def parsear_si(self):

        self.avanzar()


        condicion = self.parsear_condicion()


        if self.actual().tipo != "DOS_PUNTOS":

            raise Exception(
                "Se esperaba ':' después de la condición"
            )


        self.avanzar()


        if self.actual().tipo != "NUEVA_LINEA":

            raise Exception(
                "Se esperaba NUEVA_LINEA después de ':'"
            )


        self.avanzar()


        if self.actual().tipo != "INDENT":

            raise Exception(
                "Se esperaba INDENT después de 'si'"
            )


        self.avanzar()


        bloque_si = self.parsear_bloque()


        if self.actual().tipo != "DEDENT":

            raise Exception(
                "Se esperaba DEDENT al terminar el bloque"
            )


        self.avanzar()


        bloque_sino = None


        if (
            self.actual() is not None
            and self.actual().tipo == "SINO"
        ):

            self.avanzar()


            if self.actual().tipo != "DOS_PUNTOS":

                raise Exception(
                    "Se esperaba ':' después de 'sino'"
                )


            self.avanzar()


            if self.actual().tipo != "NUEVA_LINEA":

                raise Exception(
                    "Se esperaba NUEVA_LINEA después de ':'"
                )


            self.avanzar()


            if self.actual().tipo != "INDENT":

                raise Exception(
                    "Se esperaba INDENT después de 'sino'"
                )


            self.avanzar()


            bloque_sino = self.parsear_bloque()


            if self.actual().tipo != "DEDENT":

                raise Exception(
                    "Se esperaba DEDENT al terminar el bloque"
                )


            self.avanzar()


        return Si(
            condicion,
            bloque_si,
            bloque_sino
        )


    def parsear_mientras(self):

        self.avanzar()


        condicion = self.parsear_condicion()


        if self.actual().tipo != "DOS_PUNTOS":

            raise Exception(
                "Se esperaba ':' después de la condición"
            )


        self.avanzar()


        if self.actual().tipo != "NUEVA_LINEA":

            raise Exception(
                "Se esperaba NUEVA_LINEA después de ':'"
            )


        self.avanzar()


        if self.actual().tipo != "INDENT":

            raise Exception(
                "Se esperaba INDENT después de 'mientras'"
            )


        self.avanzar()


        bloque = self.parsear_bloque()


        if self.actual().tipo != "DEDENT":

            raise Exception(
                "Se esperaba DEDENT al terminar el bloque"
            )


        self.avanzar()


        return Mientras(
            condicion,
            bloque
        )


    def parsear_bloque(self):

        instrucciones = []


        while (
            self.actual() is not None
            and self.actual().tipo != "DEDENT"
        ):

            if self.actual().tipo == "NUEVA_LINEA":

                self.avanzar()

                continue


            instrucciones.append(
                self.parsear_instruccion()
            )


        return instrucciones


    def parsear_condicion(self):

        izquierda = self.parsear_expresion()


        operadores = {

            "MAYOR": ">",

            "MENOR": "<",

            "MAYOR_IGUAL": ">=",

            "MENOR_IGUAL": "<=",

            "IGUAL_IGUAL": "==",

            "DIFERENTE": "!="

        }


        token = self.actual()


        if token.tipo not in operadores:

            raise Exception(
                f"Se esperaba un operador de comparación, "
                f"pero apareció: {token}"
            )


        operador = operadores[
            token.tipo
        ]


        self.avanzar()


        derecha = self.parsear_expresion()


        return Comparacion(
            izquierda,
            operador,
            derecha
        )


    def parsear_expresion(self):

        izquierda = self.parsear_termino()


        while self.actual() is not None:

            if self.actual().tipo == "MAS":

                self.avanzar()

                derecha = self.parsear_termino()

                izquierda = Operacion(
                    izquierda,
                    "+",
                    derecha
                )


            elif self.actual().tipo == "MENOS":

                self.avanzar()

                derecha = self.parsear_termino()

                izquierda = Operacion(
                    izquierda,
                    "-",
                    derecha
                )


            else:

                break


        return izquierda


    def parsear_termino(self):

        izquierda = self.parsear_valor()


        while self.actual() is not None:

            if self.actual().tipo == "MULTIPLICAR":

                self.avanzar()

                derecha = self.parsear_valor()

                izquierda = Operacion(
                    izquierda,
                    "*",
                    derecha
                )


            elif self.actual().tipo == "DIVIDIR":

                self.avanzar()

                derecha = self.parsear_valor()

                izquierda = Operacion(
                    izquierda,
                    "/",
                    derecha
                )


            else:

                break


        return izquierda


    def parsear_valor(self):

        token = self.actual()


        if token.tipo == "NUMERO":

            self.avanzar()

            return Numero(
                token.valor
            )


        elif token.tipo == "STRING":

            self.avanzar()

            return Texto(
                token.valor
            )


        elif token.tipo == "IDENTIFICADOR":

            nombre = token.valor

            self.avanzar()


            if (
                self.actual() is not None
                and self.actual().tipo == "PAREN_IZQ"
            ):

                return self.parsear_llamada_funcion(
                    nombre
                )


            return Variable(
                nombre
            )


        elif token.tipo == "PAREN_IZQ":

            self.avanzar()


            expresion = self.parsear_expresion()


            if self.actual().tipo != "PAREN_DER":

                raise Exception(
                    "Se esperaba ')'"
                )


            self.avanzar()


            return expresion


        else:

            raise Exception(
                f"Valor inesperado: {token}"
            )


    def parsear_llamada_funcion(
        self,
        nombre=None
    ):

        if nombre is None:

            nombre = self.actual().valor

            self.avanzar()


        if self.actual().tipo != "PAREN_IZQ":

            raise Exception(
                "Se esperaba '(' después del nombre de la función"
            )


        self.avanzar()


        argumentos = []


        if self.actual().tipo == "PAREN_DER":

            self.avanzar()

            return LlamadaFuncion(
                nombre,
                argumentos
            )


        argumentos.append(
            self.parsear_expresion()
        )


        while (
            self.actual() is not None
            and self.actual().tipo == "COMA"
        ):

            self.avanzar()


            argumentos.append(
                self.parsear_expresion()
            )


        if self.actual().tipo != "PAREN_DER":

            raise Exception(
                "Se esperaba ')' al terminar los argumentos"
            )


        self.avanzar()


        return LlamadaFuncion(
            nombre,
            argumentos
        )