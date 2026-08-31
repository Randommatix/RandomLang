from parser import (
    GuardarVariable,
    Mostrar,
    Numero,
    Variable,
    Operacion,
    Si,
    Comparacion
)


class Interpreter:

    def __init__(self):
        self.variables = {}

    def ejecutar(self, ast):

        for nodo in ast:
            self.ejecutar_nodo(nodo)

    def ejecutar_nodo(self, nodo):

        elif isinstance(nodo, Si):

    condicion = self.evaluar(nodo.condicion)

    if condicion:

        for instruccion in nodo.bloque_si:
            self.ejecutar_nodo(instruccion)

    elif nodo.bloque_sino is not None:

        for instruccion in nodo.bloque_sino:
            self.ejecutar_nodo(instruccion)

        # ==========================
        # GUARDAR VARIABLE
        # ==========================

        if isinstance(nodo, GuardarVariable):

            valor = self.evaluar(nodo.valor)

            self.variables[nodo.nombre] = valor


        # ==========================
        # MOSTRAR
        # ==========================

        elif isinstance(nodo, Mostrar):

            valor = self.evaluar(nodo.valor)

            print(valor)


        else:
            raise Exception(
                f"Nodo desconocido: {nodo}"
            )

    # ==========================
    # EVALUAR EXPRESIONES
    # ==========================

    def evaluar(self, nodo):

        elif isinstance(nodo, Comparacion):

    izquierda = self.evaluar(
        nodo.izquierda
    )

    derecha = self.evaluar(
        nodo.derecha
    )

    if nodo.operador == ">":
        return izquierda > derecha

    elif nodo.operador == "<":
        return izquierda < derecha

    elif nodo.operador == ">=":
        return izquierda >= derecha

    elif nodo.operador == "<=":
        return izquierda <= derecha

    elif nodo.operador == "==":
        return izquierda == derecha

    elif nodo.operador == "!=":
        return izquierda != derecha

        # NÚMERO
        if isinstance(nodo, Numero):

            return nodo.valor


        # VARIABLE
        elif isinstance(nodo, Variable):

            if nodo.nombre not in self.variables:
                raise Exception(
                    f"La variable '{nodo.nombre}' no existe"
                )

            return self.variables[nodo.nombre]


        # OPERACIÓN
        elif isinstance(nodo, Operacion):

            izquierda = self.evaluar(nodo.izquierda)

            derecha = self.evaluar(nodo.derecha)

            if nodo.operador == "+":
                return izquierda + derecha

            elif nodo.operador == "-":
                return izquierda - derecha

            elif nodo.operador == "*":
                return izquierda * derecha

            elif nodo.operador == "/":
                return izquierda / derecha

            else:
                raise Exception(
                    f"Operador desconocido: {nodo.operador}"
                )


        else:
            raise Exception(
                f"No se puede evaluar: {nodo}"
            )