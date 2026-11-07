# Operadores em listas, dicionários e strings

## Operadores Universais de objetos

Expõe um conjunto amplo de operações, organizadas em três categorias funcionais. Todas são chamadas como método (`objeto.operacao(...)`) e seguem as mesmas convenções do `.add()`, descritas nas seções "Convenções comuns" e "Regras gerais de index":

| **Categoria** | **Operações catalogadas** |
|---------------|---------------------------|
| Consulta | `includes`, `startsWith`, `endsWith`, `find`, `findLast`, `indexOf`, `lastIndexOf`, `indicesOf`, `count`, `equals`, `equalsIgnoreCase`, `compare`, `isEmpty`, `isAlpha`, `isAlphaNum`, `isDigit`, `isLetter`, `isLower`, `isUpper`, `isNumber`, `isSpace`, `before`, `after`, `between` |
| Transformação | `upper`, `lower`, `title`, `trim`, `trimLeft`, `trimRight`, `replace`, `replaceAll`, `reverse`, `remove`, `removeAll`, `removeFirst`, `removeLast`, `padLeft`, `padRight`, `left`, `right`, `center`, `substring`, `slice`, `add` |
| Composição | `add`, `join`, `repeat`, `split`, `lines`, `words` |

### Convenções comuns

**1. Receptor.** Cada operação diz a quais tipos se aplica. Aplicá-la a outro tipo é `TypeMismatch PROBLEM`. A tabela abaixo é o resumo; os detalhes estão em cada operação.

| Operação | `str` | `list` | `dict` | `tuple` |
|---|:-:|:-:|:-:|:-:|
| `add` | sim | sim | sim | não (imutável) |
| `remove`, `removeAll`, `removeFirst`, `removeLast` | sim (devolve nova) | sim (modifica) | sim (modifica) | não (imutável) |
| `replace`, `replaceAll`, `reverse` | sim (devolve nova) | sim (modifica) | sim (modifica) | não (imutável) |
| `includes`, `indexOf`, `lastIndexOf`, `indicesOf`, `count`, `find`, `findLast` | sim | sim | sim | sim |
| `startsWith`, `endsWith`, `equals`, `isEmpty` | sim | sim | sim | sim |
| `compare` | sim | sim | não | sim |
| `before`, `after`, `between`, `left`, `right`, `slice`, `repeat`, `split` | sim | sim | `left` e `right` apenas | sim, exceto `split` e `repeat` |
| `join` | não | sim | não | sim |
| `equalsIgnoreCase`, `upper`, `lower`, `title`, `trim`, `trimLeft`, `trimRight`, `padLeft`, `padRight`, `center`, `substring`, `lines`, `words`, `isAlpha`, `isAlphaNum`, `isDigit`, `isLetter`, `isLower`, `isUpper`, `isNumber`, `isSpace` | sim | não | não | não |

**2. Quem é modificado e o que é devolvido.**

- **Consulta** nunca modifica o receptor e devolve o resultado.
- **`str` é imutável** (Capítulo 6): toda transformação sobre `str` devolve uma **nova** string e deixa a original intacta, inclusive se a chamada falhar. O resultado precisa ser usado ou atribuído (`A = A.upper()`).
- **`list` e `dict`** são alterados no lugar pelas operações **modificadoras**: `add`, `remove`, `removeAll`, `removeFirst`, `removeLast`, `replace`, `replaceAll` e `reverse`. Elas devolvem `null` (Decisão 3 abaixo). Todas as demais operações sobre `list`/`dict` devolvem um objeto **novo** e não modificam o receptor.
- **`tuple`** nunca é modificada: uma operação modificadora sobre ela é `ImmutableMutation PROBLEM` (Capítulo 19.5).

**3. Igualdade.** "Igual", nas operações que comparam valores (`includes`, `indexOf`, `count`, `remove`, `replace` etc.), é a igualdade de valor `==` do Capítulo 11.1, estrutural sobre coleções. Em `list` e `dict` as operações de valor olham os **valores** (nunca as chaves; para chaves existe o operador `in`, Capítulo 12.3, que continua sendo o teste de chave/índice). Texto passado a uma operação de `str` é sempre **literal**: um padrão (`format` com curinga, Capítulo 20.3) não é aceito aqui — para casamento por padrão use `~=` ou `.match()` (Capítulo 11.2).

