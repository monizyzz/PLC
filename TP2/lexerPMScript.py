import ply.lex as lex
import sys

class LexerPMScript(object):
    def __init__(self, debug = 0, optimize = 0, reflags = 0):
        self.lexer = lex.lex(module=self, debug=debug, optimize=optimize, reflags=reflags)
    
    tokens = [
        'INTVALUE',
        'FLOATVALUE',
        'STRINGVALUE',
        'ID',
        'COLON',
        'EQUALS',
        'SEMICOLON',
    ]
    
    RESERVED = {
        'INT': 'INT',
        'FLOAT': 'FLOAT',
        'STR': 'STR',
        'const': 'CONST',
        'let': 'LET',
    }
    
    tokens += list(RESERVED.values())
    
    t_INT = r'INT'
    t_STR = r'STR'
    t_FLOAT = r'FLOAT'
    
    t_INTVALUE = r'\d+'
    t_FLOATVALUE = r'\d+\.\d+'
    t_STRINGVALUE = r'\".*\"'

    t_COLON = r'\:'
    t_EQUALS = r'\='
    t_SEMICOLON = r'\;'
    
    def t_CONST(self, t):
        r'const(?=\s)'
        return t

    def t_LET(self, t):
        r'let(?=\s)'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.RESERVED.get(t.value, 'ID')
        return t
    
    t_ignore = ' \t\n'
    
    t_error = lambda self, t: print(f"Illegal character {t.value[0]} at line {t.lineno}")
        
    def input(self, s):
        self.lexer.input(s)

content = ""

with open(f"tests/{sys.argv[1]}.pms") as f:
    content = f.read()

lexer = LexerPMScript()
lexer.input(content)
token = lexer.lexer.token()

while token is not None:
    print(f"({token.type} {repr(token.value)} {token.lineno})")
    token = lexer.lexer.token()