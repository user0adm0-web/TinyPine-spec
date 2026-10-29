## Casos de Borda Formalizados

Esta seção formaliza o comportamento esperado do interpretador para entradas em casos extremos ou inesperados, complementando os casos já formalizados junto a cada construção específica (por exemplo, `pause` no Capítulo 26.4, e os erros léxicos do Capítulo 3.3). Todo erro reportado pelo interpretador segue o formato em bloco descrito na Seção 36.7. Nenhum erro é silencioso.

### Indentação

| **Entrada**                                                                          | **Comportamento formal**                                                                                                           |
|--------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Recuo de fechamento intermediário (não corresponde a nenhum bloco atualmente aberto) | `IndentMismatch PROBLEM` — nenhum bloco aberto está nesse nível de recuo; sucede o antigo `ScopeUnderflow PROBLEM` (Apêndice A.6). |
| Cabeçalho de bloco sem corpo (nem linha recuada em seguida, nem `do`)                | `EmptyBlock PROBLEM` — todo bloco precisa de ao menos uma instrução; não há bloco vazio silencioso.                                |
| TAB e espaço combinados no mesmo escopo, ou recuo inesperado                         | Ver `MixedIndentation PROBLEM` e `UnexpectedIndent PROBLEM` (Capítulo 3.3).                                                        |
| Função anônima dentro de `( )`, `[ ]` ou `{ }` sem nenhuma linha recuada depois do cabeçalho | `EmptyBlock PROBLEM` — a linha que fecha o delimitador não conta como corpo (Capítulo 4.11).                                |
| Linha recuada no máximo como a linha do `f`, ou delimitador de fechamento, depois do corpo de uma função anônima em colchetes | Encerra o corpo da função; a linha não é parte dele (Capítulo 4.11).                                               |

### repeat

| **Entrada**  | **Comportamento formal**                                                 |
|--------------|--------------------------------------------------------------------------|
| `repeat 0`   | O bloco não é executado nenhuma vez. Sem erro, sem aviso.                |
| `repeat -1`  | `InvalidRepeatCount PROBLEM` — `repeat` requer um inteiro não negativo.  |
| `repeat 1.5` | `InvalidRepeatCount PROBLEM` — `repeat` requer um inteiro, não um float. |

### Índices de Coleções

| **Entrada**  | **Comportamento formal**                                                     |
|--------------|------------------------------------------------------------------------------|
| `lista[-1]`  | há acesso reverso a partir do fim da coleção.                                |
| `lista[999]` | `IndexOutOfBounds PROBLEM` — o índice informado excede o tamanho da coleção. |

### Sistema de Identificadores

| **Caso**                        | **Comportamento formal**                                                                                                                                                                      |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ID em bloco não executado       | O identificador existe e é registrado normalmente. IDs são resolvidos na etapa de *parsing*, antes da execução (Capítulo 35) — o fato de o bloco pai não ser executado não impede o registro. |
| IDs duplicados                  | `IdDuplicate PROBLEM` — o mesmo nome de identificador não pode ser declarado duas vezes no mesmo programa, nem reutilizado por outro criador (Capítulo 28.4).                                                                                    |
| Referências circulares          | `CircularIdReference PROBLEM` — um `id` que, direta ou indiretamente, referencia a si mesmo pelo nome (Capítulo 28.2).                                                                       |

### try sem catch

Ver Capítulo 24.3.

### Chamadas e Declaração de Funções

Ver Capítulo 30.9.

### Formato de Saída de Erros e Avisos

Todo erro e todo aviso emitido pelo interpretador é reportado em um único formato, em bloco, pensado para ser lido por pessoas: diz **o que** aconteceu, **onde**, se o programa **continua** (ou se o erro é **recuperável**) e **como corrigir**. Este formato substitui a linha única `line(N): error CODIGO, because: MENSAGEM` e a notação `warning[codigo]` usadas até esta revisão, e é o único formato de diagnóstico da linguagem.

**Idioma.** Todos os textos que o interpretador imprime no bloco — rótulos fixos, mensagem, dica e menu — são em **inglês**, independentemente do idioma desta especificação. Os nomes e os códigos também não são traduzidos.

Exemplo canônico de erro, para o programa `C:\Projetos\teste.tpine`, cuja linha 12 é `print(10 / 0)`:

