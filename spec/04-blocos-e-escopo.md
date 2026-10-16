## Blocos e Escopo

A partir da 0.7, todo bloco em TinyPine pode ser aberto de duas formas equivalentes: por indentação (Capítulos 4.1 a 4.7, abaixo) ou por delimitador explícito, `:` ... `--` (Capítulo 4.8) — os dois não podem se misturar por aninhamento (Capítulo 4.9). No estilo por indentação, o bloco abre pela quebra de linha logo após a assinatura — sem `:` nem qualquer outro delimitador de abertura — e fecha pela **indentação** (recuo): o corpo do bloco é toda linha mais recuada que a assinatura, e o bloco termina na primeira linha que volta a esse recuo, ou a um recuo menor. Cada nível de indentação equivale a exatamente 2 espaços ou a exatamente 1 TAB — nunca aos dois ao mesmo tempo dentro do mesmo escopo (Capítulo 4.3). Dentro desse estilo, a indentação deixa de ser uma convenção de legibilidade e passa a ter efeito semântico direto: é o delimitador de fechamento do estilo por indentação.

### Abertura de Bloco

*TinyPine*

```tinypine
if 2 < 5
  print("Correto")
```

*Equivalente conceitual em Python*

```tinypine
if 2 < 5:
    print("Correto")
```

### Fechamento de Bloco

O interpretador mantém internamente uma pilha de blocos abertos, mas agora ela é populada automaticamente pela indentação — não por um marcador escrito pelo programador. Toda vez que uma linha aparece mais recuada que a linha anterior, um bloco é empilhado; toda vez que uma linha volta a um recuo já visto, os blocos correspondentes são desempilhados.

#### A Unidade de Indentação — 2 espaços ou 1 TAB

Um nível de indentação é, em qualquer ponto do programa, ou exatamente 2 espaços, ou exatamente 1 caractere TAB — nunca uma mistura dos dois, nunca uma contagem diferente. O primeiro corpo de bloco encontrado em cada escopo define a unidade vigente ali (ver 4.3); a partir daí, cada nível adicional de aninhamento soma mais uma unidade da mesma espécie.

```tinypine
if true
  print("AB")
```

#### Fechamento por Múltiplos Níveis

Uma linha pode devolver o recuo diretamente a um nível vários blocos acima do mais interno, fechando de uma só vez todos os blocos intermediários — o equivalente automático ao antigo `end n` (Apêndice A.6): não existe mais um marcador para isso, o próprio recuo da linha seguinte já informa quantos blocos fecham.

```tinypine
if B
  print("AB")
  repeat 3
    pause 1
print("fora de tudo")
```

*print("fora de tudo") recua direto ao nível 0, fechando repeat e if de uma vez — equivalente ao antigo end 2*

### Mistura de Estilos

Misturar TAB e espaço como unidade de indentação dentro do mesmo escopo é a única combinação proibida (Capítulo 4.2.1). "Mesmo escopo", aqui, é a cadeia de blocos atualmente abertos: uma vez que ela se fecha por completo — o programa volta ao recuo zero — um novo bloco pode recomeçar com a outra unidade sem violar a regra, ainda que isso não seja recomendado, por prejudicar a leitura. Misturar as duas unidades dentro da mesma cadeia de blocos abertos é um erro léxico: `MixedIndentation PROBLEM` (Capítulo 3.3).

```tinypine
if B
  print("AB")
	print("erro")
```

*A segunda linha usa TAB onde a primeira já havia fixado 2 espaços como unidade — MixedIndentation PROBLEM*

### Regra de Segurança de Fechamento

Não é permitido que uma linha volte a um recuo que não corresponda a nenhum bloco atualmente aberto — ou seja, pousar numa coluna intermediária entre dois níveis válidos. Esta regra é formalizada, com seus casos de borda, na Seção 36.1: `IndentMismatch PROBLEM`.

```tinypine
if A
  print("A")
 print("B")
```

*A terceira linha usa 1 espaço — não corresponde nem ao nível 0 nem ao nível de 2 espaços do bloco aberto — IndentMismatch PROBLEM*

### Blocos Encadeados — else, else if, catch, finally

`else`, else if, `catch` e `finally` são sempre escritos exatamente no recuo do `if`, else if ou `try` que abrem a cadeia — nunca mais recuados. Como o corpo do bloco anterior já termina assim que o recuo volta a esse nível, a transição é automática: não existe marcador para "reabrir" a cadeia, e não é possível inserir uma linha entre o fim de um bloco e o início do próximo `else`/`elif`/`catch`/`finally` sem quebrar a cadeia.

```tinypine
if condição
  ...
else
  ...
```

