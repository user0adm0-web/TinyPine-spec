## Coleções

A partir da 0.5, lista e dicionário são sempre delimitados de forma distinta e nunca ambígua: `[` e `]` sempre delimitam uma **lista** (valores soltos, acessados por posição); `{` e `}` sempre delimitam um **dicionário** (pares chave: valor). O delimitador do literal já determina o tipo da coleção — não há mais leitura dependente da forma dos elementos (Capítulo 19.1).

```tinypine
var lista = ["A", "B", "C"]
var dict = {"A": 10, "B": 20, "C": 30}
```

### Representação Interna

Uma coleção é lista se for delimitada por `[ ]` e dicionário se for delimitada por `{ }` — a decisão é feita exclusivamente pelo delimitador do literal, nunca pela forma dos elementos:

- **Lista (**`[ ]`**) — todo elemento é um valor solto, sem chave. O acesso é sempre por posição (índice), na ordem de inserção. Um par chave: valor dentro de** `[ ]` **é um erro de sintaxe.**

- **Dicionário (**`{ }`**) — todo elemento é um par chave: valor; a chave pode ser do tipo** `str` **ou de um tipo numérico (**`num, int, float, decim`**), inclusive misturados no mesmo dicionário. O acesso é por chave e, também, por posição (Capítulo 19.2). Um valor solto dentro de** `{ }` **é um erro de sintaxe.**

Usar a forma de conteúdo errada para o delimitador escolhido é um erro de sintaxe:

```tinypine
{"Nome", "Idade", "Ativo"}   # MixedCollectionLiteral PROBLEM
```

*Valores soltos dentro de { } — inválido*

Chaves numéricas agora são aceitas em dicionário — inclusive misturadas com chaves `str` no mesmo literal:

```tinypine
{1: "um", 2: "dois", "três": 3}
```

*Chaves numérica e str combinadas — válido a partir da 0.5*

Como o delimitador já determina se a coleção é lista ou dicionário, `colecao[N]` nunca é ambíguo quanto ao **tipo** da coleção. Dentro de um dicionário, porém, chaves numéricas tornam `colecao[N]` ambíguo entre busca por chave e acesso por posição — ambiguidade resolvida em favor da chave: em um dicionário, `colecao[N]` busca a chave `N`; a forma explícita `colecao[key N]` (19.2) faz essa mesma busca por chave, sem deixar dúvida de que `N` é uma chave.

Uma coleção vazia declarada como `[]` já é uma lista vazia; uma coleção vazia declarada como `{}` já é um dicionário vazio — nenhuma das duas representa `void`. `void` continua sendo um valor distinto (Capítulo 7.2), atribuído apenas quando o programador omite um valor onde um era esperado.

```tinypine
var listaVazia = []              # lista vazia
var dictVazio  = {}              # dicionário vazio
```

### Busca e Acesso a Elementos

| **Forma de acesso**               | **Sintaxe**         | **Comportamento**                                                                                                                                                                             |
|-----------------------------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Por chave (dicionário)            | `colecao["A"]`      | Retorna o valor associado à chave. Se a chave existir sem valor associado, ver 19.3(a). Se a chave não existir, ver 19.3(b).                                                                  |
| Por índice                        | `colecao[0]`        | Obtém o elemento na posição informada, respeitando a ordem de inserção. Em uma lista, retorna o valor armazenado nessa posição. Em um dicionário, retorna o valor do N-ésimo par chave:valor. |
| Por chave, explícito              | `colecao[key K]`    | Retorna o elemento de chave `K`. Em lista e tupla a chave de cada elemento é o seu índice (`A[key 0]` é o primeiro elemento); em dicionário é a chave do par. Chave inexistente: ver 19.3(b). |
| Por valor, explícito              | `colecao[value V]`  | Acesso pelo valor `V` (ver o exemplo abaixo; a semântica completa está em aberto — Apêndice A.2, B27).                                                                                       |

