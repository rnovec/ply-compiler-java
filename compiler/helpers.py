"""
Author: Raul Novelo
        raul.novelo@aaaimx.org

        Paul Mena
        paul.mena@aaaimx.org

        helper functions for performance especific task of compiler
        like create flat lists, generate output files and convert 
        infix into postfix expression. 
"""

import re
import csv
from .constants import (
    OPAR,
    OPRE,
    OPLO,
    PRECEDENCE,
    OPERATORS
)


def dictToCsv(data, filename):
    """Create a CSV file from a list"""
    keys = data[0].keys()
    with open(f'output/{filename}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def flatten(seq):
    """
    Returns a flat array

    :param seq: a list of list sequence
    :returns: a flat array of sequence
    """
    l = []
    t = type(seq)
    if t is not tuple and t is not list:
        return [seq]
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l


def infix_to_postfix(infix):
    '''
    Funcion para crear un posfijo desde un infijo lógico/relacional
    '''
    postfix = []
    opStack = []

    for symbol in infix:
        if symbol not in OPERATORS:
            postfix.append(symbol)
        elif symbol == '(':
            opStack.append(symbol)
        elif symbol == ')':
            symbolTope = opStack.pop()
            while symbolTope != '(':
                postfix.append(symbolTope)
                symbolTope = opStack.pop()
        else:
            while (not opStack == []) and \
                    (PRECEDENCE[opStack[len(opStack)-1]]) >= \
                    PRECEDENCE[symbol]:
                postfix.append(opStack.pop())
            opStack.append(symbol)

    while not opStack == []:
        postfix.append(opStack.pop())
    return postfix


if __name__ == '__main__':
    # infix_to_postfix(['a', '<', 'b', '&&', 'a', '==', 0])
    infix_to_postfix(['x', '*', 6, '==', 'y', '+', 7])
