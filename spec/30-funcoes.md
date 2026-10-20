# PARTE VII — FUNÇÕES, CLASSES E MÓDULOS

## Funções

Funções são declaradas com a palavra-chave `f`. Todo bloco de função segue o padrão geral de blocos por indentação, descrito no Capítulo 4.

```tinypine
f Ola()
  print("Olá")
```

*^- Sem parâmetros*

```tinypine
f soma(a, b)
  var sum = a + b
  return sum;
```

*^- Com parâmetros e retorno*

A lista de parâmetros distingue parâmetros posicionais, o marcador `?` com os parâmetros tipados que vêm depois dele, o marcador `!` com os parâmetros exclusivamente nomeados que vêm depois dele, parâmetros nomeados opcionais e o parâmetro variádico com `package`, além do valor padrão (`=`), aplicável a parâmetros posicionais, tipados e nomeados. Categorias e declaração: Capítulo 30.3; tipo de retorno: 30.4; parâmetros tipados (`?`): 30.4.1; valores padrão: 30.5; variádico: 30.6; gramática formal: 30.7; resolução de argumentos: 30.8; erros: 30.9.

### Funções Imutáveis — f const

O prefixo `const` aplicado a uma função impede que ela seja reatribuída ou redeclarada depois de criada — útil para travar comportamentos centrais do programa contra sobrescrita acidental ou intencional.

```tinypine
f const A()
  print("BLZ")
```

### Retorno Implícito

Uma função que chega ao fim de sua execução sem um `return` explícito retorna `Null` automaticamente. Isso evita repetir `return Null` em funções que existem apenas pelo efeito colateral (como imprimir algo).

```tinypine
f mensagem()
  print("Olá")
# equivale a
f mensagem()
  print("Olá")
  return Null;
```

> ***Nota:** o interpretador **não** transforma a última expressão de uma função nomeada em valor de retorno — ao contrário do que ocorre, por exemplo, em Ruby. Sem* `return` *explícito, o valor devolvido é sempre* `Null`*, mesmo que a última linha do corpo calcule um valor. Esta regra é comum a funções nomeadas e a funções anônimas (Capítulo 31.1).*
>
> ***Nota:** essa regra de retorno implícito (*`Null`*) só se aplica quando a função não declara um tipo de retorno. Quando* `: tipo` *é declarado (Cap. 30.4), chegar ao fim da execução sem um* `return` *compatível é erro de verificação estática, e não gera mais* `Null` *silenciosamente.*

```tinypine
f teste()
  5 + 5
# resultado: Null — o valor de "5 + 5" é calculado e descartado, NÃO se torna o retorno
```

### Parâmetros — Categorias e Declaração

Os parâmetros de uma função pertencem a categorias distintas, cada uma com sintaxe de declaração própria. As categorias não são intercambiáveis: cada uma define como o argumento correspondente pode — ou deve — ser fornecido na chamada.

| **Categoria**     | **Declaração**                       | **Fornecimento na chamada**                                                                  | **Argumento não fornecido**                                                                                                                                                      |
|-------------------|--------------------------------------|----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Posicional        | `qualquervar`                        | Somente por posição. A passagem por nome é inválida.                                         | `MissingArgument PROBLEM`, salvo se houver valor padrão (30.5).                                                                                                                  |
| Marcador `?`      | `?`                                  | Não é parâmetro: não recebe argumento. Inicia a seção de parâmetros tipados (30.4.1).        | —                                                                                                                                                                                |
| Tipado            | `?, e: int` (depois do marcador)     | Sem nome e sem posição própria: o argumento é ligado pelo seu tipo (30.4.1).                 | `MissingArgument PROBLEM`, salvo se houver valor padrão (30.5).                                                                                                                  |
| Marcador `!`      | `!`                                  | Não é parâmetro: não recebe argumento. Inicia a seção de parâmetros exclusivamente nomeados. | —                                                                                                                                                                                |
| Nomeado exclusivo | `!, "A": e` (depois do marcador)     | Somente por nome (`"A": 10`). A passagem por posição é inválida.                             | `MissingNamedArgument PROBLEM`, salvo se houver valor padrão (30.5).                                                                                                             |
| Nomeado opcional  | `"A": variavel` (sem `!` antes dele) | Por nome (`"A": 10`) ou por posição (`10`).                                                  | Valor padrão, se declarado (30.5); caso contrário, gera void (com ImplicitVoid WARNING) se o parâmetro for dinâmico, ou erro de verificação estática se violar o tipo declarado. |
| Variádico         | `package args`                       | Recebe os argumentos posicionais restantes (30.6).                                           | `args` é a lista/dict vazia(o) `[]/{}`.                                                                                                                                          |

