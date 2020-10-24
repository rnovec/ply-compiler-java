import re

# Funcion para crear un posfijo desde un infijo
def convertPosfijo(infijo):
    precedencia = {}
    precedencia["*"] = 3
    precedencia["/"] = 3
    precedencia["+"] = 2
    precedencia["-"] = 2
    precedencia["("] = 1
    listaPosfija = []
    pilaOperadores = []
    validator = re.compile(r'([a-zA-Z]|[0-9])')

    for simbolo in infijo:
        if validator.match(simbolo):
            listaPosfija.append(simbolo)
        elif simbolo == '(':
            pilaOperadores.append(simbolo)
        elif simbolo == ')':
            simboloTope = pilaOperadores.pop()
            while simboloTope != '(':
                listaPosfija.append(simboloTope)
                simboloTope = pilaOperadores.pop()
        else:
            while (not pilaOperadores == []) and \
                    (precedencia[pilaOperadores[len(pilaOperadores)-1]]) >= \
                    precedencia[simbolo]:
                listaPosfija.append(pilaOperadores.pop())
            pilaOperadores.append(simbolo)
    
    while not pilaOperadores == []:
        listaPosfija.append(pilaOperadores.pop())
    return listaPosfija