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
    errsint = 0
    lastID = str()

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
        value = None
        try:
            if p[1] == 'float':
                value = float(p[4])
                if not type(p[4]) == float: raise TypeError
            elif p[1] == 'int':
                value = int(p[4])
                if not type(p[4]) == int: raise TypeError
            elif p[1] == 'bool':
                value = bool(p[4])
            elif p[1] == 'string':
                value = str(p[4])
            p[0] = value
        except TypeError:
            self.type_err(p, 2)
            p[0] = value
        finally:
            self.add_var(p, 2, p[1], value)
            
                

    def p_var_declarations_error(self, p):
        '''declarations : ID ID AS1 expression'''
        self.errors[p[1]] = {
            'line': p.lineno(1),
            'value': p[1],
            'desc': "Type error",
            'type': "ERRLXTD",
            # 'pos': p.lexpos(1)
        }

    def p_expression_binop(self, p):
        '''expression : expression OPAR1 expression
                    | expression OPAR2 expression
                    | expression OPAR3 expression
                    | expression OPAR4 expression
                    | expression OPAR5 expression'''
        try:
            p[0] = self.calc(p[2], p[1], p[3])
        except TypeError:
            if p[1] is not None and p[3] is not None:
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
        '''expression : ID AS1 expression'''
        value = None
        try:
            var = self.existing_var(p)
            if type(var) == 'float':
                value = float(p[3])
                if not type(p[3]) == float: raise TypeError
            elif type(var) == 'int':
                value = int(p[3])
                if not type(p[3]) == int: raise TypeError
            elif type(var) == 'bool':
                value = bool(p[3])
            elif type(var) == 'string':
                value = str(p[3])
            #self.add_var(p, 1, type(var), value)
        except TypeError:
            if var is not None:
                self.type_err(p, 1)
        finally:
            p[0] = value
            

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
        value = None
        if p[1] == 'float':
            value = float(0)
        elif p[1] == 'int':
            value = int(0)
        elif p[1] == 'bool':
            value = bool(0)
        elif p[1] == 'string':
            value = str('')
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
                'desc': "Token inesperado",
                # 'pos': p.lexpos
            }
        pass

    def __init__(self):
        self.names = {}
        self.functions = {}
        self.semerrors = list()
        self.errors = dict()
        self.errsint = 0
        self.lexer = JavaLexer()
        self.parser = yacc.yacc(module=self)

    def compile(self, program):
        self.parser.parse(program)
        self.semerrors += self.errors.values()
        return self.semerrors, self.names

    def existing_var(self, var):
        try:
            return self.names[var[1]]['value']
        except LookupError:
            self.undef_name_err(var, 1)
            return None

    def type_err(self, p, index):
        self.semerrors.append({
            'line': p.lineno(index),
            'value': p[index],
            'desc': "Tipos incompatibles",
            'type': f"ERRSEM",
            'pos': p.lexpos(index)
        })
    
    def undef_name_err(self, name, index):
        self.semerrors.append({
            'line': name.lineno(index),
            'value': name[index],
            'desc': "Nombre indefinido",
            'type': "ERRSEM",
            # 'pos': name.lexpos(index)
        })

    def add_var(self, name, index, type, value):
        self.names[name[index]] = {
            'value': value,
            'vartype': type,
            'line': name.lineno(index),
            # 'pos': name.lexpos(index)
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
