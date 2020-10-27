from intermediate_code.helpers import infix_to_postfix, three_add_code
from django.test import TestCase

class CompilerTestCase(TestCase):

    def setUp(self):
        self.cases = [[2],  [2, '+', 1], ['a', '+', 'b', '*', 'c', '+', 'd'],
                      ['(', 'A', '+', 'B', ')', '*', '(', 'C', '+', 'D', ')'],
                      ['(', 'a', '+', 'b', ')', '*', 'c'], [2, '+', 1, '+', 2, '/', 3, '*', 3]]
        self.responses = [[2], [2, 1, '+'], ['a', 'b', 'c', '*', '+', 'd', '+'],
                          ['A', 'B', '+', 'C', 'D', '+', '*'], ['a', 'b', '+', 'c', '*'],
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
        # self.assertEqual(len(three_add_code('w', '=', self.responses[0])), 7)
        self.assertEqual(len(three_add_code('w', '=', self.responses[1])), 3)
        self.assertEqual(len(three_add_code('w', '=', self.responses[2])), 7)
        self.assertEqual(len(three_add_code('x', '=', self.responses[3])), 6)
        self.assertEqual(len(three_add_code('y', '=', self.responses[4])), 5)
        self.assertEqual(len(three_add_code('z', '=', self.responses[5])), 8)
