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
            for varName in parser.vars[varType][var]:
                print(f"Registro ({parser.vars[varType][var][varName][1]}) {varType} {varName}: {parser.vars[varType][var][varName][0]}")

# ------------------------------------------------------------  Grammar

def p_ProgramInit(p):
    "ProgramInit : Declarations Instructions"
    parser.assembly = p[1] + f"start\n{p[2]}stop\n"
    
def p_ProgramInit_NOINST(p):
    "ProgramInit : Declarations"
    parser.assembly = f"{p[1]}start\nstop\n"
    # printError("Error: No instructions were given")
    
def p_ProgramInit_NODECL(p):
    "ProgramInit : Instructions"
    parser.assembly = f"start\n{p[1]}stop\n"
    # printError("Error: No declarations were given")

def p_Declarations(p):
    """Declarations : Declarations IntDeclaration
                    | Declarations IntDeclarationInput
                    | Declarations StringDeclaration
                    | Declarations StringDeclarationInput
                    | Declarations FloatDeclaration
                    | Declarations FloatDeclarationInput
                    | Declarations ArrayDeclaration
                    | Declarations FunctionDeclaration
                    | Empty"""
    if len(p) == 3:
        p[0] = str(p[1]) + str(p[2])
    else:
        p[0] = ""
    parser.lineno += 1
    
# -----------------------------------------------------------  Function Declaration

def p_FunctionDeclaration(p):
    "FunctionDeclaration : CONST ID '=' '(' ')' '=' '>' '{' Instructions '}'"
    name = f'function{len(p.parser.functions)}'
    p.parser.functions[p[2]+"()"] = name
    body = p[9]
    p[0] = f'{name}:\n{body}\n'
    
def p_Call(p):
    "Call : CALL SEMICOLON"
    p[0] = f'PUSHA {p.parser.functions[p[1]]}\nCALL\n'
    
def p_CallWithReturn(p):
    "Call : RETURN CALL SEMICOLON"
    p[0] = f'PUSHA {p.parser.functions[p[2]]}\nCALL\n'
    
def p_Return(p):
    "Return : RETURN SEMICOLON"
    p[0] = "RETURN\n"
    
def p_ReturnValue(p):
    "Return : RETURN Expr SEMICOLON"
    p[0] = f'{p[2]}RETURN\n'

def p_ReturnValueCall(p):
    "Return : RETURN Call"
    p[0] = f'{p[2]}RETURN\n'
    
# ------------------------------------------------------------  Int Declaration

