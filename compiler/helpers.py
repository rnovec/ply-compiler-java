import re
import csv

OPAR = ['*', '/', '%', '+', '-', '(', ')']
OPRE = ['<', '>', '<=', '>=', '==', '!=']
OPLO = ['&&', '||']
PRECEDENCE = {
    "%": 3,
    "*": 3,
    "/": 3,
    "+": 2,
    "-": 2,
    "(": 1,
    "||": 0,
    "&&": 0
}


class TR:
    def __init__(self, obj, size, start, body):
        self.obj = obj
        self.jmpTrue = start + size
        self.jmpFalse = start + size + body + 1


def dictToCsv(data):
    keys = data[0].keys()
    with open('output/taddc.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def flatten(seq):
    l = []
    t = type(seq)
    if t is not tuple and t is not list:
        return [seq]
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l


def infix_to_postfix(array):
    '''
    Funcion para crear un posfijo desde un infijo
    '''
    postfix = []
    opStack = []
    infix = []
    for symbol in array:
        infix.append(symbol)

    for symbol in infix:
        if symbol not in OPAR:
            postfix.append(symbol)
        elif symbol == '(':
            opStack.append(symbol)
        elif symbol == ')':
            symbolTope = opStack.pop()
            while symbolTope != '(':
                postfix.append(symbolTope)
                symbolTope = opStack.pop()
        else:
            while (not opStack == []) and \
                    (PRECEDENCE[opStack[len(opStack)-1]]) >= \
                    PRECEDENCE[symbol]:
                postfix.append(opStack.pop())
            opStack.append(symbol)

    while not opStack == []:
        postfix.append(opStack.pop())
    return postfix


def intermediate_code(postfix, var=None, isWhile=False, start=0, body=0):
    """
    Create a Three Addres Code Table
    from a inverted postfix array
    """
    # reverse the list to use as stack
    string = list(reversed(postfix))
    aux = list() # auxiliar stack
    taddc = list()  # Three Addres Code (EDD)
    tmpCont = 1 # temporals counter
    trCont = trSize = 0 # TR counter and TR sizes
    lastPrecedence = None
    lastTr = None
    el = string.pop()  # get the first operand
    while el is not None:
        # Recorrer la expresión hasta encontrar el primer operador
        if el in OPAR:
            # Asignar a una variable auxiliar, el operador y los operandos previos
            # Asignar a una segunda variable auxiliar, el operador y los 2 operandos previos.
            op2 = aux.pop()
            op1 = aux.pop()

            # En la primera iteración
            if not lastPrecedence == PRECEDENCE[el] or lastPrecedence is None:
                tmpCont += 1
                # Se agrega un renglón en la triplo : variable temporal, primer operando y la operación (=)
                taddc.append({
                    'obj': f'T{tmpCont}',
                    'fuente': op1,
                    'op': '='
                })
                trSize += 1
                lastPrecedence = PRECEDENCE[el]

            # Se agregar otro renglón en la triplo : variable temporal, segundo operando y operador
            # A partir de la segunda iteración:
            # Se agrega un renglón en la triplo : variable temporal, operando y operador
            taddc.append({
                'obj': f'T{tmpCont}',
                'fuente': op2,
                'op': el
            })
            trSize += 1
            # Se sustituye el operador y los 2 operandos de la variable auxiliar por la variable temporal.
            aux.append(f'T{tmpCont}')

        elif el in OPRE:
            op2 = aux.pop()
            op1 = aux.pop()
            if not lastPrecedence:
                taddc.append({
                    'obj': f'T{tmpCont}',
                    'fuente': op1,
                    'op': '='
                })
                trSize += 1
            taddc.append({
                'obj': f'T{tmpCont}',
                'fuente': op2,
                'op': el
            })
            trSize += 3
            trCont += 1
            obj = f'TR{trCont}'
            if not lastTr:
                lastTr = TR(obj, trSize, start, body)
                taddc.append(lastTr)
            else:
                trN = TR(obj, trSize, start, body)
                lastTr.jmpFalse = trN.jmpFalse
                taddc.append(trN)
                lastTr = trN
            aux.append(obj)
            lastPrecedence = None
        elif el in OPLO:
            band = False
            for i in range(len(taddc)):
                if type(taddc[i]) is not dict:
                    if not band and el == '||':
                        taddc[i].jmpFalse = taddc[i].jmpTrue
                        taddc[i].jmpTrue = lastTr.jmpTrue
                        band = True
                    taddc[i] = [{
                        'obj': taddc[i].obj,
                        'fuente': 'TRUE',
                        'op': taddc[i].jmpTrue
                    }, {
                        'obj': taddc[i].obj,
                        'fuente': 'FALSE',
                        'op': taddc[i].jmpFalse
                    }]

        else:
            # agregar operando a la pila
            aux.append(el)

        # Se verifica el fin de cadena original
        if len(string) == 0:
            break
        # Se regresa al paso P2
        # se lee el siguiente operando
        el = string.pop()

    if not isWhile:
        # Se asigna la cadena auxiliar a la cadena original
        string = aux
        tmp = string.pop()
        if not lastPrecedence:
            taddc.append({
                'obj': 'T1',
                'fuente': tmp,
                'op': '='
            })
            tmp = 'T1'

        # final step, asign last temporal to variable
        taddc.append({
            'obj': var,
            'fuente': tmp,
            'op': '='
        })
    return taddc


# MAIN
if __name__ == "__main__":
    while_case = ['a', 2, '%', 0, '==', 'a', 20, '<', '||']
    data = intermediate_code(while_case, isWhile=True, start=3, body=6)
    print(data)
