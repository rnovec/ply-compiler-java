
import ply.lex as lex
import sys
import re
import csv

# Palabras Reservadas de Java
reserved = (
    'int',
    'bool',
    'float',
    'string',
    'void',
    'while'
)

multiple_tok = (
    'ID',
    'NUMBER'
)


class JavaLexer(object):
    tokens = (
        'TD1',
        'TD2',
        'TD3',
        'TD4',
        'TD5',
        'IT1',
        'OPAR1',
        'OPAR2',
        'OPAR3',
        'OPAR4',
        'OPAR5',
        # 'OPRE',
        # 'OPLO',
        'ASSIGN1',
        'DEL1',
        'DEL2',
        'DEL3',
        'DEL4',
        'SEP1',
        'END_LINE1'
    ) + multiple_tok

    counters = {}
    names = {}
    error_count = 0
    errors = []

    # Tokens

    # Operadores Aritmeticos
    t_OPAR1 = r'\+'
    t_OPAR2 = r'-|/'
    t_OPAR3 = r'\*/'
    t_OPAR4 = r'/'
    t_OPAR5 = r'\%/'

    # Operadores Relacionales
    # t_OPRE = r'>=|<=|==|!=|<|>'

    # Operadores Logicos
    # t_OPLO = r'& & | (\|\|)|\!

    t_ASSIGN1 = r'='
    t_DEL1 = r'\('
    t_DEL2 = r'\)'
    t_DEL3 = r'\{'
    t_DEL4 = r'\}'
    t_SEP1 = r','
    t_END_LINE1 = r';'
    # String que ignora espacios y tabuladores
    t_ignore = ' \t\v'
    # Ignora comentarios de tipo /* */
    t_ignore_COMMENT = r'/\*(.|\n)*?\*/'

    def t_ID(self, t):
        r'[a-zA-z_]\w*'
        if t.value in reserved:
            if t.value == 'while':
                t.type = 'IT1'
            else:
                t.type = 'TD' + str(reserved.index(t.value) + 1)
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_comment(self, t):
        r'\//.*'
        pass

    def t_error(self, t):
        line = t.lexer.lineno
        desc = "Character %s not recognized at line %d" % (t.value[0], line)
        self.error_count += 1
        t.type = 'LXERR' + str(self.error_count)
        t.value = t.value[0]
        t.lexer.skip(1)
        self.errors.append({
            'line': t.lineno,
            'type': t.type,
            'value': t.value,
            'pos': t.lexpos
        })
        return t

    # Build the lexer
    def build(self, **kwargs):
        for t in multiple_tok:
            self.counters[t] = 0
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenizer(self, data):
        self.lexer.input(data)
        tokenFile = list()
        seen = set()
        simtable = list()
        stfile = open("output/simtable.csv", "w+")
        ftok = open("output/tokensfile.txt", "w+")
        stwriter = csv.writer(stfile)
        stwriter.writerow(["LEX", "TOKEN"])

        while True:
            token = self.lexer.token()
            if not token:
                break
            if token.value not in seen:
                seen.add(token.value)
                if token.type in multiple_tok:
                    self.counters[token.type] += 1
                    token.type += str(self.counters[token.type])
                    self.names[token.value] = token.type
        
                stwriter.writerow([token.value, token.type])
                simtable.append({
                    'line': token.lineno,
                    'type': token.type,
                    'value': token.value,
                    'pos': token.lexpos
                })
            elif token.type in multiple_tok:
                token.type = self.names[token.value]

            tokenFile.append({
                'line': token.lineno,
                'type': token.type,
                'value': token.value,
                'pos': token.lexpos
            })
            if token.type == 'END_LINE1':
                ftok.write(token.type + '\n')
            else:
                ftok.write(token.type + ' ')
        stfile.close()
        ftok.close()
        return tokenFile, simtable, self.errors


# MAIN
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    datos = f.read()
    f.close()
    JL = JavaLexer()
    JL.build()
    TF, ST, ERR = JL.tokenizer(datos)
    print(ST)