```tinypine
=== DivisionByZero (E301) PROBLEM ===

We found a problem in the file:
C:\Projetos\teste.tpine

   11 | print("start")
|> 12 | print(10 / 0)
              ^^^^^^
   13 | print("end")

Line 12, characters 7 to 12.
Recoverable error with try.

It is not possible to divide a number by zero.

Hint: check the divisor used or wrap the operation in a try.

=== END ERROR ===

Press 0 to re-run, press 1 for complex diagnostics, press 2 to open the file at the error, press 3 to copy this error, press ENTER to exit
>_
```

*Exemplo 1 — erro de execução recuperável (DivisionByZero, E301)*

**Anatomia do bloco.** O bloco tem sempre as mesmas partes, na mesma ordem. As partes marcadas “erro” ou “aviso” existem só nesse tipo de diagnóstico:

| **Parte**         | **Como aparece**                                                                                                                   | **Regra**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Cabeçalho         | `=== Nome (Ennn) PROBLEM ===` ou `=== Nome (Wnnn) WARNING ===`                                                                     | Nome em PascalCase, código distinto entre parênteses e a palavra fixa PROBLEM (erro) ou WARNING (aviso), entre `===`. Nome e código identificam o mesmo diagnóstico e são os usados em toda esta especificação.                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Arquivo           | `We found a problem in the file:` (erro) ou `We found something worth checking in the file:` (aviso); na linha seguinte, o caminho | Caminho completo do arquivo em que ocorreu o problema; em programas com `import` (Cap. 29.3), é o arquivo importado, não o principal.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Trecho de código  | `\|> 12 \| print(10 / 0)` e, abaixo, uma linha de `^`                                                                                | Mostra a linha do problema com uma linha de contexto antes e outra depois, quando existem. A linha do problema leva o marcador `\|>` à esquerda; os números ficam alinhados à direita, antes de `\|`. Sob ela, uma linha de `^` marca o **menor trecho responsável** pelo problema (em `print(10 / 0)`, a operação `10 / 0`, e não a linha inteira nem os parênteses ao redor), um `^` por caractere, alinhado em coluna (o bloco é sempre exibido em fonte monoespaçada). Um TAB é mostrado como um único `→`, para não quebrar o alinhamento. Se o problema ocupa várias linhas, cada linha do trecho recebe `\|>` e a sua própria linha de `^`. |
| Posição           | `Line 12, characters 7 to 12.` ou `Lines 2 to 4.`                                                                                  | Linha e colunas contadas a partir de 1 sobre a linha física, incluindo recuos; as duas extremidades são incluídas. Um trecho de um único caractere usa o singular: `Line 3, character 11.` Um trecho de várias linhas informa só o intervalo de linhas.                                                                                                                                                                                                                                                                                                                                                                                         |
| Situação          | `Recoverable error with try.` / `Unrecoverable error.` (erro); `The program keeps running.` (aviso)                                | Em erros, informa se um bloco `try` / `catch` (Cap. 24) é capaz de interceptar o erro: erros da etapa de Execução (Cap. 35, etapa 8) são recuperáveis; erros léxicos, sintáticos e de verificação estática (etapas 1 a 7) acontecem antes da execução e não são. Em avisos, informa que a execução não é interrompida.                                                                                                                                                                                                                                                                                                                          |
| Mensagem          | Uma frase em inglês                                                                                                                | Descreve o que aconteceu em termos do programa do usuário, sem jargão interno do interpretador; uma única frase, terminada em ponto final.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Dica              | `Hint: check the divisor ...`                                                                                                      | Uma frase com a ação sugerida para corrigir o problema, iniciada em minúscula após `Hint: `. Todo erro e todo aviso tem mensagem e dica (tabelas adiante).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Pilha de chamadas | `Call stack (most recent call last):`                                                                                              | Opcional, só em erros. Aparece quando o erro ocorre dentro de uma função (ver abaixo).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Rodapé            | `=== END ERROR ===` ou `=== END WARNING ===`                                                                                       | Marca o fim do bloco, separando o diagnóstico da saída normal do programa.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Menu              | `Press 0 to re-run ...` e `>_`                                                                                                     | Só em erros, e só em terminal interativo (ver abaixo).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

**Avisos.** Um aviso usa o mesmo bloco, com três diferenças: o cabeçalho termina em WARNING e o rodapé é `=== END WARNING ===`; a linha de situação é `The program keeps running.`; e não há pilha de chamadas nem menu, porque o programa segue em execução. Um programa pode emitir vários avisos; cada um é um bloco.

