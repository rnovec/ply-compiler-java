OP_REL_AND_LOG = [">", "<", ">=", '<=', '==', '!=', '&&', '*', '/', '%', '+', '-', '||', '(', ')']
PRECEDENCE_RL = {
    ">": 3,
    "<": 3,
    ">=": 3,
    "<=": 3,
    "==": 3,
    "!=": 3,
    "%": 3,
    "*": 3,
    "/": 3,
    "+": 2,
    "-": 2,
    "&&": 2,
    "||": 2,
    "(": 1,
}


def inf_to_pos_log_rel(array):
    '''
    Funcion para crear un posfijo desde un infijo logico/relacional
    '''
    postfix = []
    opStack = []
    infix = []
    for symbol in array:
        infix.append(symbol)

    for symbol in infix:
        if symbol not in OP_REL_AND_LOG:
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
                    (PRECEDENCE_RL[opStack[len(opStack)-1]]) >= \
                    PRECEDENCE_RL[symbol]:
                postfix.append(opStack.pop())
            opStack.append(symbol)

    while not opStack == []:
        postfix.append(opStack.pop())
    return postfix