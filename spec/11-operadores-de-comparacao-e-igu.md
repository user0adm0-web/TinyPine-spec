# PARTE IV — OPERADORES

## Operadores de Comparação e Igualdade

Palavras-operador (`is`, `in` — Capítulo 12.3 para `of`) são grafadas em minúsculas e reservadas pela linguagem — nenhuma delas pode ser usada como identificador de variável ou função.

| **Símbolo** | **Nome**                       | **Semântica**                                                                                               |
|-------------|--------------------------------|-------------------------------------------------------------------------------------------------------------|
| `is`        | Identidade                     | Verdadeiro apenas quando os dois lados são o **mesmo objeto** na memória (como o `is` do Python) — não compara valor nem tipo. Ver 11.1. |
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

`is` — **identidade**. `A is B` é verdadeiro apenas quando `A` e `B` são **o mesmo objeto** na memória: não compara o valor, nem o tipo, e sim *qual objeto* é. Vale para qualquer expressão nos dois lados (não só para variáveis). É o `is` do Python.

Uma variável guarda uma **referência** a um objeto: atribuir (`var B = A`), passar como argumento e guardar numa coleção **não copiam** o objeto — os dois nomes passam a apontar para o mesmo.

| **Valor**                                                         | **Quando dois lados são o mesmo objeto**                                                                                           |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `null`, `true`, `false`                                           | sempre: cada um existe uma única vez.                                                                                              |
| `num`, `int`, `float`, `decim`, `str` (escalares, imutáveis)      | quando têm o **mesmo tipo e o mesmo valor**: como um escalar não muda, não há como distinguir duas "cópias" dele.                  |
| lista, dicionário, tupla                                          | quando são o mesmo objeto criado: cada avaliação de um literal (`[1, 2]`, `{"a": 1}`, `(1, 2)`) cria um objeto **novo**.            |
| função (nomeada ou anônima), instância de classe, objeto nativo   | quando são o mesmo objeto: cada avaliação de uma função anônima cria uma função nova; uma função nomeada é sempre ela mesma.       |

```tinypine
var A = [1, 2]
var B = A          # B referencia o mesmo objeto que A (não copia)
var C = [1, 2]

A is B             # true  — o mesmo objeto
A is C             # false — valores iguais, mas objetos diferentes
A == C             # true  — igualdade de valor (abaixo)
5 is 5             # true  — escalares com o mesmo tipo e o mesmo valor
5 is 5.0           # false — tipos diferentes (num != float)
null is null       # true
B.add(3)           # altera o único objeto: A também passa a ser [1, 2, 3]
```

`is` **não tem forma negada** própria: nega-se agrupando, como em qualquer comparação (`not (A is C)`, Capítulo 12.1). Para comparar apenas o **tipo** de dois valores, compare o que `.type` devolve (Capítulo 6.7): `A.type == C.type`.

> ***Nota (sexta revisão pós-0.7):*** *até a quinta revisão, `is` comparava só o tipo dos dois valores (`5 is 10` era* `true`*). Agora é identidade; o que `is` fazia passa a ser escrito com `.type ==`. Os braços de* `case` *(Capítulo 25) continuam usando `is`, agora com o sentido de identidade — ver B30 no Apêndice A.2.*

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

Um `format` com um **grupo curinga** `[*]` (Capítulo 20.3) produz um **padrão**: um texto que, comparado com `==`/`!=`, passado a `.match()` ou escrito à direita de `~=`, é **casado** com a string da outra ponta em vez de comparado literalmente. O casamento é sempre do texto **inteiro** (não de um pedaço).

```tinypine
format "ar[*]" == "arroz"      # true  — [*] casa zero ou mais caracteres
format "[*]a[*]" == "a"        # true  — os dois grupos casam zero caracteres
format "a[*4]" == "arroz"      # true  — "rroz" são 4 caracteres (até 4)
"casa".match(format "c[1*1]sa")   # true  — [1*1] casa exatamente um caractere
"teste".match(format "t[1*1]")    # false — "t" + um caractere tem 2 caracteres; "teste" tem 5
```

Regras:

- **Só um `format` com curinga é padrão.** Uma string comum nunca casa: `"ar[*]" == "arroz"` é `false` (igualdade literal pura). A nota da 0.5 — "`==` nunca faz correspondência por padrão" — continua verdadeira para strings comuns; a exceção é explícita no código, pelo `format`.
- O padrão pode estar **de qualquer lado** de `==`/`!=`: `"arroz" == format "ar[*]"` também é `true`. Se os **dois** lados são padrões, comparam-se os textos escritos, literalmente (sem casar). Se o outro lado não é `str`, o resultado é `false`.
- `.match(x)` e `~=` usam o mesmo casamento quando `x` é um padrão; quando `x` é uma string comum, são igualdade literal.
- `is` (identidade) e `===` **nunca** casam por padrão: `===` compara o texto escrito do padrão, e `is` pergunta se é o mesmo objeto.
- A sequência `\*` (a antiga forma de curinga, exatamente um caractere) **deixou de existir**: é `DeprecatedSyntax PROBLEM` (E118). Seu equivalente é `[1*1]`. Atenção: o novo `[*]` (zero ou mais) **não** é o antigo `\*` (exatamente um).

### != e !== — Açúcar de Negação

`!=` e `!==` não são operadores próprios — são reescritos, ainda na análise sintática, como a negação da comparação correspondente:

```tinypine
a != b    # equivale a not (a == b)
a !== b   # equivale a not (a === b)
```

Não existe negação avulsa fora de `!=`/`!==` — o símbolo `!` sozinho não é um operador válido (Capítulo 12 usa a palavra `not` para negação geral). Ver Capítulo 12.1 sobre por que negar uma comparação sempre exige agrupar a comparação inteira. A única ocorrência de `!` avulso admitida pela linguagem é o marcador estrutural da lista de parâmetros de uma declaração de função (Capítulo 30.3): ali `!` não é operador, identificador, argumento nem variável.
