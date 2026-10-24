## Tipos Primitivos Escalares

Esta seção define os seis tipos primitivos escalares do TinyPine e o comportamento da respectiva asserção de tipo (valor: tipo).

### str — Texto

```tinypine
var nome: str = "Ana"
var frase = "olá mundo"
123: str                  # TypeMismatch PROBLEM — 123 não é do tipo str
true: str                 # TypeMismatch PROBLEM
false: str                # TypeMismatch PROBLEM
```

### num — Numérico Genérico

O tipo num é a raiz do sistema numérico do TinyPine. Ele atua como um supertipo genérico, aceitando livremente valores do tipo int, float ou decim. É o tipo padrão inferido pelo compilador quando uma variável numérica é declarada sem uma asserção rígida específica, e serve como o tipo de retorno padrão para operações aritméticas mistas. Embora seja flexível entre números, ele mantém a segurança estática e rejeita qualquer tipo não numérico.

`var idade: num = 20 # OK — Aceita int `

`var preco: num = 15.70 # OK — Aceita float/decim `

`var pi: num = 3.14159 # OK — Aceita float/decim `

`var altura: num = "1.90" # StaticTypeMismatch PROBLEM — String não é num e não há coerção implícita `

`true: num # TypeMismatch PROBLEM — Booleano não é compatível com num`

### int — Inteiro

Representa números inteiros de precisão arbitrária (sem limite fixo de bits). É utilizado para contagens, índices e aritmética exata não fracionária. O tipo exige consistência estrita entre o valor matemático e a sua representação sintática: não realiza coerção automática a partir de floats ou strings e rejeita qualquer estrutura de dados que denote uma parte fracionária na atribuição direta.

```tinypine
var n: int = 42
42: int       # OK — Valor inteiro puro
3.9: int      # TypeMismatch PROBLEM — Possui parte fracionária ativa
"10": int     # TypeMismatch PROBLEM — Tipos incompatíveis (String para int)
3.00: int     # TypeMismatch PROBLEM — Literal escrito com ponto decimal
```

> ***Nota — regra formal de classificação da asserção : int: A asserção int opera de forma híbrida entre a representação sintática e a avaliação matemática.  
> ***

1.  ***Para Literais Diretos: O tipo int rejeita qualquer representação visual que contenha ponto decimal (como 3.0 ou 3.00), independentemente de a parte fracionária ser matematicamente nula. Isso garante a clareza visual e evita ambiguidade no código.***

2.  ***Para Expressões Dinâmicas (ver 10.3): O valor resultante da expressão é totalmente calculado antes da checagem de tipo. A asserção aceitará o resultado se, e somente se, o resíduo decimal final for estritamente nulo (ex: (float(9.0) / float(3.0)) : int é válido, pois o resultado final é matematicamente 3).***

### float — Ponto Flutuante

```tinypine
Representa números reais usando o padrão IEEE 754 de precisão dupla (64 bits). Oferece uma precisão de 15 a 17 dígitos decimais significativos. Se um número inteiro for atribuído a uma variável do tipo float, ele será implicitamente convertido (coerção de tipo) para ponto flutuante, adicionando .0;

var x: float = 3.14159
3.14159: float  # OK — Suporta precisão arbitrária até o limite de 64 bits
2.70: float     # OK — 2.7
3: float        # OK — Coerção implícita: vira 3.0 para corresponder ao tipo float, mas gera um Warning sobre conversão implícita 
1e10: float     # OK — Suporta notação científica (10000000000.0)
```

### decim — Decimal Dinâmico de Alta Precisão

Representa números reais com precisão decimal exata (base 10), ideal para cálculos financeiros ou científicos que não podem sofrer erros de arredondamento de hardware. A precisão não é fixa: o tipo calcula e aloca dinamicamente o espaço necessário com base na quantidade de casas decimais do valor fornecido.

```tinypine
```

`var pi: decim = 3.14159265358979323846 `

`3.14159265358979323846: decim # OK — Aloca dinamicamente o tamanho exato do literal sem perdas `

`var preco: decim = 10.50 10.50: decim # OK — Mantém exatamente o .50 (perfeito para dinheiro) `

