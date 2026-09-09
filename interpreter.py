import random


from parser import (
    GuardarVariable,
    Mostrar,
    Numero,
    Texto,
    Variable,
    Operacion,
    Si,
    Comparacion,
    Mientras,
    LlamadaFuncion
)


class Interpreter:

    def __init__(self):

        self.variables = {}


    def ejecutar(self, ast):

        for nodo in ast:

            self.ejecutar_nodo(nodo)


    def ejecutar_nodo(self, nodo):

        if isinstance(nodo, GuardarVariable):

            valor = self.evaluar(nodo.valor)

            self.variables[nodo.nombre] = valor


        elif isinstance(nodo, Mostrar):

            valor = self.evaluar(nodo.valor)

            print(valor)


        elif isinstance(nodo, Si):

            condicion = self.evaluar(
                nodo.condicion
            )


            if condicion:

                for instruccion in nodo.bloque_si:

                    self.ejecutar_nodo(
                        instruccion
                    )


            elif nodo.bloque_sino is not None:

                for instruccion in nodo.bloque_sino:

                    self.ejecutar_nodo(
                        instruccion
                    )


        elif isinstance(nodo, Mientras):

            while self.evaluar(nodo.condicion):

                for instruccion in nodo.bloque:

                    self.ejecutar_nodo(
                        instruccion
                    )


        else:

            raise Exception(
                f"Nodo desconocido: {nodo}"
            )


    def interpolar_string(self, texto):

        resultado = ""

        i = 0


        while i < len(texto):

            if texto[i] == "\\":

                inicio = i + 1

                i += 1


                while (
                    i < len(texto)
                    and texto[i] != "\\"
                ):

                    i += 1


                if i >= len(texto):

                    raise Exception(
                        "Interpolación sin cerrar"
                    )


                nombre = texto[
                    inicio:i
                ]


                if nombre not in self.variables:

                    raise Exception(
                        f"La variable '{nombre}' no existe"
                    )


                valor = self.variables[
                    nombre
                ]


                resultado += str(valor)

                i += 1

                continue


            resultado += texto[i]

            i += 1


        return resultado


    def evaluar(self, nodo):

        if isinstance(nodo, Numero):

            return nodo.valor


        elif isinstance(nodo, Texto):

            return self.interpolar_string(
                nodo.valor
            )


        elif isinstance(nodo, Variable):

            if nodo.nombre not in self.variables:

                raise Exception(
                    f"La variable '{nodo.nombre}' no existe"
                )


            return self.variables[
                nodo.nombre
            ]


        elif isinstance(nodo, Operacion):

            izquierda = self.evaluar(
                nodo.izquierda
            )

            derecha = self.evaluar(
                nodo.derecha
            )


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
                    f"Operador desconocido: "
                    f"{nodo.operador}"
                )


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


            else:

                raise Exception(
                    "Operador de comparación "
                    f"desconocido: {nodo.operador}"
                )


        elif isinstance(nodo, LlamadaFuncion):

            return self.ejecutar_funcion(
                nodo
            )


        else:

            raise Exception(
                f"No se puede evaluar: {nodo}"
            )


    def ejecutar_funcion(self, nodo):

        if nodo.nombre == "aleatorio":

            if len(nodo.argumentos) != 2:

                raise Exception(
                    "aleatorio() necesita exactamente "
                    "2 argumentos"
                )


            minimo = self.evaluar(
                nodo.argumentos[0]
            )

            maximo = self.evaluar(
                nodo.argumentos[1]
            )


            if not isinstance(minimo, int):

                raise Exception(
                    "El primer argumento de "
                    "aleatorio() debe ser un número entero"
                )


            if not isinstance(maximo, int):

                raise Exception(
                    "El segundo argumento de "
                    "aleatorio() debe ser un número entero"
                )


            if minimo > maximo:

                raise Exception(
                    "El mínimo de aleatorio() "
                    "no puede ser mayor que el máximo"
                )


            return random.randint(
                minimo,
                maximo
            )


        else:

            raise Exception(
                f"Función desconocida: "
                f"{nodo.nombre}"
            )