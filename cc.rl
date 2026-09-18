funcion absoluto(n):
    si n < 0:
        devolver 0 - n
    sino:
        devolver n

funcion maximo(a, b):
    si a > b:
        devolver a
    sino:
        devolver b

funcion minimo(a, b):
    si a < b:
        devolver a
    sino:
        devolver b

funcion limitar(valor, piso, techo):
    si valor < piso:
        devolver piso
    si valor > techo:
        devolver techo
    devolver valor

funcion potencia(base, exponente):
    si exponente < 0:
        devolver 0
    guardar res = 1
    guardar i = 1
    mientras i <= exponente:
        guardar res = res * base
        guardar i = i + 1
    devolver res

funcion es_divisible(numero, divisor):
    si divisor == 0:
        devolver Falso
    guardar resto = absoluto(numero)
    guardar d = absoluto(divisor)
    mientras resto >= d:
        guardar resto = resto - d
    si resto == 0:
        devolver Verdadero
    sino:
        devolver Falso

funcion es_par(numero):
    devolver es_divisible(numero, 2)

funcion es_primo(numero):
    si numero < 2:
        devolver Falso
    guardar divisor = 2
    mientras divisor * divisor <= numero:
        si es_divisible(numero, divisor) == Verdadero:
            devolver Falso
        guardar divisor = divisor + 1
    devolver Verdadero

funcion mcd(a, b):
    guardar x = absoluto(a)
    guardar y = absoluto(b)
    si x == 0:
        devolver y
    si y == 0:
        devolver x
    mientras x != y:
        si x > y:
            guardar x = x - y
        sino:
            guardar y = y - x
    devolver x

funcion mcm(a, b):
    si a == 0:
        devolver 0
    si b == 0:
        devolver 0
    devolver absoluto(a * b) / mcd(a, b)

funcion factorial(n):
    si n < 0:
        devolver 0
    guardar res = 1
    guardar i = 1
    mientras i <= n:
        guardar res = res * i
        guardar i = i + 1
    devolver res

funcion c(comentario):
 guardar x = comentario

funcion rango(desde, hasta):
    guardar texto = ""
    guardar i = desde
    mientras i <= hasta:
        guardar pieza = "\i\"
        si i == desde:
            guardar texto = pieza
        sino:
            guardar texto = texto + "," + pieza
        guardar i = i + 1
    si texto == "":
        devolver []
    sino:
        devolver separar(texto, ",")

funcion longitud(lista):
    guardar n = 0
    para cada item en lista:
        guardar n = n + 1
        devolver n

funcion suma_lista(lista):
    guardar total = 0
    para cada item en lista:
        guardar total = total + item
        devolver total

funcion promedio(lista):
    guardar n = longitud(lista)
    si n == 0:
        devolver 0
    sino:
        devolver suma_lista(lista) / n

funcion max_lista(lista):
    guardar mejor = lista[0]
    para cada item en lista:
        si item > mejor:
            guardar mejor = item
        devolver mejor

funcion min_lista(lista):
    guardar mejor = lista[0]
    para cada item en lista:
        si item < mejor:
            guardar mejor = item
        devolver mejor

funcion primero(lista):
    devolver lista[0]

funcion ultimo(lista):
    guardar n = longitud(lista)
    guardar i = n - 1
    devolver lista[i]

funcion invertir(lista):
    guardar n = longitud(lista)
    si n == 0:
        devolver lista
    guardar texto = ""
    para cada item en lista:
        guardar pieza = "\item\"
        si texto == "":
            guardar texto = pieza
        sino:
            guardar texto = pieza + "," + texto
        devolver separar(texto, ",")

funcion unir_lista(lista, sep):
    guardar texto = ""
    guardar n = 0
    para cada item en lista:
        guardar pieza = "\item\"
        si n == 0:
            guardar texto = pieza
        sino:
            guardar texto = texto + sep + pieza
        guardar n = n + 1
        devolver texto

funcion hay_valor(lista, valor):
    guardar encontrado = Falso
    para cada item en lista:
        si item == valor:
            guardar encontrado = Verdadero
        devolver encontrado

funcion repetir(texto, veces):
    guardar out = ""
    guardar i = 0
    mientras i < veces:
        guardar out = out + texto
        guardar i = i + 1
    devolver out

funcion esta_vacio(texto):
    si texto == "":
        devolver Verdadero
    sino:
        devolver Falso

funcion empieza_con(texto, prefijo):
    si prefijo == "":
        devolver Verdadero
    si texto == prefijo:
        devolver Verdadero
    guardar partes = separar(texto, prefijo)
    si partes[0] == "":
        devolver Verdadero
    sino:
        devolver Falso

funcion compactar(texto):
    guardar t = texto
    mientras contiene(t, "  ") == Verdadero:
        guardar t = remplazar(t, "  ", " ")
    devolver t

funcion exp(x):
    guardar resultado = 1
    guardar termino = 1
    guardar n = 1

    mientras n <= 25:
        guardar termino = termino * x / n
        guardar resultado = resultado + termino
        guardar n = n + 1

    devolver resultado

funcion cadena_a_numero(texto):
    guardar numero = 0
    guardar negativo = Falso
    guardar inicio = 0

    si texto[0] == "-":
        guardar negativo = Verdadero
        guardar inicio = 1

    guardar i = inicio
    mientras i < longitud(texto):
        guardar caracter = texto[i]
        
        si caracter == "0":
            guardar digito = 0
        sino:
            si caracter == "1":
                guardar digito = 1
            sino:
                si caracter == "2":
                    guardar digito = 2
                sino:
                    si caracter == "3":
                        guardar digito = 3
                    sino:
                        si caracter == "4":
                            guardar digito = 4
                        sino:
                            si caracter == "5":
                                guardar digito = 5
                            sino:
                                si caracter == "6":
                                    guardar digito = 6
                                sino:
                                    si caracter == "7":
                                        guardar digito = 7
                                    sino:
                                        si caracter == "8":
                                            guardar digito = 8
                                        sino:
                                            si caracter == "9":
                                                guardar digito = 9
                                            sino:
                                                guardar digito = 0
            
        guardar numero = numero * 10 + digito
        guardar i = i + 1

    si negativo == Verdadero:
        guardar numero = 0 - numero

    devolver numero