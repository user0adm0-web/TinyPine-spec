## Referência da Biblioteca Padrão

Esta seção reúne a documentação de todos os módulos da biblioteca padrão do TinyPine, um item por módulo.

### Visão Geral dos Módulos

Cada módulo tem um papel definido dentro da biblioteca padrão do TinyPine:

| **Módulo**  | **Papel**                                                                        |
|-------------|----------------------------------------------------------------------------------|
| `pen`       | Desenho e renderização baseados em cursor (modelo de tartaruga gráfica).         |
| `system`    | *Runtime* do TinyPine.                                                           |
| `os`        | Manipulação de recursos do ambiente hospedeiro (arquivos e sistema de arquivos). |
| `computer`  | Interação com a máquina hospedeira : shell, área de transferência e teclado.     |
| `time`      | Manipulação de tempo.                                                            |
| `json`      | Serialização e desserialização de dados no formato JSON.                         |
| `math`      | Módulo matemático completo.                                                      |
| `file`      | Descontinuado — funcionalidade absorvida por `os (34.6)`.                        |
| `random`    | Geração de números e escolhas pseudoaleatórias.                                  |
| `scene`     | Renderização 3D (dinâmica).                                                      |
| `input`     | Descontinuado                                                                    |
| `web`       | Funcionalidades relacionadas à web.                                              |
| `clipboard` | Descontinuado — funcionalidade absorvida por `computer.clipboard (34.7)`.        |

Dos módulos listados acima, apenas `math`, `pen`, `random`, `os` e `computer` têm suas funções, parâmetros e comportamento de erro detalhados nesta especificação (34.2 a 34.4, 34.6 e 34.7); os demais (`system`, `time`, `json`, `scene`, `web`, `clipboard`) são, por ora, anunciados apenas por esta tabela de visão geral (ver Histórico, Apêndice A — pendência de alta prioridade).

### Módulo math

O módulo `math` é responsável por operações aritméticas avançadas, funções trigonométricas e manipulações numéricas que vão além dos operadores básicos da linguagem (Capítulo 13). A lista abaixo reúne as funções já normativas (com assinatura, descrição e exemplo completos); o conjunto pode ser estendido em revisões futuras.

| **Função**                                                                     | **Descrição**                                        | **Exemplo**                                     |
|--------------------------------------------------------------------------------|------------------------------------------------------|-------------------------------------------------|
| `math.abs(int | decim)`                                                        | Retorna o valor absoluto de um número.               | `math.abs(-5)` → `5`                            |
| `math.ceil(int | decim)`                                                       | Arredonda um número para cima (teto).                | `math.ceil(4.2)` → `5`                          |
| `math.floor(int | decim)`                                                      | Arredonda um número para baixo (piso).               | `math.floor(4.8)` → `4`                         |
| `math.pow(base, exp)`                                                          | Eleva a base ao expoente fornecido.                  | `math.pow(2, 3)` → `8`                          |
| `math.sqrt(int | decim)`                                                       | Retorna a raiz quadrada do número.                   | `math.sqrt(16)` → `4`                           |
| `math.sin(rad)`                                                                | Retorna o seno do ângulo informado, em radianos.     | `math.sin(1.5707963267948966)` → `1.0`          |
| `math.cos(rad)`                                                                | Retorna o cosseno do ângulo informado, em radianos.  | `math.cos(0)` → `1.0`                           |
| `math.tan(rad)`                                                                | Retorna a tangente do ângulo informado, em radianos. | `math.tan(0.7853981633974483)` → `1.0`          |
| `math.asin(int | decim)` / `math.acos(int | decim)` / `math.atan(int | decim)` | Funções trigonométricas inversas.                    | `math.asin(0.5)` → `0.5235987755982989` (30°)   |
| `math.atan2(y, x)`                                                             | Retorna o arco-tangente de dois argumentos.          | `math.atan2(1, 1)` → `0.7853981633974483` (45°) |
| `math.radians(graus)`                                                          | Converte graus para radianos.                        | `math.radians(180)` → `3.141592653589793`       |
| `math.degrees(rad)`                                                            | Converte radianos para graus.                        | `math.degrees(3.141592653589793)` → `180.0`     |

**Constantes globais:**

- `math.PI` **— valor aproximado de π (3,14159...).**