**4. Posições.** Toda posição é um inteiro base 0, contada em unidades de caractere (`str`), elementos (`list`) ou entradas na ordem de iteração (`dict`) — a mesma unidade do `.length`. Em `dict` a posição **não** é a chave.

**5. Argumentos nomeados.** Os parâmetros opcionais abaixo são sempre nomeados e seguem o Capítulo 30.3 (`nome=valor` ou `"nome": valor`). Nome desconhecido é `UnknownNamedArgument PROBLEM`, argumento posicional a mais é `TooManyArguments PROBLEM` e a falta de um obrigatório é `MissingArgument PROBLEM`.

| Parâmetro | Em quais operações | Significado |
|---|---|---|
| `index` | `add`, `remove` | Posição de inserção (`add`) ou de remoção (`remove`). Regras na próxima seção. |
| `start`, `end` | buscas: `includes`, `indexOf`, `lastIndexOf`, `indicesOf`, `count`, `find`, `findLast` | Restringem a busca às posições de `start` a `end`, **as duas incluídas**, base 0 (o mesmo sentido do `for`, Capítulo 23, e de `A[a to b]`, Capítulo 19.2.1). Os índices devolvidos continuam contados a partir do início do receptor. |
| `fill` | `padLeft`, `padRight`, `center` | Caractere de preenchimento (uma `str` de exatamente 1 caractere). Padrão: espaço. |
| `chars` | `trim`, `trimLeft`, `trimRight` | Conjunto de caracteres a retirar (uma `str`; cada caractere vale por si). Padrão: espaço em branco. |
| `sep` | `join` | Texto colocado entre os elementos. Padrão: vazio. |

`start` e `end`, quando dados, precisam estar dentro do receptor (`0` a `length - 1`) e `start` não pode passar de `end`; fora disso é `IndexOutOfBounds PROBLEM`. Um receptor vazio aceita qualquer busca e devolve o resultado "nada encontrado".

**6. Validação e atomicidade.** Toda operação valida **todos** os argumentos antes de modificar qualquer coisa: se qualquer verificação falhar, o receptor fica exatamente como estava (regra já fixada para o `add`, ver "Validação e atomicidade", abaixo).

### Objetivo do `.add()`

A operação `.add()` insere conteúdo em uma coleção ou em uma string.

- `list.add()` insere um ou mais elementos.
- `dict.add()` insere um ou mais pares chave–valor.
- `str.add()` retorna uma nova string com o texto inserido.

A posição de inserção é controlada pelo argumento nomeado opcional `index`.

#### Sintaxe

```tinypine
lista.add(valor, index=índice)
lista.add(valor1, valor2, ..., index=índice)
dicionario.add({chave: valor, ...}, index=índice)
dicionario.add({chave1: valor1}, {chave2: valor2}, index=índice)
texto.add(outro_texto, index=índice)
texto.add(texto1, texto2, index=índice)
```

`index` é opcional.
Quando omitido, a inserção ocorre no final.

Com **mais de um argumento**, todos são inseridos, **na ordem em que foram escritos**, como um bloco só: `A.add(1, 2)` equivale a `A.add(1)` seguido de `A.add(2)`, e `A.add(7, 8, 9, index=1)` coloca `7, 8, 9` consecutivos a partir da posição 1. Em `str`, os textos são concatenados na ordem. Em `dict`, os dicionários formam um único bloco (ver "Chaves já existentes").

O marcador `...` acima é apenas uma abreviação documental para indicar que pode haver mais de um par chave–valor ou de argumento.
Não é sintaxe literal do TinyPine.

#### Regras gerais de index

Considere `length` o comprimento atual da lista ou string, ou a quantidade atual de entradas do dicionário.

| Valor de `index` | Comportamento |
|---|---|
| Omitido | Insere no final. |
| `0` | Insere no início, antes do elemento ou entrada de índice `0`. |
| Entre `0` e `length - 1` | Insere antes do elemento ou entrada existente nesse índice. |
| Igual a `length` | Insere no final. |
| Menor que `0` | Erro de índice inválido. |
| Maior que `length` | Erro de índice inválido. |

`index` deve ser um inteiro.
Um valor de outro tipo é `TypeMismatch PROBLEM`; um valor fora do intervalo é `IndexOutOfBounds PROBLEM`.

Para uma coleção vazia, `index=0` é válido e equivale à inserção no final.

#### list.add — Inserção de elementos

#### Forma

