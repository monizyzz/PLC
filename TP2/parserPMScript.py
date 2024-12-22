from lexerPMScript import lexer, LexerPMScript
import ast
import ply.yacc as yacc
import sys



# ---------------- Programa ----------------
def p_ProgramInit(p):
    "ProgramInit : Declarations"
    parser.assembly = p[1] + "start\nstop\n"
        
# ---------------- Declaration ----------------
def p_Declarations(p):
    """Declarations : IntDeclaration Declarations
                    | StringDeclaration Declarations
                    | FloatDeclaration Declarations
                    | Empty"""
    if len(p) == 3:
        p[0] = str(p[1]) + str(p[2])
    else:
        p[0] = ""
    
# ---------------- VarDeclaration ----------------
def p_IntDeclaration(p):
    """IntDeclaration : ID COLON INT EQUALS INTVALUE SEMICOLON"""
    parser.vars[p[1]] = int(p[5])
    p[0] = f"pushi 0\n" 
    
def p_StringDeclaration(p):
    """StringDeclaration : ID COLON STR EQUALS STRINGVALUE SEMICOLON"""
    parser.vars[p[1]] = "".join(p[5].strip('"'))
    p[0] = f"pushi 0\n" 
    
    
def p_FloatDeclaration(p):
    """FloatDeclaration : ID COLON FLOAT EQUALS FLOATVALUE SEMICOLON"""
    parser.vars[p[1]] = float(p[5])
    p[0] = f"pushi 0\n"

# ---------------  Empty  ---------------- #
def p_Empty(p):
    "Empty : "
    pass

def p_error(p):
    print(f"Syntax error at line {p.lineno}")
    parser.success = False


tokens = LexerPMScript.tokens
lexer = LexerPMScript()

# Create the parser
parser = yacc.yacc(start='ProgramInit')
parser.success = True
parser.assembly = ""
parser.vars = {}


# Read file
content = ""
with open(f"tests/{sys.argv[1]}.pms") as f:
    content = f.read()



lexer.input(content)
parser.parse(content, lexer=lexer.lexer)

if parser.success:
    print("Ficheiro lido com sucesso")
    with open(f'tests/{sys.argv[1]}.vm', 'w+') as f_out:
        f_out.write(parser.assembly)
        f_out.close()
    print("Código assembly gerado e guardado.")
    print(f"Variáveis: {parser.vars}")
else:
    print("Erro ao gerar o código.")