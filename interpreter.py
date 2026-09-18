import os
import random

from tokenizer import tokenize

from parser import (
    Parser,
    GuardarVariable,
    AsignarAcceso,
    Mostrar,
    Numero,
    Texto,
    Booleano,
    Nulo,
    Lista,
    Diccionario,
    AccesoLista,
    Variable,
    Operacion,
    Si,
    Comparacion,
    Mientras,
    ParaCada,
    LlamadaFuncion,
    Funcion,
    Devolver,
    Extraer,
    Romper,
    Continuar
)


class ErrorRandomLang(Exception):

    def __init__(
        self,
        mensaje,
        linea=None
    ):
        self.mensaje = mensaje
        self.linea = linea

        super().__init__(
            mensaje
        )


class ErrorEjecucionRandomLang:

    def __init__(
        self,
        mensaje,
        archivo,
        linea,
        codigo
    ):
        self.mensaje = mensaje
        self.archivo = archivo
        self.linea = linea
        self.codigo = codigo

    def __str__(self):

        if self.linea is None:
            return (
                f"{self.mensaje}"
            )

        lineas = self.codigo.splitlines()

        if (
            self.linea < 1
            or self.linea > len(lineas)
        ):
            return (
                f"{self.mensaje}"
            )

        texto = lineas[
            self.linea - 1
        ]

        return (
            f"Error en {self.archivo}, "
            f"línea {self.linea}:\n\n"
            f"    {texto}\n\n"
            f"{self.mensaje}"
        )


class RetornoFuncion(Exception):

    def __init__(self, valor):
        self.valor = valor


class RomperBucle(Exception):
    pass


class ContinuarBucle(Exception):
    pass


