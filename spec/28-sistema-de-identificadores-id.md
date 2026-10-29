## Sistema de Identificadores (`id`)

Identificadores permitem declarar blocos nomeados de código. A resolução de identificadores ocorre antes da etapa de Execução, num passo sobre os *tokens* (ver Capítulo 35). Isso permite que um identificador seja referenciado independentemente da ordem textual de sua declaração.

`id` é um **criador**, como `var`, `const`, `f` e `class`: o nome vem logo depois da palavra, **sem aspas**, e uma referência a ele é o próprio nome, **sem `@`**.

### Declaração

```tinypine
id msg
  print("olá")
```

O bloco associado ao identificador `msg` é registrado, mas seu conteúdo não é avaliado nem executado durante o registro.

O nome de um `id` segue **as mesmas regras de nome dos outros criadores** (Capítulo 3.4 e 3.4.1): um nome como `I=ÇJ`, que `var` recusaria por vários motivos (`=` e `Ç` não são permitidos), é recusado do mesmo jeito em `id I=ÇJ`; uma palavra reservada não serve de nome; e `$`, que é só de variáveis, não é aceito em `id`. O corpo é um bloco por indentação ou `do ... --` (Capítulo 4.8).

Comentários dentro da declaração não fazem parte do conteúdo guardado: são removidos pelo analisador léxico, como em qualquer lugar (Capítulo 3.1). No exemplo abaixo, o conteúdo de `soma` é só o operador `+`:

```tinypine
id soma  # um comentário na linha da declaração
  + || um comentário no meio do corpo — não é guardado ||
```

### Chamada

```tinypine
msg
```

Referencia-se um identificador **escrevendo o nome**, sem prefixo. A referência `msg` é resolvida para o conteúdo associado ao identificador `msg`. O conteúdo resultante é então avaliado conforme as regras de execução do TinyPine.

Uma ocorrência do nome é uma **referência** em qualquer posição de código, **exceto**: (a) depois de um `.` (`objeto.msg` é um membro, não o id); (b) como nome externo escrito `msg=valor` numa lista de argumentos (Capítulo 30.3); (c) na própria declaração `id msg`. O texto dentro de uma string — inclusive entre `{ }` de um `format` — não é código nesse passo e **não** é expandido.

### Registro de IDs

O interpretador coleta os identificadores antes da análise sintática: primeiro todas as declarações `id nome` do arquivo, depois a substituição das referências. Por isso um identificador pode ser referenciado independentemente da ordem textual de sua declaração.

O registro independe de o bloco correspondente ser efetivamente executado.

### Propriedades dos Identificadores

* **Imutabilidade:** identificadores não podem ser redefinidos após sua criação.
* **Registro antecipado:** identificadores são registrados antes da análise sintática (passo sobre os tokens, Capítulo 35).
* **Um nome, um significado:** o nome de um `id` é reservado no arquivo **inteiro**. Declarar o mesmo nome duas vezes, ou usá-lo como nome de outro criador (`var`, `const`, `f`, `class`, apelido de `load ... as`, parâmetro de função, variável de `for` ou de `catch`), em qualquer escopo, gera `IdDuplicate PROBLEM` (E110). O motivo é que a substituição acontece antes da análise de escopos: o mesmo nome não pode significar duas coisas.
* **Nome sem declaração:** como o nome de um `id` é um identificador comum, não existe mais um erro próprio para "id inexistente": um nome que não é de `id`, variável nem função segue a regra de `IdNotFound PROBLEM` (E308).
* **Forma antiga:** `id "nome"` (com aspas) e `@nome` não existem mais; ambos são `DeprecatedSyntax PROBLEM` (E118), assim como `id("nome")` antes deles. A declaração é sempre `id nome`, e a referência é sempre `nome`.

### Expansão da referência

A referência `nome` é substituída, no ponto em que aparece, pelo conteúdo do bloco `id nome`, antes da análise sintática do programa. Assim, `nome` pode ocupar qualquer posição em que o conteúdo caberia, inclusive dentro de uma expressão (como no exemplo abaixo, em que o conteúdo é um operador).

- `nome` sozinho no começo de um statement cola o corpo linha a linha, no recuo da linha da referência. Os blocos aninhados do corpo (`if`, `for`, `while`...) são mantidos e acompanham esse recuo; assim o mesmo identificador funciona no nível principal, dentro de um `if` ou dentro de uma função.
- `nome` no meio de uma expressão cola o corpo em linha, e as quebras de linha internas, se houver, viram `;`.
- O conteúdo é colado como está: não há parênteses implícitos, então a precedência do conteúdo segue a da posição onde é colado.
- Uma referência a si mesmo, direta ou indireta (`id a` usa `b` e `id b` usa `a`), é `CircularIdReference PROBLEM` (E202).
- As referências a outros `id` dentro do corpo de cada `id` são conferidas mesmo que esse `id` nunca seja usado: um ciclo é erro antes da execução, não só quando o corpo é colado.

### Forma da declaração

`id` só declara quando é a primeira palavra de um statement e vem seguido de um identificador. Em qualquer outra posição (por exemplo `"id"` como chave de dicionário ou de parâmetro nomeado, ou `w.id` depois de um `.`) não é declaração. Seguido de uma string (`id "nome"`), é a forma antiga (`DeprecatedSyntax`, E118); seguido de qualquer outra coisa, `ParserError PROBLEM`.

No bloco por indentação, a linha seguinte precisa estar mais recuada que o `id`; caso contrário o bloco está vazio e é `EmptyBlock PROBLEM` (E105), e a linha seguinte não é tomada como corpo.

### Terminal interativo

No terminal interativo (REPL) cada entrada é um programa à parte, mas os identificadores declarados numa entrada valem nas seguintes, como as variáveis. Redeclarar um nome já declarado numa entrada anterior é `IdDuplicate PROBLEM`. O comando `.reset` descarta os identificadores junto com o resto do estado.

### Exemplo

```tinypine
print(100 mais 100)

id mais
  +
```

Nesse exemplo, `mais` referencia o conteúdo associado ao identificador `mais`, declarado posteriormente no código-fonte: o programa é lido como `print(100 + 100)`.
