
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
    'NUMBER',
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
        t.type = 'LXERR'
        t.value = t.value[0]
        # errors.append({'value': t.value[0], 'line': line, 'type': t.type, 'desc': desc})
        t.lexer.skip(1)
        return t

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def create_set(self, T):
        seen = set()
        unique_tokens = list()
        counters = {}
        ftok = open("output/tokens.csv", "w+")
        writer = csv.writer(ftok)
        writer.writerow(["LEX", "TOKEN", "LINE", "POS"])
        for t in self.tokens:
            counters[t] = 0

        for d in T:
            if d['value'] not in seen or re.match(r'LXERR', d['type']):
                seen.add(d['value'])
                unique_tokens.append(d)

        for token in unique_tokens:
            if not re.match(r'LXERR', token['type']) and token['type'] in multiple_tok:
                counters[token['type']] += 1
                token['type'] = token['type'] + str(counters[token['type']])
            # ftok.write(f"{token['value']},{token['type']}\n")
            writer.writerow([token['value'], token['type'],
                            token['line'], token['pos']])
        ftok.close()
        return unique_tokens


    def tokenizer(self, data):
        errors = 0
        self.lexer.input(data)
        tokens = list()
        while True:
            token = self.lexer.token()
            if not token:
                break
            if not re.match(r'LXERR', token.type):
                tokens.append({
                    'line': token.lineno,
                    'type': token.type,
                    'value': token.value,
                    'pos': token.lexpos
                })
            else:
                errors += 1
                tokens.append({
                    'line': token.lineno,
                    'type': token.type + str(errors),
                    'value': token.value,
                    'pos': token.lexpos
                })
        return tokens



# MAIN
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    datos = f.read()
    f.close()
    JL = JavaLexer()
    JL.build()
    T = JL.create_set(JL.tokenizer(datos))
    print(T)
