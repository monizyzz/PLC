from lexerPMScript import lexer, LexerPMScript
import ast
import ply.yacc as yacc
import sys
import tabulate

# ------------------------------------------------------------- Auxiliar Functions

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Will check if a variable name is already defined (const, let or None)
def checkIfVariableAlreadyExists(varName):
    mutationTypes = ["const", "let"]
    for mutationType in mutationTypes:
        for varType in parser.vars[mutationType]:
            if varName in parser.vars[mutationType][varType]:
                return mutationType    
    return None

# Will return the type of a variable (INT, STR, FLOAT)
def getVariableType(varName):
    for mutationType in parser.vars:
        for varType in parser.vars[mutationType]:
            if varName in parser.vars[mutationType][varType]:
                return varType
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
    
def printVariables():
    for varType in parser.vars:
        for var in parser.vars[varType]:
            print(f"{varType} {var}: {parser.vars[varType][var]}")

# ---------------- Programa ----------------
def p_ProgramInit(p):
    """ProgramInit : Declarations Attributions
                   | Attributions
                   | Declarations"""
    parser.assembly = p[1] + f"start\n{p[2]}stop\n"


def p_Declarations(p):
    """Declarations : IntDeclaration Declarations
                    | IntDeclarationInput Declarations
                    | StringDeclaration Declarations
                    | FloatDeclaration Declarations
                    | ArrayDeclaration Declarations
                    | Empty"""
    if len(p) == 3:
        p[0] = str(p[1]) + str(p[2])
    else:
        p[0] = ""
    parser.lineno += 1
    
# ------------------------------------------------------------  Int Declaration

def p_IntDeclaration(p):
    """IntDeclaration : MutationType ID ':' INT '=' INTVALUE SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['INT'][p[2]] = int(p[6]) 
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi {int(p[6])}\n" 
    
def p_IntDeclarationInput(p):
    "IntDeclarationInput : MutationType ID ':' INT '=' Input SEMICOLON"
    value = int(input(f"{p[6].strip('\"')}"))

    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['INT'][p[2]] = value
    else:
        parser.success = False
        printError("Error: Variable was already defined before")

    p[0] = f'{p[6]} READ\nATOI\nSTOREG {p[2]}\n'

# ------------------------------------------------------------  String Declaration
    
def p_StringDeclaration(p):
    """StringDeclaration : MutationType ID ':' STR '=' STRINGVALUE SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['STR'][p[2]] = "".join(p[6].strip('"')) # Save string without quotes
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushs {"".join(p[6].strip('"'))}\n" 
  
# ------------------------------------------------------------  Float Declaration  
    
def p_FloatDeclaration(p):
    """FloatDeclaration : MutationType ID ':' FLOAT '=' FLOATVALUE SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['FLOAT'][p[2]] = float(p[6])
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushf {float(p[6])}\n"
    
    
# ------------------------------------------------------------  Array Declaration

def p_ArrayDeclaration(p):
    """ArrayDeclaration : MutationType ID ':' ARRAY '<' INT '>' '=' '[' ArrayIntDeclaration ']' SEMICOLON
                        | MutationType ID ':' ARRAY '<' FLOAT '>' '=' '[' ArrayFloatDeclaration ']' SEMICOLON
                        | MutationType ID ':' ARRAY '<' STR '>' '=' '[' ArrayStringDeclaration ']' SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]][p[6]][p[2]] = p[10]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = ""
    
    for i in range(len(p[10])):
        p[0] += f"push{'i' if p[6] == 'INT' else 'f' if p[6] == 'FLOAT' else 's'} {p[10][i]}\n"
        p[0] += f"STOREG {p[2]}_{i}\n"
    
def p_ArrayIntDeclarationAux(p):
    """ArrayIntDeclaration : ArrayIntDeclaration ',' INTVALUE
                           | INTVALUE
                           | Empty"""
    if len(p) == 4:
        p[0] = [int(float(p[3]))] + p[1] 
    else:
        p[0] = [int(float(p[1]))]
        
def p_ArrayFloatDeclarationAux(p):
    """ArrayFloatDeclaration : ArrayFloatDeclaration ',' FLOATVALUE
                             | FLOATVALUE
                             | Empty"""
    if len(p) == 4:
        p[0] = [float(p[3])] + p[1]
    else:
        p[0] = [float(p[1])]
        
def p_ArrayStringDeclarationAux(p):
    """ArrayStringDeclaration : ArrayStringDeclaration ',' STRINGVALUE 
                              | STRINGVALUE
                              | Empty"""
    if len(p) == 4:
        p[0] = p[1] + [p[3].strip('"')]
    else:
        p[0] = [p[1].strip('"')]

# ------------------------------------------------------------  Attributions

def p_Atributions(p):
    """Attributions : Attributions NormalAttribution
                    | Attributions IncDecAttribution
                    | Empty"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""
    
def p_NormalAttribution(p):
    """NormalAttribution : ID '=' INTVALUE SEMICOLON
                         | ID '=' STRINGVALUE SEMICOLON
                         | ID '=' FLOATVALUE SEMICOLON"""
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
            p[0] = f"push{'i' if varType == 'INT' else 'f' if varType == 'FLOAT' else 's'} {p[3]}\nSTOREG {p[1]}\n"

    # If variable was not defined before, raise an error
    else:
        parser.success = False
        printError("Error: Variable was not defined before")
        
def p_IncDecAttribution(p):
    """IncDecAttribution : ID DEC SEMICOLON
                         | ID INC SEMICOLON"""
    mutationType = checkIfVariableAlreadyExists(p[1])
    varType = getVariableType(p[1])
    op = "ADD" if p[2] == "++" else "SUB"
    
    # Check if variable was defined before
    if mutationType is not None:
        
        # Check if variable is a constant, if so, it cannot be changed and an error is raised
        if mutationType == "const":
            parser.success = False
            printError("Error: Cannot change value of a constant variable")
        else:
            
            # Check if variable types match (int, str, float)
            if varType == "INT" or varType == "FLOAT":
                if p[2] == "++":
                    parser.vars["let"][varType][p[1]] += 1
                else:
                    parser.vars["let"][varType][p[1]] -= 1       
                
                printSuccess(f"IncDec -> {p[1]}{p[2]}")
            else:
                parser.success = False
                printError("Skill Issue: Do you really want to increment or decrement a string?")
                p[0] = "error"
                return

            p[0] = f'PUSHG {parser.vars[mutationType][varType][p[1]]}\nPUSHI 1\n{op}\nSTOREG {p[1]}\n'

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
    
# ------------------------------------------------------------  Input

def p_Input(p):
    """Input : INPUT '(' STRINGVALUE ')'"""
    p[0] = f'{p[3]}'

# ------------------------------------------------------------  Error

def p_error(p):
    printError(f"Syntax error at line {parser.lineno}")
    printError(f"Error: Unexpected token {p.value}")
    printError(f"Error: Unexpected token {p.type}")
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
    printVariables()
else:
    print("Erro ao gerar o código.")