from lexerPMScript import lexer, LexerPMScript
import ast
import ply.yacc as yacc
import sys

# Will check if a variable name is already defined
def checkIfVariableAlreadyExists(varName):
    if varName in parser.vars["const"]:
        return "const"
    elif varName in parser.vars["let"]:
        return "let"
    return None

def printError(text):
    RED = "\033[31m"  # ANSI escape code for red
    RESET = "\033[0m"  # Reset to default color
    print(f"{RED}{text}{RESET}")


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
def p_MutationType(p):
    """MutationType : CONST
                    | LET"""
    p[0] = p[1]

def p_IntDeclaration(p):
    """IntDeclaration : MutationType ID COLON INT EQUALS INTVALUE SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]][p[2]] = int(p[6]) 
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi 0\n" 
    
def p_StringDeclaration(p):
    """StringDeclaration : MutationType ID COLON STR EQUALS STRINGVALUE SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]][p[2]] = "".join(p[6].strip('"')) # Save string without quotes
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi 0\n" 
    
    
def p_FloatDeclaration(p):
    """FloatDeclaration : MutationType ID COLON FLOAT EQUALS FLOATVALUE SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]][p[2]] = float(p[6])
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
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
parser.vars = {
    "const": {},
    "let": {},
}


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