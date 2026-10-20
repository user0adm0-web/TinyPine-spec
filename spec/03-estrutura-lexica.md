# PARTE II — LÉXICO E SINTAXE

## Estrutura Léxica

Esta seção descreve os elementos léxicos do TinyPine: comentários, sequências de escape e os erros que o analisador léxico (lexer) pode reportar antes mesmo de o programa ser interpretado como sintaxe.

### Comentários

O TinyPine define duas formas de comentário e uma forma de **instrução ao TinyPine** escrita dentro de um comentário (3.1.1):

| **Forma**   | **Alcance**                                   | **Efeito**                                  |
|-------------|-----------------------------------------------|---------------------------------------------|
| `# ...`     | até o fim da linha                            | nenhum                                      |
| `\|\| ... \|\|` | várias linhas, até o `\|\|` de fechamento      | nenhum                                      |
| `#~ ...`    | até o fim da linha                            | instrução ao TinyPine (ver 3.1.1)           |

Exemplo de uso combinado:

```tinypine
|| Teste de Comentários Combinados ||
repeat 2 # abre bloco repeat
  print("A")
  pause 1 # pausa de 1s
```

Comentários não possuem efeito semântico: são removidos pelo analisador léxico antes da etapa de *parsing* (ver Capítulo 35) e não podem alterar fluxo de execução, escopo ou modificadores.

#### Instruções ao TinyPine — `#~`

`#~` é um comentário para quem lê o programa e, ao mesmo tempo, uma **instrução ao TinyPine**: o interpretador ignora o texto como código, mas lê o que vem depois de `#~` como um comando. A instrução disponível hoje é `hide`, que impede a emissão de um aviso:

```tinypine
#~ hide W301
#~ hide the W301      # o mesmo: o "the" é opcional
```

Cada peça da instrução tem um papel fixo:

| **Peça** | **Papel**                                                                                                                     |
|----------|-------------------------------------------------------------------------------------------------------------------------------|
| `#~`     | abre uma instrução ao TinyPine. Sem uma instrução válida depois dele, o TinyPine emite um aviso (abaixo).                       |
| `hide`   | o que fazer: não emitir (esconder) o aviso mencionado.                                                                         |
| `the`    | **opcional**: indica que a próxima palavra é uma **menção**. `#~ hide W301` e `#~ hide the W301` fazem a mesma coisa.         |
| `W301`   | a menção: o **código** (`W301`) ou o **nome** (`ImplicitVoid`) de um aviso do catálogo (Capítulo 36.7).                         |

Gramática:

```ebnf
Instruction = "#~" Command [ "#" TEXT ] ;
Command     = "hide" [ "the" ] Mention ;
Mention     = WARNING_CODE | WARNING_NAME ;
```

O texto depois de um segundo `#` é só uma nota e é ignorado: `#~ hide W301 # o valor chega depois`.

**Alcance.** O alcance de um `hide` depende de onde ele está escrito:

| **Onde**                                   | **Esconde**                                                                  |
|--------------------------------------------|------------------------------------------------------------------------------|
| na mesma linha de um código                | os avisos daquela linha (ou do trecho de várias linhas que a contém)         |
| em linha própria                           | os avisos dali até o fim do arquivo                                          |
| em linha própria, no terminal interativo   | os avisos pelo resto da sessão                                               |

Uma instrução vale só no arquivo em que está escrita: um arquivo carregado com `load` (Cap. 29.5) tem as suas.

```tinypine
var a #~ hide W301
var b
#~ hide the UnusedVariable
var c
```

No exemplo, o `ImplicitVoid WARNING` de `a` é escondido; o de `b` continua sendo emitido; o `UnusedVariable WARNING` de `c` (e de tudo o que vier abaixo) é escondido.

**Só avisos podem ser escondidos.** Um erro nunca é escondido: `#~ hide E301` (ou `#~ hide the E301`) é uma instrução inválida (`UnknownMention WARNING`). O que `hide` esconde é a **emissão**: o programa se comporta exatamente como se o aviso não existisse, e um aviso que nunca aconteceria não faz a instrução falhar.

