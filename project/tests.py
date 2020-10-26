from intermediate_code.helpers import infix_to_postfix, three_add_code
from django.test import TestCase


class CompilerTestCase(TestCase):

    def setUp(self):
        self.case1 = ['a', '+', 'b', '*', 'c', '+', 'd']
        self.case2 = ['(', 'A', '+', 'B', ')', '*', '(', 'C', '+', 'D', ')']
        self.case3 = ['(', 'a', '+', 'b', ')', '*', 'c']
        self.case4 = [2, '+', 1, '+', 2, '/', 3, '*', 3]
        self.res1 = ['a', 'b', 'c', '*', '+', 'd', '+']
        self.res2 = ['A', 'B', '+', 'C', 'D', '+', '*']
        self.res3 = ['a', 'b', '+', 'c', '*']
        self.res4 = [2, 1, '+', 2, 3, '/', 3, '*', '+']

    def test_three_address_code(self):
        """Test cases for infix to postfix array"""
        self.case1 = infix_to_postfix(self.case1)
        self.case2 = infix_to_postfix(self.case2)
        self.case3 = infix_to_postfix(self.case3)
        self.case4 = infix_to_postfix(self.case4)
        self.assertEqual(self.case1, self.res1)
        self.assertEqual(self.case2, self.res2)
        self.assertEqual(self.case3, self.res3)
        self.assertEqual(self.case4, self.res4)
        self.assertEqual(infix_to_postfix(
            ['2', '+', '1', '-', '3', '*', '4', '/', '1']), ['2', '1', '+', '3', '4', '*', '1', '/', '-'])
        self.assertEqual(infix_to_postfix(
            [4, '*', 2, '+', 5, '/', 7, '*', 2, '+', 10]), [4, 2, '*', 5, 7, '/', 2, '*', '+', 10, '+'])
        self.assertEqual(infix_to_postfix(
            ['num1', '*', 'num2', '+', 'num3', '/', 'numero4', '*', 'soynumero5', '+', 'SoyNumero6']), ['num1', 'num2', '*', 'num3', 'numero4', '/', 'soynumero5', '*', '+', 'SoyNumero6', '+'])
        self.assertEqual(infix_to_postfix(
            [123445, '+', 10231, '/', 12312, '/', 123124, '*', 42123, '-', 12312351, '-', 123515123]), [123445, 10231, 12312, '/', 123124, '/', 42123, '*', '+', 12312351, '-', 123515123, '-'])
        self.assertEqual(len(three_add_code('w', '=', self.case1)), 5)
        self.assertEqual(len(three_add_code('x', '=', self.case2)), 5)
        self.assertEqual(len(three_add_code('y', '=', self.case3)), 4)
        self.assertEqual(len(three_add_code('z', '=', self.case4)), 6)