**Esconder avisos.** Um aviso pode ser escondido com a instrução `#~ hide Wnnn` (ou `#~ hide the Wnnn`) (Capítulo 3.1.1): o bloco simplesmente não é emitido. Só avisos podem ser escondidos; erros nunca.

```tinypine
=== UnusedVariable (W201) WARNING ===

We found something worth checking in the file:
C:\Projetos\teste.tpine

   2 | var a = 1
|> 3 | var name = "Dhavi"
           ^^^^
   4 | print(a)

Line 3, characters 5 to 8.
The program keeps running.

Variable "name" was declared but never used.

Hint: use it, or remove the declaration.

=== END WARNING ===
```

*Exemplo 2 — aviso (UnusedVariable, W201)*

**Pilha de chamadas.** Quando o erro ocorre dentro de uma função, o bloco inclui, depois da dica, a pilha de chamadas, da chamada mais antiga para a mais recente: cada linha traz o arquivo, a linha e o nome da função (`main` para o nível superior do programa). A última linha é sempre o ponto do erro. Erros de nível superior não têm pilha.

```tinypine
=== IndexOutOfBounds (E402) PROBLEM ===

We found a problem in the file:
C:\Projetos\teste.tpine

   7 |   var items = [1, 2, 3]
|> 8 |   print(items[999])
               ^^^^^^^^^^

Line 8, characters 9 to 18.
Recoverable error with try.

The index 999 is outside the size of the collection.

Hint: check the size of the collection before accessing the index.

Call stack (most recent call last):
  C:\Projetos\teste.tpine, line 20, in main
  C:\Projetos\teste.tpine, line 8, in A

=== END ERROR ===

Press 0 to re-run, press 1 for complex diagnostics, press 2 to open the file at the error, press 3 to copy this error, press ENTER to exit
>_
```

*Exemplo 3 — erro dentro de uma função, com pilha de chamadas (IndexOutOfBounds, E402)*

**Dicas automáticas.** Em `IdNotFound`, se existe no escopo um identificador visível cuja distância de edição (Levenshtein) para o nome usado é de no máximo 2, a dica começa com `did you mean 'x'?`, com o mais próximo (em empate, o declarado mais recentemente). Em `ParserError` por token inesperado, a dica diz o que era esperado naquele ponto (por exemplo, `an operator or the end of the line was expected here`).

**Menu interativo.** Depois do rodapé de um erro, o interpretador exibe o menu abaixo, seguido do cursor de entrada `>_`, e aguarda uma tecla:

> `Press 0 to re-run, press 1 for complex diagnostics, press 2 to open the file at the error, press 3 to copy this error, press ENTER to exit`

| **Tecla** | **Efeito**                                                                                                                                       |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `0`       | Re-executa o programa desde o início, no mesmo arquivo.                                                                                          |
| `1`       | Exibe o diagnóstico complexo: informações técnicas adicionais sobre o erro. O conteúdo exato ainda não está fechado (ver Histórico, Apêndice A). |
| `2`       | Abre o arquivo no editor, posicionado na linha do erro. Como o editor é escolhido ainda não está fechado (ver Histórico, Apêndice A).            |
| `3`       | Copia para a área de transferência o texto do bloco, sem o menu e sem cores.                                                                     |
| `ENTER`   | Encerra o interpretador.                                                                                                                         |

**Quando o menu aparece.** O menu só é exibido quando a entrada e a saída padrão são terminais interativos. Em qualquer outro caso (saída redirecionada para arquivo ou pipe, CI, execução por script) o bloco é impresso sem menu e nada fica aguardando tecla. Um erro não capturado encerra o interpretador com código de saída 1, inclusive quando o menu é encerrado com `ENTER`; um programa que termina sem erro não capturado sai com 0, mesmo que tenha emitido avisos.

**Modo --plain.** Com a opção `--plain`, cada diagnóstico vira uma única linha, no formato `arquivo:linha:coluna: error|warning Nome (Código): mensagem`, própria para editores, CI e `grep`. Não há trecho de código, dica, pilha, menu nem cores. A coluna é a do início do trecho marcado; quando não há posição (por exemplo, `CircularIdReference`), a linha traz só `arquivo: error Nome (Código): mensagem`.

