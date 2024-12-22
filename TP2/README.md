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
```

#### **GIC**

```ts
Declarations      : IntDeclaration Declarations
                  | StringDeclaration Declarations
                  | FloatDeclaration Declarations
                  | Empty

MutationType      : CONST
                  | LET

IntDeclaration    : MutationType ID ':' INT '=' INTVALUE ';'
StringDeclaration : MutationType ID ':' STR '=' STRVALUE ';'
FloatDeclaration  : MutationType ID ':' FLOAT '=' FLOATVALUE ';'
```
