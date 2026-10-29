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
print("...", "last":"\n")
# → carregando... (as duas chamadas continuam na mesma linha)
 
print("a", "b", "last":"!\n", "sep":"-")
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

Strings formatadas ( format "" ) suportam interpolação de variáveis, delimitada por `{` e `}`:

```tinypine
var A = "Top"
print(format "você é muito {A} e eu não gosto de \'\{\}\' ")
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

### Curingas e caracteres Unicode com [ ]

Dentro de um `format`, os colchetes abrem um **grupo**. Há dois tipos de grupo, e **nada mais** é aceito entre `[` e `]`:

| **Grupo**                        | **O que é**                                                                                                         | **Exemplo**                      |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------|----------------------------------|
| `[*]` · `[N*]` · `[*M]` · `[N*M]` | **curinga**: casa de `N` até `M` caracteres quaisquer. `N` omitido vale 0; `M` omitido significa sem limite.        | `format "ar[*]"`                 |
| `[u+H]`                          | **Unicode**: o caractere de ponto de código `H`, escrito em **hexadecimal**, como na notação `U+2222`.             | `format "[u+2222]"` → `∢`        |

```ebnf
Group     = "[" ( Wildcard | Unicode ) "]" ;
Wildcard  = [ Bound ] "*" [ Bound ] ;
Unicode   = "u+" ( HEXDIGIT { HEXDIGIT } | "{" Expr "}" ) ;
Bound     = INTEGER | "{" Expr "}" ;
HEXDIGIT  = "0"…"9" | "a"…"f" | "A"…"F" ;
```

**Curinga.** `[*]` casa zero ou mais caracteres; `[2*]`, pelo menos 2; `[*4]`, de 0 a 4; `[2*4]`, de 2 a 4; `[3*3]`, exatamente 3 (e `[1*1]` é exatamente 1, o antigo `\*`). Um caractere é qualquer caractere, inclusive `\n`; maiúsculas e minúsculas são diferentes. Um `format` com pelo menos um curinga produz um **padrão**, que `==`, `!=`, `.match()` e `~=` casam com a outra string (Capítulo 11.2):

```tinypine
format "ar[*]" == "arroz"      # true
format "[*]a[*]" == "a"        # true  — os dois grupos casam zero caracteres
format "a[*4]" == "arroz"      # true  — "rroz" são 4 caracteres
format "a[*3]" == "arroz"      # false — "rroz" são 4 e o máximo é 3
format "a[2*]" == "ab"         # false — o mínimo é 2 caracteres depois do "a"
```

**Unicode.** `[u+H]` vira o caractere do ponto de código `H`, escrito em **hexadecimal** (de 1 a 6 dígitos `0-9`, `a-f`, `A-F`, maiúsculas ou minúsculas; zeros à esquerda são aceitos): `[u+2222]` é `∢` (U+2222, *Spherical Angle*) e `[u+E9]` é `é`. Os limites do curinga (`N`, `M`), ao contrário, são inteiros **decimais** comuns. Um `format` que só tem grupos Unicode (e nenhum curinga) é uma `str` comum, não um padrão:

```tinypine
format "[u+2222]"     # → ∢
format "caf[u+E9]"    # → café
format "caf[u+e9]"    # → café (maiúsculas e minúsculas dos dígitos são iguais)

var C = 8738          # 8738 é 2222 em hexadecimal
format "[u+{C}]"      # → ∢  — entre { } vai um int: o próprio número do ponto de código
```

**Variáveis nos grupos.** Os colchetes **sozinhos não abrem variáveis**: `[B]` não é a variável `B` — é um grupo inválido. Para usar um valor, escreva-o entre chaves, como em qualquer parte do `format`: `[{B}*{A}]`, `[{B}*]`, `[u+{C}]`. A expressão entre chaves precisa ser um `int`; em `[u+{C}]` o `int` é o **número** do ponto de código (um `int` não carrega "base": `8738` e o literal `[u+2222]` são o mesmo caractere).

```tinypine
var A = 4
var B = 2
format "a[{B}*{A}]" == "arroz"   # true — de 2 a 4 caracteres depois do "a"
```

**Erros.** `InvalidPatternGroup PROBLEM` (E125) quando: o grupo tem outra coisa que não curinga ou `u+H` (`[]`, `[abc]`, `[B]`, `[u+]`, `[u+xyz]`); `N` ou `M` não são inteiros não negativos; `N` > `M`; o ponto de código está fora de `0` a `10FFFF` (hexadecimal) ou é um substituto (`D800` a `DFFF`). Com números escritos no próprio grupo o erro é detectado antes da execução; com `{ }`, quando o `format` é avaliado (recuperável com `try`).

**Colchetes literais.** Para um `[` ou `]` comum num `format`, escreva `\[` e `\]` (Capítulo 3.2.2) — como já se faz com `\{` e `\}`. Os colchetes **dentro** de `{ }` pertencem à expressão (`format "{lista[0]}"`) e não abrem grupo. Numa string **comum** (sem `format`), `[` e `]` são caracteres como outros. *Mudança:* um `format` que já tinha `[` ou `]` literais agora precisa do escape.

> ***Nota:*** *o que `print(format "ar[*]")` imprime, o que acontece com um padrão depois de concatenado ou fatiado, e o `.type` de um padrão ainda não estão definidos — Apêndice A.2, B32.*
