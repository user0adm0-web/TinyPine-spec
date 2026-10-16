## Entrada do Usuário — readln()

Lê um valor digitado pelo usuário e retorna uma `str`. Aceita, opcionalmente, o número mínimo e máximo de caracteres esperados.

> ***Nota:*** `readln()` *só lê — não imprime prompt, rótulo ou qualquer outro texto. Por isso os exemplos abaixo sempre chamam* `print()` *numa linha separada antes de* `readln()`*, quando querem mostrar alguma coisa para quem está digitando.*

```tinypine
print("escreva seu nome: ")
var nome = readln()
 
print("escreva sua idade: ")
var idade = readln(“min”:2, “max”:2)   # exige exatamente 2 caracteres
```

Os três parâmetros são nomeados de verdade — `min`, `max` (num) e `active` (bool) — na mesma sintaxe `nome:valor` do Capítulo 20.1. `active` vem sempre `true` quando omitido (validação ativa por padrão); qualquer combinação de nomes pode ser omitida, e a ordem entre eles não importa:

```tinypine
var idade = readln(“min”:2, “max”:2)                 # min=2, max=2, active=true (padrão)
var qualquer = readln(“active”:false)               # sem min/max — nenhuma validação
var nome = readln(“min”:3, “max”:20, “active”:false)    # dá pra combinar sem validar
```

### Parâmetros de Representação Visual — show, sep, last

`readln()` aceita três argumentos nomeados adicionais — `show`, `sep` e `last` — que controlam exclusivamente a forma como a entrada é exibida no console, sem alterar o valor efetivamente capturado e retornado. Eles coexistem com `min`, `max` e `active` (Capítulo 21): esses validam a entrada; `show`/`sep`/`last` apenas mudam sua representação visual. Todos são omissíveis e combináveis livremente, sem ordem obrigatória entre si.

`show` controla como cada caractere capturado é exibido enquanto o usuário digita. Por padrão (omitido), os caracteres aparecem normalmente. Um valor string substitui cada caractere pela mesma representação — `""` torna a entrada invisível, `"*"` mascara cada caractere com um asterisco — e uma expressão que usa a variável implícita `it` (referindo-se a cada elemento capturado) permite uma representação calculada por elemento. Em todos os casos, a captura da entrada real continua normal — apenas a exibição muda.

```tinypine
var senha = readln(“show”:"")        # nada é exibido; captura normal
var senha = readln(“show”:"*")       # cada caractere aparece como *
var texto = readln(“sep”: "·")              # separador fixo entre caracteres
```

`sep` define o separador inserido entre as representações de cada elemento — nunca aparece depois do último elemento:

```tinypine
var codigo = readln("sep":"-")              # a-b-c-d
var senha = readln("show":"*", "sep":"-")     # *-*-*-*
```

`last` define um conteúdo extra exibido apenas visualmente ao final da representação da leitura — não é incorporado ao valor retornado:

```tinypine
var email = readln("last":"@gmail.com")
# usuário digita "usuario" → tela mostra usuario@gmail.com; valor retornado continua "usuario"
```

Os três parâmetros podem ser combinados entre si e com `min`/`max`/`”active”:`

```tinypine
var codigo = readln("show":"*", "sep":"-", "last": ".com", "min":4, "max": 4)
```

Ordem conceitual de processamento a cada elemento capturado: (1) captura a entrada real; (2) representa cada elemento conforme `show`; (3) insere `sep` entre as representações; (4) exibe `last` ao final, quando definido; (5) retorna a entrada original, sem qualquer transformação aplicada por `show`/`sep`/`last`. Parâmetros de apresentação nunca alteram o valor lógico retornado, a menos que um parâmetro futuro defina esse comportamento explicitamente.

> ***Nota:*** `readln()` *permanece como a única operação de entrada da linguagem —* `show`*/*`sep`*/*`last` *são extensões dela, escritas na mesma sintaxe nome:valor do Capítulo 20.1 — não uma função de entrada separada.*

**Forma** `nome=valor`**.** Como em todo argumento nomeado (Capítulo 30.3), `show`, `sep`, `last`, `min`, `max` e `active` também podem ser escritos `nome=valor`, sem aspas:

```tinypine
var senha = readln(show="*", sep="-")              # *-*-*-*
var codigo = readln(show="*", last=".com", min=4, max=4)
```
