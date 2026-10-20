# Apêndices

## Apêndice A — Histórico da Especificação

Este apêndice é *informativo*: registra como a especificação chegou ao estado descrito nos capítulos 1–42 (normativos), mas não define, por si só, nenhuma regra da linguagem. Ele reúne, num único lugar cronológico e categorizado, tudo que em revisões anteriores deste documento aparecia espalhado — como notas dentro dos próprios capítulos técnicos — comparando o texto atual com versões anteriores. Essa separação segue a prática comum de manter um *cronologia de mudanças* (changelog) fora do corpo normativo: o leitor que só quer saber "como a linguagem se comporta hoje" lê os capítulos 1–42 sem interrupção; quem quer entender "por que ela chegou a esse comportamento" lê este apêndice.

Toda referência de capítulo abaixo aponta para o texto normativo correspondente, já com a decisão aplicada.

### Resumo — Contradições Identificadas e Resolvidas

| **\#** | **Elemento**                                   | **Cap.**    | **Natureza da contradição**                                                                                                                                                                                                  | **Status**                                                                                                                                                                    |
|--------|------------------------------------------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A1     | Retorno implícito de funções                   | 30.2 / 31.1 | Funções nomeadas nunca retornavam a última expressão implicitamente; a regra publicada para funções anônimas afirmava o oposto.                                                                                              | **Aceita** — unificado: nenhuma das duas formas tem retorno implícito.                                                                                                        |
| A2     | Papéis de `is`/`really is` vs. `is`/`==`/`===` | 11.1        | `is` (minúsculo) fazia igualdade de valor/estrutura; `really is` exigia também mesmo tipo; `==` era banido. O exemplo de `is` já demonstrava comparação estrutural, apesar de o texto descrevê-lo como restrito a escalares. | **Aceita** — papéis redistribuídos: `is` compara só tipo, `==` assume valor/estrutura, `===` assume tipo+valor; `really is` removido, `!=`/`!==` voltam como açúcar de `not`. |
| A3     | Unidade de tempo em `pause`                    | 26.4        | Duas tabelas de casos de borda para o mesmo comportamento; uma contrariava a própria regra de que milissegundos nunca são unidade pública.                                                                                   | Resolvida (consolidação editorial — não exigia decisão de projeto).                                                                                                           |
| A4     | Namespace `debug`                              | 29.1 / 34.5 | Usado simultaneamente para um bloco de controle nativo já especificado e para um módulo importável ainda planejado, com sintaxes de chamada diferentes.                                                                      | **Aceita em princípio** — nome definitivo do módulo de inspeção ainda a confirmar.                                                                                            |
| A5     | Política de chave inexistente em coleções      | 19.3        | Delegada a "uma política padrão" nunca definida; o único exemplo disponível ilustrava, na verdade, um caso distinto (chave existente com valor `void`).                                                                      | **Aceita** — `void` para chave existente sem valor (aviso renomeado); `error[key_not_found]` para chave ausente (erro novo).                                                  |
| A6     | Descrição do pipeline de processamento         | 35          | Duas descrições, de granularidade e terminologia diferentes, para as mesmas etapas internas do interpretador.                                                                                                                | Resolvida (consolidação editorial — não exigia decisão de projeto).                                                                                                           |

As decisões marcadas **Aceita** foram confirmadas pelo autor do projeto; as demais permanecem disponíveis para confirmação, ajuste ou rejeição.

### Itens Pendentes de Definição