**Parâmetro posicional.** A forma normal de declaração. O parâmetro é identificado apenas por sua posição na lista e só pode ser fornecido por posição:

```tinypine
f GJ(e)
  print(e)

GJ(10)         # e = 10
GJ("e": 10)    # NamedForPositionalOnly PROBLEM
```

Um parâmetro posicional **sem** valor padrão é obrigatório: omitir o argumento é `MissingArgument PROBLEM`. Para torná-lo opcional, declare um valor padrão (Capítulo 30.5); a anotação de tipo não o torna opcional.

```tinypine
f A(e, tempo)
  print(e)
A(2)            # MissingArgument PROBLEM — falta o argumento de tempo
f B(e, tempo = 0)
B(2)            # tempo = 0
f C(e, tempo: float)
C(2)            # MissingArgument PROBLEM
C(2, 0.5)       # ok
```

**Parâmetro nomeado opcional.** Um parâmetro pode declarar um identificador externo, usado como nome na chamada, escrito entre aspas antes do identificador interno. Sem `!` antes dele, o parâmetro nomeado é opcional e pode ser fornecido tanto por nome quanto por posição:

```tinypine
f GH("A": e)
  print(e)

GH(10)          # e = 10 — por posição
GH("A": 10)     # e = 10 — por nome
GH()            # e = void, com ImplicitVoid WARNING (Capítulo 7.2)
```

O nome externo (`"A"` acima) é usado na chamada; o identificador interno (`e`) é o nome da variável dentro do corpo da função. Os dois são independentes: o nome externo é um literal — string ou numérico — e não precisa ter relação com o identificador interno. Essa forma é distinta de `nome:valor` sem aspas (Cap. 20.1), reservado a `print`, `println` e `readln`.

```tinypine
f c("name": e): int
  print(format "seu nome é \"{e}\"")
  return 0

c("name": "Dhavi")
```

**Forma alternativa de chamada —** `nome=valor`**.** Quando o nome externo de um parâmetro nomeado é uma string que forma um identificador válido (Capítulo 3.4), o argumento também pode ser escrito `nome=valor`, sem aspas. As duas formas ligam o mesmo parâmetro e são equivalentes:

```tinypine
f A("Nome": e)
  ...

A("Nome": 10)   # forma padrão — vale para nome externo string ou numérico
A(Nome=10)       # segunda forma — só para nome externo string
```

> **1.** O nome externo numérico (`1: e`) ou string que não é identificador válido (`"meu nome": e`) só pode ser fornecido pela forma padrão; `meu=10` sem nome externo correspondente é `UnknownNamedArgument PROBLEM`, como qualquer nome desconhecido.
>
> **2.** A forma `=` vale para parâmetros nomeados opcionais e obrigatórios (depois de `!`), em funções de usuário e em módulos, e também em `print`, `println` e `readln` (Capítulos 20.1 e 21.1).
>
> **3.** Dentro de uma lista de argumentos, `IDENT = expr` é sempre argumento nomeado, nunca atribuição (Capítulo 14); `==` não é afetado. Em declaração, `=` continua separando o parâmetro do valor padrão (30.5).
>
> **4.** A ligação segue as fases e os erros do Capítulo 30.8 como se o argumento tivesse sido escrito `"nome": valor`: `A(e=10)` com `e` posicional é `NamedForPositionalOnly PROBLEM`, e `A("Nome": 1, Nome=2)` é `DuplicateArgument PROBLEM`.

**Marcador ! e parâmetros exclusivamente nomeados.** O símbolo `!` é um marcador sintático da declaração: inicia a seção de parâmetros exclusivamente nomeados. `!` não é um parâmetro — não é identificador, argumento nem variável, não recebe valor e não pode ser referenciado no corpo. Todo parâmetro escrito depois de `!` só pode ser fornecido por nome, nunca por posição. Sem valor padrão ele é obrigatório: a ausência do argumento é `MissingNamedArgument PROBLEM`. Com `= valor` (30.5) ele continua exclusivamente nomeado, mas passa a ser opcional:

```tinypine
f GG(!, "A": e)
  print(e)

GG("A": 10)     # e = 10
GG()            # MissingNamedArgument PROBLEM
GG(10)          # PositionalForNamedOnly PROBLEM
```

Com `= valor`, o parâmetro depois de `!` continua exclusivamente nomeado, mas deixa de ser obrigatório:

