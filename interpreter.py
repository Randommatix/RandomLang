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
    LlamadaFuncion,
    Funcion,
    Devolver
)


class RetornoFuncion(Exception):

    def __init__(self, valor):

        self.valor = valor


class Interpreter:

    def __init__(self):

        # ==========================
        # ÁMBITOS
        # ==========================

        # El primer ámbito es el global.
        self.ambitos = [
            {}
        ]

        # ==========================
        # FUNCIONES
        # ==========================

        self.funciones = {}


    # ==============================
    # ÁMBITO ACTUAL
    # ==============================

    def ambito_actual(self):

        return self.ambitos[-1]


    # ==============================
    # BUSCAR VARIABLE
    # ==============================

    def obtener_variable(self, nombre):

        # Buscar desde el ámbito más
        # interno hacia el global.

        for ambito in reversed(self.ambitos):

            if nombre in ambito:

                return ambito[nombre]


        raise Exception(
            f"La variable '{nombre}' no existe"
        )


    # ==============================
    # GUARDAR VARIABLE
    # ==============================

    def guardar_variable(
        self,
        nombre,
        valor
    ):

        self.ambito_actual()[nombre] = valor


    # ==============================
    # EJECUTAR PROGRAMA
    # ==============================

    def ejecutar(self, ast):

        # ==========================
        # REGISTRAR FUNCIONES
        # ==========================

        for nodo in ast:

            if isinstance(nodo, Funcion):

                if nodo.nombre in self.funciones:

                    raise Exception(
                        f"La función '{nodo.nombre}' "
                        "ya existe"
                    )


                self.funciones[
                    nodo.nombre
                ] = nodo


        # ==========================
        # EJECUTAR PROGRAMA
        # ==========================

        try:

            for nodo in ast:

                if isinstance(nodo, Funcion):

                    continue


                self.ejecutar_nodo(
                    nodo
                )


        except RetornoFuncion:

            raise Exception(
                "'devolver' solo puede utilizarse "
                "dentro de una función"
            )


    # ==============================
    # EJECUTAR NODO
    # ==============================

    def ejecutar_nodo(self, nodo):

        # ==========================
        # GUARDAR
        # ==========================

        if isinstance(nodo, GuardarVariable):

            valor = self.evaluar(
                nodo.valor
            )

            self.guardar_variable(
                nodo.nombre,
                valor
            )


        # ==========================
        # MOSTRAR
        # ==========================

        elif isinstance(nodo, Mostrar):

            valor = self.evaluar(
                nodo.valor
            )

            print(valor)


        # ==========================
        # DEVOLVER
        # ==========================

        elif isinstance(nodo, Devolver):

            valor = self.evaluar(
                nodo.valor
            )

            raise RetornoFuncion(
                valor
            )


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
        # MIENTRAS
        # ==========================

        elif isinstance(nodo, Mientras):

            while self.evaluar(
                nodo.condicion
            ):

                for instruccion in nodo.bloque:

                    self.ejecutar_nodo(
                        instruccion
                    )


        # ==========================
        # LLAMADA A FUNCIÓN
        # ==========================

        elif isinstance(nodo, LlamadaFuncion):

            self.ejecutar_funcion(
                nodo
            )


        # ==========================
        # NODO DESCONOCIDO
        # ==========================

        else:

            raise Exception(
                f"Nodo desconocido: {nodo}"
            )


    # ==============================
    # INTERPOLAR STRING
    # ==============================

    def interpolar_string(
        self,
        texto
    ):

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


                valor = self.obtener_variable(
                    nombre
                )


                resultado += str(
                    valor
                )


                i += 1

                continue


            resultado += texto[i]

            i += 1


        return resultado


    # ==============================
    # EVALUAR EXPRESIONES
    # ==============================

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

            return self.obtener_variable(
                nodo.nombre
            )


        # ==========================
        # OPERACIÓN
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
                    "Operador de comparación "
                    f"desconocido: {nodo.operador}"
                )


        # ==========================
        # LLAMADA A FUNCIÓN
        # ==========================

        elif isinstance(nodo, LlamadaFuncion):

            return self.ejecutar_funcion(
                nodo
            )


        # ==========================
        # NODO NO EVALUABLE
        # ==========================

        else:

            raise Exception(
                f"No se puede evaluar: {nodo}"
            )


    # ==============================
    # EJECUTAR FUNCIÓN
    # ==============================

    def ejecutar_funcion(self, nodo):

        # ==========================
        # FUNCIÓN ALEATORIO
        # ==========================

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


        # ==========================
        # FUNCIÓN DEL USUARIO
        # ==========================

        if nodo.nombre in self.funciones:

            funcion = self.funciones[
                nodo.nombre
            ]


            # ==========================
            # CANTIDAD DE ARGUMENTOS
            # ==========================

            if len(nodo.argumentos) != len(
                funcion.parametros
            ):

                raise Exception(
                    f"La función '{nodo.nombre}' "
                    f"espera {len(funcion.parametros)} "
                    f"argumentos, pero recibió "
                    f"{len(nodo.argumentos)}"
                )


            # ==========================
            # EVALUAR ARGUMENTOS
            # ==========================

            valores = []

            for argumento in nodo.argumentos:

                valores.append(
                    self.evaluar(argumento)
                )


            # ==========================
            # CREAR ÁMBITO LOCAL
            # ==========================

            ambito_local = {}


            for i in range(
                len(funcion.parametros)
            ):

                parametro = funcion.parametros[i]

                valor = valores[i]

                ambito_local[
                    parametro
                ] = valor


            self.ambitos.append(
                ambito_local
            )


            resultado = None


            try:

                for instruccion in funcion.bloque:

                    self.ejecutar_nodo(
                        instruccion
                    )


            except RetornoFuncion as retorno:

                resultado = retorno.valor


            finally:

                # El ámbito local desaparece
                # siempre al terminar la función.

                self.ambitos.pop()


            return resultado


        # ==========================
        # FUNCIÓN DESCONOCIDA
        # ==========================

        raise Exception(
            f"Función desconocida: "
            f"{nodo.nombre}"
        )