**Instruções inválidas.** Nada depois de `#~` é ignorado em silêncio. Toda instrução que não segue a gramática acima emite um aviso, na posição da própria instrução:

| **Caso**                                          | **Aviso**                              | **Exemplo**                       |
|---------------------------------------------------|----------------------------------------|-----------------------------------|
| nada depois de `#~`                               | `InvalidDirective (W101)`              | `#~`                              |
| comando desconhecido                              | `InvalidDirective (W101)`              | `#~ show the W301`                |
| `hide` sem menção                                 | `InvalidDirective (W101)`              | `#~ hide` · `#~ hide the`         |
| palavras sobrando depois da menção                | `InvalidDirective (W101)`              | `#~ hide W301 now`                |
| menção que não é um aviso do catálogo             | `UnknownMention (W102)`                | `#~ hide the W999`                |
| menção a um erro                                  | `UnknownMention (W102)`                | `#~ hide the E301`                |

Cada linha `#~` esconde um único aviso; para esconder vários, escreva uma linha para cada. `#~` dentro de um texto (`"#~ ..."`, `r"#~ ..."`, `""" ... """`) ou de um comentário de bloco não é uma instrução. Como todo aviso, `InvalidDirective` e `UnknownMention` também podem ser escondidos por um `#~ hide` anterior.

### Sequências de Escape

Sequências iniciadas por `\` representam caracteres ou comportamentos especiais dentro de um literal de string. Fora de uma string, o caractere `\` é sempre um erro de sintaxe — sequências de escape só têm efeito **dentro** de um literal de string. A única exceção é o delimitador de restrição de um tipo refinado, `tipo\restrição\` (Capítulo 6.9): ali a barra invertida vem logo depois do nome do tipo, abre a restrição e é fechada pela próxima barra invertida fora de uma string. Por isso uma restrição não pode conter outra restrição dentro de si.

#### Controle de Linha

| **Sequência** | **Efeito**                                                                    | **Exemplo**           | **Saída**                        |
|---------------|-------------------------------------------------------------------------------|-----------------------|----------------------------------|
| `\n`          | Insere nova linha.                                                            | `print("Olá\nMundo")` | `Olá` / `Mundo` (em duas linhas) |
| `\r`          | Retorna o cursor ao início da linha atual (sem apagar o conteúdo já escrito). | `print("12345\rABC")` | `ABC45`                          |

#### Caracteres Literais

| **Sequência** | **Efeito**               | **Exemplo**          | **Saída** |
|---------------|--------------------------|----------------------|-----------|
| `\\`          | Barra invertida literal. | `print("\\\\")`      | `\`       |
| `\"`          | Aspa dupla literal.      | `print("\\"Olá\\"")` | `"Olá"`   |

Os seguintes caracteres podem ser escapados para uso literal dentro de uma string: `\`, `"`, `'`, `{` e `}`. A presença da barra invertida remove qualquer significado especial do caractere imediatamente seguinte.

#### Correspondência por Padrão — \\

A sequência `\*`, usada dentro de um literal de string comparado por meio de `.match()` ou do operador `~=` (ver 11.2), representa **exatamente um caractere arbitrário** — não uma sequência de zero ou mais caracteres. É um curinga posicional de largura fixa, não um curinga de repetição.

```tinypine
"casa" ~= "c\*sa"              # true
"teste" ~= "t\*"               # false
"top" ~= "t\*f"                # false
```

Nota: a partir da 0.5, `==` realiza sempre igualdade literal pura — `\*` deixa de ter qualquer efeito de curinga dentro dele (ver 11.2).

### Erros Léxicos

O analisador léxico interrompe imediatamente a leitura ao encontrar uma das condições abaixo. Não há ignorância silenciosa de erros léxicos — este comportamento segue o princípio geral do interpretador de que nenhum erro é silencioso (ver Capítulo 36); o formato de exibição de cada erro está na Seção 36.7.

