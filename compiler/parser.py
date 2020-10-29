# -----------------------------------------------------------------------------
# parser.py
#
# Analizador sintáctico y semántico
# -----------------------------------------------------------------------------

import sys
import re
import json
import ply.yacc as yacc
from .lexer import JavaLexer
from .helpers import flatten, three_add_code, infix_to_postfix, dictToCsv, OPERATORS


class JavaParser(object):

    # Precedence rules for the arithmetic operators
    precedence = (
        ('left', 'OPAR1', 'OPAR2'),
        ('left', 'OPAR3', 'OPAR4')
    )

    # for storing variables
    names = {}
    functions = {}
    semerrors = list()
    taddc = list()
    errors = dict()
    tokens = JavaLexer.tokens
    errsint = 0

    """ 1 : SENTENCIAS RECURSIVAS """

    def p_statement(self, p):
        '''S : sentences S
            | sentences SEP1 S
            | sentences'''
        pass

    def p_sentences(self, p):
        '''sentences : declarations SEP1
            | expression SEP1
            | function
            | iterators'''
        pass

    """ 2 : DECLARACIONES  """

    def p_var_declarations(self, p):
        '''declarations : types ID AS1 expression'''
        self.create_new_var(p[1], p[2], p.lineno(2))
        infix = flatten(p[4])  # obtain a flat array of elements
        self.check_types(p[2], infix, p.lineno(3))
        postfix = infix_to_postfix(infix)
        data = three_add_code(p[2], p[3], postfix)
        self.taddc.append(data)

    def p_var_declarations_error(self, p):
        '''declarations : ID ID AS1 expression'''
        self.errors[p[1]] = {
            'line': p.lineno(1),
            'value': p[1],
            'desc': "Type error",
            'type': "ERRLXTD"
        }

    def p_expression_name_assign(self, p):
        '''expression : ID AS1 expression'''
        # self.names[p[1]] = p[3]
        infix = flatten(p[3])  # obtain a flat array of elements
        self.check_types(p[1], infix, p.lineno(2))
        postfix = infix_to_postfix(infix)
        data = three_add_code(p[1], p[2], postfix)
        self.taddc.append(data)

    def p_expression_binop(self, p):
        '''expression : expression OPAR1 expression
                    | expression OPAR2 expression
                    | expression OPAR3 expression
                    | expression OPAR4 expression
                    | expression OPAR5 expression'''
        p[0] = [p[1], p[2], p[3]]

    def calc(self, op, val1, val2):
        val = None
        if op == '+':
            val = val1 + val2
        elif op == '-':
            val = val1 - val2
        elif op == '*':
            val = val1 * val2
        elif op == '/':
            val = val1 / val2
        return val

    def p_expression_group(self, p):
        'expression : DEL1 expression DEL2'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : CNE'
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : ID'
        # self.existing_var(p[1], p.lineno(1))
        p[0] = p[1]

    """ 3 : FUNCIONES  """

    def p_function(self, p):
        '''function : types ID DEL1 argv DEL2 DEL3 S DEL4
                    | DEL1 argv DEL2 DEL3 S DEL4'''
        self.functions[p[2]] = 0

    def p_function_error(self, p):
        'function : ID ID DEL1 argv DEL2 DEL3 S DEL4'
        self.functions[p[2]] = 0

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
        p[0] = p[1]

    def p_expr(self, p):
        '''expr : expr_rec'''
        pass

    def p_expr_rec(self, p):
        '''expr_rec : val logical expr_rec
                    | val relational expr_rec
                    | val'''
        pass

    def p_val(self, p):
        '''val : ID
               | CNE'''
        self.existing_var(p[1], p.lineno(1))
        p[0] = p[1]

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
                'desc': "Token inesperado",
                # 'pos': p.lexpos
            }
        pass

    def __init__(self):
        self.names = {}
        self.functions = {}
        self.semerrors = list()
        self.taddc = list()
        self.errors = dict()
        self.errsint = 0
        self.lexer = JavaLexer()
        self.parser = yacc.yacc(module=self)

    def compile(self, program):
        self.parser.parse(program)
        self.semerrors += self.errors.values()
        return self.semerrors, self.names, self.taddc

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
            if symbol not in OPERATORS:
                if type(symbol) is str:
                    self.existing_var(symbol, line)
                    try:
                        if self.names[symbol]:
                            if not self.names[symbol]['vartype'] == lastType:
                                self.semerrors.append({
                                    'line': line,
                                    'value': symbol,
                                    'desc': "Tipos incompatibles",
                                    'type': f"ERRSEM"
                                })
                                break
                    except Exception as err:
                        pass
                elif not str(lastType) in str(type(symbol)) and lastType is not None:
                    self.semerrors.append({
                        'line': line,
                        'value': symbol,
                        'desc': "Tipos incompatibles",
                        'type': f"ERRSEM"
                    })
                    break

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