| **\#** | **Item**                                                                                                                                                                                                                                                                           | **Capítulo** | **Prioridade**                                                                   |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------------|
| B1     | Especificação individual das operações universais de texto (str)                                                                                                                                                                                                                   | 16           | Alta — afeta o tipo mais usado da linguagem. Adição já planejada pelo autor.     |
| B2     | Módulos `system`, `time`, `json`, `scene`, `web` sem funções especificadas                                                                                                                                                                                                         | 34.1         | Alta — módulos centrais anunciados, sem conteúdo normativo.                      |
| B3     | \~~Sintaxe de edição/adição em coleções mutáveis\~~                                                                                                                                                                                                                                | 19.4         | **Resolvido** — `add()`/`remove()`                                               |
| B4     | Especificação comportamental do módulo output — o módulo não consta mais da tabela do Cap. 34.1 nem tem seção própria (a antiga 34.5 foi removida); a saída é tratada por print/println (Cap. 20)                                                                                  | 20           | Média — confirmar se o módulo ainda é planejado.                                 |
| B5     | Comportamento de cada operador aritmético sobre cada par de tipos primitivos (precedência geral já definida em 12.1)                                                                                                                                                               | 13           | Média.                                                                           |
| B6     | Comportamento completo de `.length` (que substitui `len()`)                                                                                                                                                                                                                                                     | 33.3         | Média.                                                                           |
| B7     | Etapa "Expansão de Aliases" do pipeline — mencionada em versões anteriores deste documento, nunca definida em nenhum capítulo                                                                                                                                                      | 35           | Média.                                                                           |
| B8     | Sistema de objetos: herança, interfaces, métodos privados/estáticos, sobrecarga                                                                                                                                                                                                    | 40           | Baixa — declarado pelo próprio projeto como futuro.                              |
| B9     | Gerenciamento de memória (GC vs. contagem de referências)                                                                                                                                                                                                                          | 41           | Baixa — declarado pelo próprio projeto como futuro.                              |
| B10    | Sintaxe de referência a um identificador já existente, após a remoção do prefixo `#`                                                                                                                                                                                               | 28.2         | Média — funcionalidade descrita, sem sintaxe válida atual.                       |
| B11    | Conjunto fechado de funções do módulo `math`                                                                                                                                                                                                                                       | 34.2         | Baixa — tabela já é funcional, apenas não fechada.                               |
| B12    | Assinatura completa, parâmetros nomeados e comportamento de erro de create/write/delete/copy/move/exists/env do módulo os (Cap. 34.6) — comportamento de read já definido                                                                                                          | 34.6         | Média — tabela de funções já é normativa, comportamento de erro ainda não.       |
| B13    | Comportamento de erro de computer.clipboard e computer.keyboard (press, pressed, write), nomes de tecla aceitos e comportamento por plataforma (Cap. 34.7) — comportamento de shell já definido; app e read foram removidos do módulo                                              | 34.7         | Média — tabela de funções já é normativa, comportamento de erro ainda não.       |
| B14    | Semântica formal do operador `\|>` em caso de destino inválido, e tipo do valor retornado quando o destino não produz saída                                                                                                                                                         | 34.8         | Média.                                                                           |
| B15    | Comportamento do operador if pós-fixo (Cap. 12.4) como argumento de função definida pelo usuário — a omissão exigida em print/println não tem regra definida para aridade fixa/posicional; hoje o argumento vira void em vez de deslocar os parâmetros seguintes                   | 12.4         | Média.                                                                           |
| B16    | Conteúdo do diagnóstico complexo (opção 1 do menu de erro, Cap. 36.7) e comportamento do menu para teclas diferentes de 0, 1, 2, 3 e ENTER                                                                                                                                         | 36.7         | Média.                                                                           |
| B17    | Opções 2 e 3 do menu de erro (Cap. 36.7): como o editor é escolhido e configurado, e o que acontece quando o editor ou a área de transferência não estão disponíveis                                                                                                               | 36.7         | Média.                                                                           |
| B18    | Pilha de chamadas (Cap. 36.7): limite de profundidade em recursão profunda e formato dos quadros em arquivos importados e em funções anônimas                                                                                                                                      | 36.7         | Baixa.                                                                           |
| B19    | Sintaxe de load (Cap. 29.5): manter load "caminho" as Y (palavras reservadas, resolvível antes da execução) ou migrar para uma função do módulo os, os.load("caminho", "as": "Y") — comparação logo abaixo da tabela                                                               | 29.5         | Média — decisão de design em aberto; o Cap. 29.5 continua normativo.             |
| B20    | computer.read() era bloqueante — pendência encerrada: a função foi removida do módulo (Cap. 34.7). A leitura de teclado não bloqueante já existe em computer.keyboard.pressed                                                                                                      | 34.7         | Encerrada.                                                                       |
| B21    | Ligação posicional com package e parâmetros nomeados opcionais: o nomeado opcional (antes de !) também aceita posição e entra na sequência posicional (30.3, 30.8) — ver explicação logo abaixo da tabela                                                                          | 30.3, 30.8   | Baixa — mitigada: nomeados depois de ! só por nome e com padrão resolvem o caso. |
| B22    | unpack: desempacote de dicionário dentro de literal de lista; colisão entre as chaves de um dicionário expandido e argumentos nomeados explícitos (hoje, DuplicateArgument)                                                                                                        | 19.4.1       | Média.                                                                           |
| B23    | Consumo de gerador (emit) fora de print/println com um único argumento posicional: hoje a função roda até o fim e devolve a lista dos valores emitidos                                                                                                                             | 23.2.2       | Média.                                                                           |
| B24    | Marcador ? (Cap. 30.4.1): regras fixadas pelo interpretador sem previsão na especificação (não coexistir com package, no máximo uma seção, só antes de !, tipos únicos) e escolha entre tipos que se sobrepõem (int e float, tipo dinâmico) — ver explicação logo abaixo da tabela | 30.4.1       | Média.                                                                           |
| B25    | Módulo computer (Cap. 34.7): nomes de tecla e apelidos, janela de 200 ms de pressed fora do Windows, dependência de xdotool e de ferramentas de clipboard no Linux/macOS, valores de output-type do shell                                                                          | 34.7         | Baixa — comportamento já implementado.                                           |
| B26    | Chamada de função guardada em coleção por índice: `D["chave"](...)` e a chamada direta de elemento de lista — hoje `ParserError PROBLEM`; a função só é chamada depois de lida para uma variável. A chamada com ponto em dicionário (`D.chave(...)`) foi definida (Cap. 19.2.2, 31.3) | 19.2.2, 31.3 | Baixa — parcialmente resolvida: o caso `console.log(...)` funciona. |
| B27    | Tipos refinados `tipo\restrição\` (Cap. 6.9) e acesso `key K` / `value V` (Cap. 19.2): pontos em aberto — ver explicação logo abaixo da tabela                                                                                                                                        | 6.9, 19.2    | Alta — recurso novo, decisão do autor ainda incompleta.             |
| B28    | Interpolação `{ }` com expressões (Cap. 20.2): resultado de `format "{A-A}"` e de `format "{A.length}"` com `var A = 1` (ambos válidos, resultado não definido)                                                                                                                       | 20.2         | Média.                                                              |
| B29    | Tipagem estruturada por `\...\`, união `\|` e tipo `function` (Cap. 6.7 a 6.9): tipos aninhados sem equivalente, quando falha e com qual erro, `\|` fora de `keys:`/`values:`, `\|` e `\|\|`, `keys` fora de `dict` — ver explicação logo abaixo da tabela          | 6.7 a 6.9    | Alta — recurso novo, decisão do autor ainda incompleta.             |

**B19 — sintaxe de load (decisão em aberto).** Hoje vale `load "caminho" as Y` (Capítulo 29.5). A alternativa em discussão é uma função de `os`: `os.load("caminho", "as": "Y")`. Nenhuma das duas foi adotada em definitivo; o Capítulo 29.5 continua normativo.

- **A favor de** `load ... as`**:** leitura natural; o apelido é um identificador léxico, então o nome `Y` é conhecido antes da execução e entra na Análise Estática (Capítulo 35); consistente com `import` (29.3).

- **Contra** `load ... as`**:** reserva duas palavras (`load` e `as`); é uma forma sintática especial, fora do modelo de módulos do Capítulo 34.

- **A favor de** `os.load(...)`**:** não reserva palavra; é modular e consistente com os (34.6), que já lida com arquivos.

- **Contra** `os.load(...)`**:** a função precisaria criar um nome (`Y`) no escopo do chamador — nenhuma função de módulo declara identificadores hoje — e, com o apelido vindo de um texto, a análise estática de `Y.A` deixaria de ser possível antes da execução; `os` manipula recursos do ambiente, não nomes do programa. Além disso, `as: "Y"` sem aspas não é argumento nomeado válido (Capítulo 20.1): teria de ser `"as": "Y"` ou `as="Y"` (Capítulo 30.3).

**B21 — package com nomeados opcionais (mitigada).** A Alternativa A (Capítulos 30.3 e 30.6) torna válidas as declarações com nomeados antes ou depois de `package`, mas não muda a ligação dos argumentos (Capítulo 30.8): um nomeado opcional (sem `!` antes dele) também aceita posição e entra na sequência posicional, antes do variádico. Assim, com `f out(package ARGS, "last": END = "", "sep": SEP = "", "flush": FLUSH = true)`, a chamada `out(10, 49, 63)` liga `END = 10`, `SEP = 49`, `FLUSH = 63` e `ARGS = []`, e `out(10, 49, 63, "last": "-")` é `DuplicateArgument PROBLEM`. **Solução adotada:** declarar os nomeados depois de `!`, onde só podem ser passados por nome e podem ter valor padrão (Capítulos 30.3 e 30.8): com `f out(package ARGS, !, "last": END = "", "sep": SEP = "", "flush": FLUSH = true)`, `out(10, 49, 63)` liga `ARGS = [10, 49, 63]` e `out(10, 49, 63, "last": "-")` liga `ARGS = [10, 49, 63]` e `END = "-"`. Continua em aberto, como regra geral, se um nomeado sem `!` numa assinatura com `package` deveria deixar de aceitar posição.

**B24 — marcador** `?` **(decisões do interpretador).** A especificação original só trazia o exemplo `f a(?, e: int, a: str)` (30.4.1). Foram fixados no interpretador, sem previsão no texto: `?` aparece no máximo uma vez, antes de `!`; não coexiste com `package`; sem nome externo; tipo obrigatório e único por parâmetro; o argumento liga ao primeiro parâmetro tipado livre, na ordem de declaração, que aceita o seu tipo. Consequência a decidir: um `int` aceito por um `float` livre (com ImplicitNumericConversion WARNING) pode tirar o argumento do `int` seguinte — com `f F(?, x: float, y: int)`, `F(2, 2.5)` é `TypeMismatch PROBLEM`, e `F(2.5, 2)` funciona. As alternativas são preferir o tipo exato antes do conversível ou proibir tipos sobrepostos na mesma seção.

**B25 — módulo** `computer`**.** Fixados no interpretador, sem previsão no texto: o conjunto de nomes de tecla e seus apelidos; `"output-type"` do shell como `"0"` (êxito) ou `"1"` (falha); `pressed` fora do Windows como janela de 200 ms sobre eventos do terminal, que consome as teclas lidas; `press`/`write` no Linux por `xdotool`; área de transferência no Linux/macOS por `wl-copy`/`wl-paste`, `xclip`, `xsel`, `pbcopy`/`pbpaste`. O exemplo original de saída do shell (`"input": "Write-Output"`, `"output": " Hello World!"`) não é reproduzível por um processo real e foi substituído por `"input"` com o comando inteiro e `"output"` sem o espaço inicial.

**B26 — chamada de função guardada em coleção (parcialmente resolvida).** `D.chave(...)` foi definida: chama a função guardada na chave de um dicionário (Capítulo 19.2.2 e 31.3), com `KeyNotFound PROBLEM` para chave ausente e `TypeMismatch PROBLEM` para valor que não é função; `add` e `remove` continuam sendo os métodos da coleção. Fica em aberto a chamada por índice, `D["chave"](...)` (hoje `ParserError PROBLEM`), e a de elemento de lista (`L[0](...)`), que exigiriam que uma expressão de índice aceitasse parênteses logo depois.

- **A favor de também permitir a forma por índice:** é a única maneira de chamar uma chave que não é um identificador válido (`D["meu-log"](...)`) ou que se chama `add`/`remove`; é coerente com a função ser valor de primeira classe (Capítulo 31.1).

- **Contra:** `X[i](...)` mudaria a gramática de chamada (hoje só um nome ou um método é chamado); a leitura para uma variável já resolve o caso.


**B27 — tipos refinados e acesso por** `key`**/**`value`**.** Decididos (Cap. 6.9 e 19.2): a sintaxe `tipo\restrição\` (que substituiu a primeira proposta, com `<...>`), os tipos aceitos, as propriedades `value`, `length`, `key K` e `value V`, as regras de validação, os operadores, as condições separadas por vírgula e o erro `RefinementViolation (E316)`. O código E316 foi escolhido na redação desta revisão e pode ser trocado. Em aberto:

- **`value V`.** O exemplo `A[value 2] # 2` (com `var A = [1, 2, 3, 4]`) não diz se `value V` procura o valor `V` na coleção ou lê o segundo valor contando de 1 — e, na primeira leitura, o que acontece quando o valor não existe. O mesmo vale para `value 2 < 3` em `[1, 2, 3]: list\values: int, value 2 < 3, key 0==1\`.

