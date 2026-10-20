## Catálogo de Códigos de Erro

Como regra geral, um token que reutiliza um símbolo, palavra reservada, variável ou função já existente gera um `NameReuse WARNING` — e não interrompe a execução. A tabela a seguir cataloga os principais erros formalizados nesta especificação, e a fase do processamento (Capítulo 35) em que cada um pode ocorrer. O formato de exibição, a recuperabilidade, a mensagem e a dica de cada erro — inclusive dos que não aparecem nesta tabela — estão definidos na Seção 36.7.

| **Código**                                   | **Fase**           | **Descrição**                                                                                                 |
|----------------------------------------------|--------------------|---------------------------------------------------------------------------------------------------------------|
| `ParserError (E101) PROBLEM`                 | Léxico / Sintático | Token inesperado, string não fechada, número malformado, caractere inválido.                                  |
| `IdNotFound (E308) PROBLEM`                  | Execução           | Variável ou função referenciada sem estar declarada.                                                          |
| `IdDuplicate (E110) PROBLEM`                 | Sintático          | Identificador declarado mais de uma vez no mesmo programa.                                                    |
| `MultipleIdentifiersPerBlock (E109) PROBLEM` | Sintático          | Mais de um `id()` registrado no mesmo bloco lógico.                                                           |
| `ScopeUnderflow (E901) PROBLEM`              | Execução           | `end N` tentou fechar mais blocos do que os existentes e abertos.                                             |
| `InvalidEndCount (E902) PROBLEM`             | Execução           | `end()` recebeu um valor negativo.                                                                            |
| `InvalidRepeatCount (E306) PROBLEM`          | Execução           | `repeat` recebeu um valor negativo ou não inteiro.                                                            |
| `InvalidPauseDuration (E307) PROBLEM`        | Execução           | `pause` recebeu um valor negativo ou não numérico válido.                                                     |
| `InvalidSpecialBlock (E309) PROBLEM`         | Execução           | Nome de bloco especial desconhecido (ex.: `[banana]`).                                                        |
| `IndexOutOfBounds (E402) PROBLEM`            | Execução           | Índice de coleção negativo ou acima do tamanho da coleção.                                                    |
| `UncaughtThrow (E310) PROBLEM`               | Execução           | `throw()` não capturado por nenhum `catch`.                                                                   |
| `InvalidDirective (W101) WARNING`            | Léxico             | Instrução `#~` que não segue a gramática do Capítulo 3.1.1.                                                   |
| `UnknownMention (W102) WARNING`              | Léxico             | Menção de `#~ hide` que não é um aviso do catálogo (ou é um erro).                                        |
| `UnusedVariable (W201) WARNING`              | Análise estática   | Variável declarada e nunca lida no seu escopo (Capítulo 38).                                                  |
| `UnreachableCode (W203) WARNING`             | Análise estática   | Código depois de `return`, `break`, `continue` ou `throw`, ou bloco de condição constante (Capítulo 38).      |
| `UnusedFunction (W204) WARNING`              | Análise estática   | Função declarada e nunca chamada (Capítulo 38).                                                               |
| `UncaughtInTry (W307) WARNING`               | Execução           | `try` sem `catch` capturou um erro internamente. Emite aviso; não aborta a execução.                          |
| `MissingArgument (E501) PROBLEM`             | Execução           | Parâmetro posicional sem argumento e sem valor padrão (Capítulo 30.9).                                        |
| `MissingNamedArgument (E502) PROBLEM`        | Execução           | Parâmetro nomeado obrigatório (depois de `!`) sem valor padrão, não fornecido.                                |
| `UnknownNamedArgument (E503) PROBLEM`        | Execução           | Argumento nomeado sem parâmetro de mesmo nome externo.                                                        |
| `PositionalForNamedOnly (E504) PROBLEM`      | Execução           | Argumento posicional excedente em função com seção `!` e sem `package args`.                                  |
| `NamedForPositionalOnly (E505) PROBLEM`      | Execução           | Argumento nomeado dirigido a parâmetro exclusivamente posicional.                                             |
| `DuplicateArgument (E506) PROBLEM`           | Execução           | Mesmo parâmetro fornecido mais de uma vez (por posição e/ou por nome).                                        |
| `TooManyArguments (E507) PROBLEM`            | Execução           | Argumentos posicionais em excesso, sem `package args` e sem seção `!`.                                        |
| `InvalidBangMarker (E111) PROBLEM`           | Sintático          | Uso inválido do marcador `!` na declaração de função.                                                         |
| `InvalidVariadicParam (E112) PROBLEM`        | Sintático          | Uso inválido de `package args` na declaração de função.                                                       |
| `InvalidQuestionMarker (E123) PROBLEM`       | Sintático          | Uso inválido do marcador `?` na declaração de função (Capítulo 30.4.1).                                       |
| `ReservedSymbol (E113) PROBLEM`              | Sintático          | Uso de ~ para declarar variável ou função, ou de um objeto nativo desconhecido (~Nome diferente de ~Program). |
| `ReadOnlyProperty (E313) PROBLEM`            | Execução           | Atribuição a ~Program ou a um de seus membros (Capítulo 29.4).                                                |
| `LoadFileNotFound (E314) PROBLEM`            | Execução           | load apontou para um arquivo inexistente ou ilegível (Capítulo 29.5).                                         |
| `CircularLoad (E315) PROBLEM`                | Execução           | Dois ou mais arquivos se carregam mutuamente por load (Capítulo 29.5).                                        |
| `RefinementViolation (E316) PROBLEM`         | Execução           | Valor que não satisfaz a restrição de um tipo refinado (Capítulo 6.9).                                        |