```tinypine
lista.add(valor)
lista.add(valor1, valor2, ...)
lista.add(valor, index=índice)
```

#### Semântica

`list.add()` insere os valores na lista receptora.
Sem `index`, os elementos são acrescentados ao final.
Com `index`, os elementos são inseridos antes do elemento que ocupa aquela posição.

A operação altera a lista receptora.
Os elementos que estavam na posição de inserção ou depois dela deslocam-se para a direita.

#### Exemplos

```tinypine
var A = [10, 20, 30]

A.add(40)
# A -> [10, 20, 30, 40]

A.add(5, index=0)
# A -> [5, 10, 20, 30, 40]

A.add(15, index=2)
# A -> [5, 10, 15, 20, 30, 40]

A.add(1, 2)
# A -> [5, 10, 15, 20, 30, 40, 1, 2]

A.add(7, 8, 9, index=1)
# A -> [5, 7, 8, 9, 10, 15, 20, 30, 40, 1, 2]
```

#### dict.add — Inserção de entradas

#### Forma

```tinypine
dicionario.add({chave: valor})
dicionario.add({chave1: valor1, chave2: valor2}, index=índice)
dicionario.add({chave1: valor1}, {chave2: valor2})
```

#### Semântica

`dict.add()` insere no dicionário receptor as entradas dos dicionários fornecidos.
Sem `index`, as novas entradas são acrescentadas ao final da sequência de entradas.
Com `index`, o bloco de entradas fornecido é inserido antes da entrada que ocupa aquela posição.

Quando vários pares (ou vários dicionários) são fornecidos, a ordem relativa entre eles deve ser preservada.

A operação altera o dicionário receptor.

#### Chaves já existentes

Para evitar alterações silenciosas, a tentativa de inserir uma chave que já existe no dicionário receptor — ou que aparece duas vezes entre os argumentos — produz um erro de chave duplicada.
A operação não sobrescreve o valor existente implicitamente (para editar uma entrada existente use `D["chave"] = valor`, Capítulo 19.4.1).

Se houver conflito em qualquer chave do bloco fornecido, nenhuma das entradas desse bloco é inserida.
Isso evita uma inserção parcial.

#### Exemplos

```tinypine
var A = {"B": 2, "D": 4}

A.add({"E": 5})
# A contém, em ordem: "B": 2, "D": 4, "E": 5

A.add({"A": 1, "C": 3}, index=0)
# A contém, em ordem: "A": 1, "C": 3, "B": 2, "D": 4, "E": 5
```

Exemplo de conflito:

```tinypine
A.add({"X": 10, "B": 20})
# Erro de chave duplicada: "B" já existe.
# A operação não insere "X" nem altera o valor de "B".
```

#### Observação sobre índices

O índice de um dicionário é a posição da entrada na ordem de iteração definida pela linguagem.
Não é a chave do dicionário.
O operador `in` continua verificando a existência de uma chave em um dicionário, não a existência de um valor.

#### str.add — Inserção de texto

#### Forma

```tinypine
texto.add(outro_texto)
texto.add(texto1, texto2, ...)
texto.add(outro_texto, index=índice)
```

#### Semântica

`str.add()` retorna uma nova string com os textos inseridos na string receptora.
A string original não é alterada, pois `str` é um tipo escalar imutável.

Sem `index`, o texto é acrescentado ao final.
Com `index`, o texto é inserido antes do caractere naquela posição.

#### Exemplos

```tinypine
var A = "abcd"

var B = A.add("XY")
# B -> "abcdXY"
# A continua sendo "abcd"

var C = A.add("XY", index=1)
# C -> "aXYbcd"

var D = A.add("início", index=0)
# D -> "inícioabcd"

var E = A.add("X", "Y", index=1)
# E -> "aXYbcd"
```

O valor retornado deve ser usado ou atribuído explicitamente se for necessário conservar o resultado:

```tinypine
A = A.add("XY")
```

#### Validação e atomicidade

A operação deve validar os argumentos antes de modificar a coleção receptora.

- Um `index` inválido resulta em erro, sem modificar a lista ou o dicionário.
- Um tipo de argumento incompatível resulta em `TypeMismatch PROBLEM`; em coleção tipada (Capítulo 6.8), um valor fora do tipo declarado desfaz a inserção inteira.
- Em `dict.add()`, um conflito de chave impede a inserção de todo o bloco fornecido.
- Em `str.add()`, a operação retorna uma nova string; a string original permanece inalterada, inclusive se a chamada falhar.

