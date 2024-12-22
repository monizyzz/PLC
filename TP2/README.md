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
Declarations           : IntDeclaration "\n" Declarations
                       | StringDeclaration "\n" Declarations
                       | FloatDeclaration "\n" Declarations
                       | ArrayDeclaration "\n" Declarations
                       | Empty
   
MutationType           : CONST
                       | LET
   
// Como temos que garantir a type safety, não podemos fazer recursividade nesse caso
IntDeclaration         : MutationType ID ':' INT '=' INTVALUE ';'
StringDeclaration      : MutationType ID ':' STR '=' STRVALUE ';'
FloatDeclaration       : MutationType ID ':' FLOAT '=' FLOATVALUE ';'

ArrayDeclaration       : MutationType ID ':' 'Array' '<' INT '>' '=' '[' ArrayIntDeclaration ']' ';'
                       | MutationType ID ':' 'Array' '<' STR '>' '=' '[' ArrayFloatDeclaration ']' ';'
                       | MutationType ID ':' 'Array' '<' FLOAT '>' '=' '[' ArrayStringDeclaration ']' ';'

ArrayIntDeclaration    : INTVALUE COMMA ArrayIntDeclaration
                       | INTVALUE
                       | Empty

ArrayFloatDeclaration  : FLOATVALUE COMMA ArrayFloatDeclaration
                       | FLOATVALUE
                       | Empty

ArrayStringDeclaration : STRVALUE COMMA ArrayStringDeclaration
                       | STRVALUE
                       | Empty
```
