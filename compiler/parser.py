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

    # for storing variables
    names = {}
    functions = {}
    semerrors = list()
    errors = dict()
    tokens = JavaLexer.tokens
    errsemcount = 0
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
        try:
            value = None
            if p[1] == 'float' and type(p[4]) == float:
                value = float(p[4])
            elif p[1] == 'int' and type(p[4]) == int:
                value = int(p[4])
            elif p[1] == 'bool':
                value = bool(p[4])
            elif p[1] == 'string':
                value = str(p[4])
            else: raise TypeError
            self.add_var(p, 2, p[1], value)
            p[0] = p[4]
        except TypeError:
            print(p[1], p[2], type(p[4]))
            self.type_err(p, 2)
            p[0] = 0
            

    def p_var_declarations_error(self, p):
        '''declarations : ID ID AS1 expression'''
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
        print('Line', p.lineno(2))
        try:
            p[0] = self.calc(p[2], p[1], p[3])
        except TypeError:
            self.type_err(p, 2)
            p[0] = 0
        

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
        p[0] = self.existing_var(p)

    def p_expression_name_assign(self, p):
        'expression : ID AS1 expression'
        p[0] = self.existing_var(p)

    """ 3 : FUNCIONES  """

    def p_function(self, p):
        '''function : types ID DEL1 argv DEL2 DEL3 S DEL4'''
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
        value = None
        if p[1] == 'float':
            value = 0.0
        elif p[1] == 'int':
            value = 0
        elif p[1] == 'bool':
            value = False
        elif p[1] == 'string':
            value = ''
        self.add_var(p, 2, p[1], value)

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
        try:
            print(float(p[1]))
            p[0] = float(p[1])
        except ValueError:
            p[0] = self.existing_var(p)
              

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
                'desc': "Unexpected token",
                'pos': p.lexpos
            }
        pass

    def __init__(self):
        self.names = {}
        self.functions = {}
        self.semerrors = list()
        self.errors = dict()
        self.errsemcount = 0
        self.errsint = 0
        self.lexer = JavaLexer()
        self.parser = yacc.yacc(module=self)

    def compile(self, program):
        self.parser.parse(program)
        self.semerrors += self.errors.values()
        return self.semerrors, self.names

    def existing_var(self, var):
        try:
            print(self.names[var[1]]['value'])
            return self.names[var[1]]['value']
        except LookupError:
            # print(f"Undefined name {p[1]!r}")
            self.undef_name_err(var, 1)
            return 0

    def type_err(self, p, index):
        self.errsemcount += 1
        self.semerrors.append({
            'line': p.lineno(index),
            'value': p[index],
            'desc': "Types doesn't match",
            'type': f"ERRSEM{self.errsemcount}",
            'pos': p.lexpos(index)
        })
    
    def undef_name_err(self, name, index):
        self.errsemcount += 1
        self.semerrors.append({
            'line': name.lineno(index),
            'value': name[index],
            'desc': "Undefined name",
            'type': f"ERRSEM{self.errsemcount}",
            'pos': name.lexpos(index)
        })

    def add_var(self, name, index, type, value):
        self.names[name[index]] = {
            'value': value,
            'vartype': type,
            'line': name.lineno(index),
            'pos': name.lexpos(index)
        }
        
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
                s = input('pyjava > ')
            except EOFError:
                break
            JavaParser().parser.parse(s)