- `math.E` **— constante de Euler (2,71828...).**

**Tratamento de erros:** tentativas de divisão por zero através de funções matemáticas, ou de raiz quadrada de números negativos (`math.sqrt(-1)`), interrompem a execução imediatamente com um erro de domínio em tempo de execução.

### Módulo pen

O módulo `pen` implementa desenho e renderização por meio de um cursor no plano cartesiano (modelo de tartaruga gráfica).

| **Função**                                  | **Efeito**                                                                                                  |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `pen.init(x, y)`                            | Define o ponto inicial do cursor no plano cartesiano.                                                       |
| `pen.move(dir, num)` / `pen.move(num, num)` | Move a caneta na direção especificada (`"forward"`, `"back"`, `"left"`, `"right"`) por uma distância `num`. |
| `pen.turn(graus)`                           | Rotaciona o ângulo do cursor (ex.: 90, 180).                                                                |
| `pen.up()`                                  | Levanta a caneta (move sem desenhar rastro).                                                                |
| `pen.down()`                                | Abaixa a caneta (ativa o rastro de desenho).                                                                |
| `pen.color(str)`                            | Altera a cor do rastro (aceita valores hexadecimais ou nomes de cor).                                       |
| `pen.size(num)`                             | Define a espessura da linha.                                                                                |
| `pen.speed(num ou str)`                     | Define a velocidade da caneta.                                                                              |

#### Integração com o Sistema de Modificadores

O módulo `pen` expressa seu potencial máximo quando combinado com blocos `repeat` aninhados (Capítulo 27), que multiplicam naturalmente o total de repetições.

```tinypine
use pen
pen.init(0, 0)
pen.down()
repeat 4
  pen.move("forward", 100)
  pen.turn(90)
  pause 0.5   # aguarda meio segundo entre cada traço
```

*Exemplo 1 — Desenho de um quadrado com pausa visual*

```tinypine
|| Executa 4 x 36 = 144 iterações na árvore de execução do parser ||
repeat 4
  repeat 36
    pen.move("forward", 50)
    pen.turn(10)
```

*Exemplo 2 — Padrão geométrico complexo (composição / multiplicação)*

#### Tratamento de Erros

Seguindo o princípio geral de que nenhum erro é silencioso (Capítulo 36), o módulo `pen` interrompe a execução imediatamente com um erro de tipo em tempo de execução se `pen.move()` receber um argumento inválido (por exemplo, `pen.move("forward", "muito")`). Parâmetros de graus ou distâncias aceitam `: to-num` e suas variantes (`int`, `float`).

### Módulo random

O módulo `random` fornece funções para geração de números pseudoaleatórios determinísticos, baseados em um estado interno oculto. Não gera aleatoriedade criptográfica — seu foco é reprodutibilidade e independência de hardware.

#### Modelo de Estado e Determinismo

O módulo mantém um estado interno privado, contendo uma semente (*seed*) inteira e um contador de passos (*cursor*).

- **Pureza de estado: mesma semente + mesma ordem de chamadas ⇒ exatamente os mesmos resultados.**

- **Independência: o avanço do estado não depende do tempo de execução em tempo real, de FPS ou de renderização.**

#### Inicialização e Controle

| **Função**               | **Descrição**                                                                                                                                       |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `random.seed(config)`    | Configura ou reinicia o gerador interno. Aceita um valor int.                                                                                       |
| `random.clone("offset")` | Retorna uma nova instância isolada do gerador, baseada no estado atual somado a um deslocamento (*offset*) inteiro. Útil para simulações paralelas. |

```tinypine
use random
random.seed(12345)   # define a semente fixa
```

#### Funções Públicas

Todas as funções do módulo seguem o sistema de tipos primitivos do TinyPine.

| **Função**                   | **Descrição**                                                                                                                                                                       |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `random.int(min, max)`       | Retorna um int pseudoaleatório no intervalo inclusivo \[min, max\]. Regra: se min \> max, dispara `InvalidRandomRange PROBLEM`.                                                     |
| `random.float()`             | Retorna um float normalizado no intervalo \[0.0, 1.0) — inclui 0.0, mas é estritamente menor que 1.0. A precisão segue o padrão de ponto flutuante de 64 bits da linguagem.         |
| `random.bool(probabilidade)` | Retorna um bool pseudoaleatório. O parâmetro probabilidade é um float opcional entre 0.0 e 1.0 (padrão: 0.5), e representa a chance de o resultado ser true.                        |
| `random.pick(colecao)`       | Seleciona e retorna um elemento pseudoaleatório de uma coleção. Regra: a coleção não pode estar vazia — tentar escolher de uma coleção vazia dispara `EmptyCollectionPick PROBLEM`. |

