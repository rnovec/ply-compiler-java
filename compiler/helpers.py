import re
import csv

OPERATORS = ['*', '/', '%', '+', '-', '(', ')']
PRECEDENCE = {
    "%": 3,
    "*": 3,
    "/": 3,
    "+": 2,
    "-": 2,
    "(": 1,
}


def dictToCsv(data):
    keys = data[0].keys()
    with open('output/taddc.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def flatten(seq):
    l = []
    # if seq is not list or tuple:
    #     return [seq]
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
        if symbol not in OPERATORS:
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


def three_add_code(var, assign, postfix):
    """
    Create a Three Addres Code Table
    from a inverted postfix array
    """
    # reverse the list to use as stack
    string = list(reversed([var] + postfix + [assign]))
    aux = list()  # auxiliar stack
    taddc = list()  # Three Addres Code (EDD)
    tmpCont = 0  # counter of temporals
    el = string.pop()  # get the first operand
    lastPrecedence = None
    while el and len(string):
        # Recorrer la expresión hasta encontrar el primer operador
        if el in OPERATORS:
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
                lastPrecedence = PRECEDENCE[el]

            # Se agregar otro renglón en la triplo : variable temporal, segundo operando y operador
            # A partir de la segunda iteración:
            # Se agrega un renglón en la triplo : variable temporal, operando y operador
            taddc.append({
                'obj': f'T{tmpCont}',
                'fuente': op2,
                'op': el
            })

            # Se sustituye el operador y los 2 operandos de la variable auxiliar por la variable temporal.
            aux.append(f'T{tmpCont}')

            # Se verifica el fin de cadena original
            if len(string) == 1:
                break
        else:
            # agregar operando a la pila
            aux.append(el)
        # Se regresa al paso P2
        # se lee el siguiente operando
        el = string.pop()

    # Se asigna la cadena auxiliar a la cadena original
    string = aux

    # final step, asign last temporal to variable
    tmp = string.pop()
    var = string.pop()
    taddc.append({
        'obj': var,
        'fuente': tmp,
        'op': '='
    })
    return taddc


# MAIN
if __name__ == "__main__":
    case = [5] # define an array for debugger
    case = infix_to_postfix(case)
    three_add_code('w', '=', case)
