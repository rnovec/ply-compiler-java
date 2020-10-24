from intermediate_code.helpers import infix_to_postfix
from django.test import TestCase

class CompilerTestCase(TestCase):

    def test_convert_infix_postfix(self):
        """Test cases for infix to postfix array"""
        self.assertEqual(infix_to_postfix(
            ['a', '+', 'b', '*', 'c', '+', 'd']), ['a', 'b', 'c', '*', '+', 'd', '+'])
        self.assertEqual(infix_to_postfix(
            ['3', '+', '2', '+', '1', '/', '3', '*', '3']), ['3', '2', '1', '3', '/', '3', '*', '+', '+'])