def p_IntDeclaration(p):
    """IntDeclaration : MutationType ID ':' INT '=' INTVALUE SEMICOLON"""
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['INT'][p[2]] = [int(p[6]), parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi {int(p[6])}\n" 
    
def p_IntDeclaration_NOVALUE(p):
    """IntDeclaration : MutationType ID ':' INT SEMICOLON"""
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['INT'][p[2]] = [0, parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushi {0}\n"
    
def p_IntDeclarationInput(p):
    "IntDeclarationInput : MutationType ID ':' INT '=' Input SEMICOLON"
    value = int(input(f"READ: ")) # simulate input value
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['INT'][p[2]] = [value, parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")

    p[0] = f'{p[6]}READ\nATOI\nSTOREG {parser.vars[p[1]]["INT"][p[2]][1]}\n'

# ------------------------------------------------------------  String Declaration
    
def p_StringDeclaration(p):
    """StringDeclaration : MutationType ID ':' STR '=' STRINGVALUE SEMICOLON"""
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['STR'][p[2]] = [p[6].strip('"'), parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushs {"".join(p[6].strip('"'))}\n" 
    
def p_StringDeclaration_NOVALUE(p):
    """StringDeclaration : MutationType ID ':' STR SEMICOLON"""
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['STR'][p[2]] = ["", parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushs {""}\n"

def p_StringDeclarationInput(p):
    "StringDeclarationInput : MutationType ID ':' STR '=' Input SEMICOLON"
    value = input(f"READ: ") # simulate input value
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['STR'][p[2]] = [value, parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")

    p[0] = f'{p[6]}READ\nSTOREG {parser.vars[p[1]]["STR"][p[2]][1]}\n'
  
# ------------------------------------------------------------  Float Declaration  
    
def p_FloatDeclaration(p):
    """FloatDeclaration : MutationType ID ':' FLOAT '=' FLOATVALUE SEMICOLON"""
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['FLOAT'][p[2]] = [float(p[6]), parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushf {float(p[6])}\n"
    
def p_FloatDeclaration_NOVALUE(p):
    """FloatDeclaration : MutationType ID ':' FLOAT SEMICOLON"""
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['FLOAT'][p[2]] = [float(0), parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f"pushf {float(0)}\n"
    
def p_FloatDeclarationInput(p):
    "FloatDeclarationInput : MutationType ID ':' FLOAT '=' Input SEMICOLON"
    value = float(input(f"READ: ")) # simulate input value
    parser.regIndex += 1
    if checkIfVariableAlreadyExists(p[2]) is None:
        parser.vars[p[1]]['FLOAT'][p[2]] = [value, parser.regIndex]
    else:
        parser.success = False
        printError("Error: Variable was already defined before")
    p[0] = f'{p[6]}READ\nATOF\nSTOREG {parser.vars[p[1]]["FLOAT"][p[2]][1]}\n'
    
    
# ------------------------------------------------------------  Array Declaration

# TODO: Implement array declaration vm code
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

# ------------------------------------------------------------  Instructions
def p_Instructions(p):
    """Instructions : Instructions Instruction
                    | Instruction"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
    printSuccess(f"Instructions -> {p[1]}")
        
def p_Instruction(p):
    """Instruction : Attributions
                   | Output
                   | Call
                   | Return
                   | If
                   | Loop"""
    p[0] = p[1]

# ------------------------------------------------------------  Attributions

def p_Attributions(p):
    """Attributions : Attributions NormalAttribution SEMICOLON
                    | Attributions Expression SEMICOLON
                    | Empty"""
    if len(p) == 4:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""

def p_AttributionsIncDec(p):
    """Attributions : Attributions IncDecAttribution SEMICOLON"""
    p[0] = p[1] + p[2][0] # p[2] is a tuple with the assembly code and the variable name
    
    
def p_NormalAttribution(p):
    """NormalAttribution : ID '=' INTVALUE
                         | ID '=' STRINGVALUE
                         | ID '=' FLOATVALUE"""
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
                parser.vars["let"][varType][p[1]][0] = int(float(p[3])) # Round float to int if necessary

            elif varType == "STR" and p[3].startswith('"') and p[3].endswith('"'):
                parser.vars["let"][varType][p[1]][0] = p[3].strip('"')

            elif varType == "FLOAT" and is_float(p[3]):
                parser.vars["let"][varType][p[1]][0] = p[3]
                
            else:
                parser.success = False
                printError("Atribution Error: Variable types do not match.")

            printSuccess(f"Atrib -> {p[1]} = {p[3]}")
            p[0] = f"push{'i' if varType == 'INT' else 'f' if varType == 'FLOAT' else 's'} {p[3]}\nSTOREG {parser.vars[mutationType][varType][p[1]][1]}\n"

    # If variable was not defined before, raise an error
    else:
        parser.success = False
        printError("Error: Variable was not defined before")
    
        
def p_IncDecAttribution(p):
    """IncDecAttribution : ID DEC
                         | ID INC"""
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
                    parser.vars["let"][varType][p[1]][0] += 1
                else:
                    parser.vars["let"][varType][p[1]][0] -= 1       
                
                printSuccess(f"IncDec -> {p[1]}{p[2]}")
            else:
                parser.success = False
                printError("Skill Issue: Do you really want to increment or decrement a string?")
                p[0] = "error"
                return

            p[0] = (
                f'PUSHG {parser.vars[mutationType][varType][p[1]][1]}\nPUSHI 1\n{op}\nSTOREG {parser.vars[mutationType][varType][p[1]][1]}\n',
                p[1]
            )

    else:
        parser.success = False
        printError("Error: Variable was not defined before")
        p[0] = "error"
        
def p_Expression(p):
    "Expression : ID '=' Expr"        
    mutationType = checkIfVariableAlreadyExists(p[1])
    varType = getVariableType(p[1])
    p[0] = f"{p[3]}STOREG {parser.vars[mutationType][varType][p[1]][1]}\n"
    
# ------------------------------------------------------------  Expr

def p_Expr_Var_Inc(p):
    """Expr : IncDecAttribution"""
    varName = p[1][1]
    p[0] = p[1][0] + f"PUSHG {parser.vars['let'][getVariableType(varName)][varName][1]}\n"
    
def p_Expr_Var(p):
    "Expr : ID"
    mutationType = checkIfVariableAlreadyExists(p[1])
    varType = getVariableType(p[1])
    
    if mutationType is None:
        parser.success = False
        printError("Error: Variable was not defined before")
        p[0] = "error"
        return
    
    p[0] = f"PUSHG {parser.vars[mutationType][varType][p[1]][1]}\n"
    
def p_Expr_Int(p):
    "Expr : INTVALUE"
    p[0] = f"PUSHI {p[1]}\n"
    
def p_Expr_Float(p):
    "Expr : FLOATVALUE"
    p[0] = f"PUSHF {p[1]}\n"
    
arith_map = {
    "+": "ADD\n",
    "-": "SUB\n",
    "*": "MUL\n",
    "/": "DIV\n",
    "%": "MOD\n",
}

def p_Expr_Arith(p):
    """Expr : Expr '+' Expr
            | Expr '-' Expr
            | Expr '*' Expr
            | Expr '/' Expr
            | Expr '%' Expr"""
    p[0] = f'{p[1]}{p[3]}{arith_map[p[2]]}'
    
    
# ------------------------------------------------------------  If Statement

condition_map ={
    ">": "SUP\n",
    "<": "INF\n",
    ">=": "SUPEQ\n",
    "<=": "INFEQ\n",
    "==": "EQUAL\n",
    "!=": "EQUAL\nNOT\n",
    "or": "ADD\n",
    "and": "MUL\n",
}

def p_Cond(p):
    """Cond : Expr '<' Expr
            | Expr '>' Expr
            | Expr GEQUAL Expr
            | Expr LEQUAL Expr
            | Expr EQUAL Expr
            | Expr DIFF Expr
            | Cond OR Cond
            | Cond AND Cond"""
    if p[2] in ['&&', '||']:
        # Para operações lógicas
        p[0] = f'{p[1]}{p[3]}{condition_map["and" if p[2] == "&&" else "or"]}'
    else:
        # Para operações relacionais
        p[0] = f'{p[1]}{p[3]}{condition_map[p[2]]}'
    
def p_Cond_NOT(p):
    "Cond : NOT '(' Cond ')'"
    p[0] = f'{p[3]}NOT\n'

def p_If(p):
    "If : IF '(' Cond ')' '{' Instructions '}'"
    p[0] = f'{p[3]}JZ label{p.parser.labels}\n{p[6]}label{p.parser.labels}: NOP\n'
    p.parser.labels += 1

def p_If_Else(p):
    "If : IF '(' Cond ')' '{' Instructions '}' ELSE '{' Instructions '}'"
    p[0] = f'{p[3]}JZ label{p.parser.labels}\n{p[6]}JUMP label{p.parser.labels}f\nlabel{p.parser.labels}: NOP\n{p[10]}label{p.parser.labels}f: NOP\n'
    p.parser.labels += 1
    
# ------------------------------------------------------------  Loop

def p_Loop(p):
    """Loop : While
            | DoWhile"""
    p[0] = p[1]

def p_Do_While(p):
    "DoWhile : DO '{' Instructions '}' WHILE '(' Cond ')' SEMICOLON"
    p[0] = f'label{p.parser.labels}:\n{p[3]}{p[7]}NOT\nJZ label{p.parser.labels}\n'
    p.parser.labels += 1

def p_While(p):
    "While : WHILE '(' Cond ')' '{' Instructions '}'"
    p[0] = f'label{p.parser.labels}c: NOP\n{p[3]}JZ label{p.parser.labels}f\n{p[6]}JUMP label{p.parser.labels}c\nlabel{p.parser.labels}f: NOP\n'
    p.parser.labels += 1
    
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
    p[0] = f'PUSHS {p[3]}\nWRITES\n'

# ------------------------------------------------------------  Output

def p_Output(p):
    """Output : PRINT '(' ID ')' SEMICOLON"""
    mutationType = checkIfVariableAlreadyExists(p[3])
    varType = getVariableType(p[3])
    
    value = parser.vars[mutationType][varType][p[3]][0]
    
    p[0] = f"PUSHG {parser.vars[mutationType][varType][p[3]][1]}\nWRITE{'I' if varType == 'INT' else 'F' if varType == 'FLOAT' else 'S'}\n"   
    
def p_OutputString(p):
    """Output : PRINT '(' STRINGVALUE ')' SEMICOLON"""
    p[0] = f"PUSHS {p[3]}\nWRITES\n"

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
parser.regIndex = -1
parser.labels = 0
parser.functions = {}
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