- **Perda do acesso à chave por posição.** `key K` e `value V` substituem as formas `key, N` e `value, N` (e `key:N` / `value:N`); com elas saiu a única maneira de ler a **chave** armazenada numa posição de um dicionário. Dizer se isso é intencional ou se ganha outra forma.

- **`values`.** *Resolvido na pós-0.7:* `values: T` afirma que todo valor da coleção é do tipo `T`, e `keys: T` faz o mesmo com as chaves (Cap. 6.8 e 6.9).

- **Chave ausente dentro de uma restrição.** Em `{1: ""}: dict\key "a"==1 or key 1==""\` a chave `"a"` não existe: dá `KeyNotFound PROBLEM` (Cap. 19.3) ou a condição é simplesmente falsa?

- **Conversão dentro da restrição.** `[1, 0]: list\key 0: to-str\` termina com `["1", 0]`, ou seja, a restrição altera o valor; a regra 2 diz que a restrição é avaliada depois da conversão. Falta dizer qual das duas formas de conversão vale quando se combinam.

- **Onde se aplica.** Os exemplos mostram a asserção e a declaração de `var`; a gramática provisória permite o tipo refinado em qualquer posição de `Type` (parâmetro e retorno de função, Cap. 30.3 e 30.4), o que ainda não foi confirmado. Como combina com a tipagem estruturada (Cap. 6.8) está resolvido — `list<...>`/`dict<...>` foram substituídas por `keys:`/`values:` dentro do próprio tipo refinado —, e `.type` não é afetado (Cap. 6.7). Falta dizer o que o tipo refinado significa em parâmetro e retorno.

- **Tipo que não aceita refinamento** (por exemplo `bool`): o erro não está definido.

- **Verificação estática.** Hoje a verificação é na execução (Cap. 35); antecipar para literais fica para depois.

- **Nome do tipo.** O rascunho original escrevia `tupla`; a especificação usa `tuple` (Cap. 19.5) e foi o que entrou.

**B28 — interpolação com expressões.** O autor confirmou que `var A = 1` seguido de `format "{A-A}"` e de `format "{A.length}"` é válido (Cap. 20.2). Não está dito (a) se `{A-A}` é a subtração `A - A`, apesar de a regra do Cap. 3.4.1 tratar `A-A` colado como um nome, e (b) qual é o `.length` de um número (Cap. 33.3).

**B29 — tipagem estruturada por** `\...\`**, união** `|` **e tipo** `function`**.** Decididos (Cap. 6.7 a 6.9): `list<...>` e `dict<...>` deixam de existir, e nenhum tipo usa `<...>`; a tipagem estruturada é o tipo refinado com `keys:` (chaves de `dict`) e `values:` (valores de `list`, `dict` e `tuple`); o operador `|` é a união de tipos ("ou"), no lugar de `<T1, T2>` e de `[T1, T2]`; `function` é um tipo novo e `.type` de uma função devolve `"function"`. Em aberto:

- **Tipos aninhados.** `dict<str, dict<str, int>>` declarava a estrutura interna; a regra do Cap. 3.2 (a restrição é fechada pela próxima `\`) impede uma restrição dentro de outra, então hoje só existe `values: dict`, sem estrutura interna. Opções: (a) manter assim; (b) permitir aninhamento com uma regra de pareamento das barras; (c) outra forma de declarar o tipo interno.

- **Quando falha, e com qual erro.** Foi mantido o comportamento da anotação antiga — `keys:`/`values:` em declaração, parâmetro e retorno são verificados estaticamente (`StaticTypeMismatch`, E201), e em asserção direta sobre um valor, na execução (`RefinementViolation`, E316). Confirmar se é isso, ou se tudo passa a ser E316, ou tudo estático.

- **`|` em qualquer posição de tipo.** A união foi escrita como válida em toda posição de tipo (asserção, var/const, parâmetro, retorno), não só dentro de `keys:`/`values:`. Não está definido como ela combina com o marcador `?` (Cap. 30.4.1, B24: "cada tipo aparece uma só vez" — a quais argumentos `e: int | str` se liga?), com o `:` de asserção num argumento de chamada (Cap. 30.7) e com valor padrão.

- **Lexer.** `||` abre comentário de bloco, então `str||int` (sem espaços) não é uma união; `|>` é o pipe. O `|` solto fora de posição de tipo foi escrito como `ParserError`.

- **`keys` fora de `dict`.** Em lista e tupla as chaves são os índices (`key K`, Cap. 19.2); `keys:` num tipo `list`/`tuple` não foi definido. Também não está dito o erro de usar `keys`/`values` em tipo que não aceita refinamento (mesma lacuna de B27).

- **`function`.** Não está dito se `.type` de método de classe e de função nativa de módulo (por exemplo `math.sqrt`) também é `function`, nem se `function` precisa ser tratada como nome reservado.

### Decisões Aceitas — Sintaxe e Semântica

Mudanças de comportamento ou de sintaxe já confirmadas pelo autor do projeto, além das já registradas em A.1:

- **Papéis de comparação redistribuídos (Cap. 11) —** `is` **passa a comparar só tipo;** `==` **assume valor/estrutura;** `===` **assume tipo+valor;** `really is` **é removido.**

- `!=`**/**`!==` **voltam como açúcar sintático de** `not` **(Cap. 11.3 / 12.1) — haviam sido banidos numa revisão anterior.**

- `in` **em lista/dicionário passa a testar índice/chave, não mais valor — quem testa valor agora é** `of` **(Cap. 12.3).**

- **Papel único dos parênteses (Cap. 4.6) —** `if`**/**`while`**/**`return` **deixam de usar** `()` **como delimitador de argumento;** `()` **passa a significar, em toda a linguagem, só chamada de função e agrupamento de expressão.**

- **Parêntese opcional em** `break`**/**`continue`**/**`pause`**/**`repeat` **(Cap. 23.3, 26, 27) — mesmo estilo do item acima; a forma com parênteses continua válida.**

- `for` **sem parênteses no cabeçalho, passo movido para o corpo (Cap. 23.2) — a forma com passo no cabeçalho (23.2.1) continua coexistindo.**

- **Remoção do modificador retroativo de** `repeat` **(Cap. 27) — o prefixo** `#` **e a soma de múltiplas ocorrências no mesmo bloco-alvo deixam de existir;** `repeat n` **passa a ser sempre um bloco autônomo, atuando só para frente. Como consequência direta, a sintaxe de referência a um identificador já existente (Cap. 28.2, que dependia do mesmo prefixo** `#`**) ficou sem forma válida (ver B10).**

- **Remoção dos operadores** `>>`**/**`<<` **(Cap. 19.4) — substituídos por** `colecao.add()`**/**`colecao.remove()`

