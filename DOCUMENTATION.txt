# 📘 RandomLang — Documentación del lenguaje
Versión: 1.0.8
Extensión: .rl
Sintaxis: inspirada parcialmente en Python, pero con instrucciones propias en español.

## 1. 🧠 Conceptos básicos
RandomLang funciona mediante cuatro etapas:

Código .rl
   ↓
Tokenizer
   ↓
Parser
   ↓
AST
   ↓
Interpreter
   ↓
Resultado

Por ejemplo:
guardar numero = 10
mostrar numero

se transforma internamente en algo parecido a:
GuardarVariable(numero, Numero(10))
Mostrar(Variable(numero))

Y finalmente el intérprete ejecuta esas instrucciones.

Para ejecutar un programa debes colocar su nombre en el selector, dentro de la terminal (y si lo requiere, sus parámetros).

## 1.5 ⚠️ Errores de RandomLang
En RandomLang existen muchos tipos de errores, en esta seccion hay algunos ejemplos:

"""
Error de RandomLang en 'Programas/err.rl', línea 3:

    mostrar 1 + "hey"

unsupported operand type(s) for +: 'int' and 'str'
"""
"""
Error en 'err':
Error de RandomLang en 'Programas/err.rl', línea 2:

Se esperaba INDENT, pero apareció: fin del programa
"""
"""
Error de RandomLang en 'Programas/err.rl', línea 3:

     hola()

maximum recursion depth exceeded
"""
"""
Error de RandomLang en 'Programas/err.rl', línea 1:

    guardar res

Se esperaba IGUAL, pero apareció: NUEVA_LINEA(línea=1, columna=11)
"""

## 2. 📦 guardar
Sirve para crear o modificar una variable.

Sintaxis:
guardar nombre = valor

Ejemplo:
guardar edad = 15
guardar nombre = "Randommatix"

Ahora existen:
edad → 15
nombre → "Randommatix"

También puede almacenar expresiones:
guardar resultado = 10 + 20
Resultado:
resultado → 30

Y funciones:
guardar numero = aleatorio(1, 100)

Las variables también se pueden acceder dentro de funciones. Si vuelves a guardar una variable que ya existia dentro de una función, se usara el nuevo valor hasta que se termine la función.

## 3. 🖨️ mostrar
Sirve para mostrar un valor en la consola.

Sintaxis:
mostrar valor

Ejemplos:
mostrar 100
guardar x = 25
mostrar x
Salida:
25

También acepta operaciones:
mostrar 10 + 20
Salida:
30

Y llamadas a funciones:
mostrar aleatorio(1, 10)

## 4. 📝 Strings
RandomLang permite texto utilizando comillas dobles.
guardar nombre = "Randommatix"
mostrar nombre

También:
mostrar "Hola mundo"

## 5. 🔗 Interpolación de variables
Dentro de un string se puede insertar una variable utilizando \.

Sintaxis:
"Texto \variable\"

Ejemplo:
guardar nombre = "Randommatix"
mostrar "Hola \nombre\!"
Salida:
Hola Randommatix!

La interpolación se realiza cuando el intérprete evalúa el texto.
Actualmente la expresión entre \ debe ser el nombre de una variable.

Por ejemplo:
\resultado\
funciona.

Pero algo como:
\10 + 5\
todavía no es válido.

## 6. ➕ +
Realiza una suma.

mostrar 10 + 5
Resultado:
15

También puede utilizar variables:
guardar a = 10
guardar b = 20
mostrar a + b
Resultado:
30

Con strings, + también puede concatenar:
guardar nombre = "Random"
guardar apellido = "matix"
mostrar nombre + apellido

Resultado:
Randommatix

## 7. ➖ -
Realiza una resta.
mostrar 20 - 5
Resultado:
15

## 8. ✖️ *
Realiza una multiplicación.
mostrar 6 * 7
Resultado:
42

## 9. ➗ /
Realiza una división.
mostrar 20 / 4
Resultado:
5.0

## 10. 🔢 Prioridad matemática
Las operaciones tienen una prioridad similar a las matemáticas normales.
mostrar 10 + 5 * 2

Se interpreta como:
10 + (5 * 2)
Resultado:
20
No:
(10 + 5) * 2

También existen paréntesis:
mostrar (10 + 5) * 2
Resultado:
30

## 11. 🔍 Comparaciones
RandomLang tiene seis operadores de comparación.

