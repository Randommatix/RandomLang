# RandomLang

RandomLang es un lenguaje de programación experimental creado desde cero utilizando Python.

El objetivo del proyecto es aprender cómo funcionan internamente los lenguajes de programación mediante la creación de un intérprete propio.

# Arquitectura

RandomLang procesa el código mediante varias etapas:

Código fuente → Tokenizer → Tokens → Parser → AST → Intérprete

Características actuales

- Variables mediante "guardar"
- Mostrar valores mediante "mostrar"
- Operaciones matemáticas:
  - "+"
  - "-"
  - "*"
  - "/"
- Prioridad matemática
- Paréntesis
- Condiciones "si"
- Comparaciones:
  - ">"
  - "<"
  - ">="
  - "<="
  - "=="
  - "!="
- Bloques mediante indentación
- "sino"

Ejemplo:

=================
guardar x = 10
guardar y = 5

guardar resultado = (x + y) * 2

si resultado > 20:
    mostrar resultado
sino:
    mostrar 0
=================

Para ejecutar, ejecuta:

python main.py


Estructura:

RandomLang/
├── main.py
├── tokenizer.py
├── parser.py
├── interpreter.py
└── programa.rl

Futuras características

- Bucles "repetir"
- Bucles "mientras"
- Funciones
- Texto y cadenas
- Booleanos
- Comentarios
- Listas
- Mejor manejo de errores

RandomLang es un proyecto educativo y experimental.