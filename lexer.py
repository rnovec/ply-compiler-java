import ply.lex as lex
import sys

# Palabras Reservadas de JavaScript
reserved = (
    'int',
    'boolean',
    'float',
    'string',
    'void',
    'while'
)

# Lista de tokens
tokens = (
    'END_LINE',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LBLOCK',
    'RBLOCK',
    'ID',
    'COMA',
    'STRINGS',
    'EQUALS',
    'LESS',
    'GREATER',
    'LESSTHAN',
    'GREATERTHAN',
    'NOEQUAL',
    'YLOGIC',
    'OLOGIC',
    'EXCLA'
) + tuple(map(lambda s:s.upper(),reserved))
 

# Operadores Aritmeticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'\%'

#Operadores Relacionales
t_GREATERTHAN = r'>='
t_LESSTHAN = r'<='
t_EQUALS = r'=='
t_NOEQUAL = r'!='
t_LESS = r'<'
t_GREATER = r'>'

#Operadores Logicos
t_YLOGIC = r'&&'
t_OLOGIC = r'\|\|'
t_EXCLA = r'\!'

t_END_LINE = r';'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBLOCK = r'\{'
t_RBLOCK = r'\}'
t_COMA = r','

# Cadena de Caracteres
t_STRINGS = r'\"([^\\\n]|(\\(.|\n)))*?\"'
# String que ignora espacios y tabuladores
t_ignore = ' \t\v'
# Ignora comentarios de tipo /* */
t_ignore_COMMENT = r'/\*(.|\n)*?\*/'
    

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    print('NUMBER')
    return t
 
def t_ID(t):
    r'[a-zA-z_]\w*'
    if t.value in reserved:
        print('ID')
        t.type = t.value.upper()
    return t
 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
 
def t_comment(t):
    r'\//.*'
    pass

def t_error(t):
    line = t.lexer.lineno
    print("Character %s not recognized at line %d" % (t.value[0], line))
    t.lexer.skip(1)


lex.lex()

# MAIN 
if __name__ == "__main__":
    f = open(sys.argv[1],'r')
    datos = f.read()
    f.close()
    ftok = open("output/tokens.txt","w+")
    lex.input(datos)
    
    while 1 :
    	token = lex.token()
    	if not token: break
    	ftok.write(f"{token.lineno}: <{token.type}, {token.value}> \n")
    ftok.close()
