# TP2 - Processamento de Linguagens e Compiladores

## 1 - Inspiração

Quisemos nos inspirar na linguagem TypeScript e decidimos fazer a linguagem PMScript (**PedroMonizScript**)

## 2 - Gramática da Linguagem

### 2.1 - Declaração de variáveis

#### **PMScript**

```ts
const a: INT = 0;
let b: STR = "Olá";
const c: FLOAT = 10.9;
const arrInt: Array<INT> = [0, 1, 2, 3, 4, 5];
const arrFloat: Array<FLOAT> = [128.21, 293.19992, 75493.2123];
const arrString: Array<STR> = ["olá!", "tudo bem?"]
```

#### **GIC**

```ts
ProgramInit            : Declarations Instructions
                       | Instructions
                       | Declarations

Declarations           : Declaration Declarations
                       | Declaration

Declaration            : IntDeclaration
                       | FloatDeclaration
                       | StringDeclaration
                       | ArrayDeclaration
   
MutationType           : CONST
                       | LET
   
// Como temos que garantir a type safety, não podemos fazer recursividade nesse caso
IntDeclaration         : MutationType ID ':' 'INT' '=' INTVALUE ';'
FloatDeclaration       : MutationType ID ':' 'FLOAT' '=' FLOATVALUE ';'
StringDeclaration      : MutationType ID ':' 'STR' '=' STRVALUE ';'

ArrayDeclaration       : CONST ID ':' 'Array' '<' 'INT' '>' '=' '[' ArrayIntDeclaration ']' ';'
                       | CONST ID ':' 'Array' '<' 'FLOAT' '>' '=' '[' ArrayStringDeclaration ']' ';'
                       | CONST ID ':' 'Array' '<' 'STR' '>' '=' '[' ArrayFloatDeclaration ']' ';'

ArrayIntDeclaration    : INTVALUE ',' ArrayIntDeclaration
                       | INTVALUE

ArrayFloatDeclaration  : FLOATVALUE ',' ArrayFloatDeclaration
                       | FLOATVALUE

ArrayStringDeclaration : STRVALUE ',' ArrayStringDeclaration
                       | STRVALUE
```

___

### 2.2 - Atribuição de variáveis

#### **PMScript**

```ts
let a: INT = 10;
let b: STR = "Olá!";

// A variável b é uma variável "LET", então podemos modificar seu valor
b = "Tchau!";

// Como a variável a é um INT, caso seja atribuido um valor float, a será arredondado para o inteiro mais próximo
a = 20.3;
// output --> a = 20; 
```

#### **GIC**

```ts
Attributions           : NormalAttribution Attributions
                       | IncDecAttribution Attributions
                       | Empty

NormalAttribution      : ID '=' INTVALUE ';'
                       | ID '=' STRVALUE ';'
                       | ID '=' FLOATVALUE ';'

IncDecAttribution      | ID INC ';'
                       | ID DEC ';'
```

___

### 2.3 - Instruções

```ts
Instructions           : Instruction Instructions
                       | Instruction

Instruction            : Update ';'
                       | PRINT '(' Expression ')' ';'
                       | PRINT '(' ExpLogic ')' ';'
                       | PRINT '(' ExpressionFloat ')' ';'
                       | PRINT '(' STRVALUE ')' ';'
                       | PRINTLN '(' Expression ')' ';'
                       | PRINTLN '(' ExpLogic ')' ';'
                       | PRINTLN '(' ExpressionFloat ')' ';'
                       | PRINTLN '(' STRVALUE ')' ';'
                       | IF Boolean '{' Instructions '}' Else
                       | FOR '(' Update ';' Boolean ';' Update ')' '{' Instructions '}'
                       | FOR '(' Empty ';' Boolean ';' Update ')' '{' Instructions '}'
                       | WHILE '(' Boolean ')' '{' Instructions '}' 

Else                   : ELSE '{' Instructions '}'
                       | ELSE IF '(' Boolean ')' '{' Instructions '}' Else

Update                 : VARINT '=' Expression
                       | VARFLOAT '=' ExpressionFloat
                       | VARSTRING '=' STRVALUE
                       | VARINT PP
                       | VARINT MM
                       | VARFLOAT PP
                       | VARFLOAT MM
                       | VARARRAY '[' Expression ']' '=' Expression
                       | VARFLOAT '=' Expression
                       | VARINT '=' ExpressionFloat

Boolean                : Expression
                       | ExpLogic

STRVALUE               : VARSTRING
                       | Line
                       | INPUT '(' ')'

Empty                  : 

Expression             : Expression '+' Expression
                       | Expression '-' Expression
                       | Expression '*' Expression
                       | Expression '/' Expression
                       | Expression '%' Expression
                       | Value
                       | '(' Expression ')'

ExpressionFloat        : ExpressionFloat '+' ExpressionFloat
                       | ExpressionFloat '-' ExpressionFloat
                       | ExpressionFloat '*' ExpressionFloat
                       | ExpressionFloat '/' ExpressionFloat
                       | Expression '+' ExpressionFloat
                       | Expression '-' ExpressionFloat
                       | Expression '*' ExpressionFloat
                       | Expression '/' ExpressionFloat
                       | ExpressionFloat '+' Expression
                       | ExpressionFloat '-' Expression
                       | ExpressionFloat '*' Expression
                       | ExpressionFloat '/' Expression
                       | ValueFloat
                       | '(' ExpressionFloat ')'

Value                  : VARINT 
                       | VARARRAY '[' Expression ']'
                       | INTVALUE
                       | INT '(' STRVALUE ')'
                       | INT '(' ExpressionFloat ')'


ValueFloat             : VARFLOAT
                       | FLOATVALUE
                       | FLOAT '(' STRVALUE ')'
                       | FLOAT '(' Expression ')'

ExpLogic               : Expression EQUAL Expression
                       | Expression DIFF Expression
                       | Expression '>' Expression
                       | Expression '<' Expression
                       | Expression GEQUAL Expression
                       | Expression LEQUAL Expression
                       | ExpressionFloat EQUAL ExpressionFloat
                       | ExpressionFloat DIFF ExpressionFloat
                       | ExpressionFloat '>' ExpressionFloat
                       | ExpressionFloat '<' ExpressionFloat
                       | ExpressionFloat GEQUAL ExpressionFloat
                       | ExpressionFloat LEQUAL ExpressionFloat
                       | Expression EQUAL ExpressionFloat
                       | Expression DIFF ExpressionFloat
                       | Expression '>' ExpressionFloat
                       | Expression '<' ExpressionFloat
                       | Expression GEQUAL ExpressionFloat
                       | Expression LEQUAL ExpressionFloat
                       | ExpressionFloat EQUAL Expression
                       | ExpressionFloat DIFF Expression
                       | ExpressionFloat '>' Expression
                       | ExpressionFloat '<' Expression
                       | ExpressionFloat GEQUAL Expression
                       | ExpressionFloat LEQUAL Expression
                       | '(' ExpLogic ')'
                       | ExpLogic AND ExpLogic
                       | ExpLogic OR ExpLogic
                       | NOT ExpLogic
```