- **Escape** `\n`**/**`\r` **restrito a literais de string (Cap. 3.2) — o uso solto como argumento posicional de** `print()` **foi removido.**

- **Módulos file, input e clipboard descontinuados (Cap. 34.1) — funcionalidade absorvida por** `os (arquivos, Cap. 34.6)` **e por** `computer`

- **\|\> adicionado à lista de operadores-palavra (Cap. 3.4.1) e à tabela de precedência geral (Cap. 12.1), com a prioridade mais baixa da tabela — abaixo de** `( )`**.**

- **readln() ganha três argumentos nomeados de representação visual —** `show`**,** `sep` **e** `last` **(Cap. 21.1, novo) — coexistem com** `min`**/**`max`**/**`active` **sem alterá-los; controlam só a exibição da entrada no console, nunca o valor retornado.**

- **Novo operador if pós-expressão (Cap. 12.4, novo) — adicionado à lista de operadores-palavra (Cap. 3.4.1) e à tabela de precedência geral (Cap. 12.1), com a menor prioridade da linguagem, abaixo até de** `|>`**. Distinto da estrutura condicional de bloco do Capítulo 22, que permanece inalterada.**

- **Função anônima com corpo por indentação dentro de** `( )`**,** `[ ]` **ou** `{ }` **(Cap. 4.11, 31.3) — o corpo é medido a partir da linha do** `f` **e termina em linha recuada no máximo como ela ou no delimitador de fechamento. O uso já era previsto pelo exemplo do Capítulo 31 (função como argumento em várias linhas), mas o interpretador o rejeitava com** `EmptyBlock PROBLEM`**; a regra passa a estar escrita.**

- **Valor de função em coleção e leitura de chave de dicionário por ponto (Cap. 19.2.2, 31.3) —** `D.chave` **equivale a** `D["chave"]` **para leitura; a chamada direta com ponto, `D.chave(...)`, está definida (Cap. 19.2.2); a chamada por índice permanece indefinida (B26).**

- **Padrão de repasse** `package` **+** `unpack` **(Cap. 30.6) — a função variádica entrega seus argumentos, um a um, a outra chamada, como em** `f(package ARGS) print(unpack ARGS)`**.**

- **Tipos refinados (Cap. 6.9) —** `tipo\restrição\`**, em** `int`**,** `float`**,** `decim`**,** `num`**,** `str`**,** `list`**,** `dict` **e** `tuple`**, com as propriedades** `value`**,** `length`**,** `key K` **e** `value V`**. A barra invertida (Cap. 3.2) substituiu o rascunho com** `<...>` **para não colidir com** `<`**,** `>`**,** `<=` **e** `>=`**. Erro novo:** `RefinementViolation (E316)`**. Pontos em aberto em B27.**

- **Propriedade** `.length` **(Cap. 33.3) —** `A.length` **substitui** `len(A)`**, com o mesmo comportamento; os exemplos dos Capítulos 4 e 23 foram atualizados.**

- **Acesso explícito** `colecao[key K]` **e** `colecao[value V]` **(Cap. 19.2) — substituem** `key, N`**,** `value, N` **e** `key:N`**/**`value:N`**; em lista e tupla a chave é o índice, então** `A[key 0]` **é o primeiro elemento. A mensagem** `TypeMismatch` **"Lists have no keys" (Cap. 36.7) foi removida. Pontos em aberto em B27.**

- **Interpolação** `{ }` **aceita expressões e propriedades (Cap. 20.2) —** `format "{A-A}"` **e** `format "{A.length}"` **são válidos; resultado em aberto (B28).**

### Corrigido

Erros factuais ou de conteúdo no texto de revisões anteriores, sem impacto no comportamento normativo atual (já descrito corretamente nos capítulos 1–42):

- **Descrição de** `math.degrees()` **trocada de "eleva ℯ à potência do número" (função exponencial, incompatível com o próprio exemplo) para conversão de radianos para graus (Cap. 34.2).**

- **Nomes** `random.float.set()`**/**`random.bool.set()` **corrigidos para** `random.float()`**/**`random.bool()` **— o sufixo** `.set()` **é reservado para conversão explícita de tipo (Cap. 8), e colidia de forma enganosa com esse mecanismo (Cap. 34.4.3).**

- **Literal** `infinite` **(grafia incorreta) corrigido para** `Infinity`**, o literal formalmente definido, em exemplo de comparação com** `NaN` **(Cap. 7.4).**

- **Exemplo de interpolação de string usava** `Var $A = "Top"` **(maiúsculo indevido e prefixo global desnecessário); corrigido para** `var A = "Top"` **(Cap. 20).**

- **Exemplo de** `pause` **dentro de laço usava** `i++`**, operador nunca definido em nenhum outro ponto da especificação; corrigido para a forma de passo já padronizada (**`i = i + 1`**, Cap. 26.2).**

- **Exemplo do módulo** `random` **(Cap. 34.4.5) usava** `match (run): (1): ... --`**, sintaxe que não corresponde à gramática normativa de** `case`**/**`match` **(Cap. 25); reescrito como** `case run: is 1: ... -- --`**.**

- **Tabela de casos de borda de** `pause` **estava duplicada em dois capítulos, com uma inconsistência de unidade entre as cópias (uma delas descrevia milissegundos, contrariando a regra de que a unidade pública é sempre o segundo); consolidada em uma única fonte normativa (Cap. 26.4).**

- **Referência numérica às etapas do pipeline ("Registro de IDs (6)", "Execução (8)") não batia com a numeração da própria tabela do capítulo (etapas 5 e 7); corrigida (Cap. 35).**

- **Capítulo 1 dizia que este documento era a especificação oficial "na versão** `0.4`**", desatualizado desde a própria migração 0.4 → 0.5, que já havia avançado a capa para** `0.5`**; corrigido para acompanhar a versão vigente do documento (Cap. 1).**

### Padronização e Reorganização Estrutural

Sem impacto no comportamento da linguagem — só forma, nomenclatura e organização do documento:

- **Códigos de erro padronizados para a notação** `error[nome_do_codigo]` **(minúsculo, entre colchetes) em todo o documento — o catálogo de erros usava PascalCase (Cap. 37).**

- **Título de cada capítulo alinhado à sua entrada no Sumário (ex.: Capítulo 27 aparecia como "Modificadores de Bloco" no Sumário e "repeat — Bloco de Repetição" no corpo).**

- **Listas numeradas com numeração inicial incorreta (herdada de numeração automática do documento original) corrigidas para começar em 1: regras de funções anônimas (Cap. 31.1, pulava do item 4 pro 6), passos de instanciação de classe (Cap. 32.3, começava em 6), alternativas de gerenciamento de memória (Cap. 41, começava em 10).**

- **Referência cruzada ao apêndice de decisões de projeto corrigida de "Apêndice E" para "Apêndice A" (Cap. 2.5), refletindo a consolidação de apêndices desta revisão.**

- **Duas descrições de pipeline de processamento, com granularidade e terminologia diferentes, unificadas em um único pipeline normativo de 8 etapas (Cap. 35).**

- **Dois capítulos de importação de módulos, não contíguos e com conteúdo sobreposto, unificados em um único capítulo (Cap. 33).**

- **Duas ocorrências de documentação sobre** `tuple` **unificadas em uma única seção (Cap. 19.5).**

- **Conteúdo do módulo** `math`**, antes dividido entre um capítulo-resumo e a referência completa, unificado em um único local (Cap. 34.2).**

- **Renumeração completa da hierarquia de capítulos — o documento original reutilizava o número "3" para dois capítulos distintos, e pulava do capítulo 22 para o 24, sem capítulo 23.**

- **Toda mensagem de erro embutida em exemplo de código revisada para usar exclusivamente a notação** `error[...]`**/**`warning[...]` **(nunca texto livre).**

### Registro de Decisões de Projeto

Estrutura viva, reservada para o registro formal de decisões tomadas ao longo do desenvolvimento da linguagem que não se enquadrem como correção de contradição (A.1) nem como padronização editorial (A.5) — por exemplo, a escolha entre alternativas de design ainda em aberto. Nenhuma decisão desse tipo havia sido registrada até esta revisão; a seção é mantida como reserva, a ser preenchida incrementalmente.

**Migração 0.4 → 0.5 (revisão completa, decisões travadas pelo autor):** revisão de ruptura, tocando léxico, tipagem, coleções, operadores e blocos. Resumo das decisões; ver os capítulos citados para o texto normativo completo:

- **Coleções (Cap. 19):** `[ ]` **passa a significar sempre lista e** `{ }` **sempre dicionário — nunca mais decidido pela forma dos elementos. Chaves numéricas passam a ser aceitas em dicionário. Uma coleção vazia (**`[]` **ou** `{}`**) deixa de representar** `void` **— já nasce tipada.**

- **Tipagem (Cap. 5, 6, 8, 9, 10): os prefixos de asserção (**`str`**,** `num`**,** `int`**,** `float`**,** `decim`**,** `bool`**) e as conversões** `tipo.set(valor)` **são substituídos por um único sufixo pós-fixado:** `valor: tipo` **para asserção rígida e** `valor: to-tipo` **para conversão explícita. na versão posterior (0.7) a tipagem estática e a coerção automática de inteiros para ponto flutuante (int \|\> float) foram oficializadas para aproximar o comportamento ao do Python.**