Operador
Significado
>
mayor que
<
menor que
>=
mayor o igual
<=
menor o igual
==
igual
!=
diferente

Ejemplos:
10 > 5
→ verdadero.
10 < 5
→ falso.
10 == 10
→ verdadero.
10 != 20
→ verdadero.

Estas comparaciones son especialmente importantes para si y mientras.

## 12. 🤔 si
Permite ejecutar código dependiendo de una condición.

Sintaxis:
si condicion:
    instrucciones

Ejemplo:
guardar edad = 18
si edad >= 18:
    mostrar "Es mayor de edad"

El : indica que comienza un bloque.
La indentación determina qué instrucciones pertenecen al si.

## 13. 🔀 sino
Permite ejecutar otro bloque cuando la condición del si es falsa.

guardar edad = 15
si edad >= 18:
    mostrar "Mayor de edad"
sino:
    mostrar "Menor de edad"
Salida:
Menor de edad

Internamente, el parser genera un nodo Si que contiene:
condicion
bloque_si
bloque_sino

CUIDADO: EL "sino:" DEBE IR AL MISMO NIVEL DE INDENT QUE EL RESTO DEL "si".

## 14. 🔄 mientras
Crea un bucle.

Sintaxis:
mientras condicion:
    instrucciones

Ejemplo:
guardar numero = 1
mientras numero <= 6:
    mostrar numero
    guardar numero = numero + 1
Salida:
1
2
3
4
5

El intérprete evalúa la condición antes de cada repetición.

Conceptualmente:
mientras condición sea verdadera:
    ejecutar bloque

## 15. 🎲 aleatorio()
Es una función incorporada en RandomLang.

Sintaxis:
aleatorio(minimo, maximo)

Genera un número entero aleatorio entre ambos valores, incluyendo los extremos.

Ejemplo:
mostrar aleatorio(1, 10)
Podría producir:
7
o:
1
o:
10
etc.

También puede guardarse:
guardar dado = aleatorio(1, 6)
mostrar dado

Es equivalente conceptualmente a:
número aleatorio entre 1 y 6

Actualmente requiere exactamente dos argumentos enteros.

## 16. 🧩 funcion
Permite crear funciones propias.

Sintaxis:
funcion nombre():
    instrucciones

Ejemplo:
funcion saludar():
    mostrar "Hola!"
saludar()

Cuando RandomLang encuentra:
funcion saludar():
el parser crea un nodo:
Funcion(
    saludar,
    parametros=[],
    bloque=[...]
)

El intérprete registra la función y posteriormente puede ejecutarla.

Las/los variables/parámetros dentro de una función no se pueden usar fuera de la misma.

## 17. 📥 Parámetros de funciones
Las funciones pueden recibir información.

funcion saludar(nombre):
    mostrar "Hola \nombre\"
saludar("Randommatix")

Aquí:
nombre
es un parámetro.

Cuando hacemos:
saludar("Randommatix")
el valor:
"Randommatix"
se asigna temporalmente a:
nombre
y la función ejecuta:
mostrar "Hola \nombre\"

Resultado:
Hola Randommatix

## 18. 📥📥 Múltiples parámetros
Una función puede recibir varios parámetros.

funcion sumar(a, b):
    mostrar a + b
sumar(10, 20)

Aquí:
a = 10
b = 20
Resultado:
30

Los argumentos se separan mediante ",".

También pueden ser expresiones:
sumar(10 + 5, 20 * 2)

Los argumentos se evalúan antes de ejecutar la función.

## 19. ↩️ devolver
devolver termina la ejecución de una función y proporciona un resultado.

Sintaxis
devolver valor

Ejemplo:
funcion sumar(a, b):
    devolver a + b

La función ahora devuelve el resultado en lugar de simplemente mostrarlo.

Podemos capturarlo:
guardar resultado = sumar(15, 25)
mostrar resultado

Salida:
40

## 20. 🧮 Funciones dentro de expresiones
Como devolver proporciona un valor, las funciones pueden utilizarse dentro de expresiones.
Por ejemplo:
funcion multiplicar(a, b):
    devolver a * b
mostrar multiplicar(3, 4) + 10

Primero:
multiplicar(3, 4)
produce:
12
Después:
12 + 10
produce:
22

Esto es importante porque convierte las funciones en verdaderas expresiones evaluables.