`var total: decim = 3 3: decim # OK — Coerção implícita: vira 3 (ou 3.0) com precisão dinâmica`

### bool — Lógico

```tinypine
var ativo: bool = true
var vazio: bool = false
1: bool               # TypeMismatch PROBLEM — 1 não é do tipo bool
"true": to-bool
```

### .type — Consulta de Tipo em Tempo de Execução

A partir da 0.7, a consulta ao tipo de um valor em tempo de execução deixa de ser uma função e passa a ser uma propriedade somente leitura, acessada por `.`:

```tinypine
A.type
```

> ***Nota:*** `.type` *não é afetado pelas anotações estruturadas* `list\...\`*/*`dict\...\` *(Cap. 6.8) —* `list` *e* `dict` *continuam reportando* `list` *e* `dict` *por* `.type`*, exatamente como* `type()` *reportava antes (Cap. 19.1, 19.5.2).*

#### O tipo function

Uma função — nomeada (Capítulo 30) ou anônima (Capítulo 31) — é um valor com tipo próprio, `function`, e `.type` o devolve:

```tinypine
f dobro(x)
  return x * 2

dobro.type                    # → function

var g = f(x)
  return x + 1

g.type                        # → function
```

`function` é um nome de tipo como `int` ou `str`: serve na asserção (`valor: function`), na declaração (`var g: function = ...`) e dentro de `keys:`/`values:` (Cap. 6.8). Não aceita restrição `\...\` (Cap. 6.9). Como `is` compara só o tipo (Cap. 11.1), duas funções quaisquer são `is` uma da outra.

### Tipagem Estruturada de Coleções — `list\...\` e `dict\...\`

Além da asserção de tipo sobre os tipos primitivos escalares (Cap. 6.1–6.6), o mecanismo `valor: tipo` (Cap. 5) descreve o conteúdo de uma coleção com as propriedades `keys` e `values` de um tipo refinado (Cap. 6.9). Podem ser usadas em qualquer posição onde um tipo é esperado: declaração de var/const (Cap. 18.2), parâmetro de função (Cap. 30.3) e tipo de retorno de função (Cap. 30.4).

As antigas formas `list<...>` e `dict<chave, valor>` **deixaram de existir**: nenhum tipo usa mais `<...>` (o `<` e o `>` ficam só como operadores de comparação, Cap. 11), e a união de tipos, antes escrita `<T1, T2>` ou `[T1, T2]`, passa a ser o operador `|` (6.8.1).

```
antes (removido)             agora
list<int, str>               list\values: int | str\
dict<str, [str, int]>        dict\keys: str, values: str | int\
dict<[str, int], bool>       dict\keys: str | int, values: bool\
```

> ***Nota:*** *a tipagem estruturada é só anotação de tipo: não cria um tipo novo em tempo de execução —* `list` *e* `dict` *continuam sendo, para* `.type` *(Cap. 6.7), o tipo já definido pelo delimitador do literal (Cap. 19.1).*

**`values: T`** declara que **todo** valor da coleção é do tipo `T`; vale para `list`, `dict` e `tuple`. **`keys: T`** declara que **toda** chave é do tipo `T`; vale para `dict`. `T` é um tipo ou uma união `T1 | T2 | ...` (6.8.1) — o conjunto de tipos válidos, sem ordem semântica: `values: int | str` e `values: str | int` são a mesma restrição. Um elemento fora do conjunto declarado é erro de verificação (ver "Quando é verificado", abaixo).

```tinypine
const B = [1, 2, "arroz"]
B[1] = true                                        # válido — sem tipo declarado

