# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------
import ply.yacc as yacc
import sys
from lexer import JavaLexer


""" 1 : SENTENCIAS RECURSIVAS """


class JavaParser(object):

    # Precedence rules for the arithmetic operators
    precedence = ()

    # dictionary of names (for storing variables)
    names = {}
    functions = {}
    errors = list()
    tokens = JavaLexer.tokens

    def p_statement(self, p):
        '''S : sentences S
            | sentences END_LINE1 S'''
        pass

    def p_sentences(self, p):
        'S : sentences'
        pass

    def p_declarations(self, p):
        'sentences : declarations END_LINE1'
        pass

    def p_expressions(self, p):
        'sentences : expression END_LINE1'
        pass

    def p_functions(self, p):
        'sentences : function'
        pass

    """ 2 : DECLARACIONES  """

    def p_var_declarations(self, p):
        '''declarations : types ID ASSIGN1 expression'''
        self.names[p[2]] = p[4]

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
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_empty(self, p):
        'expression : '
        pass

    def p_expression_name(self, p):
        'expression : ID'
        try:
            p[0] = self.names[p[1]]
        except LookupError:
            print(f"Undefined name {p[1]!r}")
            self.errors.append({
                'line': p.lineno(1),
                'value': p[1],
                'desc': "Undefined name",
                'pos': p.lexpos(1)
            })
            p[0] = 0

    def p_expression_name_assign(self, p):
        'expression : ID ASSIGN1 expression'
        try:
            print(self.names[p[1]])
            self.names[p[1]] = p[3]
        except LookupError:
            print(f"Undefined name {p[1]!r}")
            self.errors.append({
                'line': p.lineno(1),
                'value': p[1],
                'desc': "Undefined name",
                'pos': p.lexpos(1)
            })
            p[0] = 0

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
        '''argv_rec : types ID SEP1 argv_rec
                    | types ID'''
        self.names[p[2]] = 0

    def p_types(self, p):
        '''types : TD1
                | TD2
                | TD3
                | TD4
                | TD5'''

    """ 4 : ERRORES  """

    def p_error(self, p):
        self.errors.append({
            'line': p.lineno,
            'value': p.value,
            'desc': "Unexpected token",
            'pos': p.lexpos
        })

    def __init__(self):
        self.errors = list()
        self.lexer = JavaLexer()
        self.parser = yacc.yacc(module=self)

    def compile(self, program):
        self.parser.parse(program)
        return self.errors


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
            yacc.parse(s)