### Operações de consulta

Nenhuma operação desta seção modifica o receptor.

#### Busca de valores

Nas formas abaixo, `x` é o valor procurado: um texto (não vazio) em `str`; qualquer valor em `list` e `dict` (comparado com `==` aos **valores**). Texto vazio como `x` é `InvalidArgument PROBLEM` (Decisão 4). `start` e `end` são os do item 5 das convenções.

| Operação | Receptor | Devolve |
|---|---|---|
| `includes(x)` | `str`, `list`, `dict`, `tuple` | `bool`: há uma ocorrência de `x`? Em `str` é a busca de substring (o mesmo que `x in S`); em `list`/`dict` é a busca de valor (o mesmo que `x of A`). |
| `indexOf(x)` | idem | A posição da **primeira** ocorrência (em `str`, a posição do primeiro caractere dela), ou `null` se não houver. |
| `lastIndexOf(x)` | idem | A posição da **última** ocorrência, ou `null`. |
| `indicesOf(x)` | idem | Uma lista com as posições de **todas** as ocorrências, em ordem crescente (`[]` se não houver). Em `str` as ocorrências não se sobrepõem: `"aaaa".indicesOf("aa")` é `[0, 2]`. |
| `count(x)` | idem | Quantas ocorrências há (`int`; `0` se não houver). Em `str`, as mesmas ocorrências não sobrepostas de `indicesOf`. |
| `find(teste)` | idem | O **primeiro elemento** para o qual a função `teste` devolve verdadeiro, ou `null` se nenhum satisfizer. |
| `findLast(teste)` | idem | O **último** elemento que satisfaz `teste`, ou `null`. |

O resultado de uma busca que não encontra nada é `null` (e não `-1`), porque índices negativos são válidos em `lista[-1]` (Capítulo 36.3) e a linguagem prefere o `Null` explícito (Capítulo 7). Em `dict`, `indexOf` devolve a **posição** da entrada, não a chave.

`teste` é uma função (nomeada ou anônima, Capítulo 31) com **um parâmetro** — o elemento (em `str`, cada caractere; em `dict`, cada valor) — cujo retorno é interpretado como em `if` (Capítulo 22). Argumento que não é função é `TypeMismatch PROBLEM`. Como `find` e `findLast` devolvem `null` tanto para "nenhum" quanto para um elemento que é o próprio `null`, quem precisa distinguir os dois casos usa `indexOf`/`includes`.

```tinypine
var L = [5, 8, 5, 3]
L.includes(8)                       # true
L.indexOf(5)                        # 0
L.lastIndexOf(5)                    # 2
L.indicesOf(5)                      # [0, 2]
L.count(5)                          # 2
L.indexOf(5, start=1)               # 2  (busca da posição 1 em diante)
L.indexOf(5, start=1, end=3)        # 2  (busca só nas posições 1 a 3)
f maior_que_seis(e)
  return e > 6
L.find(maior_que_seis)              # 8
L.findLast(f (e)                    # 3  (função anônima: o corpo leva return, Capítulo 31)
  return e < 6
)

"banana".indicesOf("an")            # [1, 3]
"banana".count("a")                 # 3
"banana".indexOf("z")               # null
{"a": 10, "b": 20}.indexOf(20)      # 1  (a posição da entrada, não a chave)
```

#### Início e fim

| Operação | Devolve |
|---|---|
| `startsWith(x)` | `bool`: o receptor **começa** por `x`? |
| `endsWith(x)` | `bool`: o receptor **termina** com `x`? |

Em `str`, `x` é um texto: `"banana".startsWith("ban")` é `true`; `startsWith("")` é `true` (todo texto começa pelo vazio). Em `list`/`tuple`, `x` é uma **lista** com os elementos iniciais (ou finais), na ordem. Em `dict`, `x` é um **dicionário** com as entradas iniciais (ou finais), na ordem, comparadas por chave e por valor. `x` maior que o receptor dá `false`.

```tinypine
"banana".endsWith("ana")            # true
[1, 2, 3].startsWith([1, 2])        # true
[1, 2, 3].endsWith([2, 3])          # true
{"a": 1, "b": 2}.startsWith({"a": 1})   # true
```

#### Comparação

