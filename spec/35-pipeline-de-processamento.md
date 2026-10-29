# PARTE VIII — REFERÊNCIA TÉCNICA DO INTERPRETADOR

## Pipeline de Processamento

| **\#** | **Etapa**                  | **Descrição**                                                                                                                                                                                                |
|--------|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1      | Análise Léxica (Lexer)     | O código-fonte é lido e convertido em uma sequência de tokens.                                                                                                                                               |
| 2      | Tokens                     | Saída da análise léxica: sequência de unidades léxicas reconhecidas.                                                                                                                                         |
| 3      | Análise Sintática (Parser) | Os tokens são organizados em uma estrutura sintática.                                                                                                                                                        |
| 4      | AST                        | Árvore de Sintaxe Abstrata (*Abstract Syntax Tree*) resultante da análise sintática.                                                                                                                         |
| 5      | Registro de IDs            | A tabela interna de identificadores (Capítulo 28) é construída a partir da AST.                                                                                                                              |
| 6      | Análise Estática de Tipos  | Tipos declarados são verificados e tipos não declarados são inferidos, com base na AST e na tabela de identificadores; incompatibilidades são reportadas nesta etapa, antes da execução (Cap. 5, 6.8, 30.4). |
| 7      | Aplicação de Modificadores | Os modificadores (Capítulo 27) são aplicados aos blocos que referenciam.                                                                                                                                     |
| 8      | Execução                   | O programa é executado sobre a árvore já resolvida.                                                                                                                                                          |
| 9      | Compilação                 | *(Reservado para uma versão futura — etapa posterior à execução.)*                                                                                                                                           |

As instruções `#~` (Capítulo 3.1.1) são lidas junto com a análise léxica (etapa 1) e valem para os avisos de **todas** as etapas: ao serem emitidos (etapas 1 a 8), os avisos escondidos por um `#~ hide` simplesmente não aparecem.

As restrições de tipos refinados (Capítulo 6.9) dependem do valor que está sendo validado e produzem `RefinementViolation PROBLEM` (E316) na execução (etapa 8); se a verificação pode ser antecipada para valores literais, na etapa 6, está em aberto (Apêndice A.2, B27).

Os identificadores `id` (Capítulo 28) são coletados e expandidos num **passo sobre os tokens**, que roda depois da análise léxica (etapas 1 e 2) e **antes** da análise sintática (etapa 3): como uma referência é o próprio nome, sem prefixo, só depois de coletar todas as declarações `id` do arquivo dá para saber quais nomes são referências. Referências antecipadas (Capítulo 28.3) são válidas por isso. A etapa 5 (Registro de IDs) continua sendo a da tabela de identificadores do programa — variáveis, funções, classes e apelidos de `load` —, onde também se confere que nenhum nome de `id` é reutilizado (`IdDuplicate`, E110). A posição desse passo na tabela do pipeline está em aberto — Apêndice A.2, B31 (e B7).