```tinypine
var dados = {"Nome": "Dhavi", "Idade": 20, "Ativo"}
dados[0]          # "Dhavi"
dados[1]          # 20
dados[2]          # void
dados["Nome"]     # "Dhavi"
dados[key "Nome"] # "Dhavi" — o mesmo que dados["Nome"]

var A = [1, 2, 3, 4]
print(A[key 0])   # 1
print(A[value 2]) # 2
print(A[0])       # 1
```

As formas explícitas `key K` e `value V` substituem as antigas `key, N` e `value, N` (e `key:N` / `value:N`), que deixam de existir. As mesmas formas, sem o nome da coleção, são usadas dentro da restrição de um tipo refinado (Capítulo 6.9).

A ordem dos elementos é sempre preservada exatamente conforme a inserção; o acesso por índice (`colecao[N]`) usa essa mesma ordem.

#### Fatia por Intervalo — \[a to b\]

`colecao[a to b]` devolve a fatia de uma lista ou de uma `str` que vai da posição `a` à posição `b`, **com as duas posições incluídas** — ao contrário do `[a:b]` do Python, o limite final não é excluído. Uma lista devolve uma lista; uma `str` devolve uma `str`.

- **Numeração.** As posições são as de `colecao[N]` (a primeira é 0). Um limite negativo conta a partir do fim, como em `lista[-1]` (Capítulo 36.3): `-1` é a última posição.

- **Limites inválidos.** Se `a` ou `b` estiver fora da coleção, ou se o início vier depois do fim (com os negativos já resolvidos), a execução é interrompida com `IndexOutOfBounds PROBLEM` — a fatia nunca é cortada nem invertida em silêncio.

- **Escrita e remoção.** `A[a to b] = valor` sobre uma `str` (Capítulo 18.4) usa exatamente a mesma regra de limites.

- **Dicionário.** Um dicionário não tem fatia: `dicionario[a to b]` é `TypeMismatch PROBLEM`. A única exceção é `~Program.line` (Capítulo 29.4).

- **Não confundir** com o literal de intervalo `[a to b]` (Capítulo 25.5), que constrói uma lista de inteiros e desce quando `a` é maior que `b`.

```tinypine
var A = [10, 20, 30, 40, 50]
A[1 to 3]       # [20, 30, 40] — as duas pontas entram
A[0 to 4]       # [10, 20, 30, 40, 50]
A[-3 to -1]     # [30, 40, 50] — os três últimos
A[0 to 5]       # IndexOutOfBounds PROBLEM — a lista tem as posições 0 a 4
A[3 to 1]       # IndexOutOfBounds PROBLEM — início depois do fim
var t = "abcdef"
t[1 to 3]       # "bcd"
```

#### Valor de Função e Acesso por Ponto

Um elemento de lista ou dicionário pode ser uma função (Capítulo 31): a coleção guarda a função, e ler o elemento a devolve **sem chamá-la**. Em dicionário, uma chave `str` que seja um identificador válido também pode ser lida com ponto: `D.chave` equivale a `D["chave"]`, inclusive quando a chave não existe — `KeyNotFound PROBLEM` (Capítulo 19.3). Sem parênteses, o ponto só lê a chave.

```tinypine
var D = {"dobro": f (x) do return x * 2 --}
var F = D["dobro"]     # lê a função; não a chama
var G = D.dobro        # o mesmo, com ponto
print(F(4), G(5))      # 810
```

**Chamada com ponto.** Com parênteses, `D.chave(...)` **chama** a função guardada na chave `"chave"`. É o que permite a um dicionário de funções servir de objeto leve, sem declarar uma classe (Capítulo 31.3):

```tinypine
var console = {"log": f(package ARGS)
  print(unpack ARGS)
}
console.log("Hello World!")     # Hello World!
```