| Operação | Receptor | Devolve |
|---|---|---|
| `equals(outro)` | qualquer | `bool`: o mesmo que `receptor == outro` (Capítulo 11.1), em forma de método — útil para encadear. |
| `equalsIgnoreCase(outro)` | `str` | `bool`: igualdade ignorando a diferença entre maiúsculas e minúsculas. `outro` precisa ser `str`. |
| `compare(outro)` | `str`, `list`, `tuple` | `-1` se o receptor vem **antes** de `outro`, `0` se são iguais, `1` se vem **depois**. A ordem é a de `<` e `>` (Capítulo 11); em coleções é lexicográfica, e a mais curta que é prefixo da outra vem antes. Tipos que `<` não compara entre si são `TypeMismatch PROBLEM`. |

```tinypine
"Casa".equalsIgnoreCase("cASA")     # true
"abc".compare("abd")                # -1
[1, 2].compare([1, 2, 0])           # -1
[1, 2].equals([1, 2])               # true
```

#### Estado e classe de caracteres

`isEmpty()` aceita qualquer tipo: é `true` quando `length` é zero.

As demais são só de `str` e respondem `bool`. **Texto vazio dá sempre `false`**, exceto em `isEmpty`.

| Operação | É `true` quando |
|---|---|
| `isAlpha()` | todo caractere é uma **letra** (qualquer letra Unicode, com acento). |
| `isLetter()` | o texto tem **exatamente um** caractere e ele é uma letra. |
| `isDigit()` | todo caractere é um dígito de `0` a `9`. |
| `isAlphaNum()` | todo caractere é letra ou dígito de `0` a `9`. |
| `isNumber()` | o texto inteiro é um literal numérico válido para `: to-num` (Capítulo 8): sinal opcional, dígitos, ponto decimal e expoente (`"-12"`, `"3.14"`, `"2e5"`), sem espaços. Difere de `isDigit`: `"3.14"` é `isNumber` e não é `isDigit`. |
| `isSpace()` | todo caractere é espaço em branco (espaço, TAB, `\n`, `\r` e demais espaços Unicode). |
| `isLower()` | há ao menos uma letra com caixa e todas as letras com caixa são minúsculas (`"abc1"` sim; `"1"` não). |
| `isUpper()` | há ao menos uma letra com caixa e todas são maiúsculas. |

```tinypine
"Olá".isAlpha()        # true
"a".isLetter()         # true
"ab".isLetter()        # false
"123".isDigit()        # true
"-12.5".isNumber()     # true
"".isAlpha()           # false
"".isEmpty()           # true
```

#### Recortes por referência: `before`, `after`, `between`

Só para `str`, `list` e `tuple`. Procuram a **primeira** ocorrência e devolvem uma parte **nova** (do mesmo tipo do receptor), sem incluir a ocorrência:

| Operação | Devolve |
|---|---|
| `before(x)` | o que vem **antes** da primeira ocorrência de `x`. |
| `after(x)` | o que vem **depois** da primeira ocorrência de `x`. |
| `between(a, b)` | o que está entre a primeira ocorrência de `a` e a primeira ocorrência de `b` **depois dela**. |

Se `x` (ou `a`, ou o `b` depois de `a`) não existe, o resultado é `null`. Se a parte pedida é vazia, o resultado é a coleção ou o texto vazio (`""` ou `[]`), que não é `null`.

```tinypine
"chave=valor".before("=")           # "chave"
"chave=valor".after("=")            # "valor"
"<b>negrito</b>".between("<b>", "</b>")   # "negrito"
[1, 2, 3, 4].before(3)              # [1, 2]
[1, 2, 3, 4].after(4)               # []
"abc".before("z")                   # null
```

### Operações de transformação

Sobre `str` devolvem uma string nova. Sobre `list`/`dict`, as **modificadoras** alteram o receptor e devolvem `null`; as demais devolvem um objeto novo (convenção 2).

#### Caixa e espaços (`str`)

| Operação | Devolve |
|---|---|
| `upper()` | tudo em maiúsculas. |
| `lower()` | tudo em minúsculas. |
| `title()` | a primeira letra de cada palavra em maiúscula e o resto em minúscula; palavra é uma sequência de caracteres sem espaço em branco. |
| `trim(chars=...)` | sem os caracteres de `chars` (padrão: espaço em branco) no início **e** no fim. |
| `trimLeft(chars=...)` | sem eles só no início. |
| `trimRight(chars=...)` | sem eles só no fim. |

A conversão de caixa independe do idioma do sistema (regras invariantes do Unicode).