```tinypine
f GP(!, "A": e = 5, "B": k)
  print(e, k)

GP("B": 1)      # e = 5, k = 1 — "A" tem valor padrão
GP()            # MissingNamedArgument PROBLEM — "B" é obrigatório
GP(1, "B": 1)   # PositionalForNamedOnly PROBLEM — nunca por posição
```

**Ordem das categorias na assinatura.** Uma assinatura é lida da esquerda para a direita e tem, no máximo, três seções, nesta ordem: a dos posicionais, a dos tipados (depois de ?) e a dos exclusivamente nomeados (depois de !). Cada marcador aparece no máximo uma vez:

> **1.** a seção anterior aos marcadores ? e ! — ou a assinatura inteira, se não houver marcador — contém parâmetros posicionais, parâmetros nomeados opcionais e, no máximo, um parâmetro variádico (`package`). Os nomeados não estão sujeitos às regras de ordenação dos posicionais e do variádico: podem ser declarados em qualquer posição, antes ou depois de `package`. O `package`, por sua vez, só precisa vir depois de todos os parâmetros posicionais (30.6);
>
> **2.** a seção posterior a `?` (opcional) contém exclusivamente parâmetros tipados (30.4.1): sem nome externo, cada um com um tipo declarado e todos de tipos distintos, e sem `package`;
>
> **3.** a seção posterior a `!` (opcional) contém exclusivamente parâmetros nomeados, obrigatórios ou com valor padrão: nenhum parâmetro posicional, nenhum tipado e nenhum `package` pode aparecer nela;
>
> **4.** `?` e `!` aparecem no máximo uma vez, `?` vem antes de `!`, e cada marcador deve ser seguido de ao menos um parâmetro. `?` e `package` não coexistem na mesma assinatura.

```tinypine
f exemplo(a, b, !, "A": c, "B": d)
  ...
# a, b: posicionais · "A": c, "B": d: exclusivamente nomeados e obrigatórios

f combinado(a, "B": b, package resto, !, "C": c)
  ...
  # a: posicional · "B": b: nomeado opcional
# package resto: variádico · "C": c: exclusivamente nomeado e obrigatório
```

Com `?`, os parâmetros tipados ficam entre os posicionais e a seção `!` (30.4.1):

```tinypine
f tipado(a, ?, e: int, u: str, !, "N": n)
  ...

# a: posicional · e, u: tipados · "N": n: exclusivamente nomeado
```

**Parâmetros nomeados e a ordem de declaração.** Parâmetros nomeados — opcionais ou obrigatórios — não estão sujeitos às regras de ordenação dos parâmetros posicionais e do variádico: podem ser declarados antes ou depois de `package`, e a presença deles não invalida a declaração. A restrição de posição de `package` vale apenas em relação aos parâmetros posicionais (30.6), e a ordem de declaração dos nomeados não altera a categoria de nenhum deles. Esta regra trata só da declaração; a ligação dos argumentos continua a do Capítulo 30.8.

```tinypine
f saida("sep": SEP = "", package ARGS)    # válido: nomeado antes de package
f saida(package ARGS, "sep": SEP = "")    # válido: nomeado depois de package
f saida(package ARGS, "A": e)             # válido: nomeado opcional sem padrão
f saida(a, package ARGS, !, "C": c)       # válido: package, e depois ! com o exclusivamente nomeado
f saida(package ARGS, !, "sep": SEP = "", "last": END = "")   # válido: package, e depois ! com nomeados que têm valor padrão
f saida(package ARGS, b)                  # InvalidVariadicParam PROBLEM — posicional depois de package
f saida("args": package ARGS)             # InvalidVariadicParam PROBLEM — package não tem nome externo
f saida(package ARGS = 0)                 # InvalidVariadicParam PROBLEM — package não tem valor padrão
f saida(!, "C": c, package ARGS)          # InvalidVariadicParam PROBLEM — package dentro da seção !
```

Na chamada, a posição textual de um argumento nomeado na lista de argumentos não afeta a ligação dos argumentos posicionais — que são numerados apenas entre si, na ordem em que aparecem — e a ordem entre argumentos nomeados não é semanticamente relevante, mesmo mecanismo já usado por `sep`/`last`/`flush` em `print` (Cap. 20.1):

```tinypine
f c(a, "name": e): int
  ...

c(1, "name": "Dhavi")
c("name": "Dhavi", 1)   # equivalente
```

### Tipo de Retorno Declarado — : tipo

Após a assinatura da função, `: tipo` declara o tipo de retorno esperado — opcional, como toda anotação de tipo na linguagem (Cap. 5):

```tinypine
f c("name": e): int
  print(format "seu nome é \"{e}\"")
  return 0
```

