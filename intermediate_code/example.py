# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

import ply.yacc as yacc
import sys
import ply.lex as lex
tokens = (
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN',
)

# Tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


# Build the lexer
lex.lex()


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


# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# dictionary of names (for storing variables)
names = {}


def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]
    var = [p[1]]
    assign = [p[2]]
    postfix = flatten(p[3]) # obtain a flat array of elements
    # reverse the list to use as stack
    string = list(reversed(var + postfix + assign))
    print(postfix)
    print(three_add_code(string))

def three_add_code(string):
    """
    Create a Three Addres Code Table
    from a inverted postfix array
    """
    aux = list() # auxiliar stack
    taddc = list()  # Three Addres Code (EDD)
    print(string)
    i = 0 # counter of iterations
    el = string.pop() # get the first operand
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

def p_statement_expr(p):
    'statement : expression'
    pass


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = [p[1], p[3], p[2]]


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]


def p_error(p):
    print(f"Syntax error at {p.value!r}")


yacc.yacc()

# MAIN
if __name__ == "__main__":
    file = sys.argv[1]
    f = open(file, 'r')
    program = f.read()
    f.close()
    yacc.parse(program)