```tinypine
"  Olá Mundo  ".trim()               # "Olá Mundo"
"  Olá".trimLeft()                   # "Olá"
"xxolaxx".trim(chars="x")            # "ola"
"olá mundo".title()                  # "Olá Mundo"
"ABC".lower()                        # "abc"
```

#### Substituição: `replace`, `replaceAll`

`replace(antigo, novo)` troca a **primeira** ocorrência; `replaceAll(antigo, novo)` troca **todas**. Se não há ocorrência, nada muda (não é erro).

- `str`: `antigo` é um texto não vazio (vazio é `InvalidArgument PROBLEM`) e `novo` é um texto (pode ser vazio, o que remove). Devolve a nova string. As ocorrências de `replaceAll` não se sobrepõem e o texto colocado **não** é procurado de novo.
- `list`: troca elementos iguais (`==`) a `antigo` por `novo`. Modifica a lista.
- `dict`: troca **valores** iguais a `antigo` por `novo`; as chaves e a ordem não mudam. Modifica o dicionário.

```tinypine
"banana".replace("a", "o")          # "bonana"
"banana".replaceAll("a", "o")       # "bonono"
var L = [1, 2, 1]
L.replaceAll(1, 9)                  # L -> [9, 2, 9]
var D = {"a": 1, "b": 1}
D.replace(1, 5)                     # D -> {"a": 5, "b": 1}
```

#### Inversão: `reverse`

`reverse()` inverte a ordem: em `str`, os caracteres (devolve nova string); em `list`, os elementos (modifica); em `dict`, a **ordem das entradas**, mantendo cada chave com seu valor (modifica).

```tinypine
"abc".reverse()                     # "cba"
var L = [1, 2, 3]
L.reverse()                         # L -> [3, 2, 1]
```

#### Remoção: `remove`, `removeAll`, `removeFirst`, `removeLast`

| Forma | Efeito |
|---|---|
| `remove(valor)` | remove a **primeira** ocorrência de `valor` (comparada por `==`). Se não existe, nada muda (Capítulo 19.4). Em `str`, `valor` é um texto não vazio. |
| `remove(index=N)` | remove o elemento (ou a entrada, ou o caractere) na posição `N`, de `0` a `length - 1`; fora disso é `IndexOutOfBounds PROBLEM`. Dá o mesmo resultado que `A[N].del`. |
| `removeAll(valor)` | remove **todas** as ocorrências. Se não há, nada muda. |
| `removeFirst(n)` | remove os `n` **primeiros** elementos, entradas ou caracteres. `n` é opcional (padrão `1`). |
| `removeLast(n)` | remove os `n` **últimos**. |

`remove` recebe **ou** o valor **ou** `index`, nunca os dois (`TooManyArguments PROBLEM`) nem nenhum (`MissingArgument PROBLEM`). Em `removeFirst`/`removeLast`, `n` é um inteiro de `0` a `length`; maior que `length` (inclusive qualquer `n` positivo num receptor vazio) é `IndexOutOfBounds PROBLEM`, sem remover nada. Sobre `str` todas devolvem a nova string; sobre `list`/`dict` modificam o receptor.

```tinypine
var A = [1, 2, 3, 2, 1]
A.remove(2)                         # A -> [1, 3, 2, 1]
A.removeAll(1)                      # A -> [3, 2]
A.removeFirst()                     # A -> [2]
"banana".removeAll("a")             # "bnn"
"abcd".remove(index=1)              # "acd"
"abcd".removeLast(2)                # "ab"
```

#### Preenchimento: `padLeft`, `padRight`, `center` (`str`)

`padLeft(largura, fill=" ")` completa **à esquerda** até a string ter `largura` caracteres; `padRight`, à direita; `center`, dos dois lados (quando falta um número ímpar, o caractere a mais vai para a **direita**). Se a string já tem `largura` ou mais, ela volta igual. `largura` é um inteiro maior ou igual a `0`; `fill` tem exatamente 1 caractere (senão `InvalidArgument PROBLEM`).

```tinypine
"7".padLeft(3, fill="0")            # "007"
"ab".padRight(5, fill=".")          # "ab..."
"ab".center(5, fill="*")            # "*ab**"
```

#### Pontas e recortes: `left`, `right`, `substring`, `slice`