class Interpreter:

    def __init__(
        self,
        carpeta_programas="Programas",
        argumentos=None,
        archivo_actual=None,
        codigo_actual=""
    ):

        self.ambitos = [
            {}
        ]

        self.funciones = {}

        self.carpeta_programas = (
            carpeta_programas
        )

        self.argumentos = (
            argumentos
            if argumentos is not None
            else []
        )

        self.archivo_actual = (
            archivo_actual
        )

        self.codigo_actual = (
            codigo_actual
        )

        self.linea_actual = None

    # ==============================
    # ERRORES
    # ==============================

    def error(self, mensaje, nodo=None):

        linea = self.linea_actual

        if nodo is not None:
            linea = getattr(
                nodo,
                "linea",
                linea
            )

        raise ErrorRandomLang(
            mensaje,
            linea
        )

    # ==============================
    # ÁMBITOS
    # ==============================

    def ambito_actual(self):
        return self.ambitos[-1]

    def obtener_variable(self, nombre):

        for ambito in reversed(
            self.ambitos
        ):
            if nombre in ambito:
                return ambito[nombre]

        self.error(
            f"La variable '{nombre}' "
            "no existe."
        )

    def guardar_variable(
        self,
        nombre,
        valor
    ):
        self.ambito_actual()[
            nombre
        ] = valor

    # ==============================
    # FUNCIONES
    # ==============================

    def registrar_funcion(
        self,
        funcion
    ):

        if funcion.nombre in self.funciones:
            self.error(
                f"La función "
                f"'{funcion.nombre}' "
                "ya existe."
            )

        self.funciones[
            funcion.nombre
        ] = funcion

    # ==============================
    # EXTRAER
    # ==============================

    def extraer_programa(
        self,
        nombre
    ):

        ruta = os.path.join(
            self.carpeta_programas,
            nombre + ".rl"
        )

        if not os.path.isfile(ruta):
            self.error(
                f"No se encontró el programa "
                f"'{nombre}.rl' en "
                f"'{self.carpeta_programas}'."
            )

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:
            codigo = archivo.read()

        tokens = tokenize(codigo)

        parser = Parser(tokens)

        ast = parser.parsear()

        cantidad = 0

        for nodo in ast:

            if isinstance(
                nodo,
                Funcion
            ):
                self.registrar_funcion(
                    nodo
                )

                cantidad += 1

        return cantidad

    # ==============================
    # PREPARAR
    # ==============================

    def preparar_programa(
        self,
        ast
    ):

        for nodo in ast:

            if isinstance(
                nodo,
                Funcion
            ):
                self.registrar_funcion(
                    nodo
                )

        for nodo in ast:

            if isinstance(
                nodo,
                Extraer
            ):
                self.extraer_programa(
                    nodo.nombre
                )

    # ==============================
    # EJECUTAR
    # ==============================

    def ejecutar(self, ast):

        self.preparar_programa(
            ast
        )

        try:

            for nodo in ast:

                if isinstance(
                    nodo,
                    Funcion
                ):
                    continue

                if isinstance(
                    nodo,
                    Extraer
                ):
                    continue

                self.ejecutar_nodo(
                    nodo
                )

        except RetornoFuncion:

            self.error(
                "'devolver' solo puede "
                "utilizarse dentro de "
                "una función."
            )

        except (
            RomperBucle,
            ContinuarBucle
        ):

            self.error(
                "'romper' y 'continuar' "
                "solo pueden utilizarse "
                "dentro de un bucle."
            )

    # ==============================
    # EJECUTAR NODOS
    # ==============================

    def ejecutar_nodo(
        self,
        nodo
    ):

        if isinstance(
            nodo,
            GuardarVariable
        ):

            valor = self.evaluar(
                nodo.valor
            )

            self.guardar_variable(
                nodo.nombre,
                valor
            )

        elif isinstance(
            nodo,
            AsignarAcceso
        ):

            valor = self.evaluar(
                nodo.valor
            )

            self.asignar_acceso(
                nodo.acceso,
                valor
            )

        elif isinstance(
            nodo,
            Mostrar
        ):

            valor = self.evaluar(
                nodo.valor
            )

            self.mostrar_valor(
                valor
            )

        elif isinstance(
            nodo,
            Devolver
        ):

            valor = self.evaluar(
                nodo.valor
            )

            raise RetornoFuncion(
                valor
            )

        elif isinstance(
            nodo,
            Romper
        ):

            raise RomperBucle()

        elif isinstance(
            nodo,
            Continuar
        ):

            raise ContinuarBucle()

        elif isinstance(
            nodo,
            Si
        ):

            condicion = self.evaluar(
                nodo.condicion
            )

            if condicion:

                self.ejecutar_bloque(
                    nodo.bloque_si
                )

            elif (
                nodo.bloque_sino
                is not None
            ):

                self.ejecutar_bloque(
                    nodo.bloque_sino
                )

        elif isinstance(
            nodo,
            Mientras
        ):

            while self.evaluar(
                nodo.condicion
            ):

                try:

                    self.ejecutar_bloque(
                        nodo.bloque
                    )

                except RomperBucle:
                    break

                except ContinuarBucle:
                    continue

        elif isinstance(
            nodo,
            ParaCada
        ):

            elementos = self.evaluar(
                nodo.lista
            )

            if not isinstance(
                elementos,
                list
            ):
                self.error(
                    "La expresión de "
                    "'para cada' debe ser "
                    "una lista."
                )

            # IMPORTANTE:
            # NO se crea un ámbito nuevo.
            # La variable y los cambios
            # quedan en el ámbito actual.

            for elemento in elementos:

                self.guardar_variable(
                    nodo.variable,
                    elemento
                )

                try:

                    self.ejecutar_bloque(
                        nodo.bloque
                    )

                except RomperBucle:
                    break

                except ContinuarBucle:
                    continue

        elif isinstance(
            nodo,
            LlamadaFuncion
        ):

            self.ejecutar_funcion(
                nodo
            )

        else:

            self.error(
                f"Nodo desconocido: "
                f"{nodo}"
            )

    def ejecutar_bloque(
        self,
        bloque
    ):

        for instruccion in bloque:

            self.ejecutar_nodo(
                instruccion
            )

    # ==============================
    # MOSTRAR
    # ==============================

    def convertir_mostrar(
        self,
        valor
    ):

        if valor is True:
            return "Verdadero"

        if valor is False:
            return "Falso"

        if valor is None:
            return "Nulo"

        if isinstance(
            valor,
            list
        ):

            elementos = []

            for elemento in valor:
                elementos.append(
                    self.convertir_mostrar(
                        elemento
                    )
                )

            return (
                "["
                + ", ".join(elementos)
                + "]"
            )

        if isinstance(
            valor,
            dict
        ):

            elementos = []

            for clave, elemento in (
                valor.items()
            ):

                elementos.append(
                    f'"{clave}": '
                    f'{self.convertir_mostrar(elemento)}'
                )

            return (
                "{"
                + ", ".join(elementos)
                + "}"
            )

        return str(valor)

    def mostrar_valor(
        self,
        valor
    ):

        print(
            self.convertir_mostrar(
                valor
            )
        )

    # ==============================
    # INTERPOLACIÓN
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
                    self.error(
                        "Interpolación sin cerrar."
                    )

                nombre = texto[
                    inicio:i
                ]

                valor = self.obtener_variable(
                    nombre
                )

                resultado += (
                    self.convertir_mostrar(
                        valor
                    )
                )

                i += 1

                continue

            resultado += texto[i]

            i += 1

        return resultado

    # ==============================
    # EVALUAR
    # ==============================

    def evaluar(
        self,
        nodo
    ):

        if isinstance(
            nodo,
            Numero
        ):
            return nodo.valor

        if isinstance(
            nodo,
            Texto
        ):
            return self.interpolar_string(
                nodo.valor
            )

        if isinstance(
            nodo,
            Booleano
        ):
            return nodo.valor

        if isinstance(
            nodo,
            Nulo
        ):
            return None

        if isinstance(
            nodo,
            Lista
        ):

            resultado = []

            for elemento in (
                nodo.elementos
            ):

                resultado.append(
                    self.evaluar(
                        elemento
                    )
                )

            return resultado

        if isinstance(
            nodo,
            Diccionario
        ):

            resultado = {}

            for clave, valor in (
                nodo.elementos
            ):

                resultado[clave] = (
                    self.evaluar(
                        valor
                    )
                )

            return resultado

        if isinstance(
            nodo,
            AccesoLista
        ):

            contenedor = self.evaluar(
                nodo.lista
            )

            indice = self.evaluar(
                nodo.indice
            )

            return self.obtener_acceso(
                contenedor,
                indice
            )

        if isinstance(
            nodo,
            Variable
        ):

            return self.obtener_variable(
                nodo.nombre
            )

        if isinstance(
            nodo,
            Operacion
        ):

            izquierda = self.evaluar(
                nodo.izquierda
            )

            derecha = self.evaluar(
                nodo.derecha
            )

            try:

                if nodo.operador == "+":
                    return izquierda + derecha

                if nodo.operador == "-":
                    return izquierda - derecha

                if nodo.operador == "*":
                    return izquierda * derecha

                if nodo.operador == "/":
                    return izquierda / derecha

            except Exception as error:

                self.error(
                    f"No se pudo realizar "
                    f"la operación: {error}"
                )

            self.error(
                f"Operador desconocido: "
                f"{nodo.operador}"
            )

        if isinstance(
            nodo,
            Comparacion
        ):

            izquierda = self.evaluar(
                nodo.izquierda
            )

            derecha = self.evaluar(
                nodo.derecha
            )

            try:

                if nodo.operador == ">":
                    return izquierda > derecha

                if nodo.operador == "<":
                    return izquierda < derecha

                if nodo.operador == ">=":
                    return izquierda >= derecha

                if nodo.operador == "<=":
                    return izquierda <= derecha

                if nodo.operador == "==":
                    return izquierda == derecha

                if nodo.operador == "!=":
                    return izquierda != derecha

            except Exception as error:

                self.error(
                    f"No se pudo realizar "
                    f"la comparación: {error}"
                )

            self.error(
                "Operador de comparación "
                "desconocido."
            )

        if isinstance(
            nodo,
            LlamadaFuncion
        ):

            return self.ejecutar_funcion(
                nodo
            )

        self.error(
            f"No se puede evaluar: "
            f"{nodo}"
        )

    # ==============================
    # ACCESO A LISTAS/DICCIONARIOS
    # ==============================

    def obtener_acceso(
        self,
        contenedor,
        indice
    ):

        if isinstance(
            contenedor,
            list
        ):

            if not isinstance(
                indice,
                int
            ):
                self.error(
                    "El índice de una lista "
                    "debe ser un número entero."
                )

            if (
                indice < 0
                or indice >= len(contenedor)
            ):
                self.error(
                    f"Índice fuera de rango: "
                    f"{indice}"
                )

            return contenedor[
                indice
            ]

        if isinstance(
            contenedor,
            dict
        ):

            if not isinstance(
                indice,
                str
            ):
                self.error(
                    "La clave de un diccionario "
                    "debe ser texto."
                )

            if indice not in contenedor:
                self.error(
                    f"La clave '{indice}' "
                    "no existe en el diccionario."
                )

            return contenedor[
                indice
            ]

        self.error(
            "Solo se pueden indexar "
            "listas y diccionarios."
        )

    def asignar_acceso(
        self,
        acceso,
        valor
    ):

        if not isinstance(
            acceso,
            AccesoLista
        ):
            self.error(
                "Asignación inválida."
            )

        contenedor = self.evaluar(
            acceso.lista
        )

        indice = self.evaluar(
            acceso.indice
        )

        if isinstance(
            contenedor,
            list
        ):

            if not isinstance(
                indice,
                int
            ):
                self.error(
                    "El índice de una lista "
                    "debe ser un entero."
                )

            if (
                indice < 0
                or indice >= len(contenedor)
            ):
                self.error(
                    f"Índice fuera de rango: "
                    f"{indice}"
                )

            contenedor[
                indice
            ] = valor

            return

        if isinstance(
            contenedor,
            dict
        ):

            if not isinstance(
                indice,
                str
            ):
                self.error(
                    "La clave de un diccionario "
                    "debe ser texto."
                )

            contenedor[
                indice
            ] = valor

            return

        self.error(
            "Solo se pueden modificar "
            "listas y diccionarios mediante []."
        )

    # ==============================
    # FUNCIONES
    # ==============================

    def ejecutar_funcion(
        self,
        nodo
    ):

        # ==========================
        # ALEATORIO
        # ==========================

        if nodo.nombre == "aleatorio":

            if len(nodo.argumentos) != 2:
                self.error(
                    "aleatorio() necesita "
                    "exactamente 2 argumentos."
                )

            minimo = self.evaluar(
                nodo.argumentos[0]
            )

            maximo = self.evaluar(
                nodo.argumentos[1]
            )

            if not isinstance(
                minimo,
                int
            ):
                self.error(
                    "El primer argumento de "
                    "aleatorio() debe ser entero."
                )

            if not isinstance(
                maximo,
                int
            ):
                self.error(
                    "El segundo argumento de "
                    "aleatorio() debe ser entero."
                )

            if minimo > maximo:
                self.error(
                    "El mínimo no puede ser "
                    "mayor que el máximo."
                )

            return random.randint(
                minimo,
                maximo
            )

        # ==========================
        # CONTIENE
        # ==========================

        if nodo.nombre == "contiene":

            if len(nodo.argumentos) != 2:
                self.error(
                    "contiene() necesita "
                    "exactamente 2 argumentos."
                )

            valor = self.evaluar(
                nodo.argumentos[0]
            )

            contenido = self.evaluar(
                nodo.argumentos[1]
            )

            if isinstance(
                valor,
                str
            ):

                if not isinstance(
                    contenido,
                    str
                ):
                    self.error(
                        "El segundo argumento "
                        "de contiene() debe ser "
                        "texto."
                    )

                return contenido in valor

            if isinstance(
                valor,
                list
            ):

                return contenido in valor

            self.error(
                "El primer argumento de "
                "contiene() debe ser texto "
                "o lista."
            )

        # ==========================
        # SEPARAR
        # ==========================

        if nodo.nombre == "separar":

            if len(nodo.argumentos) != 2:
                self.error(
                    "separar() necesita "
                    "exactamente 2 argumentos."
                )

            texto = self.evaluar(
                nodo.argumentos[0]
            )

            separador = self.evaluar(
                nodo.argumentos[1]
            )

            if not isinstance(
                texto,
                str
            ):
                self.error(
                    "El primer argumento de "
                    "separar() debe ser texto."
                )

            if not isinstance(
                separador,
                str
            ):
                self.error(
                    "El segundo argumento de "
                    "separar() debe ser texto."
                )

            return texto.split(
                separador
            )

        # ==========================
        # REMPLAZAR
        # ==========================

        if nodo.nombre == "remplazar":

            if len(nodo.argumentos) != 3:
                self.error(
                    "remplazar() necesita "
                    "exactamente 3 argumentos."
                )

            texto = self.evaluar(
                nodo.argumentos[0]
            )

            buscar = self.evaluar(
                nodo.argumentos[1]
            )

            reemplazo = self.evaluar(
                nodo.argumentos[2]
            )

            if not all(
                isinstance(valor, str)
                for valor in (
                    texto,
                    buscar,
                    reemplazo
                )
            ):
                self.error(
                    "Los argumentos de "
                    "remplazar() deben ser "
                    "texto."
                )

            return texto.replace(
                buscar,
                reemplazo
            )

        # ==========================
        # LONGITUD
        # ==========================

        if nodo.nombre == "longitud":

            if len(nodo.argumentos) != 1:
                self.error(
                    "longitud() necesita "
                    "exactamente 1 argumento."
                )

            valor = self.evaluar(
                nodo.argumentos[0]
            )

            if not isinstance(
                valor,
                (list, str, dict)
            ):
                self.error(
                    "longitud() solo acepta "
                    "listas, textos o "
                    "diccionarios."
                )

            return len(valor)

        # ==========================
        # AGREGAR
        # ==========================

        if nodo.nombre == "agregar":

            if len(nodo.argumentos) != 2:
                self.error(
                    "agregar() necesita "
                    "exactamente 2 argumentos."
                )

            lista = self.evaluar(
                nodo.argumentos[0]
            )

            valor = self.evaluar(
                nodo.argumentos[1]
            )

            if not isinstance(
                lista,
                list
            ):
                self.error(
                    "El primer argumento de "
                    "agregar() debe ser una lista."
                )

            lista.append(valor)

            return None

        # ==========================
        # ELIMINAR
        # ==========================

        if nodo.nombre == "eliminar":

            if len(nodo.argumentos) != 2:
                self.error(
                    "eliminar() necesita "
                    "exactamente 2 argumentos."
                )

            lista = self.evaluar(
                nodo.argumentos[0]
            )

            indice = self.evaluar(
                nodo.argumentos[1]
            )

            if not isinstance(
                lista,
                list
            ):
                self.error(
                    "El primer argumento de "
                    "eliminar() debe ser una lista."
                )

            if not isinstance(
                indice,
                int
            ):
                self.error(
                    "El índice de eliminar() "
                    "debe ser entero."
                )

            if (
                indice < 0
                or indice >= len(lista)
            ):
                self.error(
                    f"Índice fuera de rango: "
                    f"{indice}"
                )

            return lista.pop(indice)

        # ==========================
        # INSERTAR
        # ==========================

        if nodo.nombre == "insertar":

            if len(nodo.argumentos) != 3:
                self.error(
                    "insertar() necesita "
                    "exactamente 3 argumentos."
                )

            lista = self.evaluar(
                nodo.argumentos[0]
            )

            indice = self.evaluar(
                nodo.argumentos[1]
            )

            valor = self.evaluar(
                nodo.argumentos[2]
            )

            if not isinstance(
                lista,
                list
            ):
                self.error(
                    "El primer argumento de "
                    "insertar() debe ser una lista."
                )

            if not isinstance(
                indice,
                int
            ):
                self.error(
                    "El índice de insertar() "
                    "debe ser entero."
                )

            lista.insert(
                indice,
                valor
            )

            return None

        # ==========================
        # PARAMETRO
        # ==========================

        if nodo.nombre == "parametro":

            if len(nodo.argumentos) != 1:
                self.error(
                    "parametro() necesita "
                    "exactamente 1 argumento."
                )

            nombre = self.evaluar(
                nodo.argumentos[0]
            )

            if not isinstance(
                nombre,
                str
            ):
                self.error(
                    "El parámetro de "
                    "parametro() debe ser texto."
                )

            if nombre.startswith("--"):
                clave = nombre[2:]
            else:
                clave = nombre

            for argumento in self.argumentos:

                if isinstance(
                    argumento,
                    dict
                ):

                    if clave in argumento:
                        return argumento[
                            clave
                        ]

                else:

                    if clave == "":
                        return argumento

            self.error(
                f"No se encontró el parámetro "
                f"'{nombre}'."
            )

        # ==========================
        # OBTENER
        # ==========================

        if nodo.nombre == "obtener":

            if len(nodo.argumentos) != 1:
                self.error(
                    "obtener() necesita "
                    "exactamente 1 argumento."
                )

            ruta = self.evaluar(
                nodo.argumentos[0]
            )

            if not isinstance(
                ruta,
                str
            ):
                self.error(
                    "La ruta de obtener() "
                    "debe ser texto."
                )

            try:

                with open(
                    ruta,
                    "r",
                    encoding="utf-8"
                ) as archivo:
                    return archivo.read()

            except Exception as error:

                self.error(
                    f"No se pudo leer "
                    f"'{ruta}': {error}"
                )

        # ==========================
        # CREAR ARCHIVO
        # ==========================

        if nodo.nombre == "crearArchivo":

            if len(nodo.argumentos) != 2:
                self.error(
                    "crearArchivo() necesita "
                    "exactamente 2 argumentos."
                )

            ruta = self.evaluar(
                nodo.argumentos[0]
            )

            contenido = self.evaluar(
                nodo.argumentos[1]
            )

            if not isinstance(
                ruta,
                str
            ):
                self.error(
                    "La ruta de crearArchivo() "
                    "debe ser texto."
                )

            if not isinstance(
                contenido,
                str
            ):
                self.error(
                    "El contenido de "
                    "crearArchivo() debe ser texto."
                )

            try:

                with open(
                    ruta,
                    "w",
                    encoding="utf-8"
                ) as archivo:
                    archivo.write(
                        contenido
                    )

            except Exception as error:

                self.error(
                    f"No se pudo crear "
                    f"'{ruta}': {error}"
                )

            return None

        # ==========================
        # FUNCIÓN DEL USUARIO
        # ==========================

        if nodo.nombre in self.funciones:

            funcion = self.funciones[
                nodo.nombre
            ]

            if len(
                nodo.argumentos
            ) != len(
                funcion.parametros
            ):
                self.error(
                    f"La función "
                    f"'{nodo.nombre}' espera "
                    f"{len(funcion.parametros)} "
                    f"argumentos, pero recibió "
                    f"{len(nodo.argumentos)}."
                )

            valores = []

            for argumento in (
                nodo.argumentos
            ):

                valores.append(
                    self.evaluar(
                        argumento
                    )
                )

            ambito_local = {}

            for i in range(
                len(funcion.parametros)
            ):

                parametro = (
                    funcion.parametros[i]
                )

                ambito_local[
                    parametro
                ] = valores[i]

            self.ambitos.append(
                ambito_local
            )

            resultado = None

            try:

                for instruccion in (
                    funcion.bloque
                ):
                    self.ejecutar_nodo(
                        instruccion
                    )

            except RetornoFuncion as retorno:

                resultado = retorno.valor

            finally:

                self.ambitos.pop()

            return resultado

        self.error(
            f"Función desconocida: "
            f"'{nodo.nombre}'."
        )