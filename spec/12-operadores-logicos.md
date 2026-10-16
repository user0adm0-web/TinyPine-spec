## Operadores Lógicos

| **Símbolo** | **Nome**                | **Semântica**                                                                                                                                                                         |
|-------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `not`       | Negação lógica          | Inverte o valor lógico da expressão à direita. Maior prioridade que `and`/`xor`/`or` (ver 12.1). Não confundir com `!=`/`!==` (Capítulo 11.3) — `not` sozinho nunca é seguido de `=`. |
| `and`       | Conjunção lógica        | Retorna `true` apenas quando ambas as expressões avaliadas são `true`. Retorna `bool`.                                                                                                |
| `or`        | Disjunção lógica        | Retorna `true` quando pelo menos uma das expressões avaliadas é `true`. Retorna `bool`.                                                                                               |
| `xor`       | Ou-exclusivo            | Retorna `true` quando exatamente uma das duas expressões avaliadas é `true` — `false` quando as duas são iguais. Ver 12.2.                                                            |
| `of`        | Pertencimento por valor | Testa se um VALOR existe em uma lista ou dicionário (não índice/chave). Em string, gera TypeMismatch PROBLEM. Ver 12.3.                                                               |

### Precedência — not e Parênteses

`not` possui precedência maior que `and`, `xor` e `or`. Assim, a expressão:

```tinypine
not A and B
```

é interpretada como:

```tinypine
(not A) and B
```

O modificador de precedência `^` (usado como em `not x ^and y`) foi removido na 0.5. Para forçar uma ligação diferente da precedência padrão, use parênteses explícitos:

```tinypine
not (x and y)      # equivalente ao antigo not x ^and y
```

`!=` e `!==` continuam existindo como açúcar sintático de `not` (Capítulo 11.3) — a forma explícita com `not (...)` também é sempre válida.

A tabela a seguir consolida a precedência entre todos os operadores da linguagem — do agrupamento explícito por parênteses (maior prioridade) até a disjunção lógica (menor prioridade):

| **Prioridade** | **Símbolo(s)**                                                    |
|----------------|-------------------------------------------------------------------|
| 1              | `( )`                                                             |
| 2              | `not`                                                             |
| 3              | `*`, `/`, `**`, `%`                                               |
| 4              | `+`, `-`                                                          |
| 5              | `&and`, `&or`, `&xor`                                             |
| 6              | `is`, `==`, `===`, `!=`, `!==`, `in`, `of`, `>`, `<`,  `<=`, `>=` |
| 7              | `and`                                                             |
| 8              | `xor`                                                             |
| 9              | `or`                                                              |
| 10             | `\|>`                                                              |
| 11             | `IF`                                                              |

O operador `|>` (34.8) foi incluído nesta tabela por consolidar a precedência geral da linguagem — abaixo inclusive de `( )`, e só perde em prioridade pro próprio if pós-fixo (Capítulo 12.4), o único operador mais baixo que ele. Nem `|>` nem if são operadores lógicos como os demais desta tabela: `|>` envia o valor à sua esquerda para o destino à sua direita (ver 34.8); if decide se a expressão à sua esquerda chega a ser avaliada (ver 12.4).

### Operadores Bit a Bit — prefixo &

Os símbolos `&`, `|` e `^` são operadores bit a bit — cada um aplica a operação lógica correspondente (E, OU, OU-exclusivo) a cada bit dos dois operandos (convertidos para `int` — Capítulo 6, truncando a parte fracionária de um `num`, se houver):

| **Símbolo** | **Nome**               | **Semântica**                                                                         |
|-------------|------------------------|---------------------------------------------------------------------------------------|
| `&and`      | E bit a bit            | Cada bit do resultado é 1 só quando o bit correspondente é 1 nos dois operandos.      |
| `&or`       | OU bit a bit           | Cada bit do resultado é 1 quando o bit correspondente é 1 em pelo menos um operando.  |
| `&xor`      | OU-exclusivo bit a bit | Cada bit do resultado é 1 quando o bit correspondente difere entre os dois operandos. |

```tinypine
10 &and 121   # 10 = 0b0001010, 121 = 0b1111001 → 0b0001000 = 8
10 &or 121    # → 0b1111011 = 123
10 &xor 121   # → 0b1110011 = 115
```

*sempre devolvem* `int` *— mesmo quando os dois operandos são* `num`*.*

### in e of sobre Coleções

`in` e `of` fazem perguntas diferentes sobre a mesma coleção: `in` pergunta "esse índice/chave existe?"; `of` pergunta "esse valor existe?". Em string, só `in` se aplica (substring) — `of` não tem sentido definido e é erro:

```tinypine
"A" in "ARROZ"          # true — substring
"a" in {"a": 10}         # true — a CHAVE "a" existe
1 in ["", ""]           # true — o ÍNDICE 1 existe (lista de 2 posições)
10 of {"a": 10}          # true — o VALOR 10 existe
"x" of ["a", "x"]       # true — o VALOR "x" existe na lista
"A" of "ARROZ"          # TypeMismatch PROBLEM — of não funciona em string
```

### Operador Condicional Pós-fixo — IF

O operador condicional pós-fixo `expressão if condição` avalia condição primeiro. Se for verdadeira, expressão é avaliada normalmente e seu valor é o resultado; se for falsa, expressão nunca chega a ser avaliada, e o resultado é `void` (Capítulo 7.2). É o operador de menor precedência de toda a linguagem — menor até que `|>` (Capítulo 34.8) — e é inteiramente distinto da estrutura condicional de bloco do Capítulo 22:

```tinypine
var A = true
var B = false
print("oi" if A)
print("não aparece" if B else "apareceu não")
```

Como argumento de `print` / `println` (Capítulo 20.1), uma condição falsa remove o argumento inteiro da lista — inclusive o `sep` correspondente — em vez de deixar um void no lugar dele:

```tinypine
print("A" if true, "B" if false, "C" if true, “sep”:"-")
# → A-C (B nunca aparece — nem como void, nem como separador sobrando)
```

Nota: quando usado como argumento de uma função definida pelo usuário (aridade fixa, posicional), essa omissão não tem regra fechada — hoje o argumento vira void na posição, em vez de deslocar os parâmetros seguintes (pendência B15, ver Apêndice A.2).
