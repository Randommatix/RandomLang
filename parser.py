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

class GuardarVariable:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def __repr__(self):
        return f"GuardarVariable({self.nombre}, {self.valor})"


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


class Variable:
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Variable({self.nombre})"


class Operacion:
    def __init__(self, izquierda, operador, derecha):
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


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0


    def actual(self):

        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]

        return None


    def avanzar(self):
        self.posicion += 1


    def esperar(self, tipo):

        token = self.actual()

        if token is None or token.tipo != tipo:
            raise Exception(
                f"Se esperaba {tipo}, "
                f"pero se encontró {token}"
            )

        self.avanzar()

        return token


    # ==========================
    # PROGRAMA
    # ==========================

    def parsear(self):

        programa = []

        while self.actual() is not None:

            # Ignorar saltos de línea
            if self.actual().tipo == "NUEVA_LINEA":
                self.avanzar()
                continue

            programa.append(
                self.parsear_instruccion()
            )

        return programa


    # ==========================
    # INSTRUCCIÓN
    # ==========================

    def parsear_instruccion(self):

        token = self.actual()

        if token.tipo == "GUARDAR":
            return self.parsear_guardar()

        elif token.tipo == "MOSTRAR":
            return self.parsear_mostrar()

        elif token.tipo == "SI":
            return self.parsear_si()

        else:
            raise Exception(
                f"Instrucción inesperada: {token}"
            )


    # ==========================
    # GUARDAR
    # ==========================

    def parsear_guardar(self):

        self.avanzar()

        nombre = self.esperar("IDENTIFICADOR")

        self.esperar("IGUAL")

        valor = self.parsear_expresion()

        self.esperar("NUEVA_LINEA")

        return GuardarVariable(
            nombre.valor,
            valor
        )


    # ==========================
    # MOSTRAR
    # ==========================

    def parsear_mostrar(self):

        self.avanzar()

        valor = self.parsear_expresion()

        self.esperar("NUEVA_LINEA")

        return Mostrar(valor)


    # ==========================
    # SI / SINO
    # ==========================

    def parsear_si(self):

        # Saltar SI
        self.avanzar()

        condicion = self.parsear_condicion()

        self.esperar("DOS_PUNTOS")

        self.esperar("NUEVA_LINEA")

        # Inicio del bloque
        self.esperar("INDENT")

        bloque_si = self.parsear_bloque()

        self.esperar("DEDENT")


        bloque_sino = None

        # ¿Existe SINO?
        if (
            self.actual() is not None
            and self.actual().tipo == "SINO"
        ):

            self.avanzar()

            self.esperar("DOS_PUNTOS")

            self.esperar("NUEVA_LINEA")

            self.esperar("INDENT")

            bloque_sino = self.parsear_bloque()

            self.esperar("DEDENT")


        return Si(
            condicion,
            bloque_si,
            bloque_sino
        )


    # ==========================
    # BLOQUE
    # ==========================

    def parsear_bloque(self):

        bloque = []

        while (
            self.actual() is not None
            and self.actual().tipo != "DEDENT"
        ):

            if self.actual().tipo == "NUEVA_LINEA":
                self.avanzar()
                continue

            bloque.append(
                self.parsear_instruccion()
            )

        return bloque


    # ==========================
    # CONDICIONES
    # ==========================

    def parsear_condicion(self):

        izquierda = self.parsear_expresion()

        token = self.actual()

        operadores = [
            "MAYOR",
            "MENOR",
            "MAYOR_IGUAL",
            "MENOR_IGUAL",
            "IGUAL_IGUAL",
            "DIFERENTE"
        ]

        if token is None or token.tipo not in operadores:
            raise Exception(
                "Se esperaba un operador de comparación"
            )

        operador = token.valor

        self.avanzar()

        derecha = self.parsear_expresion()

        return Comparacion(
            izquierda,
            operador,
            derecha
        )


    # ==========================
    # EXPRESIONES
    # ==========================

    def parsear_expresion(self):

        izquierda = self.parsear_termino()

        while (
            self.actual() is not None
            and self.actual().tipo in [
                "MAS",
                "MENOS"
            ]
        ):

            operador = self.actual().valor

            self.avanzar()

            derecha = self.parsear_termino()

            izquierda = Operacion(
                izquierda,
                operador,
                derecha
            )

        return izquierda


    # ==========================
    # * y /
    # ==========================

    def parsear_termino(self):

        izquierda = self.parsear_valor()

        while (
            self.actual() is not None
            and self.actual().tipo in [
                "MULTIPLICAR",
                "DIVIDIR"
            ]
        ):

            operador = self.actual().valor

            self.avanzar()

            derecha = self.parsear_valor()

            izquierda = Operacion(
                izquierda,
                operador,
                derecha
            )

        return izquierda


    # ==========================
    # VALORES
    # ==========================

    def parsear_valor(self):

        token = self.actual()

        if token is None:
            raise Exception(
                "Se esperaba un valor"
            )


        if token.tipo == "NUMERO":

            self.avanzar()

            return Numero(token.valor)


        elif token.tipo == "IDENTIFICADOR":

            self.avanzar()

            return Variable(token.valor)


        elif token.tipo == "PAREN_IZQ":

            self.avanzar()

            expresion = self.parsear_expresion()

            self.esperar("PAREN_DER")

            return expresion


        else:
            raise Exception(
                f"Valor inesperado: {token}"
            )