| Operação | Receptor | Devolve |
|---|---|---|
| `left(n)` | `str`, `list`, `dict`, `tuple` | os `n` primeiros caracteres, elementos ou entradas, como objeto novo do mesmo tipo. |
| `right(n)` | idem | os `n` últimos. |
| `substring(início, quantidade)` | `str` | `quantidade` caracteres a partir da posição `início`. |
| `slice(início, fim)` | `str`, `list`, `tuple` | o recorte de `início` a `fim`, **as duas pontas incluídas**: o mesmo que `A[início to fim]` (Capítulo 19.2.1), com as mesmas regras de limites negativos e de erro. |

`left`/`right`: `n` é um inteiro de `0` a `length`; maior que isso é `IndexOutOfBounds PROBLEM` (o recorte não é "aparado" em silêncio). `substring`: `início` de `0` a `length - 1` e `início + quantidade` até `length`, senão `IndexOutOfBounds PROBLEM`; sobre string vazia, só `substring(0, 0)` é válido. `dict` não tem `slice` (Capítulo 19.2.1).

```tinypine
"abcdef".left(2)                    # "ab"
"abcdef".right(2)                   # "ef"
"abcdef".substring(1, 3)            # "bcd"
"abcdef".slice(1, 3)                # "bcd"
[1, 2, 3, 4].slice(-2, -1)          # [3, 4]
{"a": 1, "b": 2, "c": 3}.left(2)    # {"a": 1, "b": 2}
```

### Operações de composição

#### `join`, `repeat`, `split`, `lines`, `words`

| Operação | Receptor | Devolve |
|---|---|---|
| `join(sep="")` | `list`, `tuple` | uma `str` com os elementos separados por `sep`. **Todos os elementos precisam ser `str`**: não há conversão implícita (Capítulo 9.2); um elemento de outro tipo é `TypeMismatch PROBLEM`. Lista vazia dá `""`. |
| `repeat(n)` | `str`, `list` | o receptor repetido `n` vezes, como objeto novo; é o mesmo que `receptor * n` (Capítulo 13). `n` é um `int` maior ou igual a `0`; senão `InvalidRepeatCount PROBLEM`. |
| `split(sep)` | `str` | uma `list` de `str` com os pedaços entre as ocorrências de `sep`. `sep` é um texto não vazio (senão `InvalidArgument PROBLEM`); sem ocorrência, a lista tem um só elemento (o texto inteiro). Ocorrências vizinhas produzem pedaços vazios. |
| `split(sep)` | `list` | uma `list` de listas: os pedaços entre os elementos iguais (`==`) a `sep`. |
| `lines()` | `str` | uma `list` de `str` com as linhas, separadas por `\n`, `\r\n` ou `\r`. Uma quebra no fim **não** cria uma última linha vazia; `""` dá `[]`. |
| `words()` | `str` | uma `list` de `str` com as palavras: sequências de caracteres sem espaço em branco, ignorando os espaços (`"  a  b "` dá `["a", "b"]`). |

Não confundir `split(sep)` (separa por um texto) com `/` (Capítulo 10.2), que parte um receptor em `n` pedaços **iguais**.

```tinypine
["a", "b", "c"].join("-")           # "a-b-c"
"ab".repeat(3)                      # "ababab"
"a,b,,c".split(",")                 # ["a", "b", "", "c"]
[1, 0, 2, 3, 0, 4].split(0)         # [[1], [2, 3], [4]]
"um\ndois\n".lines()                # ["um", "dois"]
"  olá   mundo ".words()            # ["olá", "mundo"]
```

### Diagnósticos

Todas as falhas usam diagnósticos já existentes, exceto os dois marcados como **novo**, que dependem da Decisão 4.

| Situação | Diagnóstico |
|---|---|
| Operação aplicada a um tipo que não a aceita; argumento de tipo errado (`index` não inteiro, `teste` que não é função, elemento não `str` em `join`) | `TypeMismatch PROBLEM` (E302) |
| Operação modificadora sobre `tuple` | `ImmutableMutation PROBLEM` (E312) |
| `index`, `start`, `end`, `n`, `largura` ou `quantidade` fora do intervalo permitido | `IndexOutOfBounds PROBLEM` (E402) |
| Argumento obrigatório ausente / posicional a mais / nome nomeado desconhecido | `MissingArgument` (E501) / `TooManyArguments` (E507) / `UnknownNamedArgument` (E503) |
| `repeat(n)` com `n` negativo ou não inteiro | `InvalidRepeatCount PROBLEM` (E306, já existente) |
| Texto de busca, `sep` ou `antigo` vazio; `fill` com mais ou menos de um caractere | `InvalidArgument PROBLEM` (**novo**) |
| `dict.add()` com chave já existente | `DuplicateKey PROBLEM` (**novo**) |

