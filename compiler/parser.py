# -----------------------------------------------------------------------------
# parser.py
#
# Analizador sintáctico y semántico 
# -----------------------------------------------------------------------------
import ply.yacc as yacc
import sys
from .lexer import JavaLexer
import re

class JavaParser(object):

    # Precedence rules for the arithmetic operators
    precedence = ()

    # dictionary of names (for storing variables)
    names = {}
    functions = {}
    vars = list()
    semerrors = list()
    errors = dict()
    tokens = JavaLexer.tokens
    errsemcount = 0
    errsint = 0


    """ 1 : SENTENCIAS RECURSIVAS """

    def p_statement(self, p):
        '''S : sentences S
            | sentences SEP1 S'''
        pass

    def p_sentences(self, p):
        'S : sentences'
        pass

    def p_declarations(self, p):
        'sentences : declarations SEP1'
        pass

    def p_expressions(self, p):
        'sentences : expression SEP1'
        pass

    def p_functions(self, p):
        'sentences : function'
        pass

    def p_iterators(self, p):
        'sentences : iterators'
        pass


    """ 2 : DECLARACIONES  """

    def p_var_declarations(self, p):
        '''declarations : types ID AS1 expression'''
        print(p[4])
        value = None
        if p[1] == 'float':
            value = float(p[4])
        elif p[1] == 'int':
            value = int(p[4])
        elif p[1] == 'bool':
            value = bool(p[4])
        elif p[1] == 'char':
            value = str(p[4])
        self.names[p[2]] = {
            'value': value,
            'vartype': p[1],
            'line': p.lineno(2),
            'pos': p.lexpos(2)
        }
        p[0] = p[4]

    def p_var_declarations_error(self, p):
        '''declarations : ID ID AS1 expression'''
        print('Tipo:', p[1])
        self.errors[p[1]] = {
            'line': p.lineno(1),
            'value': p[1],
            'desc': "Type error",
            'type': "ERRLXTD",
            'pos': p.lexpos(1)
        }

    def p_expression_binop(self, p):
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

    def p_expression_group(self, p):
        'expression : DEL1 expression DEL2'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : CNE'
        p[0] = p[1]

    def p_expression_empty(self, p):
        'expression : '
        pass

    def p_expression_name(self, p):
        'expression : ID'
        try:
            print(self.names[p[1]]['value'])
            p[0] = self.names[p[1]]['value']
        except LookupError:
            print(f"Undefined name {p[1]!r}")
            self.errsemcount += 1
            self.semerrors.append({
                'line': p.lineno(1),
                'value': p[1],
                'desc': "Undefined name",
                'type': f"ERRSEM{self.errsemcount}",
                'pos': p.lexpos(1)
            })
            p[0] = 0

    def p_expression_name_assign(self, p):
        'expression : ID AS1 expression'
        try:
            print(self.names[p[1]]['value'])
            self.names[p[1]]['value'] = p[3]
        except LookupError:
            print(f"Undefined name {p[1]!r}")
            self.errsemcount += 1
            self.semerrors.append({
                'line': p.lineno(1),
                'value': p[1],
                'desc': "Undefined name",
                'type': f"ERRSEM{self.errsemcount}",
                'pos': p.lexpos(1)
            })
            p[0] = 0

    """ 3 : FUNCIONES  """

    def p_function(self, p):
        '''function : types ID DEL1 argv DEL2 DEL3 S DEL4'''
        self.functions[p[2]] = 0

    def p_function_error(self, p):
        'function : ID ID DEL1 argv DEL2 DEL3 S DEL4'
        print(p[1], p[2])
        self.functions[p[2]] = 0

    def p_argv(self, p):
        '''argv : argv_rec
                | '''
        pass

    def p_argv_rec(self, p):
        '''argv_rec : types ID SEP2 argv_rec
                    | types ID'''
        value = None
        if p[1] == 'float':
            value = 0.0
        elif p[1] == 'int':
            value = 0
        elif p[1] == 'bool':
            value = False
        elif p[1] == 'char':
            value = ''
        self.names[p[2]] = {
            'value': value,
            'vartype': p[1],
            'line': p.lineno(2),
            'pos': p.lexpos(2)
        }

    def p_types(self, p):
        '''types : TD1
                | TD2
                | TD3
                | TD4
                | TD5'''
        p[0] = p[1]

    """ 4 : SECUENCIAS ITERATIVAS"""

    def p_while(self, p):
        '''iterators : IT1 DEL1 expr DEL2 DEL3 S DEL4'''
        print(p[1])

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
            print(f"Unexpected token '{p.value}'")
            self.errors[p.value] = {
                'line': p.lineno,
                'value': p.value,
                'type': 'ERR' + p.type,
                'desc': "Unexpected token",
                'pos': p.lexpos
            }
        pass

    def __init__(self):
        self.errors = dict()
        self.semerrors = list()
        self.errsemcount = 0
        self.lexer = JavaLexer()
        self.parser = yacc.yacc(module=self)

    def compile(self, program):
        self.parser.parse(program)
        self.semerrors += self.errors.values()
        return self.semerrors, self.names


# MAIN
if __name__ == "__main__":
    try:
        file = sys.argv[1]
        f = open(file, 'r')
        program = f.read()
        f.close()
        JavaParser().compile(program)
    except IndexError:
        while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            JavaParser().parser.parse(s)
