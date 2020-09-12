# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------
import ply.yacc as yacc
import sys
from lexer import tokens

# Precedence rules for the arithmetic operators
precedence = ()

# dictionary of names (for storing variables)
names = {}
functions = {}
errors = list()

""" 1 : SENTENCIAS RECURSIVAS """

def p_statement(p):
    '''S : sentences S
         | sentences END_LINE1 S'''
    pass


def p_sentences(p):
    'S : sentences'
    pass


def p_declarations(p):
    'sentences : declarations END_LINE1'
    pass


def p_expressions(p):
    'sentences : expression END_LINE1'
    pass


def p_functions(p):
    'sentences : function'
    pass


""" 2 : DECLARACIONES  """

def p_var_declarations(p):
    '''declarations : types ID ASSIGN1 expression'''
    names[p[2]] = p[4]


def p_expression_binop(p):
    '''expression : expression OPAR1 expression
                  | expression OPAR2 expression
                  | expression OPAR3 expression
                  | expression OPAR4 expression
                  | expression OPAR5 expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_group(p):
    'expression : DEL1 expression DEL2'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_empty(p):
    'expression : '
    pass


def p_expression_name(p):
    'expression : ID'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        errors.append("Sintantic: syntax error '%s' in line %d" %
                      (p[1], p.lexer.lineno))
        p[0] = 0


def p_expression_name_assign(p):
    'expression : ID ASSIGN1 expression'
    try:
        print(names[p[1]])
        names[p[1]] = p[3]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        errors.append("Sintantic: syntax error '%s' in line %d" %
                      (p[1], p.lexer.lineno))
        p[0] = 0


""" 3 : FUNCIONES  """

def p_function(p):
    '''function : types ID DEL1 argv DEL2 DEL3 S DEL4'''
    functions[p[2]] = 0
    

def p_function_error(p):
    'function : ID ID DEL1 argv DEL2 DEL3 S DEL4'
    functions[p[2]] = 0
    
def p_argv(p):
    '''argv : argv_rec
            | '''
    pass


def p_argv_rec(p):
    '''argv_rec : types ID SEP1 argv_rec
                | types ID'''
    names[p[2]] = 0

def p_types(p):
    '''types : TD1
             | TD2
             | TD3
             | TD4
             | TD5'''
    

""" 4 : ERRORES  """
def p_error(p):
    print("Sintantic: syntax error '%s' in line %d" % (p.value, p.lineno))
    sys.exit()


yacc.yacc()
# MAIN
if __name__ == "__main__":
    try:
        file = sys.argv[1]
        f = open(file, 'r')
        program = f.read()
        f.close()
        parser = yacc.yacc()
        result = parser.parse(program)
        print(result)
    except IndexError:
        while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            yacc.parse(s)
