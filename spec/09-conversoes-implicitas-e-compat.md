## Conversões Implícitas e Compatibilidade entre Tipos

O interpretador aplica conversão implícita apenas em um caso específico e restrito, descrito em 9.1; em todos os demais casos de incompatibilidade de tipos entre operandos, a execução é interrompida com um erro de tipo. O TinyPine, portanto, favorece deliberadamente a tipagem explícita sobre a coerção automática.

### Conversão Implícita de bool para Numérico

Valores booleanos podem participar de operações numéricas por meio de conversão implícita, definida como:

```tinypine
true  → 1
false → 0
```

Essa conversão é permitida **apenas em operações numéricas**. Sempre que ocorrer, o interpretador executa a operação normalmente, mas registra um `ImplicitBoolConversion WARNING` no log — a operação nunca falha silenciosamente nem é impedida, mas a conversão implícita é sempre reportada.

```tinypine
1 + true
# Resultado: 2
# Log: ImplicitBoolConversion WARNING
```

### Incompatibilidade entre str e Tipos Numéricos

Operações entre um valor do tipo `str` e um tipo numérico **não são permitidas**. Sempre que uma operação envolver tipos incompatíveis nesse sentido, o interpretador interrompe a execução da instrução com um erro de tipo — não há conversão implícita de string para número em contexto operacional (para isso, o programador deve usar `: to-num` ou equivalente, de forma explícita).

```tinypine
"5" + 1   # TypeMismatch PROBLEM
"5" > 2   # TypeMismatch PROBLEM
```

**Concatenação de texto.** O operador `+` entre dois valores `str` os concatena; entre um `str` e um tipo numérico é `TypeMismatch PROBLEM` — não há coerção automática, nem do número para texto nem do texto para número. Para juntar texto e número, converta o número com `: to-str` (Capítulo 8); para somar, converta o texto com `: to-num`.

```tinypine
"Idade: " + 20             # TypeMismatch PROBLEM
"Idade: " + 20: to-str     # "Idade: 20" — o sufixo : to-str vale só para o 20
"Idade: " + (20: to-str)   # equivalente, com parênteses para ficar explícito
"5": to-num + 1            # 6
```
