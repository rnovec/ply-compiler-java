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
    ">": 3,
    "<": 3,
    ">=": 3,
    "<=": 3,
    "==": 3,
    "!=": 3,
    "%": 3,
    "*": 3,
    "/": 3,
    "+": 2,
    "-": 2,
    "&&": 2,
    "||": 2,
    "(": 1,
    "||": 0,
    "&&": 0
}
