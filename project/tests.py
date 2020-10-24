from intermediate_code.helpers import infix_to_postfix
from django.test import TestCase

class CompilerTestCase(TestCase):

    def test_convert_infix_postfix(self):
        """Test cases for infix to postfix array"""
        self.assertEqual(infix_to_postfix(
            ['a', '+', 'b', '*', 'c', '+', 'd']), ['a', 'b', 'c', '*', '+', 'd', '+'])
        self.assertEqual(infix_to_postfix(
            ['(', 'A', '+', 'B', ')', '*', '(', 'C', '+', 'D', ')']), ['A', 'B', '+', 'C', 'D', '+', '*'])
        self.assertEqual(infix_to_postfix(
            ['(', 'a', '+', 'b', ')', '*', 'c']), ['a', 'b', '+', 'c', '*'])
        self.assertEqual(infix_to_postfix(
            [2, '+', 1, '+', 2, '/', 3, '*', 3]), ['2', '1', '+', '2', '3', '/', '3', '*', '+'])
        self.assertEqual(infix_to_postfix(
            ['2','+','1','-','3','*','4','/','1']), ['2', '1', '+', '3', '4', '*', '1', '/', '-'])
        self.assertEqual(infix_to_postfix(
            [4, '*', 2, '+', 5, '/', 7, '*', 2, '+', 10]), ['4', '2', '*', '5', '7', '/', '2', '*', '+', '10', '+'])
        self.assertEqual(infix_to_postfix(
            ['num1', '*', 'num2', '+', 'num3', '/', 'numero4', '*', 'soynumero5', '+', 'SoyNumero6']), ['num1', 'num2', '*', 'num3', 'numero4', '/', 'soynumero5', '*', '+', 'SoyNumero6', '+'])
        self.assertEqual(infix_to_postfix(
            ['123445', '+','10231', '/', '12312', '/', '123124', '*', '42123', '-', '12312351', '-', '123515123']), ['123445', '10231', '12312', '/', '123124', '/', '42123', '*', '+', '12312351', '-', '123515123', '-'])



