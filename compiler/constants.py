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
