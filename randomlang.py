variables = {}

with open("programa.rl", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

for linea in lineas:
    linea = linea.strip()

    # Ignorar líneas vacías
    if not linea:
        continue

    partes = linea.split()

    # GUARDAR
    if partes[0] == "guardar":

        nombre = partes[1]

        # Ejemplo:
        # guardar x = 10
        valor = partes[3]

        # Si es un número
        if valor.isdigit():
            valor = int(valor)

        variables[nombre] = valor

    # MOSTRAR
    elif partes[0] == "mostrar":

        nombre = partes[1]

        if nombre in variables:
            print(variables[nombre])
        else:
            print(f"Error: la variable '{nombre}' no existe")