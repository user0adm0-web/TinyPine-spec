# PARTE VI — ESTRUTURAS DE CONTROLE

## Impressão e Interpolação de Strings

| **Forma**        | **Comportamento**                                                                                                   |
|------------------|---------------------------------------------------------------------------------------------------------------------|
| `print(valor)`   | Escreve o valor na saída padrão, sem quebra de linha automática ao final.                                           |
| `println(valor)` | Escreve o valor seguido de quebra de linha automática — equivalente a `print` com `\n` embutido ao final da string. |
| `println(valor)` | Escreve o valor seguido de quebra de linha no final e retorna `null` (Capítulo 7.1).                                |

`println(valor)` escreve o valor seguido de uma quebra de linha no final e retorna `null`; portanto, `var r = println("B")` atribui `null` a `r`.

```tinypine
println("A")           # escreve A e quebra a linha
var r = println("B")   # escreve B, quebra a linha; r = null
```

### Argumentos Nomeados — sep, last, flush

`print` e `println` aceitam argumentos nomeados opcionais, escritos como `nome:valor` diretamente na lista de argumentos (sem colchetes — não é um dict, é a mesma sintaxe chave:valor emprestada para argumento de chamada). Três nomes são reconhecidos: `sep` (separador entre os valores impressos — padrão `""`), `last` (texto anexado ao final — padrão `""` em `print`, `"\n"` em `println`) e `flush` (bool — força a saída imediata; padrão `true`). Nomes omitidos mantêm o padrão, e a ordem entre eles não importa:

```tinypine
print("a", "b", "c")
# → abc (sep padrão "", sem quebra ao final)
 
print("a", "b", "c", "sep":", ")
# → a, b, c
 
print("carregando", "last":"")
print("...", “last”:"\n")
# → carregando... (as duas chamadas continuam na mesma linha)
 
print("a", "b", “last”:"!\n", “sep”:"-")
# → a-b! (ordem entre os nomeados não importa)

f Teste("out":e, "end":k, "fun":y)
  print(format "|{y}|>", e, "last":k)
```

`println("x")` *equivale a* `print("x", “last”:"\n")` *— mesmo motor por baixo, só o default de* `last` *muda.*

Um argumento nomeado é reconhecido assim: um IDENT seguido imediatamente de `:` dentro da lista de argumentos. Isso não colide com nada mais na linguagem — argumentos posicionais continuam sendo só uma expressão, sem dois-pontos.

**Forma** `nome=valor`**.** Os nomes reconhecidos por `print` e `println` (`sep`, `last`, `flush`) também podem ser escritos `nome=valor`, sem aspas — é a forma alternativa de argumento nomeado do Capítulo 30.3. As formas são equivalentes e podem ser combinadas na mesma chamada:

```tinypine
print("a", "b", "c", sep=", ")          # → a, b, c   (igual a "sep": ", ")
print("carregando", last="")           # igual a "last": ""
print("a", "b", last="!\n", sep="-")   # → a-b!
```

> ***Nota:** a sintaxe* `nome:valor` *sem aspas, em argumento de chamada, só é reconhecida nos parsers de* `print`*,* `println` *e* `readln` *(Capítulo 21). Uma função definida pelo usuário recebe argumentos nomeados pela forma com aspas,* `"nome": valor`*, ou — quando o nome externo é uma string que forma um identificador válido — por* `nome=valor` *(Capítulo 30.3), correspondentes a um parâmetro declarado com identificador externo entre aspas (*`"nome": param`*) — ver Capítulos 30.3 e 30.8, um mecanismo distinto, com sintaxe própria. Chamar uma função de usuário com* `nome:valor` *sem aspas é erro de sintaxe. ( REMOVIDO ) ATUAL: todo argumento não importa qual função o recebe, tem que estar “nome”: valor OU nome=valor ( caso nome seja um string ná declaração dos parâmetros )*

Strings suportam interpolação de variáveis, delimitada por `{` e `}`:

```tinypine
var A = "Top"
print("você é muito {A} e eu não gosto de \'\{\}\' ")
# → você é muito Top e eu não gosto de '{}'
```

No exemplo acima, `{A}` é substituído pelo valor da variável `A`, enquanto `\{` e `\}` produzem chaves literais, sem interpolação — ver Capítulo 3.2 para a lista completa de sequências de escape.

### Expressões dentro de { }

O que fica entre `{` e `}` não precisa ser só o nome de uma variável: também são aceitas expressões e propriedades (como `.length`, Capítulo 33.3). Os dois exemplos abaixo são válidos — não geram erro:

```tinypine
var A = 1
format "{A-A}"        # válido
format "{A.length}"   # válido
```

> ***Nota:*** *o resultado de cada um desses dois exemplos (a interação do* `-` *com a regra do Capítulo 3.4.1 e o* `.length` *de um número) ainda não está definido — Apêndice A.2, B28.*