const I: list\values: int | str\ = [1, 2, "arroz"]                   # válido — todo valor é int ou str
const A: dict\keys: str, values: int | str\ = {"a": 1, "b": "arroz"}  # chave: sempre str; valor: int ou str
var P: dict\keys: str | int, values: bool\ = {"a": true, 1: false}    # chave: str ou int; valor: sempre bool
var F: dict\keys: str, values: function\ = {"log": f(package ARGS) print(unpack ARGS)}
```

`keys` e `values` podem se combinar com as demais condições do tipo refinado, separadas por vírgula (Cap. 6.9): `dict\length > 1, keys: str, values: int\`. Uma coleção vazia satisfaz `keys:` e `values:` — nenhum elemento viola a condição.

Valores (e chaves) de tipos diferentes podem coexistir livremente na mesma coleção, desde que cada um pertença ao conjunto declarado — o mesmo princípio já vale para chaves `str` e numéricas misturadas (Cap. 19.1). Anotar parte da coleção não obriga o resto: sem `values:`, a lista continua heterogênea.

**Tipos aninhados.** O tipo depois de `keys:`/`values:` é sempre um tipo simples ou uma união de tipos simples, sem restrição própria — a restrição é fechada pela próxima `\`, então não cabe uma restrição dentro da outra (Cap. 3.2). Por isso `values: dict` aceita qualquer dicionário, sem declarar a estrutura interna dele; a antiga `dict<str, dict<str, int>>` não tem equivalente nesta versão (Apêndice A.2, B29).

**Quando é verificado.** Na declaração de `var`/`const`, no parâmetro e no tipo de retorno de função, `keys:` e `values:` são verificados **estaticamente** (Cap. 35, etapa 6), como a anotação `<...>` já era — `StaticTypeMismatch PROBLEM`. As demais condições, e a asserção direta sobre um valor (`[1, "a"]: list\values: int\`), são verificadas na execução: `RefinementViolation PROBLEM` (Cap. 6.9). Esta divisão está em aberto (B29).

**Inferência automática:** quando nenhuma anotação é fornecida, o tipo de uma coleção é inferido a partir do seu conteúdo, seguindo o mesmo princípio de união:

- **Coleção vazia:** `[]` ou `{}` (Cap. 19.1) inferem, respectivamente, `list` ou `dict` "com void dentro" — o tipo dos elementos/valores ainda não é conhecido.

- **Valor aninhado:** um valor aninhado inferido usa apenas o rótulo genérico do seu tipo de coleção, sem aprofundar na estrutura interna:

```tinypine
var exemplo = {1: {}}   # nome: exemplo; tipo: dict; chave: int; valor: dict
```

#### União de tipos — `|`

`T1 | T2` lê-se "T1 **ou** T2": o valor precisa pertencer a **pelo menos um** dos tipos. Não converte nada — é só um conjunto de tipos válidos, como a asserção `:` (Cap. 5). Vale em qualquer posição de tipo, não só dentro de `keys:`/`values:`:

```tinypine
var x: int | str = 10        # válido
x = "dez"                    # válido — str também está na união
x = true                     # StaticTypeMismatch PROBLEM — bool não está na união
f mostra(v: int | str): str
  return v: to-str
