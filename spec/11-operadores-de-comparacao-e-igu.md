# PARTE IV — OPERADORES

## Operadores de Comparação e Igualdade

Palavras-operador (`is`, `in` — Capítulo 12.3 para `of`) são grafadas em minúsculas e reservadas pela linguagem — nenhuma delas pode ser usada como identificador de variável ou função.

| **Símbolo** | **Nome**                       | **Semântica**                                                                                               |
|-------------|--------------------------------|-------------------------------------------------------------------------------------------------------------|
| `is`        | Igualdade de tipo              | Compara apenas o TIPO dos dois valores (o que `.type` retornaria para cada um) — nunca o valor. Ver 11.1.   |
| `==`        | Igualdade de valor             | Compara o VALOR dos dois operandos, com igualdade estrutural recursiva sobre coleções. Ver 11.1.            |
| `===`       | Igualdade de tipo e valor      | Verdadeiro apenas quando `esquerda.type == direita.type` E os valores também são iguais por `==`. Ver 11.1. |
| `!=`        | Diferença de valor             | Açúcar sintático para `not (a == b)`. Ver 11.3.                                                             |
| `!==`       | Diferença de tipo e/ou valor   | Açúcar sintático para `not (a === b)`. Ver 11.3.                                                            |
| `in`        | Pertencimento por índice/chave | Em string, testa substring. Em lista/dicionário, testa se o ÍNDICE/CHAVE existe — não o valor. Ver 12.3.    |
| `>`         | Maior que                      | Verifica se o valor à esquerda é maior que o valor à direita. Retorna bool.                                 |
| `<`         | Menor que                      | Verifica se o valor à esquerda é menor que o valor à direita. Retorna bool.                                 |
| `>=`        | Maior ou igual                 | Verifica se o valor à esquerda é maior ou igual ao valor à direita. Retorna bool.                           |
| `<=`        | Menor ou igual                 | Verifica se o valor à esquerda é menor ou igual ao valor à direita. Retorna bool.                           |

### Definição Unificada de is, == e ===

`is` — igualdade de tipo. Compara `esquerda.type` com `direita.type` (Capítulo 9.2/19.5) e nada mais — o valor de cada lado é irrelevante:

```tinypine
5 is 10        # true — os dois são num
5 is "5"       # false — num não é str
[1,2] is [3,4] # true — os dois são collection
```

`==` — igualdade de valor. Sobre tipos escalares (`str`, `num`, `int`, `float`, `decim`, `bool`), compara o valor diretamente. Sobre coleções e tuplas, aplica igualdade estrutural recursiva: duas coleções são iguais quando têm o mesmo formato (ambas lista ou ambas dicionário), os mesmos elementos — ou os mesmos pares chave:valor, no caso de dicionário — na mesma ordem, com os elementos correspondentes também considerados iguais por `==`.

```tinypine
[1, 2] == [1, 2]   # true
null == null       # true
5 == 5.0           # true
```

`===` — igualdade de tipo e valor. Verdadeiro apenas quando os dois critérios acima batem ao mesmo tempo: mesmo `.type` e mesmo valor por `==`.

```tinypine
5 === 5           # true
[1,2] === [1,2]   # true
```

### Correspondência por Padrão sobre Strings

Quando o argumento de `.match()` — ou o operando à direita de `~=` — é uma string contendo a sequência de escape `\*` (ver 3.2.3), a correspondência é por padrão em vez de igualdade literal: cada ocorrência de `\*` corresponde a exatamente um caractere arbitrário na posição equivalente da string à esquerda. A partir da 0.5, `==` nunca faz correspondência por padrão — é sempre igualdade literal pura, mesmo que `\*` apareça na string.

```tinypine
"casa".match("c\*sa")   # true
"teste".match("t\*")    # false — "t\*" tem 2 caracteres; "teste" tem 5
```

`is` *nunca faz correspondência por padrão — ele nem olha pro valor, só pro tipo.*

### != e !== — Açúcar de Negação

`!=` e `!==` não são operadores próprios — são reescritos, ainda na análise sintática, como a negação da comparação correspondente:

```tinypine
a != b    # equivale a not (a == b)
a !== b   # equivale a not (a === b)
```

Não existe negação avulsa fora de `!=`/`!==` — o símbolo `!` sozinho não é um operador válido (Capítulo 12 usa a palavra `not` para negação geral). Ver Capítulo 12.1 sobre por que negar uma comparação sempre exige agrupar a comparação inteira. A única ocorrência de `!` avulso admitida pela linguagem é o marcador estrutural da lista de parâmetros de uma declaração de função (Capítulo 30.3): ali `!` não é operador, identificador, argumento nem variável.
