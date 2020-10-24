import re


def flatten(seq):
    l = []
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l


def infix_to_postfix(infix):
    ''' 
    Funcion para crear un posfijo desde un infijo
    '''
    precedence = {
        "*": 3,
        "/": 3,
        "+": 2,
        "-": 2,
        "(": 1,
    }
    postfix = []
    opStack = []
    validator = re.compile(r'([a-zA-Z]|[0-9])')

    for symbol in infix:
        if validator.match(symbol):
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
                    (precedence[opStack[len(opStack)-1]]) >= \
                    precedence[symbol]:
                postfix.append(opStack.pop())
            opStack.append(symbol)

    while not opStack == []:
        postfix.append(opStack.pop())
    return postfix


def three_add_code(string):
    """
    Create a Three Addres Code Table
    from a inverted postfix array
    """
    aux = list()  # auxiliar stack
    taddc = list()  # Three Addres Code (EDD)
    print(string)
    i = 0  # counter of iterations
    el = string.pop()  # get the first operand
    while el and len(string):
        # Recorrer la expresión hasta encontrar el primer operador
        if el in ['*', '-', '+', '/']:
            # Asignar a una variable auxiliar, el operador y los operandos previos
            # Asignar a una segunda variable auxiliar, el operador y los 2 operandos previos.
            op1 = aux.pop()
            op2 = aux.pop()

            # En la primera iteración:
            if i == 0:
                # Se agrega un renglón en la triplo : variable temporal, primer operando y la operación (=)
                taddc.append({
                    'obj': 'T1',
                    'fuente': op2,
                    'op': '='
                })
            # Se agregar otro renglón en la triplo : variable temporal, segundo operando y operador
            # A partir de la segunda iteración:
            # Se agrega un renglón en la triplo : variable temporal, operando y operador
            taddc.append({
                'obj': 'T1',
                'fuente': op1,
                'op': el
            })

            # Se sustituye el operador y los 2 operandos de la variable auxiliar por la variable temporal.
            aux.append('T1')
            i += 1  # increment counter

            # Se verifica el fin de cadena original
            if len(string) == 1:
                # Se asigna la cadena auxiliar a la cadena original
                string = aux
                break
        else:
            # agregar operando a la pila
            aux.append(el)
        # Se regresa al paso P2
        # se lee el siguiente operando
        el = string.pop()

    # final step, asign last temporal to variable
    tmp = string.pop()
    var = string.pop()
    taddc.append({
        'obj': var,
        'fuente': tmp,
        'op': '='
    })
    return taddc