- **Tuplas e const (Cap. 18.2, 19.5):** `tuple` **deixa de ser prefixo de tipo e passa a ser função nativa,** `tuple(...)`**, única forma de criar tupla.** `const` **passa a impedir tanto a reatribuição do identificador quanto a mutação do conteúdo, mesmo fora de tuplas.**

- **Operadores-palavra (Cap. 3.4.1, 11, 12):** `is`**,** `and`**,** `or`**,** `xor`**,** `not`**,** `in`**,** `of`**,** `to` **passam a ser grafados em minúsculas; a restrição do Cap. 3.4.1 contra identificador 100% maiúsculo é removida.** `SEND-TO` **é removido e substituído pelo operador** `|>` **(Cap. 34.8). O operador condicional pós-fixo if (Cap. 12.4) é removido sem substituto direto de expressão — decisão revertida depois, ver A.6.**

- **Blocos (Cap. 4): a abertura de bloco por** `:` **é removida em toda a linguagem — todo bloco abre pela quebra de linha após a assinatura. Nova palavra-chave** `do` **funciona como escape explícito para um corpo de instrução única na mesma linha (**`if true do print("oi") --`**).**

- **Comentários (Cap. 3.1): restam apenas duas formas —** `#` **para linha e** `|| ... ||` **para bloco. O inline simples** `| ...` **e o bloco decorado** `|X| ... |X|` **são removidos.**

- **Erros (Cap. 17, 24):** `.try` **e** `.try.catch(err)` **são removidos por completo —** `try` **/** `catch` **em bloco (Cap. 24) passa a ser o único modelo de recuperação de erro da linguagem.**

- **Correspondência por padrão (Cap. 3.2.3, 11.2): o curinga** `\*` **deixa de operar sobre** `==`**, que passa a ser sempre igualdade literal pura; a correspondência por padrão passa a ser feita por** `.match()` **ou pelo operador** `~=`**.**

Escopo desta revisão: reescrita normativa dos capítulos afetados, exemplos de código correspondentes e Sumário. Numeração de capítulo preservada onde possível para não quebrar referências cruzadas existentes; capítulos inteiramente removidos (17, 12.4) foram mantidos como títulos com aviso de remoção, em vez de renumerados, pelo mesmo motivo — o Cap. 12.4 deixou de se enquadrar nisso numa revisão posterior (ver A.6): a remoção foi revertida, e ele voltou a ser capítulo normativo pleno, sem aviso de remoção nenhum.

**Migração 0.5 → 0.6 (revisão de sintaxe de blocos):** o delimitador de fechamento de bloco por `--` — o primeiro delimitador de fechamento da linguagem, em uso desde a v0.1 — é retirado e marcado como histórico; blocos passam a fechar pela indentação (Capítulo 4). Resumo das decisões:

- **Unidade de indentação (Cap. 4.2.1): cada nível de bloco equivale a exatamente 2 espaços ou exatamente 1 TAB, nunca aos dois ao mesmo tempo dentro do mesmo escopo (a cadeia de blocos atualmente abertos). Misturar as duas unidades nesse escopo é** `error[mixed_indentation]` **(Cap. 3.3, novo).**

- **Fechamento por múltiplos níveis (Cap. 4.2.2):** `end n` **é retirado — dedentar diretamente vários níveis fecha os blocos correspondentes de uma só vez, sem marcador.**

- **Blocos encadeados (Cap. 4.5, antigo "Fechamento Automático de Blocos"): deixa de ser uma exceção sobre quando se pode omitir** `--` **e passa a ser o comportamento geral —** `else`**/**`elif`**/**`catch`**/**`finally` **apenas precisam estar no mesmo recuo do bloco que encadeiam.**

- **Regra de Segurança de Fechamento (Cap. 4.4, 36.1): reformulada para recuo —** `error[indent_mismatch]` **sucede** `error[scope_underflow]`**;** `error[invalid_end_count]` **é retirado junto com** `end n`**. Novo** `error[empty_block]` **(Cap. 36.1) cobre cabeçalho de bloco sem corpo.**

- **Corpo de instrução única (Cap. 4.1, palavra-chave** `do`**): adaptado para não exigir mais fechamento —** `if true do print("oi") --` **(v0.5) passa a** `if true do print("oi")` **(v0.6), já que uma única linha física não tem o que dedentar.**

- **Novos erros léxicos (Cap. 3.3):** `error[mixed_indentation]` **e** `error[unexpected_indent]`**.**

- **Correção bônus: remanescentes da sintaxe de abertura por** `:` **que não haviam sido limpos na migração 0.4 → 0.5 — tabela de** `break()`**/**`continue()` **(Cap. 23), e frases descritivas nos capítulos 24, 26, 27, 29, 30 e 32 — foram corrigidos nesta revisão.**

Escopo desta revisão: reescrita normativa do Capítulo 4, das tabelas de erro dos Capítulos 3.3 e 36.1, e de todos os exemplos de código do documento que dependiam de `--` ou `end n` para fechamento. Sumário atualizado para as seções 4.2.1, 4.2.2 e 4.5. Numeração de capítulo preservada.

**Migração 0.6 → 0.7 (dois estilos de abertura de bloco):** a linguagem passa a ter dois estilos equivalentes de abertura de bloco — por indentação (já existente) e por delimitador `: ... --` (Capítulo 4.8), novo. Resumo das decisões:

- **Blocos (Cap. 4.8): reintroduzido o estilo de abertura por** `:`**, fechado por** `--`**, como segunda forma plenamente equivalente ao estilo por indentação (Cap. 4.1) — indentação dentro desse estilo é puramente visual, e blocos aninhados do mesmo estilo fecham como parênteses (um** `--` **por nível).**

- **Desambiguação do** `:` **(Cap. 4.8.1): conflito com asserção de tipo (Cap. 10.3/10.4) e conversão explícita (Cap. 8) resolvido por lookahead sobre o conjunto fechado dos seis tipos primitivos e das seis palavras** `to-*` **— se o token após** `:` **for um deles, é operador pós-fixo; caso contrário, abre bloco.**

- **Mistura de estilos (Cap. 4.9, novo** `error[mixed_block_style]`**): proibida apenas por aninhamento — um bloco de um estilo não pode conter, aninhado, um bloco do outro estilo, e vice-versa. Blocos irmãos (não aninhados) podem divergir de estilo livremente.**

- **Blocos encadeados no estilo delimitador (Cap. 4.10): a regra de "mesmo recuo" (Cap. 4.5) é substituída por "logo após o** `--` **anterior" —** `else`**/**`else if`**/**`catch`**/**`finally` **mantêm o mesmo estilo do início ao fim da cadeia.**

