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

> ***Nota:*** `.type` *não é afetado pelas anotações estruturadas* `list<...>`*/*`dict<...>` *(Cap. 6.8) —* `list` *e* `dict` *continuam reportando* `list ou dict ` *por* `.type`*, exatamente como* `type()` *reportava antes (Cap. 19.1, 19.5.2).*

### Tipagem Estruturada de Coleções — list\<...\> e dict\<...\>

Além da asserção de tipo sobre os seis tipos primitivos escalares (Cap. 6.1–6.6), o mecanismo `valor: tipo` (Cap. 5) aceita duas formas estruturadas, destinadas a coleções: `list<...>` e `dict<chave, valor>`. Podem ser usadas em qualquer posição onde um tipo é esperado: declaração de var/const (Cap. 18.2), parâmetro de função (Cap. 30.3) e tipo de retorno de função (Cap. 30.4).

> ***Nota:*** `list<...>` *e* `dict<...>` *são apenas anotação de tipo, verificada estaticamente na etapa de Análise Estática de Tipos do pipeline (Cap. 35). Elas não criam um tipo novo em tempo de execução —* `list` *e* `dict` *continuam sendo, para* `.type` *(Cap. 6.7), o tipo* `list `*ou* `dict` *já definido pelo delimitador do literal (Cap. 19.1).*

**List\<T1, T2, ...\>:** a notação declara o conjunto de tipos válidos que um elemento pode assumir — não uma lista posicional, e sem ordem semântica: `list<int, str>` e `list<str, int> `são exatamente a mesma restrição. Um elemento fora do conjunto declarado é erro de verificação estática.

```tinypine
const B = [1, 2, "arroz"]
B[1] = true                     # válido

const I: list<int, str> = [1, 2, "arroz"]    # válido — elementos batem com os tipos declarados
```

**dict\<chave, valor\>:** o primeiro parâmetro declara o(s) tipo(s) válido(s) de chave; o segundo, o(s) tipo(s) válido(s) de valor. Cada um pode ser um único tipo ou uma união, escrita com a mesma notação `<T1, T2, ...>` usada em `list<...>`:

```tinypine
const A: dict<str, [str, int]> = {"a": 1, "b": "arroz"}   # chave: sempre str; valor: int ou str
dict<[str, int], bool>                                      # chave: str ou int; valor: sempre booleano
```

Valores (e chaves) de tipos diferentes podem coexistir livremente na mesma coleção, desde que cada um pertença ao conjunto declarado — o mesmo princípio já vale para chaves `str` e numéricas misturadas (Cap. 19.1).

**Tipos aninhados:** ao contrário da inferência automática (abaixo), uma anotação explícita preserva a estrutura interna recursivamente, sem colapsar para o rótulo genérico:

```tinypine
dict<str, dict<str, int>>   # o valor continua sendo dict<str, int>, não apenas "dict"
```

**Inferência automática:** quando nenhuma anotação é fornecida, o tipo de uma coleção é inferido a partir do seu conteúdo, seguindo o mesmo princípio de união:

- **Coleção vazia:** `[]` ou `{}` (Cap. 19.1) inferem, respectivamente, `list` ou `dict` "com void dentro" — o tipo dos elementos/valores ainda não é conhecido.

- **Valor aninhado:** um valor aninhado inferido usa apenas o rótulo genérico do seu tipo de coleção, sem aprofundar na estrutura interna:

```tinypine
var exemplo = {1: {}}   # nome: exemplo; tipo: dict; chave: int; valor: dict
```
