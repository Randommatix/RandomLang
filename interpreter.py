from parser import (
    GuardarVariable,
    Mostrar,
    Numero,
    Texto,
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


    # ==========================
    # EJECUTAR NODO
    # ==========================

    def ejecutar_nodo(self, nodo):

        # ==========================
        # GUARDAR VARIABLE
        # ==========================

        if isinstance(nodo, GuardarVariable):

            valor = self.evaluar(
                nodo.valor
            )

            self.variables[nodo.nombre] = valor


        # ==========================
        # MOSTRAR
        # ==========================

        elif isinstance(nodo, Mostrar):

            valor = self.evaluar(
                nodo.valor
            )

            print(valor)


        # ==========================
        # SI
        # ==========================

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


        # ==========================
        # NODO DESCONOCIDO
        # ==========================

        else:

            raise Exception(
                f"Nodo desconocido: {nodo}"
            )


    # ==========================
    # INTERPOLAR STRING
    # ==========================

    def interpolar_string(self, texto):

        resultado = ""

        i = 0

        while i < len(texto):

            # ==========================
            # COMIENZO DE VARIABLE
            # ==========================

            if texto[i] == "\\":

                inicio = i + 1

                i += 1


                # Buscar la segunda barra

                while (
                    i < len(texto)
                    and texto[i] != "\\"
                ):

                    i += 1


                # No se encontró la barra final

                if i >= len(texto):

                    raise Exception(
                        "Interpolación sin cerrar"
                    )


                nombre = texto[
                    inicio:i
                ]


                # ==========================
                # COMPROBAR VARIABLE
                # ==========================

                if nombre not in self.variables:

                    raise Exception(
                        f"La variable '{nombre}' "
                        f"no existe"
                    )


                valor = self.variables[
                    nombre
                ]


                resultado += str(valor)

                i += 1

                continue


            # ==========================
            # CARÁCTER NORMAL
            # ==========================

            resultado += texto[i]

            i += 1


        return resultado


    # ==========================
    # EVALUAR
    # ==========================

    def evaluar(self, nodo):

        # ==========================
        # NÚMERO
        # ==========================

        if isinstance(nodo, Numero):

            return nodo.valor


        # ==========================
        # TEXTO
        # ==========================

        elif isinstance(nodo, Texto):

            return self.interpolar_string(
                nodo.valor
            )


        # ==========================
        # VARIABLE
        # ==========================

        elif isinstance(nodo, Variable):

            if nodo.nombre not in self.variables:

                raise Exception(
                    f"La variable '{nodo.nombre}' "
                    f"no existe"
                )

            return self.variables[
                nodo.nombre
            ]


        # ==========================
        # OPERACIÓN MATEMÁTICA
        # ==========================

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


        # ==========================
        # COMPARACIÓN
        # ==========================

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
                    f"Operador de comparación "
                    f"desconocido: {nodo.operador}"
                )


        # ==========================
        # NODO NO EVALUABLE
        # ==========================

        else:

            raise Exception(
                f"No se puede evaluar: {nodo}"
            )