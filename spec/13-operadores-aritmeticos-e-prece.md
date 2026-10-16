## Operadores Aritméticos e Precedência Geral

A precedência geral segue a convenção matemática padrão — multiplicação e divisão antes de adição e subtração:

```tinypine
1 + 2 * 3
# Resultado: 7 — a multiplicação possui prioridade maior que a soma
```

O comportamento detalhado de cada operador aritmético (`+`, `-`, `*`, `/`, `%`, `**`) sobre cada par de tipos primitivos ainda não está fechado; a precedência relativa entre eles já está consolidada na tabela do Capítulo 12.1 (ver Histórico, Apêndice A, item de pendências). Uma regra já está fechada: `+` entre `str` e um tipo numérico é `TypeMismatch PROBLEM`, sem coerção automática (Capítulo 9.2) — converta com `: to-str` ou `: to-num`.
