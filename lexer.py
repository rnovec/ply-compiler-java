
import ply.lex as lex
import sys
import re

# Palabras Reservadas de Java
reserved = (
    'int',
    'bool',
    'float',
    'string',
    'void',
    # 'while'
)

tokens = (
    'ID',
    'TD',
    # 'IT',
    'OPAR',
    # 'OPRE',
    # 'OPLO',
    'NUMBER',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LBLOCK',
    'RBLOCK',
    'COMA',
    'END_LINE'
)

# Tokens

# Operadores Aritmeticos
t_OPAR = r'\+|-|\*|\%|/'

# Operadores Relacionales
# t_OPRE = r'>=|<=|==|!=|<|>'

# Operadores Logicos
# t_OPLO = r'& & | (\|\|)|\!

t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBLOCK = r'\{'
t_RBLOCK = r'\}'
t_COMA = r','
t_END_LINE = r';'
# String que ignora espacios y tabuladores
t_ignore = ' \t\v'
# Ignora comentarios de tipo /* */
t_ignore_COMMENT = r'/\*(.|\n)*?\*/'


def t_ID(t):
    r'[a-zA-z_]\w*'
    if t.value in reserved:
        if t.value == 'while':
            t.type = 'IT'
        else:
            t.type = 'TD'  # t.value.upper()
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_comment(t):
    r'\//.*'
    pass


def t_error(t):
    line = t.lexer.lineno
    desc = "Character %s not recognized at line %d" % (t.value[0], line)
    t.type = 'LXERR'
    t.value = t.value[0]
    # errors.append({'value': t.value[0], 'line': line, 'type': t.type, 'desc': desc})
    t.lexer.skip(1)
    return t


def tokenizer(data):
    errors = 0
    ftok = open("output/tokens.txt", "w+")
    lex.input(data)
    tokens_matched = list()
    while True:
        token = lex.token()
        if not token:
            break
        ftok.write(f"{token.value}\t\t{token.type}\n")
        if not re.match(r'LXERR', token.type):
            tokens_matched.append({
                # 'line': token.lineno,
                'type': token.type,
                'value': token.value,
                # 'pos': token.lexpos
            })
        else:
            errors += 1
            tokens_matched.append({
                'line': token.lineno,
                'type': token.type + str(errors),
                'value': token.value,
                'pos': token.lexpos
            })
    ftok.close()
    return tokens_matched


# Build the lexer
lex.lex()


# MAIN
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    datos = f.read()
    f.close()
    tokenizer(datos)