**Regra de compatibilidade:** `else` e else if só encadeiam com um bloco `if` ou else if imediatamente anterior, no mesmo recuo; `catch` e `finally` só encadeiam com um bloco `try` imediatamente anterior, no mesmo recuo (Capítulo 24).

### Papel Único dos Parênteses — if, while, return, ...

`()` tem uma responsabilidade única em toda a linguagem: chamada de função e agrupamento de expressões. As palavras-chave `if`, `while`, `return,` etc. não usam `()` como delimitador do valor que recebem.

- `()` **— chamadas de função e agrupamento de expressões;**

- **O recuo (indentação) — fecha um bloco/contexto ao diminuir (Capítulo 4.2).**

```tinypine
if condicao
  ...
while ativo
  ...
return valor;
```

*^- Sintaxe atual*

O `return` não abre um bloco — por isso não depende de recuo — e é encerrado por `;` para marcar de forma inequívoca o fim da instrução.

Quando a condição realmente exige agrupamento por precedência de operadores, `()` continua disponível — exclusivamente com esse papel:

```tinypine
if (A + B) > C
  ...
```

*^- Agrupamento de expressão, não argumento do if*

> ***Nota:** o parser aceita as mesmas expressões e a mesma precedência de operadores em qualquer contexto —* `()` *tem, em qualquer ponto da linguagem, um único significado: agrupar expressão ou chamar função.*

### Papel Único do ; — fecha uma linha e inicia outra

`var S = "Serpente"

if "" != S
  pause len(S)+5*len(S);`

> ***Nota:** Não obrigatório pois o TinyPine,  
> tem um sistema inteligente que faz uma análise semântica*

### Estilo Alternativo de Abertura — Delimitador:  do ... --

A partir da 0.7, todo bloco também pode ser aberto por `do` ao final da assinatura e fechado por `--` em uma linha própria — uma segunda forma, plenamente equivalente ao estilo por indentação (Capítulo 4.1), válida para qualquer construção que abra bloco na linguagem (if, while, for, repeat, try/catch/finally, function, classe, função anônima). Dentro de um bloco `do` ... `--`, a indentação é puramente visual: o bloco só termina no `-- `correspondente, não importa a coluna em que o corpo esteja escrito.

```tinypine
if true do
print(1)
--
```

`:` aninhados do mesmo estilo fecham como parênteses: cada nível precisa do seu próprio `--`, e o `--` mais próximo sempre fecha o `:` mais interno ainda aberto.

```tinypine
if true do
if true or false do
print("dois níveis")
--
--
```

nesta revisão: o estilo `do` ... `--` cobre o caso — e se generaliza a qualquer bloco da linguagem, não apenas ao corpo de uma instrução condicional.

```tinypine
while true do print(1) --

if x: to-bool
print(1)
```

*':' aqui é conversão (to-bool é palavra reservada) — o bloco do if abre por indentação na linha seguinte*

```tinypine
if x do
print(1)
--
```

*'do' aqui abre bloco (nada reservado o segue) — fecha em '--'*

### Proibição de Mistura entre Estilos

Os dois estilos de abertura de bloco (indentação, Capítulo 4.1; delimitador, Capítulo 4.8) não podem se aninhar um dentro do outro: um bloco aberto por indentação não pode conter, aninhado, um bloco aberto por `do ... --`, e um bloco `do ... --` não pode conter, aninhado, um bloco aberto por indentação. Misturar os dois estilos dentro da mesma cadeia de blocos abertos é um erro léxico: `MixedBlockStyle PROBLEM` (Capítulo 3.3).

Blocos irmãos — lado a lado, sem um estar aninhado dentro do outro — podem usar estilos diferentes livremente; a proibição vale só para aninhamento.

```tinypine
if true
if true do
print(1)
--
```

*MixedBlockStyle PROBLEM — o if interno abre por do dentro de um bloco já aberto por indentação*

```tinypine
if true do print(1) --
if true or false
print("estilos diferentes, mas irmãos — permitido")
```

### Blocos Encadeados em Estilo Delimitador

No estilo `do ... --` (Capítulo 4.8), a regra de encadeamento de `else`, `else if`, `catch` e `finally` (Capítulo 4.5) muda de forma: como a indentação não tem efeito nesse estilo, a exigência de "mesmo recuo" (4.5) é substituída por "logo após o `--` que fecha o bloco anterior" — nenhuma instrução pode aparecer entre o `--` e a próxima palavra da cadeia, sob pena de quebrar o encadeamento. Além disso, pela regra de não mistura (Capítulo 4.9), toda a cadeia — `if`, `else if` e `else`; ou `try`, `catch` e `finally` — deve manter o mesmo estilo do início ao fim: não é possível abrir a cadeia com `do` e encadear um bloco por indentação, nem o inverso.

```tinypine
if condição: do
...
--
Else do
...
--
```
