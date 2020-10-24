# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

import ply.yacc as yacc
import sys
import ply.lex as lex
from .helpers import three_add_code, infix_to_postfix
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
    print(infix_to_postfix(postfix))
    string = list(reversed(var + postfix + assign))
    
    print(three_add_code(string))


def p_statement_expr(p):
    'statement : expression'
    pass


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = [p[1], p[2], p[3]]


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
