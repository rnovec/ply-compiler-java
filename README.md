## Instalation

### Entorno virtual

    virtualenv venv --python=python3
    source venv/bin/activate
    pip install -r requirements.txt

## Run Server

    python app.py

## Programmatly

    python parse.py test/1-vars.java
    python parse.py test/2-functions.java
    python parse.py test/3-iterators.java

# Gramaticas

```
Grammar

Regla 0 S' -> S
Regla 1 S -> sentences S
Regla 2 S -> sentences SEP1 S
Regla 3 S -> sentences
Regla 4 sentences -> declarations SEP1
Regla 5 sentences -> expression SEP1
Regla 6 sentences -> function
Regla 7 declarations -> types ID AS1 expression
Regla 8 declarations -> ID ID AS1 expression
Regla 9 expression -> expression OPAR1 expression
Regla 10 expression -> expression OPAR2 expression
Regla 11 expression -> expression OPAR3 expression
Regla 12 expression -> expression OPAR4 expression
Regla 13 expression -> expression OPAR5 expression
Regla 14 expression -> DEL1 expression DEL2
Regla 15 expression -> CNE
Regla 16 expression -> <empty>
Regla 17 expression -> ID
Regla 18 expression -> ID AS1 expression
Regla 19 function -> types ID DEL1 argv DEL2 DEL3 S DEL4
Regla 20 function -> ID ID DEL1 argv DEL2 DEL3 S DEL4
Regla 21 argv -> argv_rec
Regla 22 argv -> <empty>
Regla 23 argv_rec -> types ID SEP2 argv_rec
Regla 24 argv_rec -> types ID
Regla 25 types -> TD1
Regla 26 types -> TD2
Regla 27 types -> TD3
Regla 28 types -> TD4
Regla 29 types -> TD5

```

## Algoritmo

### Analisis Léxico

- Por cada lexema en el código
  - Se ignoran espacios. comentarios y tabuladores
  - Se separa cada lexema que corresponda a alguno de las Expresiones Regulares
  - **ID**, **TD**, **CNE**, **IT**, **DEL**, **SEP**, **AS**, **OPLO**, **OPAR**...
  - Si algun caracter/lexema no coincide con ningun token, se considera error léxicos
  - Se aumenta el contador de errores y se le asigna el error ERRLX + i
  - Al final se obtiene una lista de tokens, algunos duplicados como constantes numericas (CNE) e Identificadores (ID)
- Por cada lexema duplicado:
  - Se agrega a la lista de vistos, tokens y tabla de simbolos
  - Si es un token duplicado se le signa el valor de su primera aparicion
  - Si es un SEP1 se agrega un salto de linea al archivo de tokens, sino un espacio.
- Se cierran los archivos de salida y se devuelven las listas generadas (*Archivo de tokens*, *Tabla de símbolos* y *Errores léxicos*)

### Analisis Sintáctico

- Con el analisi léxico realizado y los componentes léxicos generados
- Se toma las listas de tokens y se identifican patrones que correspondan a las producciones
  - Se inicia en una sentencia S que puede tener 3 variantes
  - Declaraciones, funciones e iteradores
  - Se asegura que cada uno de los tokens correspondan a alguna de las gramaticas y producciones establecidas
  - Si es asi se continua la inspeccion de los siguientes tokens
  - Si alguno no coincide con la proudccion esperada se arroja un error sintactico
  - Se agrega la linea, el token, el valor y la pósicion donde ocurrio el error
- Finalmente, se compara con el archivo de tokens para identificar los tokens que tuvieron error

### Analisis Semántico

- Para las producciones de declaracion de variables se guarda el valor y el tipo de dato de la variable
  - Se anexa al arreglo de nombres
  - Si en las producciones de llamadas a variables no se reconoce el **ID** de la variable
  - Es decir no se encuentra en el arreglo de nombres, se agrega un error al arreglo de errores
  - Sino se actualiza el valor de la variable y se compara si los tipos de datos coinciden entre las variables involucradas en la asignacion
- Finalmente, se compara la tabla de simbolos con el arreglo de nombres de variables y se asigna el tipo de dato a los tokens de tipo **ID**.
