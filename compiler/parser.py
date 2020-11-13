"""
Author: Raul Novelo
        raul.novelo@aaaimx.org

        `parser.py` is a implementation of Yacc and uses 
        tokens declared in `lexer.py`.

        Sintatic and Semantic Analysis.
"""

import sys
import re
import json
import ply.yacc as yacc
from .lexer import JavaLexer
from .helpers import *
from .three_add_code import *
from random import randint


class JavaParser(object):
    """
    Class for Sintatic and Semantic Analysis
    """

    # Precedence rules for the arithmetic operators
    precedence = (
        ('left', 'OPAR1', 'OPAR2'),
        ('left', 'OPAR3', 'OPAR4')
    )

    # for storing variables
    names = {}
    functions = {}
    semerrors = list()
    triplo = list()
    errors = dict()
    tokens = JavaLexer.tokens
    errsint = 0

    """ 1 : SENTENCIAS RECURSIVAS """

    def p_statement(self, p):
        '''S : sentences S
            | sentences SEP1 S
            | sentences'''
        p[0] = p[1]

    def p_sentences(self, p):
        '''sentences : declarations SEP1
            | expression SEP1
            | function
            | iterators'''
        p[0] = p[1]
        if p[1]:
            self.triplo.append(p[1])

    """ 2 : DECLARACIONES  """

    def p_var_declarations(self, p):
        '''declarations : types ID AS1 expression'''
        self.create_new_var(p[1], p[2], p.lineno(2))
        p[0] = self.taddc_aritmetic(p[2], p[3], p[4], p.lineno(2))

    def p_var_declarations_error(self, p):
        '''declarations : ID ID AS1 expression'''
        self.errors[p[1]] = {
            'line': p.lineno(1),
            'value': p[1],
            'desc': "Type error",
            'type': "ERRLXTD"
        }
        p[0] = self.taddc_aritmetic(p[2], p[3], p[4], p.lineno(2))

    def p_expression_name_assign(self, p):
        '''declarations : ID AS1 expression'''
        # self.names[p[1]] = p[3]
        p[0] = self.taddc_aritmetic(p[1], p[2], p[3], p.lineno(2))

    def p_expression_binop(self, p):
        '''expression : expression OPAR1 expression
                    | expression OPAR2 expression
                    | expression OPAR3 expression
                    | expression OPAR4 expression
                    | expression OPAR5 expression'''
        p[0] = [p[1], p[2], p[3]]

    def p_expression_group(self, p):
        'expression : DEL1 expression DEL2'
        p[0] = [p[1], p[2], p[3]]

    def p_expression_number(self, p):
        'expression : CNE'
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : ID'
        p[0] = p[1]

    """ 3 : FUNCIONES  """

    def p_function(self, p):
        '''function : types ID DEL1 argv DEL2 DEL3 S DEL4
                    | DEL1 argv DEL2 DEL3 S DEL4'''
        pass

    def p_function_error(self, p):
        'function : ID ID DEL1 argv DEL2 DEL3 S DEL4'
        pass

    def p_argv(self, p):
        '''argv : argv_rec
                | '''
        pass

    def p_argv_rec(self, p):
        '''argv_rec : types ID SEP2 argv_rec
                    | types ID'''
        self.create_new_var(p[1], p[2], p.lineno(2))

    def p_types(self, p):
        '''types : TD1
                | TD2
                | TD3
                | TD4
                | TD5'''
        p[0] = p[1]

    """ 4 : ITERADORES """

    def p_while(self, p):
        '''iterators : IT1 DEL1 expr DEL2 DEL3 S DEL4'''
        infix = flatten(p[3])
        p[0] = {'type': p[1],
                'line': p.lineno(1),
                'cond': infix_to_postfix(infix),
                'triplo': [],
                'end': p.lineno(7)
                }

    def p_expr(self, p):
        '''expr : expr_rec'''
        p[0] = p[1]

    def p_expr_binop(self, p):
        '''expr : expr OPAR1 expr
                | expr OPAR2 expr
                | expr OPAR3 expr
                | expr OPAR4 expr
                | expr OPAR5 expr'''
        p[0] = [p[1], p[2], p[3]]

    def p_val(self, p):
        '''expr : ID
               | CNE'''
        p[0] = p[1]

    def p_expr_rec(self, p):
        '''expr_rec : expr logical expr
                    | expr relational expr'''
        p[0] = [p[1], p[2], p[3]]

    def p_relational(self, p):
        '''relational : OPRE1
                | OPRE2
                | OPRE3
                | OPRE4
                | OPRE5
                | OPRE6'''
        p[0] = p[1]

    def p_logical(self, p):
        '''logical : OPLO1
                | OPLO2
                | OPLO3'''
        p[0] = p[1]

    """ 5 : ERRORES  """

    def p_error(self, p):
        self.errsint += 1
        if not re.match(r'ERRLX', p.type):
            # print(f"Unexpected token '{p.value}'")
            self.errors[p.value] = {
                'line': p.lineno,
                'value': p.value,
                'type': 'ERR' + p.type,
                'desc': "Token inesperado"
            }
        pass

    def __init__(self):
        self.names = {}
        self.functions = {}
        self.semerrors = list()
        self.triplo = list()
        self.errors = dict()
        self.errsint = 0
        self.lexer = JavaLexer()
        self.parser = yacc.yacc(module=self)
        self.taddc = IntermediateCode()

    def compile(self, program):
        self.parser.parse(program)
        self.semerrors += self.errors.values()
        self.triplo = list(sorted(self.triplo, key=lambda i: i['line']))
        size = start = body = 0
        taddc_table = list()
        isWhile = False
        for i in range(len(self.triplo)):
            el = self.triplo[i]
            if el['type'] == 'while':
                w_index = i
                start = size + 1
                isWhile = True
                continue
            elif isWhile:
                line_end = self.triplo[w_index]['end']
                if el['line'] <= line_end:
                    t = self.triplo[i]
                    self.triplo[w_index]['triplo'] += t['triplo']
                try:
                    nextEl = self.triplo[i + 1]
                except:
                    nextEl = None
                if not nextEl or nextEl['line'] > line_end:
                    body = len(self.triplo[w_index]['triplo'])
                    data = self.taddc.iterative(
                        self.triplo[w_index]['cond'], start=start, body=body)
                    taddc_table += flatten(data)
                    taddc_table += self.triplo[w_index]['triplo']
                    taddc_table.append({
                        'obj': '',
                        'fuente': start,
                        'op': 'JR'
                    })
                    size = len(taddc_table)
                    isWhile = False
            else:
                taddc_table += el['triplo']
                size += len(el['triplo'])
        taddc_table.append({
            'obj': '',
            'fuente': '',
            'op': ''
        })
        return self.semerrors, self.names, taddc_table

    def taddc_aritmetic(self, var, assign, expression, line):
        infix = flatten(expression)  # obtain a flat array of elements
        self.check_types(var, infix, line)
        postfix = infix_to_postfix(infix)
        data = self.taddc.aritmetic(postfix, var)
        return {
            'type': 'aritmetic',
            'line': line,
            'triplo': data
        }

    def compile_from_file(self, file_path):
        f = open(file_path, 'r')
        program = f.read()
        self.compile(program)
        f.close()

    def existing_var(self, name, line):
        try:
            float(name)
        except ValueError as err:
            try:
                if self.names[name]['vartype']:
                    pass
            except KeyError as err:
                # print('Undefined name:', err)
                self.semerrors.append({
                    'value': name,
                    'line': line,
                    'desc': "Nombre indefinido",
                    'type': "ERRSEM"
                })

    def check_types(self, var, infix, line):
        lastType = None
        self.existing_var(var, line)
        try:
            if self.names[var]:
                lastType = self.names[var]['vartype']
        except Exception as err:
            pass
        for symbol in infix:
            if symbol not in OPAR:
                if type(symbol) is str:
                    self.existing_var(symbol, line)
                    try:
                        if self.names[symbol]:
                            if not self.names[symbol]['vartype'] == lastType:
                                self.add_type_err(symbol, line)
                                break
                    except Exception as err:
                        pass
                elif not str(lastType) in str(type(symbol)) and lastType is not None:
                    self.add_type_err(symbol, line)
                    break

    def add_type_err(self, symbol, line):
        self.semerrors.append({
            'line': line,
            'value': symbol,
            'desc': "Tipos incompatibles",
            'type': f"ERRSEM"
        })

    def create_new_var(self, type, name, line):
        self.names[name] = {
            'value': name,
            'vartype': type,
            'line': line
        }
        # print('New name declared:', self.names[name])


# MAIN
if __name__ == "__main__":
    while True:
        try:
            s = input('pyjava > ')
        except EOFError:
            break
        JavaParser().parser.parse(s)
