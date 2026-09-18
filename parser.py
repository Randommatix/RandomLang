class GuardarVariable:

    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def __repr__(self):
        return f"GuardarVariable({self.nombre}, {self.valor})"


class AsignarAcceso:

    def __init__(self, acceso, valor):
        self.acceso = acceso
        self.valor = valor

    def __repr__(self):
        return (
            f"AsignarAcceso("
            f"{self.acceso}, "
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


class Booleano:

    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Booleano({self.valor})"


class Nulo:

    def __repr__(self):
        return "Nulo()"


class Lista:

    def __init__(self, elementos):
        self.elementos = elementos

    def __repr__(self):
        return f"Lista({self.elementos})"


class Diccionario:

    def __init__(self, elementos):
        self.elementos = elementos

    def __repr__(self):
        return (
            f"Diccionario("
            f"{self.elementos}"
            f")"
        )


class AccesoLista:

    def __init__(self, lista, indice):
        self.lista = lista
        self.indice = indice

    def __repr__(self):
        return (
            f"AccesoLista("
            f"{self.lista}, "
            f"{self.indice}"
            f")"
        )


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


class ParaCada:

    def __init__(
        self,
        variable,
        lista,
        bloque
    ):
        self.variable = variable
        self.lista = lista
        self.bloque = bloque

    def __repr__(self):
        return (
            f"ParaCada("
            f"variable={self.variable}, "
            f"lista={self.lista}, "
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


class Extraer:

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Extraer({self.nombre})"


class Romper:

    def __repr__(self):
        return "Romper()"


class Continuar:

    def __repr__(self):
        return "Continuar()"


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def actual(self):
        if self.posicion >= len(self.tokens):
            return None

        return self.tokens[self.posicion]

    def avanzar(self):
        self.posicion += 1

    def esperar(self, tipo):
        token = self.actual()

        if (
            token is None
            or token.tipo != tipo
        ):
            raise Exception(
                f"Se esperaba {tipo}, "
                f"pero apareció: {token}"
            )

        self.avanzar()

        return token

    def parsear(self):
        instrucciones = []

        while self.actual() is not None:
            if self.actual().tipo in (
                "NUEVA_LINEA",
                "DEDENT"
            ):
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

        if token.tipo == "MOSTRAR":
            return self.parsear_mostrar()

        if token.tipo == "SI":
            return self.parsear_si()

        if token.tipo == "MIENTRAS":
            return self.parsear_mientras()

        if token.tipo == "PARA":
            return self.parsear_para_cada()

        if token.tipo == "FUNCION":
            return self.parsear_funcion()

        if token.tipo == "DEVOLVER":
            return self.parsear_devolver()

        if token.tipo == "EXTRAER":
            return self.parsear_extraer()

        if token.tipo == "ROMPER":
            self.avanzar()
            self.esperar("NUEVA_LINEA")
            return Romper()

        if token.tipo == "CONTINUAR":
            self.avanzar()
            self.esperar("NUEVA_LINEA")
            return Continuar()

        if token.tipo == "IDENTIFICADOR":
            return self.parsear_instruccion_identificador()

        raise Exception(
            f"Instrucción inesperada: {token}"
        )

    def parsear_instruccion_identificador(self):

        nombre = self.esperar(
            "IDENTIFICADOR"
        ).valor

        if self.actual() is not None:
            if self.actual().tipo == "PAREN_IZQ":

                llamada = self.parsear_llamada_funcion(
                    nombre
                )

                self.esperar(
                    "NUEVA_LINEA"
                )

                return llamada

            if self.actual().tipo == "CORCHETE_IZQ":

                acceso = self.parsear_accesos(
                    Variable(nombre)
                )

                self.esperar("IGUAL")

                valor = self.parsear_expresion()

                self.esperar(
                    "NUEVA_LINEA"
                )

                return AsignarAcceso(
                    acceso,
                    valor
                )

        raise Exception(
            f"Se esperaba una llamada o "
            f"una asignación después de "
            f"'{nombre}'"
        )

    def parsear_guardar(self):

        self.avanzar()

        nombre = self.esperar(
            "IDENTIFICADOR"
        ).valor

        self.esperar("IGUAL")

        valor = self.parsear_expresion()

        self.esperar("NUEVA_LINEA")

        return GuardarVariable(
            nombre,
            valor
        )

    def parsear_mostrar(self):

        self.avanzar()

        valor = self.parsear_expresion()

        self.esperar("NUEVA_LINEA")

        return Mostrar(valor)

    def parsear_devolver(self):

        self.avanzar()

        valor = self.parsear_expresion()

        self.esperar("NUEVA_LINEA")

        return Devolver(valor)

    def parsear_extraer(self):

        self.avanzar()

        token = self.esperar(
            "IDENTIFICADOR"
        )

        self.esperar("NUEVA_LINEA")

        return Extraer(
            token.valor
        )

    def parsear_funcion(self):

        self.avanzar()

        nombre = self.esperar(
            "IDENTIFICADOR"
        ).valor

        parametros = []

        if (
            self.actual() is not None
            and self.actual().tipo == "PAREN_IZQ"
        ):
            self.avanzar()

            if self.actual().tipo != "PAREN_DER":
                while True:

                    parametro = self.esperar(
                        "IDENTIFICADOR"
                    )

                    parametros.append(
                        parametro.valor
                    )

                    if (
                        self.actual().tipo
                        != "COMA"
                    ):
                        break

                    self.avanzar()

            self.esperar("PAREN_DER")

        self.esperar("DOS_PUNTOS")
        self.esperar("NUEVA_LINEA")
        self.esperar("INDENT")

        bloque = self.parsear_bloque()

        self.esperar("DEDENT")

        return Funcion(
            nombre,
            parametros,
            bloque
        )

    def parsear_si(self):

        self.avanzar()

        condicion = self.parsear_condicion()

        self.esperar("DOS_PUNTOS")
        self.esperar("NUEVA_LINEA")
        self.esperar("INDENT")

        bloque_si = self.parsear_bloque()

        self.esperar("DEDENT")

        bloque_sino = None

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

    def parsear_mientras(self):

        self.avanzar()

        condicion = self.parsear_condicion()

        self.esperar("DOS_PUNTOS")
        self.esperar("NUEVA_LINEA")
        self.esperar("INDENT")

        bloque = self.parsear_bloque()

        self.esperar("DEDENT")

        return Mientras(
            condicion,
            bloque
        )

    def parsear_para_cada(self):

        self.avanzar()

        self.esperar("CADA")

        variable = self.esperar(
            "IDENTIFICADOR"
        )

        self.esperar("EN")

        lista = self.parsear_expresion()

        self.esperar("DOS_PUNTOS")
        self.esperar("NUEVA_LINEA")
        self.esperar("INDENT")

        bloque = self.parsear_bloque()

        self.esperar("DEDENT")

        return ParaCada(
            variable.valor,
            lista,
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

        if (
            token is None
            or token.tipo not in operadores
        ):
            raise Exception(
                "Se esperaba un operador "
                f"de comparación, pero apareció: "
                f"{token}"
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

        if token is None:
            raise Exception(
                "Se esperaba un valor"
            )

        if token.tipo == "NUMERO":

            self.avanzar()

            valor = Numero(
                token.valor
            )

        elif token.tipo == "STRING":

            self.avanzar()

            valor = Texto(
                token.valor
            )

        elif token.tipo == "VERDADERO":

            self.avanzar()

            valor = Booleano(True)

        elif token.tipo == "FALSO":

            self.avanzar()

            valor = Booleano(False)

        elif token.tipo == "NULO":

            self.avanzar()

            valor = Nulo()

        elif token.tipo == "IDENTIFICADOR":

            nombre = token.valor

            self.avanzar()

            if (
                self.actual() is not None
                and self.actual().tipo
                == "PAREN_IZQ"
            ):
                valor = self.parsear_llamada_funcion(
                    nombre
                )

            else:
                valor = Variable(
                    nombre
                )

        elif token.tipo == "PAREN_IZQ":

            self.avanzar()

            valor = self.parsear_expresion()

            self.esperar(
                "PAREN_DER"
            )

        elif token.tipo == "CORCHETE_IZQ":

            valor = self.parsear_lista()

        elif token.tipo == "LLAVE_IZQ":

            valor = self.parsear_diccionario()

        else:
            raise Exception(
                f"Valor inesperado: {token}"
            )

        return self.parsear_accesos(valor)

    def parsear_lista(self):

        self.esperar(
            "CORCHETE_IZQ"
        )

        elementos = []

        if self.actual().tipo == "CORCHETE_DER":

            self.avanzar()

            return Lista(elementos)

        while True:

            elementos.append(
                self.parsear_expresion()
            )

            if self.actual().tipo != "COMA":
                break

            self.avanzar()

        self.esperar(
            "CORCHETE_DER"
        )

        return Lista(elementos)

    def parsear_diccionario(self):

        self.esperar(
            "LLAVE_IZQ"
        )

        elementos = []

        while (
            self.actual() is not None
            and self.actual().tipo != "LLAVE_DER"
        ):
            if self.actual().tipo == "NUEVA_LINEA":
                self.avanzar()
                continue

            clave = self.esperar(
                "STRING"
            )

            self.esperar("DOS_PUNTOS")

            valor = self.parsear_expresion()

            elementos.append(
                (
                    clave.valor,
                    valor
                )
            )

            if self.actual().tipo == "COMA":
                self.avanzar()
                continue

            if self.actual().tipo == "NUEVA_LINEA":
                continue

            if self.actual().tipo != "LLAVE_DER":
                raise Exception(
                    "Se esperaba ',' o '}' "
                    "en el diccionario"
                )

        self.esperar(
            "LLAVE_DER"
        )

        return Diccionario(
            elementos
        )

    def parsear_accesos(self, valor):

        while (
            self.actual() is not None
            and self.actual().tipo
            == "CORCHETE_IZQ"
        ):
            self.avanzar()

            indice = self.parsear_expresion()

            self.esperar(
                "CORCHETE_DER"
            )

            valor = AccesoLista(
                valor,
                indice
            )

        return valor

    def parsear_llamada_funcion(
        self,
        nombre=None
    ):

        if nombre is None:
            nombre = self.esperar(
                "IDENTIFICADOR"
            ).valor

        self.esperar(
            "PAREN_IZQ"
        )

        argumentos = []

        if (
            self.actual().tipo
            == "PAREN_DER"
        ):
            self.avanzar()

            return LlamadaFuncion(
                nombre,
                argumentos
            )

        while True:

            argumentos.append(
                self.parsear_expresion()
            )

            if (
                self.actual().tipo
                != "COMA"
            ):
                break

            self.avanzar()

        self.esperar(
            "PAREN_DER"
        )

        return LlamadaFuncion(
            nombre,
            argumentos
        )