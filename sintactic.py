import ply.yacc as yacc
import os
import codecs
import re
from lexer import tokens
import sys


precedence = (
    ('right', 'ID', 'WHILE'),
    ('right', 'ASSIGN'),
    ('left', 'NOEQUAL'),
    ('left', 'GREATERTHAN', 'LESSTHAN', 'LESS', 'GREATER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'EXCLA'),
)



""" SENTENCIAS RECURSIVAS : FUNCIONES Y DECLARACIONES """


def p_rec_sentences(p):
    '''S : sentences S
         | sentences END_LINE'''
    print('Sentences 1')

def p_sentences(p):
    'S : sentences'
    print('Sentences 2')



def p_declarations(p):
    'sentences : declaration'
    print('Declaraciones 3')


""" 1 : DECLARACIONES """


def p_declaration(p):
    'declaration : types ID ASSIGN values'
    print('Variable declaration')


def p_types(p):
    '''types : INT
             | STRING
             | FLOAT
             | BOOLEAN
             | VOID'''
    print('tipos')


def p_values(p):
    '''values : NUMBER'''
    print('valor')

""" 1 : FUNCIONES """


# def p_function(p):
#     'funciones : tipos ID LPAREN argv RPAREN LBLOCK bloque_tipo RBLOCK'
#     pass


def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("Sintantic: syntax error '%s' in line %d" % (p.value, p.lineno))
    sys.exit()


# MAIN
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    parser = yacc.yacc()
    result = parser.parse(program)
    print(result)