```tinypine
C:\Projetos\teste.tpine:12:7: error DivisionByZero (E301): It is not possible to divide a number by zero.
C:\Projetos\teste.tpine:2:3: error MixedBlockStyle (E106): Mixed block styles: a block opened by indentation cannot contain a block opened by ':' ... '--'.
C:\Projetos\teste.tpine:3:5: warning UnusedVariable (W201): Variable "name" was declared but never used.
```

*Exemplo 4 — saída em modo --plain*

**Cores.** Em terminal com suporte a cores, o cabeçalho, o marcador `|>` e os `^` saem em vermelho (erro) ou amarelo (aviso), e a linha `Hint:` sai em amarelo nos dois casos; o restante usa a cor padrão do terminal. As cores são desligadas quando a saída não é um terminal, quando a variável de ambiente `NO_COLOR` está definida e no modo `--plain`. O texto do bloco é idêntico com ou sem cores.

**Código.** Cada erro e cada aviso tem um código distinto, que nunca é reutilizado por outro diagnóstico nem alterado depois de publicado. Erros usam `E` + três dígitos; avisos usam `W` + três dígitos. O primeiro dígito indica a fase, com o mesmo significado nos dois casos: `1xx` léxico e sintático; `2xx` análise estática; `3xx` execução — valores, tipos e fluxo; `4xx` coleções; `5xx` chamadas de função; `6xx` módulos; `E9xx` legado (só erros). Variantes do mesmo diagnóstico (por exemplo, os quatro casos de `ParserError`) compartilham o código e diferem na mensagem.

**Erros capturados.** Um erro interceptado por `try` / `catch` (Cap. 24) não é impresso: o bloco só é exibido quando o erro não é capturado. O objeto recebido por `catch(err)` é a string da mensagem do erro, isto é, a frase da linha de mensagem do bloco. Avisos emitidos dentro de um `try` continuam sendo impressos.

**Um bloco de erro por execução.** Um erro não capturado interrompe a execução; portanto cada execução exibe, no máximo, um bloco de erro — o do primeiro erro encontrado, na ordem do pipeline (Cap. 35). Avisos não têm esse limite.

**Notação nesta especificação.** Um diagnóstico é citado pelo nome do cabeçalho seguido de PROBLEM ou WARNING, por exemplo `DivisionByZero PROBLEM` e `UnusedVariable WARNING`; nas tabelas de catálogo, o código acompanha o nome (`DivisionByZero (E301) PROBLEM`). Os códigos `error[snake_case]` e `warning[snake_case]` usados até esta revisão foram substituídos pelo nome equivalente em PascalCase (`index_out_of_bounds` passa a `IndexOutOfBounds`). Anotações que antes eram texto livre em exemplos (`# erro`, `Warning: ...`) passaram a citar o nome do diagnóstico correspondente. Os registros históricos do Apêndice A mantêm a notação da época.

**Erros: mensagens-padrão e dicas.** A tabela a seguir fixa o código, a recuperabilidade, a mensagem e a dica de cada erro. Valores de exemplo (como `@` ou `12.5.7`) são ilustrativos: o interpretador os substitui pelos valores reais do programa. As descrições dos demais capítulos continuam sendo a referência normativa de quando cada diagnóstico ocorre; estas tabelas definem o que é exibido.