```tinypine
var acertou = random.bool(0.75)   # 75% de chance de ser true
var itens = ["espada", "escudo", "poção"]
var drop = random.pick(itens)
```

#### Casos de Borda

| **Caso / Entrada**              | **Comportamento formal**                      | **Código do erro**                       |
|---------------------------------|-----------------------------------------------|------------------------------------------|
| `random.int(“min”:10, “max”:1)` | min maior que max.                            | `InvalidRandomRange (E601) PROBLEM`      |
| `random.pick([])`               | Tentativa de escolher de uma coleção vazia.   | `EmptyCollectionPick (E602) PROBLEM`     |
| `random.seed(3.14)`             | Passagem de um float para a semente.          | `InvalidSeedType (E603) PROBLEM`         |
| `random.bool(-0.5)`             | Probabilidade fora do intervalo \[0.0, 1.0\]. | `InvalidProbabilityRange (E604) PROBLEM` |

#### Exemplo de Uso no Fluxo da Linguagem

```tinypine
use random, system
var run = 1: to-int
random.seed(999)   # garante o mesmo drop em toda execução
case run
  is 1
    var loot = ["ouro", "madeira", "rubi"]
    var item_ganho = random.pick(loot)
    if item_ganho == "rubi"
      print("Drop raro conseguido!")
```

### Módulo debug

Está planejada a criação de um módulo `debug`, destinado à inspeção interna do interpretador e do programa em execução, importável como os demais módulos da biblioteca padrão. Este módulo é distinto do bloco de controle nativo `debug.*()` (Capítulo 29.1) — ambos compartilham o nome provisoriamente; o nome definitivo deste módulo importável ainda está a confirmar (ver Histórico, Apêndice A).

```tinypine
use debug
```

Métodos previstos:

| **Função**       | **Descrição**                                                       |
|------------------|---------------------------------------------------------------------|
| `debug.tree()`   | Exibe a árvore de execução.                                         |
| `debug.ast()`    | Exibe a *Abstract Syntax Tree* (AST).                               |
| `debug.tokens()` | Lista os tokens produzidos pelo analisador léxico.                  |
| `debug.ids()`    | Lista todos os identificadores registrados durante o processamento. |
| `debug.memory()` | Mostra informações sobre utilização de memória.                     |
| `debug.time()`   | Exibe o tempo gasto em cada etapa da execução.                      |

O módulo poderá ser expandido futuramente com novas ferramentas de diagnóstico, mantendo a mesma interface baseada em namespaces usada pelos demais módulos da linguagem.

### Módulo os

O módulo `os` reúne operações de manipulação de recursos do ambiente hospedeiro, com foco no sistema de arquivos. Segue a regra conceitual central que separa os dois módulos do sistema (ver também 34.7): `os` manipula recursos — ele não interage com processos ou aplicações em execução.

| **Função**                   | **Efeito**                                                                                                                  |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `os.create(name, type, dir)` | Cria um novo recurso (por exemplo, um arquivo) no diretório informado. O parâmetro type é uma string (por exemplo, "file"). |
| `os.write(file, conteúdo)`   | Escreve conteúdo em um arquivo existente.                                                                                   |
| `os.read(file)`              | Lê o conteúdo de um arquivo.                                                                                                |
| `os.delete(file)`            | Remove um arquivo do sistema de arquivos.                                                                                   |
| `os.copy(origem, destino)`   | Copia um recurso de um caminho para outro.                                                                                  |
| `os.move(origem, destino)`   | Move ou renomeia um recurso.                                                                                                |
| `os.exists(caminho)`         | Verifica se um recurso existe no caminho informado.                                                                         |
| `os.env(nome)`               | Consulta uma variável de ambiente do sistema.                                                                               |

```tinypine
use os

os.create(
    name:"teste.txt",
    type:"file",
    dir:"C:\Temp"
)

os.write(
    file:"C:\Temp\teste.txt",
    "oiii"
)
```

