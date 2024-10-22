from django.test import TestCase
from compiler.lexer import JavaLexer
from compiler.parser import JavaParser
from compiler.helpers import infix_to_postfix
from compiler.three_add_code import *

class CompilerTestCase(TestCase):

    def setUp(self):
        self.cases = [[2],  [2, '+', 1], ['a', '+', 'b', '*', 'c', '+', 'd'],
                      ['(', 'A', '+', 'B', ')', '*', '(', 'C', '+', 'D', ')'],
                      ['(', 'a', '+', 'b', ')', '*', 'c'], [2, '+', 1, '+', 2, '/', 3, '*', 3]]
        self.responses = [[2], [2, 1, '+'], ['a', 'b', 'c', '*', '+', 'd', '+'],
                          ['A', 'B', '+', 'C', 'D', '+',
                              '*'], ['a', 'b', '+', 'c', '*'],
                          [2, 1, '+', 2, 3, '/', 3, '*', '+']]

    def test_three_address_code(self):
        """Test cases for infix to postfix array"""
        i = 0
        for case in self.cases:
            case = infix_to_postfix(case)
            self.assertEqual(case, self.responses[i])
            i += 1
        self.assertEqual(infix_to_postfix(
            ['2', '+', '1', '-', '3', '*', '4', '/', '1']), ['2', '1', '+', '3', '4', '*', '1', '/', '-'])
        self.assertEqual(infix_to_postfix(
            [4, '*', 2, '+', 5, '/', 7, '*', 2, '+', 10]), [4, 2, '*', 5, 7, '/', 2, '*', '+', 10, '+'])
        self.assertEqual(infix_to_postfix(
            ['num1', '*', 'num2', '+', 'num3', '/', 'numero4', '*', 'soynumero5', '+', 'SoyNumero6']), ['num1', 'num2', '*', 'num3', 'numero4', '/', 'soynumero5', '*', '+', 'SoyNumero6', '+'])
        self.assertEqual(infix_to_postfix(
            [123445, '+', 10231, '/', 12312, '/', 123124, '*', 42123, '-', 12312351, '-', 123515123]), [123445, 10231, 12312, '/', 123124, '/', 42123, '*', '+', 12312351, '-', 123515123, '-'])
        taddc = IntermediateCode()
        self.assertEqual(len(taddc.aritmetic(self.responses[0], 'w')), 2)
        self.assertEqual(len(taddc.aritmetic(self.responses[1], 'w')), 3)
        self.assertEqual(len(taddc.aritmetic(self.responses[2], 'w')), 6)
        self.assertEqual(len(taddc.aritmetic(self.responses[3], 'x')), 6)
        self.assertEqual(len(taddc.aritmetic(self.responses[4], 'y')), 5)
        self.assertEqual(len(taddc.aritmetic(self.responses[5], 'z')), 8)

    def test_for_iterators(self):
        self.assertEqual(infix_to_postfix(['a', '<', 'b', '&&', 'a', '==', 0]),
                         ['a', 'b', '<',  'a', 0, '==', '&&'])
        self.assertEqual(infix_to_postfix(['a', '%', 2, '==', 0, '&&', 'a', '<', 20]),
                         ['a', 2, '%', 0, '==', 'a', 20, '<', '&&'])
        self.assertEqual(infix_to_postfix(
            ['x', '*', 6, '==', 'y', '+', 7]), ['x', 6, '*', 'y',  7, '+', '==',])

    def test_compiler_parser(self):
        """Test for JavaParser and JavaLexer"""
        JL, JP = JavaLexer(), JavaParser()
        JL.from_file('examples/ejemplo4.java')
        JP.compile_from_file('examples/ejemplo4.java')
