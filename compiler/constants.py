"""
Author: Raul Novelo
        raul.novelo@aaaimx.org

        Constants of the program
"""

OPAR = ['*', '/', '%', '+', '-', '(', ')']
OPRE = ['<', '>', '<=', '>=', '==', '!=']
OPLO = ['&&', '||']
OPERATORS = OPAR + OPRE + OPLO
PRECEDENCE = {
    "%": 4,
    "*": 4,
    "/": 4,
    "+": 3,
    "-": 3,
    "(": 2,
    ">": 1,
    "<": 1,
    ">=": 1,
    "<=": 1,
    "==": 1,
    "!=": 1,
    "||": 0,
    "&&": 0,
}
ASSEMBLY = {
    "=": 'MOV',
    "%": 'DIV',
    "*": 'MUL',
    "/": 'DIV',
    "+": 'ADD',
    "-": 'SUB',
    ">": 'JG',
    "<": 'JL',
    ">=": 'JGE',
    "<=": 'JLE',
    "==": 'JE',
    "!=": 'JNE'
}

REGISTERS = {
    'T1': 'AX',
    'T2': 'BX',
    'T3': 'CX',
    'T4': 'DX',
}