```

O `|` só tem este uso, e só em posição de tipo. Escreva-o com espaços: `||` abre sempre um comentário de bloco (Cap. 3.1), e `|>` é o pipe (Cap. 34.8). Um `|` fora de posição de tipo é `ParserError PROBLEM`, como qualquer caractere inválido (Cap. 3.3).

### Tipos Refinados — `tipo\restrição\`

Um **tipo refinado** restringe os valores aceitos por um tipo por meio de uma expressão lógica, escrita logo depois do nome do tipo e delimitada por barras invertidas: `tipo\restrição\`. Pode ser usado na asserção de tipo (`valor: tipo\...\`, Cap. 5) e na declaração de `var`/`const` (Cap. 18.2).

```tinypine
10: int\value < 100\
100: int\value == 100\
"Aaa": str\length == 3\
[1, 2, 3]: list\values: int, value 2 < 3, key 0==1\
{1: ""}: dict\key "a"==1 or key 1==""\
[1, 0]: list\key 0: int\                                       # asserção: válido (nada é convertido)
var G: dict\length>1, 1==1, key "a": str\ = {"a": "1", "b": "2"}
{"a": 1}: dict\keys: str, values: int | str\
```

**Delimitador.** A barra invertida delimita a restrição, o que permite usar `<`, `>`, `<=` e `>=` dentro dela sem conflito (nenhum tipo usa `<...>`, Cap. 6.8). Fora de uma string, a barra invertida não tem outro uso (Cap. 3.2).

#### Tipos que aceitam refinamento

Nesta versão, apenas: `int`, `float`, `decim`, `num`, `str`, `list`, `dict` e `tuple`. Os demais tipos não aceitam tipos refinados.

#### Propriedades disponíveis

| **Propriedade** | **Tipos**                                | **Significado**                                                                                              |
|-----------------|------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| `value`         | `int`, `float`, `decim`, `num`           | O próprio valor numérico.                                                                                    |
| `length`        | `str`, `list`, `dict`, `tuple`           | O comprimento do valor — exatamente o mesmo que `.length` (Cap. 33.3).                                       |
| `key K`         | `str`, `list`, `dict`, `tuple`           | O elemento de chave `K`: em `dict`, a chave; em `list`, `tuple` e `str`, o índice (forma `colecao[key K]`, Cap. 19.2). |
| `value V`       | `list`, `dict`, `tuple`                  | O valor dentro da coleção (forma `colecao[value V]`, Cap. 19.2).                                             |
| `keys`          | `dict`                                   | O conjunto das chaves. `keys: T` afirma que toda chave é do tipo `T` (Cap. 6.8).                             |
| `values`        | `list`, `dict`, `tuple`                  | O conjunto dos valores. `values: T` afirma que todo valor é do tipo `T` (Cap. 6.8).                          |

Dentro da restrição, as propriedades se referem ao próprio valor que está sendo validado: em `[1, 2, 3]: list\key 0==1\`, `key 0` lê o elemento de chave `0` dessa lista.

#### Regras de validação

1. A restrição é avaliada sobre o valor que está sendo validado.

2. Quando o valor vem de uma conversão explícita (`x: to-int: int\...\`), a restrição é avaliada **depois** dela.

3. Se a condição for falsa, a operação produz `RefinementViolation PROBLEM` (E316).

4. Tipos fora da lista acima não aceitam tipos refinados nesta versão.

5. Dentro da restrição, `null` conta como verdadeiro: só um `false` de verdade reprova o valor. Qualquer outro resultado que não seja `bool` nem `null` é `TypeMismatch PROBLEM` (E302).

```tinypine
200: int\value < 100\        # RefinementViolation PROBLEM — 200 não é menor que 100
"Aaaa": str\length == 3\     # RefinementViolation PROBLEM — o texto tem 4 caracteres
```

#### Operadores e expressões compostas

Dentro da restrição valem `==`, `!=`, `<`, `>`, `<=` e `>=` e, de modo geral, todas as operações da linguagem (por exemplo `or`, Cap. 12). Uma restrição pode ter várias condições separadas por vírgula: todas precisam ser verdadeiras, e basta uma ser falsa para o erro de restrição.

```tinypine
var G: dict\length>1, 1==1, key "a": str\ = {"a": "1", "b": "2"}
# 1ª condição: o dicionário tem mais de um elemento
# 2ª condição: 1==1 (sempre verdadeira)
# 3ª condição: o valor da chave "a" é do tipo str
```

Dentro da restrição, `:` seguido de um tipo — ou de uma união `T1 | T2`, Cap. 6.8.1 — faz uma asserção sobre aquela parte do valor (`key "a": str`, `values: int | str`), . **Conversão (`: to-tipo`) não é aceita dentro da restrição:** ela só valida o valor, nunca o transforma, então `int\0: to-bool\` e `list\value 2: to-str\` são `ConversionInRefinement PROBLEM` (E124), erro sintático que aborta o programa antes de rodar. Para validar o tipo de uma parte use a asserção (`key 0: str`); para converter, converta o valor antes (`var x = v: to-str`).

> ***Nota:*** *os pontos em aberto deste recurso — semântica de* `value V` *e de* `values`*, chave ausente dentro de uma restrição, uso em parâmetros e retornos de função, e a mensagem de erro para tipos que não aceitam refinamento — estão registrados no Apêndice A.2 (B27); os da tipagem estruturada, da união `|` e de* `function` *estão em B29.*