Quando o tipo de retorno é declarado, cada `return` que produz valor é verificado estaticamente contra esse tipo (Cap. 35, Análise Estática de Tipos); um valor incompatível é erro de verificação estática:

```tinypine
f c(): int
  return 10        # válido
  return "abc"      # StaticTypeMismatch PROBLEM
```

Chegar ao fim da execução sem um `return` compatível com o tipo declarado também é erro de verificação estática — nesse caso, a regra de retorno implícito `Null` (Cap. 30.2) não se aplica.

Quando o tipo de retorno não é declarado, não há restrição estática sobre o valor retornado: a função pode retornar valores de tipos diferentes em `return`s diferentes, seguindo o mesmo princípio de uma variável sem tipo declarado (Cap. 5) — nesse caso, a regra de retorno implícito `Null` (Cap. 30.2) permanece válida normalmente.

#### Parâmetros Tipados — o Marcador ?

O marcador `?` inicia uma seção de parâmetros **tipados**: parâmetros sem nome externo e sem posição própria, que o TinyPine liga ao argumento pelo **tipo** declarado. Com isso a ordem em que esses argumentos são escritos na chamada deixa de importar, desde que os tipos sejam diferentes:

```tinypine
f a(?, e: int, a: str)
  print(e, a)
  return [e, a]

a("teste", 9)   # e = 9, a = "teste"
a(9, "teste")   # o mesmo resultado
```

Regras:

- `?` não é parâmetro, como `!`: não recebe argumento nem pode ser referenciado no corpo. Os parâmetros depois dele formam a seção tipada, que vai até o fim da lista ou até o marcador `!`.

- Todo parâmetro tipado declara o seu tipo (`e: int`), e **cada tipo aparece uma só vez** na seção: o tipo é a única chave de ligação. Tipo ausente ou repetido é `InvalidQuestionMarker PROBLEM`.

- Na chamada, os argumentos posicionais que sobram depois dos posicionais comuns são ligados aos parâmetros tipados: cada um vai para o primeiro parâmetro tipado ainda livre, na ordem de declaração, que aceita o tipo do argumento. Argumento que não casa com nenhum parâmetro tipado restante é `TypeMismatch PROBLEM`; parâmetro tipado que fica sem argumento e sem valor padrão é `MissingArgument PROBLEM`; argumento a mais, depois de todos os tipados ligados, é `TooManyArguments PROBLEM`.

- Um parâmetro tipado aceita valor padrão (`n: int = 3`); sem argumento, recebe o padrão (30.5).

- Ordem permitida: `posicionais [ ? tipados ] [ ! nomeados ]`. `?` aparece no máximo uma vez, não vem depois de `!` e não coexiste com `package`: `package` antes de `?` é `InvalidVariadicParam PROBLEM`, e depois de `?` é `InvalidQuestionMarker PROBLEM`. `?` sem nenhum parâmetro depois dele também é `InvalidQuestionMarker PROBLEM`.

- A análise estática compara a quantidade de argumentos que sobram com a de parâmetros tipados sem valor padrão (Capítulo 35).

A seção tipada convive com a seção `!`: os nomeados continuam sendo passados por nome, em qualquer posição da lista de argumentos, e não interferem na ligação pelo tipo:

```tinypine
f TESTE(?, e: str, u: int, !, "nome": T)
  print(e, u, T)

TESTE(7, "oi", "nome": 1)    # e = "oi", u = 7, T = 1
TESTE("nome": 1, "oi", 7)    # equivalente
```

Os itens acima que não constavam da especificação original (não coexistir com `package`, no máximo uma seção, só antes de `!`, tipo único por parâmetro) foram fixados pelo interpretador de referência; a escolha entre tipos que se sobrepõem — um `int` pode ligar a um parâmetro `float`, com ImplicitNumericConversion WARNING, se ele vier antes de um `int` livre — também está em aberto (Apêndice A.2, B24).

### Valores Padrão — =

Um parâmetro posicional ou nomeado opcional pode declarar um valor padrão com `=`, escrito depois do identificador interno. O valor padrão é utilizado somente quando o argumento correspondente não é fornecido na chamada; quando o argumento é fornecido, o valor padrão é ignorado.

**Parâmetro posicional com valor padrão:**

```tinypine
f X(e = 0)
  print(e)

X()        # e = 0
X(10)      # e = 10
```

**Parâmetro nomeado com valor padrão** — o nome externo continua sendo o literal entre aspas; o identificador interno vem antes de `=`:

```tinypine
f XC("a": e = null)
  print(e)

XC()            # e = null
XC("a": 10)     # e = 10
```

Regras:

- Parâmetro nomeado opcional **sem** valor padrão, quando nenhum argumento é fornecido, recebe `void`, com ImplicitVoid WARNING (Capítulo 7.2). Com valor padrão, recebe esse valor, sem aviso.

- Parâmetro posicional sem valor padrão é de presença obrigatória: a ausência do argumento é `MissingArgument PROBLEM`.

- Parâmetro nomeado depois de `!` admite valor padrão: continua exclusivamente nomeado (nunca recebe posição), mas deixa de ser obrigatório — sem argumento, recebe o padrão, sem aviso. Sem padrão, a ausência é `MissingNamedArgument PROBLEM`.

- Parâmetro tipado (depois de `?`, Capítulo 30.4.1) também admite valor padrão; sem padrão, a ausência do argumento é `MissingArgument PROBLEM`.

- Não existe forma abreviada para argumentos nomeados: um literal sem `:` na chamada nunca é lido como "o nome sem valor", e sim como argumento posicional.

```tinypine
XC("a")         # e = "a" — "a" é literal posicional
```

### Parâmetros Variádicos — package args

O prefixo `package` na declaração de um parâmetro o torna variádico: ele captura, em uma única coleção, a quantidade variável de argumentos posicionais que sobrarem na chamada.

```tinypine
f fun(package args)
  print(args)

fun("arroz", "açucar", "melhor", "eficiência")
# args = ["arroz", "açucar", "melhor", "eficiência"]
```

O `package` tem função especial apenas na **declaração**: depois que a captura foi declarada, o parâmetro é usado pelo identificador, sem o prefixo — `package` não faz parte do nome da variável

**Combinação com parâmetros normais.** A captura variádica pode aparecer depois de parâmetros posicionais: os parâmetros normais consomem os argumentos correspondentes e `package args` captura os restantes.

```tinypine
f fun(a, package args)
  print(a)
  print(args)

fun("arroz", "açucar", "melhor", "eficiência")
# a    = "arroz"
# args = ["açucar", "melhor", "eficiência"]
```

Regras:

- `args` é uma lista (Capítulo 19.1) com os argumentos capturados, na ordem em que foram passados. Se não sobrar nenhum argumento, `args` é a lista vazia `[]`.

- **Posição de** `package args`**:** `package args` é o último entre os parâmetros posicionais: nenhum parâmetro posicional pode ser declarado depois dele, e só pode haver um `package` por assinatura. Parâmetros nomeados — opcionais ou obrigatórios — não contam para essa regra e podem ser declarados antes ou depois dele (Capítulo 30.3). Como `package args` não é parâmetro nomeado, também não pode aparecer na seção posterior a ! — mas pode vir antes dela: `f out(package ARGS, !, "sep": SEP = "")` — nem coexistir com o marcador `?` (30.4.1).

- `package args` captura somente argumentos posicionais; argumentos nomeados nunca são capturados por ele. `package args` não tem nome externo nem valor padrão.

- `package` é palavra reservada, como `load` e `as` (Capítulo 29.5): não pode ser usada como identificador de variável ou função.

- Declarações que violam essas regras são `InvalidVariadicParam PROBLEM` (Capítulo 30.9).

**package declara, unpack espalha.** `package` só existe na declaração: depois dele, o parâmetro é usado pelo identificador (`args`). `unpack` é o operador que **espalha** uma lista como argumentos separados (Capítulo 19.4.1), em chamadas e dentro de literais de lista. Os dois se complementam; repare que passar uma lista inteira a um parâmetro variádico a embrulha em mais um nível:

```tinypine
var A = [1, 2, 3]
f pack(package args)
  return [unpack args]       # espalha o que package capturou
pack(A)                     # [[1, 2, 3]] — A é UM argumento: args = [[1, 2, 3]]
pack(unpack A)              # [1, 2, 3]   — unpack A vira três argumentos: args = [1, 2, 3]
print(unpack A)             # 123 — print recebe 1, 2 e 3 como argumentos separados, sem separador
```

**Repassar argumentos.** `package` e `unpack` juntos formam o padrão de repasse: a função variádica recebe os argumentos em `args` e os entrega, um a um, a outra chamada. O exemplo imprime o que receber, sem separador — é a base de um objeto "console" guardado em um dicionário (Capítulo 31.3):

```tinypine
f repassar(package ARGS)
  print(unpack ARGS)
repassar(1, 2, 3)       # 123
repassar(2 ** 6)        # 64
```

### Gramática Formal de Parâmetros