- **Palavra-chave** `do` **(Cap. 4.1, Apêndice A.6 v0.5/v0.6): retirada — o estilo delimitador cobre corpo de instrução única independente de recuo, generalizado a qualquer bloco. Exemplos do Capítulo 23 (**`do print(x)`**) e a tabela de** `break()`**/**`continue()` **atualizados para** `: ... --`**.**

Escopo desta revisão: reescrita normativa do Capítulo 4 (novas seções 4.8, 4.8.1, 4.9 e 4.10) e dos exemplos do Capítulo 23 e da tabela de `break()`/`continue()` que dependiam de `do`. Sumário a atualizar (F9) para incluir as novas seções 4.8 a 4.10. Numeração de capítulo preservada.

**Sessão de revisão e fortificação (pós-0.7):** revisão de consolidação, sem ruptura de sintaxe — foco em corrigir dívida acumulada entre spec e implementação, e em reverter uma remoção anterior que não se sustentou na prática. Resumo das decisões:

- **Operador if pós-fixo revertido (Cap. 12.4):** a remoção decidida na migração 0.4 → 0.5 não se concretizou — o autor decidiu mantê-lo como recurso ativo da linguagem, já implementado e em uso. Cap. 12.4 deixa de ser um título com aviso de remoção e volta a ser capítulo normativo pleno, incluindo a linha de precedência 11 (Cap. 12.1) que havia sido retirada da tabela geral junto com a remoção original.

- **Suíte de testes automatizada (tests/run_tests.py, novo):** antes desta revisão, validar o interpretador significava rodar cada arquivo de teste manualmente e comparar a saída de olho, sessão após sessão, sem registro do que era comportamento correto nem separação entre bug antigo conhecido e regressão nova. Passa a existir um runner que compara a saída de cada teste contra um snapshot gravado, e que rastreia explicitamente os bugs pré-existentes já conhecidos (hoje: o hello-world oficial e um caso de bloco não fechado) em vez de tratá-los como surpresa a cada rodada.

Escopo desta revisão: Cap. 12.4 e a tabela de precedência do Cap. 12.1 reescritos como normativos; Cap. 17 resumido (mesmo conteúdo histórico, menos espaço na leitura corrida — o texto integral continua neste apêndice); abertura do Cap. 24 corrigida para não tratar .try como se ainda existisse; Parte VIII renomeada e com aviso explícito de que é referência técnica, não leitura obrigatória; duplicata de “PARTE IV — OPERADORES” (Sumário e corpo) removida. Numeração de capítulo preservada.

**Sessão de tipagem híbrida — explícita + inferência (pós-0.7):** revisão de extensão, sem ruptura de sintaxe existente — formaliza o princípio “tudo pode ser tipado explicitamente ou ter seu tipo inferido” para coleções e funções, e cria a primeira etapa de verificação estática de tipos do pipeline. Resumo das decisões:

- **Verificação estática de tipos (Cap. 5, 35, novo):** quando um identificador (var/const, parâmetro, retorno) declara um tipo explicitamente, toda atribuição a ele é verificada estaticamente contra esse tipo, numa nova etapa do pipeline (Análise Estática de Tipos), inserida logo após o Registro de IDs. Sem tipo declarado, o identificador permanece dinamicamente tipado, podendo mudar de tipo livremente entre atribuições.

- **.type substitui type() (Cap. 6.7, 11.1, 19.5.2):** a consulta ao tipo de um valor em tempo de execução deixa de ser uma função e passa a ser propriedade — `valor.type` em vez de `type(valor)`. Semântica idêntica; `list` e `dict` continuam reportando `collection`.

- **Tipagem estruturada de coleções (Cap. 6.8, novo):** `list<...>` e `dict<chave, valor>` passam a ser aceitos como anotação de tipo (não alteram `.type`). `list<T1, T2, ...>` representa o conjunto (sem ordem) de tipos válidos para os elementos. Em `dict<chave, valor>`, cada parâmetro pode ser um tipo único ou uma união `<T1, T2, ...>`; tipos aninhados são preservados recursivamente quando declarados explicitamente (`dict<str, dict<str, int>>`), mas colapsam para o rótulo genérico na inferência automática (ex.: `{1: {}}` infere chave int, valor dict).

- **Atribuição por índice/chave (Cap. 19.4.2, novo):** `colecao[chave] = valor` e `colecao[índice] = valor` passam a editar um elemento já existente de `list` ou `dict`; chave/índice inexistente é erro. Criar uma entrada nova continua sendo função exclusiva de `.add()`.

- **Parâmetros nomeados de função (Cap. 30.3, novo; nota do Cap. 20.1 revisada):** um parâmetro pode declarar um identificador externo entre aspas (`"nome": param`), usado também na chamada (`f("nome": valor)`) — mecanismo distinto do `nome:valor` sem aspas, que continua restrito a print/println/readln. Parâmetros nomeados e posicionais podem coexistir; a ordem entre nomeados não é relevante.

- **Tipo de retorno declarado (Cap. 30.4, novo; Cap. 30.2 com ressalva):** `: tipo` após a assinatura declara o tipo de retorno, opcional. Declarado, cada `return` é verificado estaticamente, e chegar ao fim sem um retorno compatível é erro (a regra de retorno implícito `Null` do Cap. 30.2 deixa de se aplicar nesse caso). Não declarado, o retorno permanece livre, e a regra de `Null` implícito continua valendo normalmente.

Escopo desta revisão: novas seções 6.7, 6.8, 19.4.2, 30.3 e 30.4; Cap. 5 (parágrafo normativo do princípio híbrido), 11.1, 19.5.2 (`type()` → `.type`), 20.1 (nota revisada) e 30.2 (ressalva sobre retorno declarado) atualizados; nova etapa na tabela do Cap. 35 (Análise Estática de Tipos, entre Registro de IDs e Aplicação de Modificadores), com renumeração das etapas seguintes (6→7, 7→8, 8→9) e ajuste da referência cruzada logo abaixo da tabela. Sumário a atualizar (F9) para incluir as novas seções. Numeração de capítulo preservada.

**Sessão de parâmetros de função (pós-0.7):** revisão de extensão, sem ruptura de sintaxe existente — formaliza as categorias de parâmetros, valores padrão e parâmetros variádicos

- `unpack args` **como sintaxe de parâmetro variádico (Cap. 30.6, novo):** `f fun(unpack args)` captura em `args` a coleção de todos os argumentos posicionais restantes; pode vir depois de parâmetros posicionais (`f fun(a, unpack args)`).

- `!` **como marcador de parâmetros nomeados obrigatórios (Cap. 30.3):** `f GG(!, "A": e)`; `!` é marcador estrutural da declaração, não parâmetro; a ausência de `"A"` é erro de chamada.

- **Parâmetros nomeados sem** `!` **são opcionais (Cap. 30.3):** `f GH("A": e)` aceita `GH(10)` e `GH("A": 10)`; sem argumento, aplica-se o valor padrão ou, não havendo, `void`.

- **Parâmetros posicionais são exclusivamente posicionais (Cap. 30.3):** a passagem por nome é inválida.

- `=` **para valores padrão (Cap. 30.5, novo):** `f X(e = 0)`; o padrão só é usado quando o argumento correspondente não é fornecido.

- **Valores padrão em posicionais e nomeados (Cap. 30.5):** `f XC("a": e = null)`; `XC()` resulta em `e = null` e `XC("a": 10)` em `e = 10`. Não existe forma abreviada de argumento nomeado.

- **Nome externo versus identificador interno (Cap. 30.3):** em `"A": e`, `"A"` é o nome usado na chamada e `e` é a variável do corpo.

- **Gramática, resolução de argumentos e erros (Cap. 30.7 a 30.9, 36.6 e 37, novos):** gramática EBNF de parâmetros e argumentos, resolução determinística em quatro fases e novos códigos de erro de chamada e de declaração.

- `println(valor)` **adicionado (Cap. 20):** escreve o valor, quebra a linha no final e retorna `null`.

Escopo desta revisão: novas seções 30.5 a 30.9 e 36.6; Cap. 30.3 reescrito e retitulado (“Parâmetros — Categorias e Declaração”); introdução do Cap. 30, 31.1 (item 6), 11.3, 13, 14 (notas sobre `!` e `=`), 20 (tabela e `println`; linha duplicada `print(valor)` corrigida para `println(valor)`), 20.1 (nota revisada e exemplo de `println` corrigido), 36 e 37 atualizados. Sumário atualizado. Numeração de capítulo preservada.

**Sessão de formato de diagnósticos (pós-0.7):** revisão de extensão, sem ruptura de sintaxe — substitui o formato de saída de erro de linha única e a notação de avisos por um formato em bloco, em inglês, com código distinto por diagnóstico. Resumo das decisões:

- **Formato em bloco (Cap. 36.7, novo):** erros passam a ser exibidos como “=== Nome (Ennn) PROBLEM === ... === END ERROR ===” e avisos como “=== Nome (Wnnn) WARNING === ... === END WARNING ===”. Substitui o formato “line(N): error CODIGO, because: MENSAGEM” do Cap. 36 e a notação warning\[...\].

- **Idioma:** todos os textos impressos no bloco (rótulos, mensagem, dica, menu) são em inglês, independentemente do idioma da especificação.

- **Código distinto por diagnóstico:** 41 erros (E101 a E902) e 9 avisos (W201 a W307), agrupados por fase. Variantes do mesmo diagnóstico compartilham o código.

- **Trecho de código:** uma linha de contexto antes e outra depois, marcador “\|\>” na linha do problema e “^” sob o menor trecho responsável (em “print(10 / 0)”, a operação “10 / 0”); problemas de várias linhas marcam cada linha.

- **Pilha de chamadas e dicas automáticas:** erros dentro de funções listam a pilha de chamadas; IdNotFound sugere o nome mais próximo (“did you mean”) e ParserError informa o que era esperado.

- **Menu e código de saída:** novas opções 2 (abrir o arquivo na linha do erro) e 3 (copiar o erro); o menu só aparece em terminal interativo; erro não capturado encerra com código de saída 1.

- **Modo --plain e cores:** linha única “arquivo:linha:coluna: error\|warning Nome (Código): mensagem” para editores e CI; cores (vermelho, amarelo) desligadas fora de terminal, com NO_COLOR e em --plain.

- **Avisos no novo formato:** warning\[uncaught_in_try\] e as menções livres a Warning/aviso passam a nove avisos nomeados: UnusedVariable, NameReuse, ImplicitVoid, PrecisionLoss, ImplicitBoolConversion, ValueIsVoid, MatchWithoutElse, NoopPause e UncaughtInTry.

- **Códigos de erro renomeados:** error\[snake_case\] passa a NomePascalCase PROBLEM em todo o corpo do documento (ex.: error\[index_out_of_bounds\] passa a IndexOutOfBounds PROBLEM). Os registros históricos deste apêndice mantêm a notação da época. A notação volta ao PascalCase abandonado na migração 0.4 → 0.5 (A.5), agora sem colchetes e com o sufixo PROBLEM.

- **Erros com nome novo:** anotações que eram texto livre nos exemplos (“# erro”, “# ERRO”, “# erro de tipo”, “# erro de verificação estática”) passam a citar o nome do erro: DivisionByZero, TypeMismatch, StaticTypeMismatch, PrecisionExceeded, InvalidConversion, ConstReassignment e ImmutableMutation.

- **Recuperabilidade explícita:** erros das etapas 1 a 7 do pipeline (léxico, sintaxe, IDs e tipos estáticos) são não recuperáveis; erros da etapa de Execução são recuperáveis com try.

Escopo desta revisão: nova seção 36.7; Cap. 3.3, 4.9, 7.2, 8, 12.3, 19, 24, 25.3, 26.4, 30.6, 30.9, 34.4, 36 (introdução e 36.1 a 36.4), 37 (introdução e nomes) e 38.1 atualizados, além de todos os exemplos de código com anotação de erro ou aviso; novas pendências B16 a B18 no Apêndice A.2. Sumário a atualizar (F9) para incluir a seção 36.7. Numeração de capítulo preservada.

**Sessão de** `nome=valor`**,** `~Program` **e** `load` **(pós-0.7):** revisão de extensão, sem ruptura de sintaxe existente — três adições decididas pelo autor; ver os capítulos citados para o texto normativo.

- **Forma alternativa de argumento nomeado (Cap. 20.1, 21.1, 30.3, 30.7, 30.8):** `nome=valor` equivale a `"nome": valor` quando o nome externo é uma string que forma identificador válido; vale para funções de usuário, módulos, `print`, `println` e `readln`. Dentro de uma lista de argumentos, `IDENT = expr` é sempre argumento nomeado, nunca atribuição. A forma com aspas continua sendo a forma padrão (e a única para nome externo numérico).

- **Objeto do programa** `~Program` **(Cap. 3.4, 29.4):** `~` não declara variável nem função e passa a ser o prefixo reservado dos objetos nativos; `~Program` expõe `path`, `lines`, `line` (dict de chaves inteiras a partir de 1, com `[-N]` contando do fim) e `content`, todos somente leitura. O mesmo objeto, visto de fora de um arquivo carregado, é `Y.~Program`.

- `load <caminho> as Y` **(Cap. 29.5):** executa um arquivo `.tpine` uma vez, em escopo próprio, e o expõe sob o apelido `Y` (variáveis, funções, classes e `~Program` do nível de topo). Coexiste com `import` (29.3), que incorpora o arquivo no escopo corrente. `load` e `as` tornam-se palavras reservadas.

- **Diagnósticos novos (Cap. 36.7 e 37):** `ReservedSymbol` (E113), `ReadOnlyProperty` (E313), `LoadFileNotFound` (E314) e `CircularLoad` (E315); variante de `IdDuplicate` (E110) para apelido repetido.

Escopo desta revisão: novas seções 29.4 e 29.5; Cap. 3.4, 20.1, 21.1, 30.3, 30.7, 30.8, 36.7 e 37 atualizados. Sumário a atualizar (F9) para incluir as seções 29.4 e 29.5. Capa mantida em “Versão 0.7”. Numeração de capítulo preservada.

**Sessão de sincronização com o Sys (pós-0.7):** revisão de extensão, sem ruptura de sintaxe existente — registra comportamentos constatados no interpretador e a nova regra de parâmetros nomeados. Resumo das decisões:

- **package para o parâmetro variádico (Cap. 30.3, 30.6 a 30.9, 37):** na declaração, `unpack args` passa a `package args`; `unpack` fica só como operador de expansão (19.4.1), agora também em literais de lista (`[unpack A, 4]`). `package` é palavra reservada. Mensagem de ParserError (E101) e dicas de E112 revisadas.

- **Parâmetros nomeados e ordem de declaração (Cap. 30.3, 30.6, 30.7, 30.9):** Alternativa A — nomeados não estão sujeitos às regras de ordenação dos posicionais; `package` só precisa vir depois dos posicionais, e `f A(package A, "A": e)` é válido. `package` continua sem nome externo, sem valor padrão e fora da seção `!`. Gramática ajustada (PosItem). A ligação dos argumentos não mudou; o conflito com os exemplos propostos fica em B21.

- **Valor padrão não é argumento fornecido (Cap. 30.8, 30.9):** o padrão só entra na fase 4 e nunca causa DuplicateArgument.

- **Fatia por intervalo (Cap. 19.2.1, 18.4, 29.4):** `[a to b]` inclusivo nas duas pontas, base 0, limites negativos contam do fim, fora da coleção ou invertido é IndexOutOfBounds; `~Program.line[a to b]` devolve `list<str>` (base 1). Corrigido o exemplo `A[4 to 13] = ""` do Cap. 18.4 (resultado `olá,`).

- **Concatenação de texto (Cap. 9.2, 13, 37):** `+` entre `str` e número é TypeMismatch; usar `: to-str`/`: to-num`. Nenhum exemplo do documento concatenava texto com número.

- **emit e geradores (Cap. 23.2.2):** `emit` vale com `for`, `while` e fora de laço; print/println consomem o fluxo em série só com um único argumento posicional; fora disso, a chamada devolve a lista.

- **Outros (Cap. 26, 30.3, 29.4, 34.8):** exemplo de MissingArgument com padrão; pause 0 em laço e a proteção com if; ~Program no terminal interativo (path `""`, lines 0); computer.read() bloqueante.

- **Pendências novas:** B19 (sintaxe de load), B20 (computer.read não bloqueante), B21 (package com nomeados opcionais), B22 (unpack e dicionário em lista), B23 (consumo de gerador).

Escopo desta revisão: Cap. 9.2, 13, 18.4, 19.2.1 (novo), 19.4.1, 23.2.2, 26, 29.4, 30.3, 30.6 a 30.9, 34.8 e 37 (E101, E112, E302); novas pendências B19 a B23 no Apêndice A.2. `unpack` nos exemplos de declaração foi renomeado para `package`; os registros históricos deste apêndice mantêm a notação da época. Sumário a atualizar (F9) para incluir a seção 19.2.1. Capa mantida em "Versão 0.7".

**Segunda sessão de sincronização com o Sys (pós-0.7):** registra comportamentos do interpretador posteriores à primeira sincronização e reorganiza a numeração. Resumo das decisões:

- **! com valor padrão (Cap. 30.3, 30.5, 30.7 a 30.9, 37):** os parâmetros depois de `!` são exclusivamente nomeados; sem valor padrão são obrigatórios (MissingNamedArgument), com `= valor` são opcionais. `package` coexiste com `!`: `f out(package ARGS, !, "sep": SEP = "")`. InvalidBangMarker (E111) deixa de reprovar `= valor` depois de `!`; a dica foi revista. Resolve o caso de B21.

- **Marcador ? e parâmetros tipados (Cap. 30.3, 30.4.1, 30.5, 30.7 a 30.9, 37):** `?` abre a seção de parâmetros ligados pelo tipo; novo erro InvalidQuestionMarker (E123); ordem `posicionais [ ? tipados ] [ ! nomeados ]`; gramática com TypedSection e NamedSection. Decisões do interpretador em B24.

- **Módulo computer (Cap. 34.1, 34.7, 34.8, 37):** `computer.shell` devolve um dict (`"input"`, `"output-type"`, `"output"`) e o encaminhamento `|>` devolve o mesmo dict; `computer.clipboard.content`; `computer.keyboard.press`, `pressed` e `write`, com `"key"`, `"keys"` e `"*"`; `app` e `read` removidos do módulo (B20 encerrada); novos erros InvalidKey (E617) e ComputerKeyboardError (E618). Decisões em B25.

- **Organização:** a numeração do Cap. 34 foi corrigida (o operador `|>` passa a 34.8; `os` é 34.6 e `computer` é 34.7, e todas as referências cruzadas foram ajustadas, inclusive as do Sumário em cache); o segundo 19.4.1 passa a 19.4.2; 30.4.1 passa a subseção de nível 4; as mensagens de B12 a B14 foram renumeradas.

- **Pendências:** B13 reescrita, B14 renumerada, B20 encerrada, B21 mitigada, novas B24 (marcador `?`) e B25 (módulo `computer`).

Escopo desta revisão: Cap. 19.4.2 (renumerado), 30.1, 30.3 a 30.9, 34.1, 34.6 a 34.8 e 37 (E111, E123, E617, E618); Apêndice A.2 (B12 a B14, B20, B21, B24, B25). O Sumário em cache foi corrigido na numeração, mas os números de página só se atualizam no Word (clique com o botão direito no Sumário e escolha Atualizar campo, ou F9). Capa mantida em "Versão 0.7".

**Terceira sessão de sincronização com o Sys (pós-0.7) — instruções `#~` e avisos de código morto:** resumo das decisões:

- **Instruções ao TinyPine `#~` (Cap. 3.1.1):** nova forma de comentário que o TinyPine lê como comando. A primeira instrução é `#~ hide the W301` (`#~` abre o comando, `hide` é o que fazer, `the` indica que a próxima palavra é uma menção, `W301` é a menção — código ou nome de um aviso); o `the` é **opcional**, e `#~ hide W301` faz o mesmo: o aviso não é emitido. Alcance: na mesma linha de um código, só aquela linha; em linha própria, dali até o fim do arquivo (no terminal interativo, pela sessão). Só avisos podem ser escondidos. Uma instrução inválida nunca é ignorada em silêncio: emite `InvalidDirective (W101)` ou `UnknownMention (W102)`.
- **Cap. 3.1:** a frase "o TinyPine define três formas de comentário", que aparecia sem a lista, foi reescrita como duas formas de comentário (`#` e `|| ... ||`) mais a forma de instrução `#~`.
- **Avisos novos (Cap. 36.7, 37, 38):** `InvalidDirective (W101)`, `UnknownMention (W102)`, `UnreachableCode (W203)` (código depois de `return`/`break`/`continue`/`throw`, e blocos de condição constante) e `UnusedFunction (W204)` (função nunca chamada).
- **`UnusedVariable (W201)` por escopo (Cap. 38):** o Cap. 38 já dizia que a análise considera o escopo; a implementação olhava o programa inteiro e agora liga cada leitura à declaração visível. O que conta como uso e o que nunca gera o aviso ficaram escritos no capítulo.
- **Pipeline (Cap. 35):** nota de que as instruções `#~` valem para os avisos de todas as etapas.
- **Chamada com ponto em dicionário (Cap. 19.2.2, 31.3; B26 parcialmente resolvida):** `D.chave(...)` chama a função anônima guardada numa chave de dicionário, o que permite um objeto leve como `console.log("Hello World!")` (`var console = {"log": f(package ARGS) print(unpack ARGS)}`). Chave ausente: `KeyNotFound PROBLEM`; valor que não é função: `TypeMismatch PROBLEM`; as chaves `add` e `remove` continuam sendo os métodos da coleção. A chamada por índice, `D["chave"](...)`, e a de elemento de lista seguem em aberto (B26).

Escopo desta revisão: Cap. 3.1 e 3.1.1 (novo), 19.2.2, 31.3, 35, 36.7, 37 e 38; Apêndice A.2 (B26). Capa mantida em "Versão 0.7". Ideias que ficaram de fora de propósito: outros comandos além de `hide` (por exemplo, uma instrução para voltar a emitir um aviso escondido) e esconder vários avisos numa só linha.

**Quarta sessão de sincronização com o Sys (pós-0.7) — tipos refinados, `.length` e acesso por `key`/`value`:** resumo das decisões:

- **Tipos refinados (Cap. 6.9, novo):** sintaxe `tipo\restrição\` (a versão com `<*>` foi trocada por `\*\`), tipos aceitos, propriedades, regras de validação, operadores e condições separadas por vírgula (basta uma falsa para dar erro). Lexer: a barra invertida fora de string passa a ter este único uso (Cap. 3.2). Gramática provisória em `gramatica.ebnf`.
- **Erro novo:** `RefinementViolation (E316) PROBLEM` (Cap. 36.7, 37); nota no pipeline (Cap. 35) de que a restrição é verificada na execução.
- **`.length` (Cap. 33.3):** `len(*)` vira `*.length`; "a mesma coisa de `len`" foi a resposta do autor à pendência de semântica de `length`. Cap. 4 e 23 atualizados.
- **Acesso por `key K` / `value V` (Cap. 19.1 e 19.2):** formas antigas removidas; mensagem "Lists have no keys" removida do Cap. 36.7.
- **Interpolação (Cap. 20.2, novo):** `{A-A}` e `{A.length}` são válidos dentro de `format`.
- **Pendências:** novas B27 (tipos refinados e `key`/`value`) e B28 (interpolação); B6 reescrita para `.length`.

Escopo desta revisão: Cap. 3.2, 4.7, 5, 6.9 (novo), 19.1 e 19.2, 20.2 (novo), 23, 33.3, 35, 36.7, 37 e `gramatica.ebnf`; Apêndice A.2 (B6, B27, B28). Capa mantida em "Versão 0.7". Ideias que ficaram de fora de propósito: tipos refinados em `bool` e em outros tipos, e restrições aninhadas.

**Quinta sessão de sincronização com o Sys (pós-0.7) — tipagem estruturada por `\...\`, união `|` e tipo `function`:** resumo das decisões:

- **`<...>` removido de todos os tipos (Cap. 6.8):** `list<...>` e `dict<chave, valor>` (e a união `<T1, T2>`/`[T1, T2]` dentro delas) deixam de existir; a sintaxe antiga não coexiste com a nova. Equivalências: `list<int, str>` → `list\values: int | str\`; `dict<str, [str, int]>` → `dict\keys: str, values: str | int\`.
- **Propriedades `keys` e `values` (Cap. 6.9):** `keys: T` (toda chave de `dict` é `T`) e `values: T` (todo valor de `list`/`dict`/`tuple` é `T`) entram na tabela de propriedades do tipo refinado; a pendência do `values` em B27 foi encerrada.
- **Operador `|` (Cap. 6.8.1, novo):** união de tipos ("ou"), válido em toda posição de tipo; substitui `<T1, T2>`.
- **Tipo `function` (Cap. 6.7):** `.type` de uma função nomeada ou anônima devolve `"function"`; `function` é nome de tipo (asserção, declaração, `keys:`/`values:`), sem refinamento.
- **Nota do `.type` (Cap. 6.7):** o texto "reportando `list ou dict`" foi corrigido para "`list` e `dict`".
- **Cap. 29.4 (`~Program.line`):** `dict<int, str>` → `dict\keys: int, values: str\`; `list<str>` → `list\values: str\`. Cap. 30.7 e `gramatica.ebnf`: `Type` com união `|` e `function` entre os nomes de tipo.
- **Pendências:** nova B29 (tipos aninhados sem equivalente, erro estático × execução, `|` em toda posição, `||`/`|>`, `keys` fora de `dict`, `function` em método/função nativa); B27 atualizada.

Escopo desta revisão: Cap. 6.7, 6.8, 6.8.1 (novo), 6.9, 29.4, 30.7 e `gramatica.ebnf`; Apêndice A.2 (B27, B29). Capa mantida em "Versão 0.7". Entradas históricas anteriores, que citam `list<...>`/`dict<...>`, ficaram como estavam. Ideias que ficaram de fora de propósito: tipos aninhados, `function` com assinatura (parâmetros e retorno) e testes executáveis dos exemplos novos (dependem do Sys).