### Resumo do contrato

| Tipo | Modifica o receptor? | Retorno das modificadoras | Posições |
|---|---|---|---|
| `list` | só `add`, `remove*`, `replace*`, `reverse` | `null` | elementos, base 0 |
| `dict` | só `add`, `remove*`, `replace*`, `reverse` | `null` | entradas na ordem de iteração |
| `str` | nunca (imutável) | — (devolve nova `str`) | caracteres, base 0 |
| `tuple` | nunca | — | elementos, base 0 |

| Ação | Sem `index` | Com `index` |
|---|---|---|
| `add` em `list` | acrescenta ao final | antes da posição indicada |
| `add` em `dict` | acrescenta ao final da sequência | antes da posição indicada |
| `add` em `str` | acrescenta ao final do texto | antes do caractere indicado |
| `remove` | por valor | `remove(index=N)` remove a posição `N` |

### Decisões que devem ser confirmadas antes da publicação

> ***Nota de implementação:*** *enquanto as decisões abaixo não são confirmadas, a implementação de referência (Sys) adota a recomendação de cada uma delas, e é isso que este capítulo descreve. Os testes estão em* `Sys/tests/methods/`*.*

1. **Chaves duplicadas em `dict.add()`:** esta proposta recomenda erro, sem sobrescrita e sem inserção parcial.
2. **Indexação de strings:** confirmar a unidade de indexação usada pelo TinyPine — por exemplo, pontos de código Unicode ou outra unidade já adotada pelas operações de texto. O texto acima diz "a mesma do `.length`".
3. **Retorno das modificadoras:** esta proposta fixa `null` para toda operação que altera uma `list` ou `dict` no lugar (`add`, `remove*`, `replace*`, `reverse`). Alternativas: devolver a própria coleção (permite encadear: `A.add(1).reverse()`) ou `void`. Não há como obter o elemento removido com `removeFirst`/`removeLast` (leia-o antes, por índice).
4. **Diagnósticos:** esta proposta reaproveita `TypeMismatch`, `ImmutableMutation`, `IndexOutOfBounds` e os de chamada, e pede **dois códigos novos** — `InvalidArgument` (valor de argumento inválido, como texto vazio onde se exige texto não vazio ou `fill` que não tem um caractere) e `DuplicateKey` (chave repetida em `dict.add`) —, que precisam entrar nos Capítulos 36.7 e 37.
5. **`dict`: valor ou chave.** As operações de valor (`includes`, `indexOf`, `count`, `replace`, `remove`...) olham os **valores**, e as posições são posições de entrada. Para chaves ficam `in` e o acesso `D["chave"]`. Confirmar se alguma delas deve ter uma forma por chave.
6. **Rigor nos limites.** `left`, `right`, `removeFirst`, `removeLast`, `substring`, `start` e `end` fora do receptor são erro (nada é "aparado" em silêncio), coerente com `index` do `add`. A alternativa é devolver o que existe (`"abc".left(5)` dar `"abc"`).
7. **`find`/`findLast` com função** e não com valor (o valor já é `indexOf`/`includes`); `null` serve a "nenhum" e a "o elemento é `null`".
8. **`remove(index=N)`** é uma forma nova, simétrica ao `add(index=)`; equivale a `A[N].del`. Confirmar se fica ou se `.del` basta.
9. **Textos são literais.** Um padrão `format` não é aceito como texto de busca; o casamento por padrão continua só em `==`/`!=`/`~=`/`.match()`.
10. **`isNumber`, `isLetter`, `isAlpha`:** a diferença de `isLetter` (um caractere) para `isAlpha` (todos os caracteres) é uma escolha desta proposta, já que o catálogo lista as duas. `isDigit` aceita só `0`–`9`.
11. **`const` e as modificadoras.** O efeito de `const` sobre `add`/`remove` e semelhantes segue o Capítulo 18.2/19.4.2 e continua pendente (B36 do Apêndice A: o Capítulo 19.5 e o 19.4.2 divergem).
12. **`repeat` duplica o `*`?** `repeat(n)` e `receptor * n` são a mesma operação; manter as duas formas ou deixar só uma.
