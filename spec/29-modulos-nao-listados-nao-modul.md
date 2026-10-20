## módulos não listados & não módulos

Todos usam a sintaxe padrão de chamada funcional `nome_do_bloco(parâmetros)`, delimitada por indentação como qualquer outro bloco.

### debug.\*() — Escopo de Depuração

Permite ativar ferramentas de inspeção interna (como exibição da AST, dos tokens gerados ou de estados de memória) restritas ao bloco de código envolvido. `debug` designa exclusivamente este bloco de controle nativo; o **módulo importável** de inspeção global (Capítulo 34.6) usa um nome distinto, ainda a confirmar, para não colidir com este (ver Histórico, Apêndice A).

```tinypine
debug.metodo()
  comandos
```

*Sintaxe*

Sem parâmetro (`debug.ast()`, por exemplo): executa o código interno normalmente e gera/exibe todos os logs de depuração correspondentes no console do interpretador.

```tinypine
debug.ast()
  var x = 10 + 5
```

### loop() — Laço de Repetição Infinito com Tick Controlado

Estrutura de repetição contínua que substitui o laço infinito tradicional, fornecendo controle nativo de tempo por ciclo (*tick*/*delay*), para evitar sobrecarga de processamento.

```tinypine
loop velocidade_ou_void
  comandos
```

*Sintaxe*

Sem parâmetro (`loop()`): executa o laço continuamente, na velocidade máxima permitida pela CPU, sem aplicar atraso entre os ciclos.

Com valor numérico (`loop(0.5)`): define o tempo de espera (*delay*), em segundos, entre cada iteração.

```tinypine
|| loop que executa a cada 1.5 segundo ||
loop(1.5)
  print("Novo tick executado...")
```

### import \<caminho do arquivo local\> —incorpora um arquivo de um diretório 

incorpora um arquivo de um diretório localmente:

```tinypine
import "C:\\Temp\\file.tpine" # daqui em diante vale
import "C:\\Temp\\file_1.tpine", "C:\\Temp\\file.tpine_2" # daqui em diante vale
```

### ~Program — Objeto do Programa

O prefixo `~` é reservado pela linguagem para os objetos nativos do programa. Um objeto nativo é escrito `~Nome` e não é declarado pelo usuário: `~` não pode iniciar o nome de uma variável ou função, e `~Program` é, por ora, o único objeto nativo — qualquer outro `~Nome` é `ReservedSymbol PROBLEM`. O operador `~=` (Capítulo 11.2) não é afetado: o lexer reconhece `~=` primeiro (maior casamento).

`~Program` descreve o arquivo `.tpine` em execução. Todos os seus membros são somente leitura:

| **Expressão**      | **Tipo**         | **Descrição**                                                                                                                                                                                                                                                                          |
|--------------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `~Program`         | `dict`           | Dicionário com as chaves "path", "lines", "line" e "content", cujos valores são os membros abaixo; `~Program["path"]` equivale a `~Program.path`.                                                                                                                                      |
| `~Program.path`    | `str`            | Caminho absoluto resolvido do arquivo `.tpine`, com o nome do arquivo e o separador nativo do sistema operacional. `""` quando não há arquivo (terminal interativo, entrada padrão).                                                                                                   |
| `~Program.lines`   | `int`            | Número de linhas. Um `\n` final não cria linha extra; arquivo vazio tem 0 linhas.                                                                                                                                                                                                      |
| `~Program.line`    | `dict\keys: int, values: str\` | Dicionário de chaves inteiras 1, 2, …, `lines` — a numeração começa em 1, a mesma das mensagens de erro — e valores `str` com o texto da linha, sem a quebra de linha.                                                                                                                 |
| `~Program.line[N]` | `str`            | Linha de número N (N ≥ 1). Em `~Program.line`, `[-N]` conta a partir do fim (`[-1]` é a última linha): regra própria deste dicionário, que não altera a regra geral de `colecao[N]` em dicionários (Capítulo 19.1). N = 0, N \> `lines` ou N \< -`lines` é `IndexOutOfBounds PROBLEM`. |
| `~Program.content` | `str`            | Texto completo do arquivo, com as quebras de linha normalizadas para `\n` e sem BOM.                                                                                                                                                                                                   |

```tinypine
print(~Program.path)
print(~Program.lines)
print(~Program.line[1])    # primeira linha
print(~Program.line[-1])   # última linha
print(~Program["lines"])   # o mesmo que ~Program.lines
var linhas = ~Program.line   # dict\keys: int, values: str\
print(linhas[3])             # chave 3 — a terceira linha
var ~x = 1                  # ReservedSymbol PROBLEM
f ~g()                      # ReservedSymbol PROBLEM
print(~Outro)               # ReservedSymbol PROBLEM
~Program.path = "a"         # ReadOnlyProperty PROBLEM
~Program = {}               # ReadOnlyProperty PROBLEM
print(~Program.line[999])   # IndexOutOfBounds PROBLEM
```

**Fatia de linhas.** `~Program.line[a to b]` devolve uma lista de `str` com as linhas de `a` a `b`, as duas incluídas, numeradas a partir de 1; um limite negativo conta a partir do fim, como em `~Program.line[-N]`. Limite fora de 1 a `lines`, ou início depois do fim, é `IndexOutOfBounds PROBLEM`. Como os demais membros, é somente leitura, e a análise estática a tipa como `list\values: str\`. Os demais dicionários não têm fatia (Capítulo 19.2.1).

```tinypine
print(~Program.line[1 to 3])      # as três primeiras linhas, em uma lista
print(~Program.line[-2 to -1])    # as duas últimas
```

**No terminal interativo.** Sem arquivo em execução, `~Program.path` é `""` e `~Program.lines` é `0`:

```tinypine
print(~Program.lines)    # no terminal interativo: 0
print(~Program.path)     # no terminal interativo: "" (texto vazio)
```

**Retrato do arquivo.** O conteúdo é lido no início da execução e não muda enquanto o programa roda. No editor da Gui, vale o texto do editor — mesmo não salvo —, não o do disco.

**Somente leitura.** Atribuir a `~Program` ou a qualquer membro é `ReadOnlyProperty PROBLEM`; a propriedade `.type` (Capítulo 6.7) também é somente leitura. `var p = ~Program` copia o dicionário, e a cópia é editável como qualquer dicionário.

**Em arquivos carregados e importados.** Dentro de um arquivo carregado por `load` (29.5), `~Program` descreve o próprio arquivo carregado; de fora, ele é acessado como `Y.~Program`. Dentro de um arquivo trazido por `import` (29.3), `~Program` continua descrevendo o arquivo principal, já que o `import` incorpora o código ao programa.

**Análise estática.** Os tipos dos membros são conhecidos antes da execução — `path` e `content` são `str`, `lines` é `int`, `line` é `dict\keys: int, values: str\` — e entram na Análise Estática de Tipos (Capítulo 35, etapa 6).

### load \<caminho\> as Y — carrega um arquivo sob um apelido

`load` executa outro arquivo `.tpine` e o expõe por um apelido, sem misturar os nomes dele com os do programa atual — ao contrário de `import` (29.3), que incorpora o arquivo no escopo corrente. `load` e `as` são palavras reservadas: nenhuma das duas pode ser usada como identificador.

```tinypine
load "util.tpine" as Y

print(Y.A)                  # a variável A do arquivo carregado
print(Y.~Program.line[-1])  # a última linha do arquivo carregado
Y.saudar("Dhavi")           # uma função declarada em util.tpine
```

> **1. Sintaxe.** `load <caminho> as <apelido>`. O apelido é obrigatório: `load "x.tpine"` sem `as` é `ParserError PROBLEM`. O caminho é um literal `str` ou qualquer expressão que produza `str`, e a extensão `.tpine` é obrigatória. Um caminho relativo é resolvido a partir da pasta do arquivo que contém o `load` (no terminal interativo, a partir do diretório de execução).
>
> **2. Execução.** O arquivo é executado por inteiro, uma vez, no ponto em que a linha `load` é executada — não na etapa de Registro de IDs —, com todos os efeitos colaterais (`print`, leitura de entrada etc.). Cada caminho absoluto é executado no máximo uma vez: carregar o mesmo arquivo de novo, com outro apelido, reaproveita a instância já executada, e os dois apelidos compartilham o mesmo estado.
>
> **3. Isolamento.** O arquivo carregado roda num escopo global próprio: não enxerga as variáveis do programa que o carregou, e os `use` dele ficam restritos a ele, sem vazar para `Y`.
>
> **4. O que** `Y` **expõe.** As variáveis, funções e classes declaradas no nível de topo do arquivo carregado, mais o `~Program` dele (`Y.~Program`); nada de dentro de blocos. Atribuir a um membro de fora (`Y.A = 5`) segue as regras do Capítulo 18.2: permitido para `var`; para `const`, reatribuir é `ConstReassignment PROBLEM`. `Y.Z` inexistente é `IdNotFound PROBLEM`, e `.~Program` aplicado a algo que não é apelido de `load` também. `Y.type` é `"module"`.
>
> **5. Apelido.** O apelido é registrado como identificador na etapa de Registro de IDs (Capítulo 35, etapa 5); um apelido que repete outro identificador do mesmo escopo é `IdDuplicate PROBLEM`.
>
> **6. Erros.** Arquivo inexistente ou ilegível: `LoadFileNotFound PROBLEM` (recuperável com `try`). Erro dentro do arquivo carregado: propaga como qualquer erro, com o nome do arquivo carregado no trecho de código e na pilha (Capítulo 36.7). Carga circular — A carrega B, que carrega A: `CircularLoad PROBLEM`.
>
> **7. Análise estática.** Tudo que é acessado por `Y.` é dinâmico: o caminho pode ser calculado em tempo de execução, então nenhum tipo de `Y.*` é verificado antes da execução.