Notação EBNF: terminais entre aspas; `|` separa alternativas; `[ ... ]` é opcional; `{ ... }` repete zero ou mais vezes. `IDENT` é um identificador (Capítulo 3.4), `STRING` e `NUMBER` são literais, `Expr` é uma expressão e `Type` é um tipo (Capítulos 5, 6.8 e 6.9); dentro da gramática, `"|"` entre aspas é o operador de união de tipos (Capítulo 6.8.1), não o separador de alternativas. Esta gramática complementa a estrutura de blocos do Capítulo 4.

<!-- include: gramatica.ebnf -->

Observações que tornam a gramática não ambígua para um parser:

- **Categoria pelo primeiro token.** Dentro de `PosSection`, um parâmetro iniciado por `IDENT` é posicional; iniciado por `STRING` ou `NUMBER`, é nomeado opcional; iniciado por `package`, é variádico. Depois de ?, todo parâmetro é iniciado por IDENT e é tipado. Depois de !, todo parâmetro é iniciado por STRING ou NUMBER e é exclusivamente nomeado.

- `!` **é terminal próprio** (`BangMarker`): não gera parâmetro, não liga identificador algum e só é válido como primeiro elemento de NamedSection.

- **? é terminal próprio** (QuestionMarker): não gera parâmetro, não liga identificador algum e só é válido como primeiro elemento de TypedSection. Todo TypedParam tem Type e nenhum ExtName; os tipos de uma TypedSection são distintos entre si, e TypedSection não coexiste com VariadicParam. Violações são InvalidQuestionMarker PROBLEM (ou InvalidVariadicParam PROBLEM, se `package` vem antes de `?`), verificadas na análise da declaração.

- **NamedParam pode ter Default.** Com `= valor`, o parâmetro exclusivamente nomeado é opcional; sem ele, é obrigatório. NamedSection só pode ser a última seção da lista.

- **VariadicParam** ocorre no máximo uma vez em PosSection, sem ExtName e sem Default, e depois de todo PositionalParam. OptNamedParam pode ser declarado antes ou depois dele: a regra de posição vale só entre posicionais e variádico (30.3). Violações são InvalidVariadicParam PROBLEM, verificadas na análise da declaração, não pela gramática.

- `:` **em** `ParamId` introduz a anotação de tipo (Capítulos 5 e 6.8); em OptNamedParam/NamedParam, o primeiro `:` (logo após `ExtName`) separa o nome externo do identificador interno.

- `:` **em** `NamedArg`**.** Em argumento de chamada, se o token após `:` for um nome de tipo (os tipos primitivos, mais `function`, Capítulo 6) ou uma palavra `to-*` (Capítulos 5 e 8), o `:` é o operador de asserção/conversão aplicado a um `PositionalArg`; caso contrário, é o separador de `NamedArg`.

- **= em NamedArg.** Em argumento de chamada, `IDENT = expr` é sempre argumento nomeado (nunca atribuição) e só liga a parâmetro cujo nome externo é uma string igual a IDENT (Capítulo 30.3).

- `=` **em** `Default` não é atribuição (Capítulo 14).

### Resolução de Argumentos em Chamadas

Dada uma chamada, a ligação entre argumentos e parâmetros é determinística e ocorre em quatro fases, sempre nesta ordem, antes da execução do corpo da função. Uma violação interrompe a chamada com o erro indicado (Capítulo 30.9); havendo mais de uma, é reportada a da primeira fase em que ocorre e, dentro dela, a do argumento mais à esquerda.

> **1. Classificação.** Cada argumento é classificado apenas por sua forma: é **nomeado** se escrito `literal: expr` (literal str ou numérico antes de `:`) ou `IDENT = expr` (forma alternativa, Capítulo 30.3), e **posicional** se for apenas uma expressão. Não há forma abreviada: um literal sem `:` é sempre posicional.
>
> **2. Ligação dos posicionais.** A sequência posicional da função é formada pelos parâmetros posicionais e pelos nomeados opcionais, na ordem de declaração, e, por último, pelo variádico, quando existe — onde quer que `package` tenha sido declarado; parâmetros depois de ! (exclusivamente nomeados) nunca fazem parte dela. O k-ésimo argumento posicional liga-se ao k-ésimo parâmetro da sequência. Se a assinatura tem seção ?, os argumentos que sobram são ligados pelo tipo aos parâmetros tipados, em vez de capturados (Capítulo 30.4.1). Os argumentos posicionais que sobram são capturados por `package args`, se declarado; sem `package args`, sobram como `PositionalForNamedOnly PROBLEM`, se a assinatura tem seção `!`, ou `TooManyArguments PROBLEM`, se não tem.
>
> **3. Ligação dos nomeados.** Cada argumento nomeado liga-se ao parâmetro nomeado (opcional ou exclusivamente nomeado) de mesmo nome externo, por igualdade literal exata (maiúsculas e minúsculas contam). Se nenhum parâmetro tem esse nome externo: se o nome coincide com o identificador interno de um parâmetro posicional, é `NamedForPositionalOnly PROBLEM`; caso contrário, `UnknownNamedArgument PROBLEM`. Se o parâmetro já estiver ligado — por posição na fase 2 ou por outro argumento de mesmo nome — é `DuplicateArgument PROBLEM`.
>
> **4. Parâmetros sem argumento.** Posicional sem padrão: `MissingArgument PROBLEM`; posicional com padrão: recebe o padrão. Nomeado opcional: recebe o padrão ou, sem padrão, `void` com ImplicitVoid WARNING (Capítulo 7.2). Nomeado depois de !: o padrão, se declarado; sem padrão, MissingNamedArgument PROBLEM. Tipado (depois de ?): o padrão, se declarado; sem padrão, MissingArgument PROBLEM. Variádico: `args = []`.
>
> **Forma** `IDENT = expr`**.** Na fase 3, um argumento `IDENT = expr` equivale a `"IDENT": expr`, com uma diferença: só liga a parâmetros cujo nome externo é string; um nome externo numérico nunca casa com ele.

