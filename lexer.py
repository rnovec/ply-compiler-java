#-----------------------
#
# Análisis Léxico
#
#-----------------------
import ply.lex as lex
import sys
import re
import csv

# Palabras Reservadas
reserved = (
    'int',
    'bool',
    'float',
    'string',
    'void',
    'while'
)

# tokens multiples (0-N)
multiple_tok = (
    'ID',
    'CNE'
)


class JavaLexer(object):
    '''
    Clase para el analisis lexico
    '''
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
        'AS1',
        'DEL1',
        'DEL2',
        'DEL3',
        'DEL4',
        'SEP1',
        'SEP2'
    ) + multiple_tok

    # variables auxiliares
    counters = {}
    names = {}
    error_count = 0
    errors = []

    # Tokens

    # Operadores Aritmeticos
    t_OPAR1 = r'\+'
    t_OPAR2 = r'-'
    t_OPAR3 = r'\*'
    t_OPAR4 = r'/'
    t_OPAR5 = r'\%'

    # Operadores Relacionales
    # t_OPRE = r'>=|<=|==|!=|<|>'

    # Operadores Logicos
    # t_OPLO = r'& & | (\|\|)|\!

    t_AS1 = r'='

    # Delimitadores
    t_DEL1 = r'\('
    t_DEL2 = r'\)'
    t_DEL3 = r'\{'
    t_DEL4 = r'\}'

    # Separadores
    t_SEP1 = r';'
    t_SEP2 = r','

    # Ignora espacios, comentarios y tabuladores
    t_ignore = ' \t\v'                      
    t_ignore_COMMENT = r'/\*(.|\n)*?\*/'   

    def t_ID(self, t):
        r'[a-zA-z_]\w*'
        # si es una palabra reservada, asignar token IT o TD
        if t.value in reserved:
            if t.value == 'while':
                t.type = 'IT1'
            else:
                t.type = 'TD' + str(reserved.index(t.value) + 1)
        return t

    def t_CNE(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        # contador de saltos de linea
        t.lexer.lineno += t.value.count("\n") 

    def t_comment(self, t):
        r'\//.*'
        pass

    def t_error(self, t):
        # por cada error lexico
        # aumentar contador de errores
        line = t.lexer.lineno
        self.error_count += 1
        t.type = 'LXERR' + str(self.error_count)
        t.value = t.value[0]
        t.lexer.skip(1) # saltar este token
        return t

    def __init__(self, **kwargs):
        '''
        Este método inicializa el Lexer
        '''
        # contadores de tokens multiples
        for t in multiple_tok:
            self.counters[t] = 0

        # inicilizar los errores en vacio
        self.errors = list()
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenizer(self, data):
        '''
        Params:
        
            data: Un código fuente como string
        '''
        # Archivo de tokens, tabla de simbolos y tokens duplicados
        tokenFile = list()
        seen = set()
        simtable = list()

        # Abrir archivos TXT y CSV
        stfile = open("output/simtable.csv", "w+")
        ftok = open("output/tokensfile.txt", "w+")
        stwriter = csv.writer(stfile)
        stwriter.writerow(["LEX", "TOKEN"])

        self.lexer.input(data)

        while True:
            # mientras haya tokens
            token = self.lexer.token()
            if not token:
                break
            
            if token.value not in seen:
                # si el tokens no esta duplicado
                seen.add(token.value)
                if token.type in multiple_tok:
                    # si es token multiple
                    # aumentar su contador
                    self.counters[token.type] += 1
                    token.type += str(self.counters[token.type])
                    self.names[token.value] = token.type

                # escribirlo en el archivo CSV y agregarlo a lista de tokens únicos
                stwriter.writerow([token.value, token.type])
                simtable.append({
                    'line': token.lineno,
                    'type': token.type,
                    'value': token.value,
                    'pos': token.lexpos
                })
            elif token.type in multiple_tok:
                # si esta repetido asignar el token existente
                token.type = self.names[token.value]

            tokenFile.append({
                'line': token.lineno,
                'type': token.type,
                'value': token.value,
                'pos': token.lexpos
            })
            if token.type == 'SEP1':
                ftok.write(token.type + '\n')
            else:
                ftok.write(token.type + ' ')
        stfile.close()
        ftok.close()
        return tokenFile, simtable


# MAIN
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    datos = f.read()
    f.close()
    JL = JavaLexer()
    TF, ST = JL.tokenizer(datos)
    print(ST)