*Exemplo — criação e escrita em arquivo via os*

A leitura de um arquivo inexistente (`os.read`) já segue o modelo geral de erros recuperáveis e pode ser capturada com `try` / `catch` (Capítulo 24). A assinatura completa, os parâmetros nomeados e o comportamento de erro das demais funções do módulo ainda não estão fechados (ver Histórico, Apêndice A).

### Módulo computer

O módulo `computer` representa a interação com a máquina hospedeira (shell, área de transferência e teclado), em contraste com os (34.6), que manipula recursos do ambiente. Funções de execução não recebem um nome dedicado (como `run`); em vez disso, o destino de um valor enviado pelo operador \|\> (34.8) determina o que acontece com ele.

| **Função**                                        | **Efeito**                                                                                                                                                                                                                                                                  |
|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `computer.shell(programa, valor)`                 | Executa `valor` (um comando) no interpretador de shell `programa` (por exemplo, `cmd`, `pwsh`, `bash`; também aceita caminhos) e devolve um dict com `"input"`, `"output-type"` e `"output"`. `computer.shell(programa)`, sem `valor`, é o destino do operador `\|>` (34.8). |
| `computer.clipboard.content`                      | Devolve o conteúdo atual da área de transferência (`str`). `computer.clipboard`, sem `.content`, é destino de `\|>`: `"texto" \|> computer.clipboard` copia o texto.                                                                                                          |
| `computer.keyboard.press("key": "e")`             | Pressiona a tecla `"e"` (`"key"`) ou uma combinação (`"keys"`, lista). Sem argumento é `MissingArgument PROBLEM`.                                                                                                                                                           |
| `computer.keyboard.pressed("key": "e")`           | Devolve `true` se a tecla `"e"` (ou todas as de `"keys"`) está pressionada no momento da chamada. Sem argumento, ou com `"*"`, pergunta por qualquer tecla.                                                                                                                 |
| `computer.keyboard.write("text": "Hello World!")` | Escreve o texto usando o teclado                                                                                                                                                                                                                                            |

```tinypine
use computer

println("dir" |> computer.shell("cmd"))
```

*Exemplo — envio de dados para um shell via computer*

Diferente do modelo geral de erros recuperáveis, `computer.shell` não interrompe a execução quando o comando falha: a falha volta no próprio dict, com "output-type" igual a "1" e a mensagem de erro do processo (por exemplo, do PowerShell) em "output" — não há exceção capturável por try / catch. O módulo não tem funções para abrir aplicativos nem para ler uma linha do console (a entrada de linha é o readln(), Capítulo 21); o comportamento de erro das funções de área de transferência e de teclado, os nomes de tecla e o comportamento por plataforma estão descritos abaixo e ainda dependem de confirmação (ver Histórico, Apêndice A, B13 e B25).

**Dict de** `computer.shell`**.** Tem sempre as três chaves, e os três valores são `str`: `"input"` é o comando enviado, por inteiro; `"output"` é a saída padrão, sem a quebra de linha final; `"output-type"` é `"0"` quando o comando terminou bem (a saída vem do stdout) e `"1"` quando falhou — comando inexistente, código de saída diferente de zero ou exceção do processo — caso em que `"output"` traz a saída de erro. `computer.shell(programa, valor)` e `valor |> computer.shell(programa)` devolvem o mesmo dict.

**Área de transferência.** No Windows, o interpretador usa a API do sistema; nos demais sistemas depende de uma ferramenta externa (`wl-copy`/`wl-paste`, `xclip`, `xsel`, `pbcopy`/`pbpaste`, a que existir) e, sem nenhuma delas, a chamada é `NotImplemented PROBLEM`.

`"key"` **e** `"keys"`**.** `"key"` recebe uma tecla (`str`) e também liga por posição (`pressed("space")`); `"keys"` recebe uma combinação (lista de `str`) e só liga por nome — a diferença entre os dois nomes é intencional. Passar uma lista em `"key"`, um texto em `"keys"`, os dois juntos ou uma lista vazia é `TypeMismatch PROBLEM`. Em `press("keys": [a, b, c])` as teclas descem na ordem dada e sobem na ordem inversa (o modo de escrever `shift` + `3`); `pressed("keys": [...])` é `true` só se todas estão pressionadas ao mesmo tempo. `pressed()` sem argumento, ou com `"*"`, pergunta por qualquer tecla; `press()` sem tecla é `MissingArgument PROBLEM`.

