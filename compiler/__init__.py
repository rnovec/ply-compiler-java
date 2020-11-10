"""
Author: Raul Novelo
        raul.novelo@aaaimx.org

** JavaCompiler **

This program was developed as a part of compiler-design course.
It is a translator high level expressions like Java Lenguage to 3-Address intermediate code
using principles of compiler design(lexer, parser, code generator, optimizer etc)

The language in consideration consists of aritmetic expression of simple
form such as
x = 7 + 9/2
y = (x + x) + 5
...

each line contains one expression with clealy defined high leve code (Aritmetic, Functions and Iterators).
each expression must be a variable and can be: number, function, expression


With this language description in mind, this program implements following
- Lexer (`lexer.py`)
- Parser (`parser.py)`
- Intermediate Code Generator (`three_add_code.py`)
- TODO: Intermediate Code Optimizer
"""