## 21. 🔀 devolver dentro de si
También podemos devolver diferentes resultados dependiendo de una condición.
funcion mayor(a, b):
    si a > b:
        devolver a
    sino:
        devolver b

Después:
mostrar mayor(15, 8)
mostrar mayor(4, 20)
Resultado:
15
20

Esto permite construir funciones mucho más complejas.

## 22. 📼 Verdadero/Falso/Nulo
Permite trabajar con Verdadero/Falso/Nulo.

Sintaxis:
Verdadero
Falso
Nulo

Ejemplo:
guardar valor1 = Verdadero
si valor1 == Verdadero:
 mostrar Verdadero

Los Verdadero/Falso/Nulo no necesitan comillas (").

Los booleanos internamente son valores, no simples palabras especiales que solamente sirven para si.

## 23. 🔑 contiene()
Una función integrada que devuelve Verdadero/falso.

Sintaxis:
contiene(Texto, comparacion)

Ejemplo:
guardar valor1 = aleatorio(2, 7) / 2
mostrar valor1
guardar valor1 = "\valor1\" + "00"
si contiene(valor1, ".000") == Verdadero:
  mostrar "No tiene coma real."
sino:
  mostrar "Tiene coma real."

"contiene" ya se puede usar en listas.

## 24. ⤵️ extraer
Permite acceder a todas las funciones de otro programa.

Sintaxis:
extraer nombre_de_otro_programa

Ejemplo:
extraer primos
si es_primo(2) == Verdadero:
  mostrar "2 es Primo."

La función es_primo() no se define en el programa que ejecutamos, pero si en el programa que extraemos. El nombre del programa va sin comillas.

### 24.5 ▶️ "cc.rl"
La primer biblioteca de funciones que se creó que no es parte oficial de RandomLang se llama "commons", que permite llamar varias funciones, entre ellas:
es_divisible(numero, divisor)
absoluto(n)
maximo(a, b)
minimo(a, b)
limitar(valor, piso, techo)
potencia(base, exponente)
es_divisible(numero, divisor)
es_primo(numero)
es_par(numero)
mcd(a, b)
mcm(a, b)
factorial(n)
c(comentario)
longitud(lista)
suma_lista(lista_n)
promedio(lista_n)
max_lista(lista_n)
min_lista(lista_n)
primero(lista)
ultimo(lista)
invertir(lista)
unir_lista(lista, sep)
hay_valor(lista, valor)
repetir(texto, veces)
esta_vacio(texto)
empieza_con(texto, prefijo)
compactar(texto)
exp(x)
cadena_a_numero(lista_N_on_str)

Ejemplo:
extraer cc
c("Los comentarios de texto van con comillas")
guardar lista = [2, 5, 8]
c("Aca guardamos cosas:")
guardar mayor = maximo(lista[0], lista[2])
guardar potente = potencia(lista[2], lista[0])
guardar lista2 = lista[2]
guardar lista0 = lista[0]
c("Acá las mostramos:")
mostrar lista
mostrar "Mayor: \mayor\"
mostrar "\lista2\^\lista0\ es igual a \potente\"

## 25. 📜 Listas
Las listas permiten organizar el texto y acceder a solo una parte de un texto largo.

Sintaxis
[valor1, valor2, valor3...]

Ejemplo:
guardar mi_lista = ["Hola", "como,", "estas?"]
mostrar mi_lista[0]
mostrar mi_lista[2]

Para acceder a una posición especifica de una lista, debes colocar un numero entre "[]". Empieza en el "0". No requiere comillas (").

Para aclarar, si se puede hacer esto:
si lista == [1, 2]
mientras lista != [2, 1]

También no se puede acceder a listas dentro de strings:
mostrar "Esto causa un error: \lista[0]\"

Para editar una lista, debes redefinir algo:
lista[0] = "ejemplo"

## 26 ↔️ separar(texto, separador)
Funcion integrada. Devuelve una lista de objetos diferentes separados por un separador.

Ejemplo:
guardar texto = "Hola a todos!"
guardar lista = separar(texto, " ")
mostrar lista[0]

## 27. 🆕️ remplazar(texto, buscar, remplazo)
Otra funcion integrada en RandomLang. Devuelve el mismo texto con la modificación de que todos las apariciones del buscar se remplazan por el remplazo.

Ejemplo:
guardar valor1 = "Hola RandomLang!"
remplazar(valor1, "RandomLang!", "mundo!")

## 28. #️⃣ para cada [valor] en [lista]:
Obtiene todos los valores en la lista accedida.

Ejemplo:
guardar texto = "Hola-Mundo-Randommatix"
para cada palabra en separar(texto, "-"):
   mostrar palabra

"para cada..." si propaga las variables fuera de su propio bloque.

## 29. 📄 obtener(ruta)
Permite acceder a un archivo. Se busca desde la carpeta principal, asi que se recomienda colocar "Programas/" antes del nombre.

Ejemplo:
guardar x = obtener("Programas/data.txt")
mostrar x

## 30. 📝 crearArchivo(ruta, contenido)
Crea un nuevo archivo. Se busca desde la carpeta principal, asi que se recomienda colocar "Programas/" antes del nombre.

Ejemplo:
guardar var = "Randommatix"
crearArchivo("Programas/var.txt", var)

Si ya existe un archivo con ese nombre, se sobreescribe. Ambos parametros solo aceptan texto, no diccionarios ni listas ni etc...

## 31. 🎛️ parametro(identificador)
Desde la consola se deben pasar estos argumentos. SIEMPRE deben incluir "--" antes del nombre.

Ejemplo:
guardar texto = parametro("--txt")
crearArchivo("Programas/mytexto.txt", texto)

## 32. 🗂️ Diccionarios con {} y acceso mediante []
Similares a las listas, pero cada valor tiene un identificador.

Ejemplo:
guardar persona = {
    "Nombre": "Randommatix",
    "Edad": 20,
    "Activo": Verdadero
}
mostrar persona["Nombre"]
mostrar persona["Edad"]
mostrar persona["Activo"]

Para cambiar un valor de asignación: diccionario["clave"] = valor

## 33. 🪆 Diccionarios anidados
Diccionarios dentro de otros.

Ejemplo:
guardar persona = {
    "Nombre": "Randommatix",
    "Perfil": {
        "Pais": "Argentina",
        "Activo": Verdadero
    }
}
mostrar persona["Perfil"]["Pais"]

Aclaración: Los diccionarios pueden ocupar varias líneas.

## 34. 🧨 romper
Romper permite salir de un bucle sin que se cumpla la condición.

Ejemplo:
mientras condicion = Verdadero:
 si aleatorio(1, 2) == 1:
  romper

## 35. ✅️ continuar
Permite saltar a la siguiente instancia de un bucle.

Ejemplo:
mientras condicion = Verdadero:
 si aleatorio(1, 2) == 1:
  continuar

## 36. ↔️ longitud(lista)
Devuelve el tamaño de una lista.

Ejemplo:
si longitud([1, 2]) == 2:
  mostrar Verdadero

## 37. 🅰️ agregar(lista, objeto)
Agrega un objeto a una lista.

Ejemplo:
guardar lista = [1, 2]
guardar lista = agregar(lista, 3)
mostrar lista

## 38. 🚫 eliminar(lista, posición)
Elimina de la lista el objetivo. Empieza en 0.

Ejemplo:
guardar lista = [1, 2]
guardar lista = eliminar(lista, 1)
mostrar lista

## 39. 🔽 insertar(lista, posición, objeto)
Inserta un objeto en una lista. Empieza desde 0.

Ejemplo:
guardar lista = [1, 2]
guardar lista = insertar(lista, 1, 3)
mostrar lista

## 40. 🧪 Ejemplo
Con todo lo que tenemos actualmente, ya podemos hacer programas bastante interesantes:


funcion es_par(n):
    guardar mitad = n / 2
    guardar texto = "\mitad\"
    si contiene(texto, ".0") == Verdadero:
        devolver Verdadero
    sino:
        devolver Falso

guardar n = aleatorio(2, 50)
guardar pasos = 0
guardar pico = n

mostrar "=== COLLATZ DE \n\ ==="

mientras n > 1:
    mostrar n
    si es_par(n) == Verdadero:
        guardar n = n / 2
    sino:
        guardar n = n * 3 + 1
    si n > pico:
        guardar pico = n
    guardar pasos = pasos + 1

mostrar n
mostrar "Pasos: \pasos\"
mostrar "Numero mas alto: \pico\"

Posible resultado:
=== COLLATZ DE 13 ===
13
40
20.0
10.0
5.0
16.0
8.0
4.0
2.0
1.0
Pasos: 9
Numero mas alto: 40