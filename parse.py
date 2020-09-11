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
errors = list()

""" SENTENCIAS RECURSIVAS """

def p_statement(p):
    '''S : sentences S
         | sentences END_LINE S'''
    print(p[1])


def p_sentences(p):
    'S : sentences'
    p[0] = p[1]


def p_declarations(p):
    'sentences : declarations'
    p[0] = p[1]


def p_expressions(p):
    'sentences : expression'
    p[0] = p[1]


# def p_functions(p):
#     'sentences : function'
#     print(p[1])


""" 1 : DECLARACIONES  """

def p_var_declarations(p):
    'declarations : TD ID EQUALS expression'
    names[p[2]] = p[4]


def p_expression_binop(p):
    '''expression : expression OPAR expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
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
                      (p.value, p.lineno))
        p[0] = 0


""" 1 : FUNCIONES  """


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