| **Code** | **Name**                      | **Rec.** | **Message**                                                                                                                                              | **Hint**                                                                                                                      |
|----------|-------------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `E101`   | `ParserError`                 | No       | Unexpected character '@'.                                                                                                                                | an operator or the end of the line was expected here; remove the character or, if it is part of a text, put it inside quotes. |
| `E101`   | `ParserError`                 | No       | Unterminated string: the closing quote is missing.                                                                                                       | close the string with a quote before the end of the line.                                                                     |
| `E101`   | `ParserError`                 | No       | Malformed number '12.5.7'.                                                                                                                               | a number can have at most one decimal point.                                                                                  |
| `E101`   | `ParserError`                 | No       | 'unpack A' is only valid in a call's argument list or inside a list literal (to declare a variadic parameter use 'package A' in the function signature). | to expand a collection use unpack in a call or list literal; to declare a variadic parameter write package in the signature.  |
| `E102`   | `MixedIndentation`            | No       | Mixed TABs and spaces in the indentation of the same scope.                                                                                              | use only 2 spaces, or only 1 TAB, per indentation level within the same scope.                                                |
| `E103`   | `UnexpectedIndent`            | No       | Unexpected indent: the line is more indented than the previous one, which does not open a block.                                                         | remove the extra indentation or open a block on the previous line.                                                            |
| `E104`   | `IndentMismatch`              | No       | The indentation of this line does not match any open block.                                                                                              | align the line with the indentation of an open block (multiples of 2 spaces, or of 1 TAB).                                    |
| `E105`   | `EmptyBlock`                  | No       | Block without a body: every block needs at least one statement.                                                                                          | write at least one indented statement below the block header, or remove the block.                                            |
| `E106`   | `MixedBlockStyle`             | No       | Mixed block styles: a block opened by indentation cannot contain a block opened by ':' ... '--'.                                                         | use the same style in all nested blocks: only indentation, or only ':' and '--'.                                              |
| `E107`   | `MixedCollectionLiteral`      | No       | Loose value inside { }: a dictionary requires key: value pairs.                                                                                          | use key: value pairs inside { }, or replace { } with \[ \] to create a list.                                                  |
| `E108`   | `MultipleElseMatch`           | No       | More than one else clause in the same case block.                                                                                                        | keep a single else clause per case block.                                                                                     |
| `E110`   | `IdDuplicate`                 | No       | The identifier "spawn" has already been declared in this program.                                                                                        | choose a different name for the second id "nome".                                                                                  |
| `E110`   | `IdDuplicate`                 | No       | The alias 'Y' has already been declared in this program.                                                                                                 | choose a different name for the alias in load ... as.                                                                         |
| `E111`   | `InvalidBangMarker`           | No       | Invalid use of '!' in the parameter list.                                                                                                                | after ! declare only named parameters (they can only be passed by name; add = value to make one optional): f G(!, "A": e).    |
| `E112`   | `InvalidVariadicParam`        | No       | Invalid use of the variadic parameter package args.                                                                                                      | declare package after the positional parameters, without a default value and without an external name.                        |
| `E113`   | `ReservedSymbol`              | No       | The symbol '~' is reserved and cannot start the name of a variable or function.                                                                          | remove the '~'; the only built-in object is ~Program.                                                                         |
| `E113`   | `ReservedSymbol`              | No       | Unknown built-in object '~Outro'.                                                                                                                        | the only built-in object is ~Program.                                                                                         |
| `E118`   | `DeprecatedSyntax`            | No       | The syntax 'id "msg"' no longer exists. | write id msg (no quotes) to declare, and the bare name msg to refer to it; '@' is no longer a prefix. For a wildcard use a group such as [1*1] inside a format string, not the sequence \*. |
| `E124`   | `ConversionInRefinement`      | No       | The conversion ': to-str' is not accepted inside a refinement: a restriction only checks the value, it never converts it. | remove the conversion from the restriction; convert the value before the declaration, or use an assertion such as key 0: str. |
| `E125`   | `InvalidPatternGroup`         | No       | The group '[abc]' in the format string is not valid: only a wildcard such as [*] or [2*4] and a Unicode group such as [u+2222] are accepted. | to write a literal bracket use \[ and \]; to use a variable put it in braces: [{B}*{A}]; a Unicode group is written in hexadecimal: [u+2222]. |
| `E125`   | `InvalidPatternGroup`         | Yes      | The pattern bounds are not valid: the minimum 5 is greater than the maximum 3. | use non-negative integers with the minimum not greater than the maximum; a code point must be between 0 and 10FFFF (hexadecimal) and not a surrogate (D800 to DFFF). |
| E123     | InvalidQuestionMarker         | No       | Invalid use of '?' in the parameter list.                                                                                                                | after ? declare typed parameters, each with a different type: f A(?, e: int, a: str).                                         |
| `E201`   | `StaticTypeMismatch`          | No       | The value "a" is incompatible with the declared type of A (int).                                                                                         | assign a value of type int or remove the type declaration from A.                                                             |
| `E202`   | `CircularIdReference`         | No       | Circular reference between identifiers: 'a' → 'b' → 'a'.                                                                   | break the cycle by removing one of the references.                                                                            |
| `E301`   | `DivisionByZero`              | Yes      | It is not possible to divide a number by zero.                                                                                                           | check the divisor used or wrap the operation in a try.                                                                        |
| `E308`   | `IdNotFound`                  | Yes      | The identifier 'totl' was not found.                                                                                                                     | did you mean 'total'? Otherwise, declare 'totl' before using it.                                                              |
| `E306`   | `InvalidRepeatCount`          | Yes      | repeat requires a non-negative integer; got -1.                                                                                                          | use 0 or a positive integer, for example: repeat 3.                                                                           |
| `E306`   | `InvalidRepeatCount`          | Yes      | repeat requires an integer; got 1.5 (float).                                                                                                             | convert the value to an integer: repeat 1.5: to-int.                                                                          |
| `E307`   | `InvalidPauseDuration`        | Yes      | The pause duration cannot be negative.                                                                                                                   | use 0 or a positive number of seconds, for example: pause 1.                                                                  |
| `E307`   | `InvalidPauseDuration`        | Yes      | The given value is not a valid duration.                                                                                                                 | use a real number of seconds, for example: pause 0.5.                                                                         |
| `E303`   | `TypeError`                   | Yes      | pause requires a number; got a string.                                                                                                                   | convert the string explicitly: pause "1": to-num.                                                                             |
| `E302`   | `TypeMismatch`                | Yes      | The of operator does not work on strings.                                                                                                                | to look for a piece of text, use in: "A" in "ARROZ".                                                                          |
| `E302`   | `TypeMismatch`                | Yes      | Cannot add "str" and "int" — string concatenation requires both operands to be strings.                                                                  | convert explicitly with a conversion such as : to-num or : to-str before the operation.                                       |
| `E302`   | `TypeMismatch`                | Yes      | The value 123 is not of type str.                                                                                                                        | to get a text, convert with : to-str instead of using a type assertion.                                                       |
| `E304`   | `PrecisionExceeded`           | Yes      | The calculated value exceeds the physical capacity of the hardware.                                                                                      | simplify the mathematical expression or reduce the exponent to prevent hardware overflow.                                     |
| `E305`   | `InvalidConversion`           | Yes      | void cannot be converted to bool.                                                                                                                        | assign a value to AA before converting it.                                                                                    |
| `E401`   | `KeyNotFound`                 | Yes      | The key "y" does not exist in the collection.                                                                                                            | use .add() to create a new entry.                                                                                             |
| `E402`   | `IndexOutOfBounds`            | Yes      | The index 999 is outside the size of the collection.                                                                                                     | check the size of the collection before accessing the index.                                                                  |
| `E311`   | `ConstReassignment`           | Yes      | A is const and does not accept reassignment.                                                                                                             | declare A with var if it needs to be reassigned.                                                                              |
| `E312`   | `ImmutableMutation`           | Yes      | B is const and its contents cannot be changed.                                                                                                           | declare B with var or create a new collection with the desired contents.                                                      |
| `E312`   | `ImmutableMutation`           | Yes      | A tuple never accepts content mutation.                                                                                                                  | use a list if the contents need to change.                                                                                    |
| `E316`   | `RefinementViolation`         | Yes      | The value 200 does not satisfy the restriction 'value < 100' of type int.                                                                                | use a value that satisfies the restriction, or relax the restriction in the type.                                             |
| `E313`   | `ReadOnlyProperty`            | Yes      | ~Program.path is read-only and does not accept assignment.                                                                                               | read the value into a variable instead: var p = ~Program.path.                                                                |
| `E314`   | `LoadFileNotFound`            | Yes      | The file "util.tpine" was not found.                                                                                                                     | check the path; a relative path is resolved from the file that contains the load.                                             |
| `E315`   | `CircularLoad`                | Yes      | Circular load: 'a.tpine' → 'b.tpine' → 'a.tpine'.                                                                                                        | break the cycle by removing one of the load statements.                                                                       |
| `E310`   | `UncaughtThrow`               | Yes      | Exception thrown with throw and not caught: "failed to load".                                                                                            | wrap the code in a try with a catch to handle the exception.                                                                  |
| `E309`   | `InvalidSpecialBlock`         | Yes      | Unknown special block: 'banana'.                                                                                                                         | check the special block name in the specification.                                                                            |
| `E501`   | `MissingArgument`             | Yes      | Missing argument for parameter 'e', which has no default value.                                                                                          | pass a value for 'e' or declare a default: f A(e = 0).                                                                        |
| `E502`   | `MissingNamedArgument`        | Yes      | Missing required named argument "A".                                                                                                                     | pass it by name: G("A": 10).                                                                                                  |
| `E503`   | `UnknownNamedArgument`        | Yes      | No parameter has the external name "B".                                                                                                                  | check the external names declared in the function signature.                                                                  |
| `E504`   | `PositionalForNamedOnly`      | Yes      | Unexpected positional argument: parameter "A" only accepts being passed by name.                                                                         | pass the value by name: G("A": 10).                                                                                           |
| `E505`   | `NamedForPositionalOnly`      | Yes      | Parameter 'e' is positional and does not accept being passed by name.                                                                                    | pass the value by position: A(10).                                                                                            |
| `E506`   | `DuplicateArgument`           | Yes      | Parameter "A" has already received a value.                                                                                                              | pass each parameter only once.                                                                                                |
| `E507`   | `TooManyArguments`            | Yes      | Too many arguments: the function accepts 1 and received 2.                                                                                               | remove the extra argument or declare package args to capture the remaining ones.                                              |
| `E601`   | `InvalidRandomRange`          | Yes      | The minimum (10) is greater than the maximum (1).                                                                                                        | swap the limits: random.int("min":1, "max":10).                                                                               |
| `E602`   | `EmptyCollectionPick`         | Yes      | It is not possible to pick an element from an empty collection.                                                                                          | check that the collection has elements before using random.pick.                                                              |
| `E603`   | `InvalidSeedType`             | Yes      | The seed must be an integer; got 3.14 (float).                                                                                                           | use an integer as the seed: random.seed(3).                                                                                   |
| `E604`   | `InvalidProbabilityRange`     | Yes      | The probability must be between 0.0 and 1.0; got -0.5.                                                                                                   | use a value from 0.0 to 1.0, for example: random.bool(0.5).                                                                   |
| E617     | InvalidKey                    | Yes      | Unknown key name "xyz".                                                                                                                                  | use a key name such as "e", "space", "enter", "up" or "f1".                                                                   |
| E618     | ComputerKeyboardError         | Yes      | computer.keyboard.press: the keyboard could not be accessed.                                                                                             | check that keyboard access is available in this environment.                                                                  |
| `E901`   | `ScopeUnderflow`              | Yes      | end 3 tries to close more blocks than are open. (legacy: end n was removed in 0.6)                                                                       | reduce the end count or remove it: since 0.6, blocks close by indentation.                                                    |
| `E902`   | `InvalidEndCount`             | Yes      | end() does not accept a negative value; got -1. (legacy: end n was removed in 0.6)                                                                       | remove the end: since 0.6, blocks close by indentation.                                                                       |