As regras da chamada são as de qualquer função (Capítulo 30): parâmetros, `package`/`unpack`, valores de retorno e o escopo de criação da função anônima (ela enxerga as variáveis do lugar onde foi escrita, não as do lugar de onde é chamada). Casos particulares:

| **Caso**                                                     | **Resultado**                                                                                         |
|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| a chave não existe                                           | `KeyNotFound PROBLEM` (Capítulo 19.3)                                                                 |
| a chave existe, mas o valor não é uma função                 | `TypeMismatch PROBLEM`: o valor guardado não pode ser chamado                                         |
| a chave se chama `add` ou `remove`                           | vale o método da coleção (Capítulo 19.4); para chamar a função, leia-a antes: `var F = D["add"]`      |

A chamada com ponto vale para dicionário. Em lista, e na forma `D["chave"](...)` (índice seguido de parênteses), a função ainda precisa ser lida para uma variável antes de ser chamada (Apêndice A, B26).

### Chave Inexistente versus Valor void

O acesso por chave (19.2) distingue dois cenários:

**(a) Chave existente, sem valor associado** — o valor é `void` por definição (19.1). O acesso retorna `void`, com aviso `ValueIsVoid WARNING`.

**(b) Chave verdadeiramente ausente da coleção** — o acesso interrompe a execução com `KeyNotFound PROBLEM`, em coerência com o princípio geral de que nenhum erro é silencioso (Capítulo 36) e com o padrão já adotado para índices de coleção fora do intervalo (`IndexOutOfBounds PROBLEM`, Capítulo 36.3).

### Edição e Adição de Elementos

Coleções mutáveis (lista e dicionário) expõem dois métodos nativos: `add()` e `remove()`. Tuplas são imutáveis e não aceitam nenhum dos dois (Capítulo 19.5).

`colecao.add(valor)` — insere valor no final da coleção:

```tinypine
var A = ["x", "y"]
A.add("z")
print(A)
# → ["x", "y", "z"]
```

Para inserir em uma posição específica em vez de no final, utilizasse o parâmetro “position” e uma lista

```tinypine
var A = ["x", "y", "z"]
A.add("w", "position": ["before", 0])    # insere antes do índice 0
print(A)          # → ["w", "x", "y", "z"]
 
A.add("!", "position": ["after": 1])    # insere depois do índice 1 (empurra o resto)
print(A)          # → ["w", "x", "!", "y", "z"]
```

`colecao.remove(valor)` — remove a primeira ocorrência de valor na coleção (comparada por `==`, Capítulo 11.1). Se o valor não existir, a coleção permanece inalterada:

```tinypine
var A = ["x", "y", "z", "y"]
A.remove("y")
print(A)
# → ["x", "z", "y"] — só a primeira ocorrência sai
```

`remove()` já era usado em `str` (Capítulo 18.4, ex. `A.remove(A[1])`) — o comportamento em coleções segue o mesmo princípio, generalizado para lista e dicionário (removendo por valor; em dicionário, remove o primeiro par cujo valor bate).

#### Desempacote de dicts ou lists

` `o `unpack desempacota uma lista ou um dicionario retornando seus valores fora de uma estrutura`

```tinypine
var A = [1, 2, 3]

println(unpack A)

# saída: 123

var B = {"sep": "-", "last": "\n", "Hello World!"}

print(unpack B)
# saída: H-e-l-l-o- -W-o-r-l-d-!
```

`unpack` também é aceito dentro de um literal de lista, onde espalha os elementos de uma lista no lugar: `[unpack A, 4]` equivale a escrever os elementos de `A` seguidos de `4`. Fora de uma lista de argumentos de chamada e de um literal de lista, `unpack X` é `ParserError PROBLEM`. O desempacote de um dicionário dentro de um literal de lista não está definido (Apêndice A.2, B22).

```tinypine
var A = [1, 2, 3]
println([unpack A, 4])       # [1, 2, 3, 4]
println([0, unpack A, 9])    # [0, 1, 2, 3, 9]
```