**Valor padrão não é argumento fornecido.** Um valor padrão (Capítulo 30.5) só é aplicado na fase 4, a um parâmetro que chegou até lá sem argumento: ele nunca participa das fases 2 e 3 e, portanto, nunca causa `DuplicateArgument`. Esse erro ocorre apenas quando o **chamador** fornece dois argumentos ao mesmo parâmetro — por posição e por nome, ou por dois nomes iguais. Quando há argumento fornecido, ele substitui o padrão.

Exemplos normativos:

```tinypine
f ex(a, "B": b = 5, package resto, !, "C": c)
  print(a, b, resto, c)

ex(1, "C": 9)               # a=1  b=5  resto=[]      c=9
ex(1, 2, 3, 4, "C": 9)      # a=1  b=2  resto=[3, 4]  c=9
ex(1, "C": 9, "B": 7)       # a=1  b=7  resto=[]      c=9
ex(1, 2, "B": 7, "C": 9)    # DuplicateArgument PROBLEM
ex("C": 9)                  # MissingArgument PROBLEM
ex(1)                       # MissingNamedArgument PROBLEM
ex(1, "D": 3, "C": 9)       # UnknownNamedArgument PROBLEM
f GJ(e)
  print(e)

GJ(10)                      # posicional

f GH("A": e)
  print(e)

GH()                        # e = void, com ImplicitVoid WARNING
GH("A": 10)                 # nomeado opcional, por nome

f GG(!, "A": e)
  print(e)

GG("A": 10)                 # nomeado obrigatório

f X(e = 0)
  print(e)

X()                         # e = 0
X(42)                       # e = 42

f XC("a": e = null)
  print(e)

XC()                        # e = null
XC("a": 42)                 # e = 42
XC("a")                     # e = "a" — literal posicional

f fun(package args)
  print(args)

fun("arroz", "açucar", "melhor", "eficiência")
# args = ["arroz", "açucar", "melhor", "eficiência"]

f fun2(a, package args)
  print(a)
  print(args)

fun2("arroz", "açucar", "melhor", "eficiência")
# a = "arroz"
# args = ["açucar", "melhor", "eficiência"]
```

Exemplos de `package` com parâmetros nomeados (ligação conforme as fases acima):

```tinypine
f exemplo("sep": SEP = "")
  print(SEP)
exemplo()                  # SEP = "" — valor padrão, sem DuplicateArgument
exemplo("sep": "-")        # SEP = "-" — o argumento fornecido substitui o padrão
f saida(package ARGS, "sep": SEP = "")      # nomeado opcional depois de package
saida("sep": "-")          # ARGS = [], SEP = "-"
saida(1, 2, "sep": "-")    # DuplicateArgument PROBLEM — o 1 já ligou SEP por posição (ver B21)
f saida2(package ARGS, !, "sep": SEP)      # exclusivamente nomeado: nunca recebe posição
saida2(1, 2, "sep": "-")   # ARGS = [1, 2], SEP = "-"
saida2(1, 2)               # MissingNamedArgument PROBLEM
```

Com `!`, a assinatura de um `print` próprio — todos os valores em `ARGS` e os nomeados só por nome, com padrão — é válida (resolve o caso de B21):