| **Caso**                                                                       | **Comportamento formal**                                                                                                                                                                                                                 |
|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Caractere inválido (ex.: `@`)                                                  | `ParserError PROBLEM` — Unexpected character `'@'`. O lexer interrompe imediatamente a leitura.                                                                                                                                          |
| String não fechada                                                             | `ParserError PROBLEM` — Unterminated string: the closing quote is missing. Detectado quando o lexer atinge o fim da linha ou o fim do arquivo sem encontrar o fechamento das aspas.                                                      |
| Número malformado (ex.: `12.5.7`)                                              | `ParserError PROBLEM` — Malformed number `'12.5.7'`. Múltiplos pontos decimais no mesmo literal numérico são inválidos.                                                                                                                  |
| Indentação mista (TAB e espaço no mesmo escopo)                                | `MixedIndentation PROBLEM` — Mixed TABs and spaces in the indentation of the same scope. Detectado quando uma linha usa TAB onde o escopo já havia fixado espaço como unidade, ou vice-versa (Capítulo 4.3).                             |
| Recuo inesperado (linha mais recuada sem que a anterior tenha aberto um bloco) | `UnexpectedIndent PROBLEM` — Unexpected indent: the line is more indented than the previous one, which does not open a block. O lexer encontrou uma linha mais recuada que a anterior sem que esta terminasse em posição de abrir bloco. |

### Identificadores (Nomes de Variável e Função)

O conjunto de caracteres válidos num identificador é definido por uma lista de exceção — mais restrito do que a maioria das linguagens, e proposital: com um conjunto pequeno, nunca há dúvida sobre o que é identificador e o que é operador.

Permitido:

- **letras ASCII, maiúsculas ou minúsculas (a–z, A–Z) — sem acento e sem ç;**

- **dígitos (0–9), em qualquer posição menos a primeira;**

- **o símbolo** `-` **— só no meio do nome, nunca no início nem no fim (Capítulo 3.4.1);**

- **o símbolo** `_` **— só no meio ou no início do nome, nunca no fim.**

- **o símbolo** `$` **— só no início do nome e no fim do nome. ( apenas variáveis )**

Proibido — qualquer outro símbolo, incluindo (mas não só): `& + * ´ \` ' " \# % ( ) \[ \] { } ; : \\ / , = ç ~ ? @ .\` ´

Também são inválidos: acentos, ç, e qualquer emoji (inclusive variantes de um mesmo emoji, como ♡/♻) — nenhum caractere fora de a–z/A–Z/0–9/`-`/`_` é aceito, então isso já decorre da regra acima; fica dito aqui de forma explícita para não deixar dúvida.

```tinypine
var nome = "Dhavi"         # válido
var idade2 = 20            # válido — dígito no meio/fim
var minha(idade = 20       # inválido — "(" não é permitido
var são = true             # inválido — "ã" não é permitido
```

> ***Nota:** o símbolo* `~` *não pertence ao alfabeto de identificadores e não pode ser usado para declarar variável ou função (*`ReservedSymbol PROBLEM`*).* `~Program` *é um objeto nativo do programa, não uma declaração (Capítulo 29.4). O operador* `~=` *(Capítulo 11.2) não é afetado.*

#### O símbolo - em identificadores

*Nota — histórico (v0.5): até a v0.4, um identificador nunca podia ser 100% maiúsculo, pois essa forma era reservada aos operadores-palavra da linguagem — regra removida nesta revisão, já que os operadores-palavra passam a ser grafados em minúsculas (Capítulos 11 e 12).* `var NOME = "Dhavi"` *volta a ser um identificador válido (ver Apêndice A).*

O símbolo `-` é aceito dentro de um identificador, mas nunca como o primeiro ou o último caractere — o último caractere só pode ser letra ou dígito:

```tinypine
var Syntax-Clean = true   # válido
var -um = true  # inválido — - não pode terminar ou começar o nome
```

> ***Nota:** o símbolo - dentro de um identificador nunca colide com subtração de variáveis — O parser faz uma lógica para verificar se o elemento anterior a - e o após a - sejam variáveis. caso sejam ele devolve erro. Regra prática equivalente: A-b colado (sem espaços) é nome; A - b com espaço é subtração; número-número é sempre subtração, já que um número nunca é variável.*