**Avisos: mensagens-padrão e dicas.** Mesma regra da tabela anterior; avisos nunca interrompem a execução.

| **Code** | **Name**                 | **Message**                                                                           | **Hint**                                                           |
|----------|--------------------------|---------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| `W101`   | `InvalidDirective`       | Unknown instruction 'show' after '#~'.                                                | write a valid instruction after '#~', for example: #~ hide the W301.|
| `W102`   | `UnknownMention`         | 'W999' is not a known warning.                                                        | mention a warning by its code (W301) or by its name (ImplicitVoid).|
| `W201`   | `UnusedVariable`         | Variable "name" was declared but never used.                                          | use it, or remove the declaration.                                 |
| `W202`   | `NameReuse`              | The name 'print' is already in use by a built-in function.                            | choose a different name so the original is not hidden.             |
| `W203`   | `UnreachableCode`        | This code is never executed: it comes after a return.                                 | remove the code, or change the flow so that it can be reached.     |
| `W204`   | `UnusedFunction`         | Function 'name' was declared but never called.                                        | call it, or remove the declaration.                                |
| `W301`   | `ImplicitVoid`           | No value was given for 'score': it was set to void.                                   | assign a value, for example: var score = 0.                        |
| `W302`   | `PrecisionLoss`          | Precision lost converting value to int: the value was truncated via : to-int.         | make sure truncation is what you want; the original value is lost. |
| `W303`   | `ImplicitBoolConversion` | The bool true was implicitly converted to the number 1 in a numeric operation.        | convert explicitly with : to-num to make the intent clear.         |
| `W304`   | `ValueIsVoid`            | The key "x" exists but has no value: the access returned void.                        | assign a value to the key before reading it.                       |
| `W305`   | `MatchWithoutElse`       | No pattern matched and the case block has no else clause: nothing was executed.       | add an else clause to handle the other values.                     |
| `W306`   | `NoopPause`              | pause 0 does nothing: execution continues immediately.                                | remove the pause or use a duration greater than 0.                 |
| `W307`   | `UncaughtInTry`          | A try without catch caught an error: "It is not possible to divide a number by zero." | add a catch block to handle the error explicitly.                  |
