from lexerPMScript import lexer, LexerPMScript
import ast
import ply.yacc as yacc
import sys

# ------------------------------------------------------------- Auxiliar Functions

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Will check if a variable name is already defined
# TODO: Make this function more efficient
def checkIfVariableAlreadyExists(varName):
    if varName in parser.vars["const"]["INT"]:
        return "const"
    elif varName in parser.vars["const"]["STR"]:
        return "const"
    elif varName in parser.vars["const"]["FLOAT"]:
        return "const"
    elif varName in parser.vars["let"]["INT"]:
        return "let"
    elif varName in parser.vars["let"]["STR"]:
        return "let"
    elif varName in parser.vars["let"]["FLOAT"]:
        return "let"
    else:
        return None
    
def getVariableType(varName):
    if varName in parser.vars["const"]["INT"]:
        return "INT"
    elif varName in parser.vars["const"]["STR"]:
        return "STR"
    elif varName in parser.vars["const"]["FLOAT"]:
        return "FLOAT"
    elif varName in parser.vars["let"]["INT"]:
        return "INT"
    elif varName in parser.vars["let"]["STR"]:
        return "STR"
    elif varName in parser.vars["let"]["FLOAT"]:
        return "FLOAT"
    else:
        return None

# Used for logging errors in red
def printError(text):
    RED = "\033[31m"  # ANSI escape code for red
    RESET = "\033[0m"  # Reset to default color
    print(f"{RED}{text}{RESET}")

def printSuccess(text):
    GREEN = "\033[32m"  # ANSI escape code for green
    RESET = "\033[0m"  # Reset to default color
    print(f"{GREEN}{text}{RESET}")


# ---------------- Programa ----------------
def p_ProgramInit(p):
    """ProgramInit : Declarations Attributions"""
    parser.assembly = p[1] + "start\nstop\n"


def p_Declarations(p):
    """Declarations : IntDeclaration Declarations
                    | StringDeclaration Declarations
                    | FloatDeclaration Declarations
                    | ArrayDeclaration Declarations
                    | Empty"""
    if len(p) == 3:
        p[0] = str(p[1]) + str(p[2])
    else:
        p[0] = ""
    
# ------------------------------------------------------------  Int Declaration

def p_IntDeclaration(p):
    """IntDeclaration : MutationType ID ':' INT '=' INTVALUE ';'"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['INT'][p[2]] = int(p[6]) 
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi 0\n" 

# ------------------------------------------------------------  String Declaration
    
def p_StringDeclaration(p):
    """StringDeclaration : MutationType ID ':' STR '=' STRINGVALUE ';'"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['STR'][p[2]] = "".join(p[6].strip('"')) # Save string without quotes
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi 0\n" 
  
# ------------------------------------------------------------  Float Declaration  
    
def p_FloatDeclaration(p):
    """FloatDeclaration : MutationType ID ':' FLOAT '=' FLOATVALUE ';'"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['FLOAT'][p[2]] = float(p[6])
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi 0\n"
    
    
# ------------------------------------------------------------  Array Declaration

def p_ArrayDeclaration(p):
    """ArrayDeclaration : MutationType ID ':' ARRAY '<' INT '>' '=' '[' ArrayIntDeclaration ']' ';'
                        | MutationType ID ':' ARRAY '<' FLOAT '>' '=' '[' ArrayFloatDeclaration ']' ';'
                        | MutationType ID ':' ARRAY '<' STR '>' '=' '[' ArrayStringDeclaration ']' ';'"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]][p[6]][p[2]] = p[10]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi 0\n"
    
def p_ArrayIntDeclarationAux(p):
    """ArrayIntDeclaration : INTVALUE ',' ArrayIntDeclaration
                           | INTVALUE
                           | Empty"""
    if len(p) == 4:
        p[0] = [int(p[1])] + p[3]
    else:
        p[0] = [int(p[1])]
        
def p_ArrayFloatDeclarationAux(p):
    """ArrayFloatDeclaration : FLOATVALUE ',' ArrayFloatDeclaration
                             | FLOATVALUE
                             | Empty"""
    if len(p) == 4:
        p[0] = [float(p[1])] + p[3]
    else:
        p[0] = [float(p[1])]

def p_ArrayStringDeclarationAux(p):
    """ArrayStringDeclaration : STRINGVALUE ',' ArrayStringDeclaration
                              | STRINGVALUE
                              | Empty"""
    if len(p) == 4:
        p[0] = [p[1].strip('"')] + p[3]
    else:
        p[0] = [p[1].strip('"')]

# ------------------------------------------------------------  Attributions

def p_Atributions(p):
    """Attributions : NormalAttribution Attributions
                   | Empty"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""
    
def p_NormalAttribution(p):
    """NormalAttribution : ID '=' INTVALUE ';'
                        | ID '=' STRINGVALUE ';'
                        | ID '=' FLOATVALUE ';'"""
    mutationType = checkIfVariableAlreadyExists(p[1])
    varType = getVariableType(p[1])
    
    # Check if variable was defined before
    if mutationType is not None:
        
        # Check if variable is a constant, if so, it cannot be changed and an error is raised
        if mutationType == "const":
            parser.success = False
            printError("Error: Cannot change value of a constant variable")
        else:
            
            # Check if variable types match (int, str, float)
            # TODO: Do this for arrays
            # TODO: Do vm code for ints and floats
            if varType == "INT" and is_float(p[3]):
                parser.vars["let"][varType][p[1]] = int(float(p[3])) # Round float to int if necessary

            elif varType == "STR" and p[3].startswith('"') and p[3].endswith('"'):
                parser.vars["let"][varType][p[1]] = p[3].strip('"')

            elif varType == "FLOAT" and is_float(p[3]):
                parser.vars["let"][varType][p[1]] = p[3]
                
            else:
                parser.success = False
                printError("Atribution Error: Variable types do not match.")

            printSuccess(f"Atrib -> {p[1]} = {p[3]}")
            p[0] = f"pop {p[1]}\n"

    # If variable was not defined before, raise an error
    else:
        parser.success = False
        printError("Error: Variable was not defined before")

# ------------------------------------------------------------  Empty 

def p_Empty(p):
    "Empty : "
    pass

# ------------------------------------------------------------  MutationType 

def p_MutationType(p):
    """MutationType : CONST
                    | LET"""
    p[0] = p[1]

# ------------------------------------------------------------  Error

def p_error(p):
    print(f"Syntax error at line {parser.lineno}")
    parser.success = False


tokens = LexerPMScript.tokens
lexer = LexerPMScript()

# Create the parser
parser = yacc.yacc(start='ProgramInit')
parser.lineno = 1
parser.success = True
parser.assembly = ""
parser.vars = {
    "const": {
        "INT": {},
        "STR": {},
        "FLOAT": {},
        },
    "let": {
        "INT": {},
        "STR": {},
        "FLOAT": {},
    },
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