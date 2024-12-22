# TP2 - Processamento de Linguagens e Compiladores

## 1 - Inspiração

Quisemos nos inspirar na linguagem TypeScript e decidimos fazer a linguagem PMScript (**PedroMonizScript**)

## 2 - Gramática da Linguagem

### 2.1 - Declaração de variáveis

#### **PMScript**

```ts
a: INT = 0;
b: STR = "Olá";
c: FLOAT = 10.9;
```

#### **GIC**

```ts
Declarations      : IntDeclaration Declarations
                  | StringDeclaration Declarations
                  | FloatDeclaration Declarations
                  | Empty

IntDeclaration    : ID ':' INT '=' INTVALUE ';'
StringDeclaration : ID ':' STR '=' STRVALUE ';'
FloatDeclaration  : ID ':' FLOAT '=' FLOATVALUE ';'
```