```tinypine
f out(package ARGS, !, "last": END = "", "sep": SEP = "", "flush": FLUSH = true)
  ...

out(10, 49, 63)                  # ARGS = [10, 49, 63], END = "", SEP = "", FLUSH = true
out(10, 49, 63, "last": "-")     # ARGS = [10, 49, 63], END = "-"
out("sep": "/", 1, 2, 3)         # ARGS = [1, 2, 3], SEP = "/"
```

### Erros de Chamada e de Declaração

Esta é a única tabela normativa dos erros de chamada e de declaração de parâmetros — os Capítulos 36.6 e 37 a referenciam em vez de repetir o conteúdo. Todos seguem o formato geral de erro (Seção 36.7).

| **Caso**                                                   | **Exemplo**                                                                                                                                                          | **Comportamento formal**                                                                                                                                                                                                                                               |
|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Parâmetro posicional ausente                               | `f A(e)` · `A()`                                                                                                                                                     | `MissingArgument PROBLEM` — nenhum argumento para `e` e sem valor padrão. O mesmo vale para parâmetro tipado (depois de ?) sem argumento: f A(?, e: int) · A().                                                                                                        |
| Parâmetro nomeado obrigatório ausente                      | `f G(!, "A": e)` · `G()`                                                                                                                                             | `MissingNamedArgument PROBLEM` — o nome externo `"A"` não foi fornecido e não há valor padrão.                                                                                                                                                                         |
| Argumento nomeado desconhecido                             | `f H("A": e)` · `H("B": 1)`                                                                                                                                          | `UnknownNamedArgument PROBLEM` — nenhum parâmetro tem o nome externo `"B"`; vale também para funções que só têm `package args`, que não capturam nomeados.                                                                                                             |
| Argumento posicional para parâmetro exclusivamente nomeado | `f G(!, "A": e)` · `G(10)`                                                                                                                                           | `PositionalForNamedOnly PROBLEM` — argumento posicional excedente, sem `package args`, em assinatura com seção `!`.                                                                                                                                                    |
| Argumento nomeado para parâmetro exclusivamente posicional | `f A(e)` · `A("e": 10)`                                                                                                                                              | `NamedForPositionalOnly PROBLEM` — o nome coincide com o identificador de um parâmetro posicional.                                                                                                                                                                     |
| Argumento duplicado                                        | `H(1, "A": 2)` · `H("A": 1, "A": 2)`                                                                                                                                 | `DuplicateArgument PROBLEM` — o parâmetro já foi ligado por posição ou por outro argumento nomeado. Um valor padrão não conta como argumento fornecido (Capítulo 30.8).                                                                                                |
| Excesso de argumentos sem variádico                        | `f A(e)` · `A(1, 2)`                                                                                                                                                 | `TooManyArguments PROBLEM` — argumento posicional excedente, sem `package args` e sem seção `!`.                                                                                                                                                                       |
| Uso inválido de `!`                                        | `f A(!)` · `f A(!, e)` · `f A(!, "A": e, !, "B": k)`                                                                                                                 | `InvalidBangMarker PROBLEM` — `!` sem nenhum nomeado depois, seguido de parâmetro posicional ou `package`, ou repetido. Fora de uma lista de parâmetros, `!` avulso é `ParserError PROBLEM` (Capítulo 11.3).                                                           |
| Uso inválido de ?                                          | `f A(?)` · `f A(?, e)` · `f A(?, e: int, u: int)` · `f A(?, e: int, ?, u: str)` · `f A(!, "A": e, ?, e: int)`                                                        | `InvalidQuestionMarker PROBLEM` — `?` sem parâmetro depois, parâmetro tipado sem tipo ou com tipo repetido, `?` repetido, depois de `!` ou seguido de `package`. `package` declarado antes de `?` é `InvalidVariadicParam PROBLEM` (Capítulo 30.4.1).                  |
| Argumento sem parâmetro tipado compatível                  | `f A(?, e: int, a: str)` · `A(1, 2)`                                                                                                                                 | `TypeMismatch PROBLEM` — o argumento 2 não casa com nenhum parâmetro tipado restante. Argumento a mais, depois de todos os tipados ligados (`A(1, "x", 3)`), é `TooManyArguments PROBLEM`.                                                                             |
| Uso inválido de `package args`                             | `f A(package args, b)` · `f A(package a, package b)` · `f A(!, package args)` · `f A(package args = 0)` · f A("args": package args) · f A(package args, ?, e: int) \| `InvalidVariadicParam PROBLEM` — `package` seguido de parâmetro posicional, repetido, dentro da seção !, antes do marcador ?, ou com valor padrão ou nome externo. Parâmetros nomeados declarados antes ou depois de `package` não causam este erro (Capítulo 30.3). |
