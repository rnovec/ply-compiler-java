
"""
Author: Raul Novelo
        raul.novelo@aaaimx.org

        Intermdiate code classes and 3-Address Code table generation
"""

from .constants import *
from .helpers import *


class TR(object):
    """
    Conditional reference for jumps (JR)
    """

    def __init__(self, obj, size, start, body):
        self.obj = obj
        self.jmpTrue = start + size
        self.jmpFalse = start + size + body + 1


class IntermediateCode(object):
    """
    3-Address Code class representation
    """

    def aritmetic(self, postfix, var=None):
        """
        Intermediate code for an aritmetic expression

        :list postfix: a postfix array expression
        :str var: a name to be asigned for default None
        :returns: a lsit of dicts that contains 3-Address Code
        """
        # reverse the list to use as stack
        string = list(reversed(postfix))
        aux = list()  # auxiliar stack
        taddc = list()  # Three Addres Code (EDD)
        tmpCont = 0  # temporals counter
        lastPrecedence = None
        el = string.pop()  # get the first operand
        while el is not None:
            # Recorrer la expresión hasta encontrar el primer operador
            if el in OPAR:
                # Asignar a una variable auxiliar, el operador y los operandos previos
                # Asignar a una segunda variable auxiliar, el operador y los 2 operandos previos.
                op2 = aux.pop()
                op1 = aux.pop()

                # En la primera iteración
                if not lastPrecedence == PRECEDENCE[el] or lastPrecedence is None:
                    tmpCont += 1
                    # Se agrega un renglón en la triplo : variable temporal, primer operando y la operación (=)
                    taddc.append({
                        'obj': f'T{tmpCont}',
                        'fuente': op1,
                        'op': '='
                    })
                    lastPrecedence = PRECEDENCE[el]

                # Se agregar otro renglón en la triplo : variable temporal, segundo operando y operador
                # A partir de la segunda iteración:
                # Se agrega un renglón en la triplo : variable temporal, operando y operador
                taddc.append({
                    'obj': f'T{tmpCont}',
                    'fuente': op2,
                    'op': el
                })
                # Se sustituye el operador y los 2 operandos de la variable auxiliar por la variable temporal.
                aux.append(f'T{tmpCont}')
            else:
                # agregar operando a la pila
                aux.append(el)

            # Se verifica el fin de cadena original
            if len(string) == 0:
                break
            # Se regresa al paso 2
            # se lee el siguiente operando
            el = string.pop()

        # Se asigna la cadena auxiliar a la cadena original
        string = aux
        tmp = string.pop()

        # si es una asignación simple
        if not lastPrecedence:
            taddc.append({
                'obj': 'T1',
                'fuente': tmp,
                'op': '='
            })
            tmp = 'T1'
        # final step, asign last temporal to variable
        taddc.append({
            'obj': var,
            'fuente': tmp,
            'op': '='
        })
        return taddc

    def iterative(self, postfix, start=0, body=0):
        """
        Intermediate Code for `while` instruction
        """
        # reverse the list to use as stack
        string = list(reversed(postfix))
        aux = list()  # auxiliar stack
        taddc = list()  # Three Addres Code (EDD)
        tmpCont = 1  # temporals counter
        trCont = trSize = 0  # TR counter
        lastPrecedence = lastOpLo = None
        lastTr = None
        el = string.pop()  # get the first operand
        while el is not None:
            if el in OPAR:
                op2 = aux.pop()
                op1 = aux.pop()
                tmpCont += 1
                taddc.append({
                    'obj': f'T{tmpCont}',
                    'fuente': op1,
                    'op': '='
                })
                trSize += 1
                taddc.append({
                    'obj': f'T{tmpCont}',
                    'fuente': op2,
                    'op': el
                })
                trSize += 1
                aux.append(f'T{tmpCont}')

            elif el in OPRE:
                op2 = aux.pop()
                op1 = aux.pop()
                taddc.append({
                    'obj': f'T{tmpCont}',
                    'fuente': op1,
                    'op': '='
                })
                trSize += 1
                taddc.append({
                    'obj': f'T{tmpCont}',
                    'fuente': op2,
                    'op': el
                })
                trSize += 3
                trCont += 1
                obj = f'TR{trCont}'
                if not lastTr:
                    lastTr = TR(obj, trSize, start, body)
                    taddc.append(lastTr)
                else:
                    trN = TR(obj, trSize, start, body)
                    lastTr.jmpFalse = trN.jmpFalse
                    taddc.append(trN)
                    lastTr = trN
                aux.append(obj)
                lastPrecedence = None
            elif el in OPLO:
                band = False
                for i in range(len(taddc)):
                    if type(taddc[i]) is not dict:
                        if not band and el == '||':
                            taddc[i].jmpFalse = taddc[i].jmpTrue
                            taddc[i].jmpTrue = lastTr.jmpTrue
                            band = True
                        taddc[i] = [{
                            'obj': taddc[i].obj,
                            'fuente': 'TRUE',
                            'op': taddc[i].jmpTrue
                        }, {
                            'obj': taddc[i].obj,
                            'fuente': 'FALSE',
                            'op': taddc[i].jmpFalse
                        }]
                lastOpLo = el

            else:
                aux.append(el)
            if len(string) == 0:
                break
            el = string.pop()
        if not lastOpLo:
            band = False
            for i in range(len(taddc)):
                if type(taddc[i]) is not dict:
                    taddc[i] = [{
                        'obj': taddc[i].obj,
                        'fuente': 'TRUE',
                        'op': taddc[i].jmpTrue
                    }, {
                        'obj': taddc[i].obj,
                        'fuente': 'FALSE',
                        'op': taddc[i].jmpFalse
                    }]
        return taddc


if __name__ == "__main__":
    while_case = ['a', 2, '%', 0, '==', 'a', 20, '<', '||']
    data = IntermediateCode.iterative(
        while_case, isWhile=True, start=3, body=6)
    print(data)