#### Atribuição por Índice/Chave — Edição de Elemento Existente

`colecao[chave] = valor` e `colecao[índice] = valor` editam o valor associado a uma chave (`dict`) ou a um elemento já existente (`list`), sem criar uma entrada nova — criar uma entrada nova continua sendo função exclusiva de `.add()` (acima). Se a chave ou o índice não existir na coleção, a atribuição interrompe a execução com erro.

```tinypine
var A = {"x": 1}
A["x"] = 2        # válido — edita a chave já existente
A["y"] = 5        # KeyNotFound PROBLEM — chave "y" não existe (use .add() para criar)
var L = [1, 2, 3]
L[0] = 10         # válido — edita o índice já existente
L[5] = 10         # IndexOutOfBounds PROBLEM — índice 5 não existe
```

Essa regra se combina com var/const (Cap. 18.2) da mesma forma que a mutação por `.add()`/`.remove()`: `const` permite editar uma chave/índice já existente, mas não permite reatribuir o identificador:

```tinypine
const A = {"x": 1}
A["x"] = 2        # válido — const permite mutação de conteúdo
A = {"x": 3}      # ConstReassignment PROBLEM — const não permite reatribuição do identificador
```

### tuple — Coleções Imutáveis

`tuple()` é uma função nativa que converte um literal de coleção, uma variável de coleção existente ou uma string em uma **tupla** — um valor imutável por natureza, que nunca aceita `.add()` nem `.remove()`, com ou sem `const`. Separadamente, `const` controla a reatribuição do **identificador** e, a partir da 0.5, também a mutação do conteúdo — mesmo quando esse conteúdo não é uma tupla:

```tinypine
var A = ["A", "B"]
A.add("C")              # OK — var permite mutação de conteúdo
A = ["X", "Y"]          # OK — var permite reatribuição do identificador
const B = ["A", "B"]
B.add("C")              # ImmutableMutation PROBLEM — const não permite mutação de conteúdo
B = ["X", "Y"]          # ConstReassignment PROBLEM — const não permite reatribuição do identificador
var T = tuple(["A", "B"])
T.add("C")              # ImmutableMutation PROBLEM — tupla nunca aceita mutação de conteúdo
T = tuple(["X", "Y"])   # OK — var permite reatribuir o identificador
```

Uma tupla pode ser criada a partir de um literal de coleção, de uma string ou de uma variável já existente:

```tinypine
tuple(["x", "y", "z"])   # tupla literal
```

#### Por que não usar () para tuplas, como em Python?

Porque `()` já cumpre um papel central na linguagem: agrupar expressões. Se `()` também criasse tuplas, o interpretador precisaria adivinhar pelo contexto qual dos dois papéis se aplica em cada ocorrência — o que complicaria o analisador sintático e tornaria o código ambíguo para quem lê.

```tinypine
var A = A and not (C and B)
# aqui "()" agrupa uma expressão — não é uma tupla
```

Por isso, `tuple()` é tratado como uma função nativa de conversão, distinta do agrupamento por `()` — assim como qualquer outra chamada de função, ela recebe seu argumento entre parênteses, sem introduzir nenhum papel novo para `()`.

#### Conversão entre Tuplas e Coleções

```tinypine
var lista = [1, 2, 3]
var t = tuple(lista)
var l = [t]
```

Tuplas são imutáveis após a criação: uma vez criadas, não aceitam inserção nem edição. Internamente, o interpretador pode usar uma estrutura de dados semelhante à de uma coleção comum, mas `tuple`() é tratado como uma função de conversão distinta — o que reserva espaço para otimizações futuras (por exemplo, integração com *hashing* e com a estrutura `case`/`match`, Capítulo 25) sem quebra de compatibilidade.

```tinypine
var A = tuple([1, 2, 3])
A.type   # → tuple
 
var B = [1, 2, 3]
B.type   # → list
```