**Nomes de tecla.** Letras `a` a `z`, dígitos `0` a `9`, `f1` a `f12` e `enter`, `space`, `esc`, `tab`, `backspace`, `delete`, `up`, `down`, `left`, `right`, `home`, `end`, `pageup`, `pagedown`, `shift`, `ctrl`, `alt`. Maiúsculas e minúsculas não se distinguem (`"E"` é `"e"`), e há apelidos (`return`, `escape`, `spacebar`, `del`, `control`, `pgup`, `pgdn`, `bksp`). Nome fora da lista é `InvalidKey PROBLEM` (E617); falha do sistema ao pressionar ou escrever é `ComputerKeyboardError PROBLEM` (E618).

**Plataformas.** No Windows, `press` e `write` usam a API de entrada do sistema, e `pressed` lê o estado real do teclado, mesmo com o terminal sem foco. No Linux, `press` e `write` precisam do comando `xdotool` (X11), e `pressed` lê o terminal: como terminais não avisam quando a tecla é solta, vale uma janela de 200 ms depois do último evento — uma aproximação, que consome as teclas lidas (um `readln()` depois delas não as vê). Sem `xdotool`, ou com a entrada do terminal redirecionada, ou em outros sistemas, a chamada é `NotImplemented PROBLEM`.

Exemplo:

```tinypine
use computer

computer.keyboard.press("key": "e")                 # pressiona "e"
computer.keyboard.press("keys": ["shift", "3"])     # combinação: shift + 3
println(computer.keyboard.pressed("keys": ["alt", "m"]))
computer.keyboard.write("text": "Hello World!")

R = computer.shell("pwsh", "Write-Output 'Hello World!'")
println(R)
# saída: {"input": "Write-Output 'Hello World!'", "output-type": "0", "output": "Hello World!"}
println(R["output"])    # Hello World!
```

computer.keyboard.pressed("keys": \["alt", "m"\]) \# nota, a diferença entre “key” e “Keys” nessa função  
  
println(computer.shell(`"pwsh", "Write-Output 'Hello World!'"`))  
\# saída: {"input": "Write-Output `'Hello World!'`", "output-type": "0", "output": "`Hello World!`"}

### Operador de Encaminhamento — \|\>

O operador `|>` funciona como um operador de encaminhamento (pipeline), na forma geral `VALOR |> DESTINO`. O valor à esquerda é enviado ao destino à direita, e é o destino que determina o que acontece com o valor — enviar um comando a um shell ou um texto à área de transferência são todos comportamentos do destino, não do operador.

```tinypine
"dir" |> computer.shell("cmd")
```

*Exemplo 1 — envio de um comando para um shell*

O resultado produzido pelo destino pode ser usado pela próxima operação, de modo que `|>` também funciona como um pipe semântico — conceitualmente equivalente a `A |> B`, mas em uma forma mais legível:

```tinypine
print(
    "dir" |> computer.shell("cmd")
)
```

*Exemplo 2 — encadeamento do resultado de \|\> em print*

A linguagem evita uma função de execução dedicada, como `computer.run(...)`; a execução é representada pelo destino do encaminhamento (por exemplo, `script |> computer.shell("node")`), o que torna a linguagem mais uniforme.

Um destino `computer.shell(programa)` devolve o mesmo dict de `computer.shell(programa, valor)` (34.7), de modo que `println("dir" |> computer.shell("cmd"))` imprime o dict inteiro. A semântica formal de \|\> em caso de destino inválido, e o tipo do valor retornado quando o destino não produz saída (como `computer.clipboard`), ainda não estão fechados (ver Histórico, Apêndice A).

**Aviso:** os Capítulos 1–34 (Partes I–VII) já cobrem tudo que é preciso pra escrever programas em TinyPine. Os capítulos desta parte documentam o funcionamento interno do interpretador (pipeline de processamento, tabelas exaustivas de casos de borda, catálogo de códigos de erro, análise estática) — referência de consulta, não leitura obrigatória pra usar a linguagem no dia a dia. Quem só quer escrever TinyPine pode parar por aqui; quem quer entender como o interpretador decide o que decide, ou depurar um caso extremo, continua.
