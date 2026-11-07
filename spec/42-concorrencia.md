## Concorrência

A concorrência do TinyPine é construída em camadas. Cada camada resolve um problema diferente, e quase todo programa precisa só das duas primeiras:

| **Camada**                  | **Para quê**                                                         | **Peças**                                                |
|-----------------------------|----------------------------------------------------------------------|----------------------------------------------------------|
| 1. Tarefas cooperativas     | Esperar sem travar o resto: arquivos, comandos, temporizadores, UI.  | `f async`, `await`, `pause`                              |
| 2. Concorrência estruturada | Garantir que nenhuma tarefa fique perdida e que erros apareçam.      | `scope`, `with parallel`, `with timeout`, cancelamento   |
| 3. Comunicação              | Tarefas conversando sem compartilhar variáveis.                      | `chan`, `select`                                         |
| 4. Paralelismo real         | Usar vários núcleos do processador em trabalho pesado.               | `thread`, `lock`, `task.atomic`                          |

Os princípios que orientam o capítulo seguem os do Capítulo 2:

- **Comportamento previsível.** Tarefas `async` não sofrem preempção: só trocam de lugar em **pontos de suspensão** que estão escritos no código (42.2.5). Sem threads nem E/S real, o mesmo programa produz sempre a mesma ordem de execução (42.11).

- **Nada fica perdido.** Toda tarefa pertence a um escopo, e um escopo só termina quando todas as suas tarefas terminam (42.3). Um erro numa tarefa sempre chega a alguém (42.10).

- **Controle explícito.** Cancelamento, prazo, limite de simultaneidade e política de falha são parâmetros do próprio bloco, não código manual (42.3 e 42.4).

- **Leitura natural.** Esperar é `await`, enviar é `|>`, proteger é `lock`, escolher entre eventos é `select`. Só `|>` é símbolo, e ele já existia (Capítulo 34.8).

> ***Nota:*** *esta é a revisão que substitui o rascunho anterior do capítulo. As decisões que mudaram em relação a ele — por exemplo, `async` deixou de ser prefixo de chamada, o recebimento de canal deixou de usar `<|` e `case` deixou de ser usado no `select` — estão registradas no Apêndice A.6 (Sessão de concorrência).*

### Palavras e Módulo

A concorrência acrescenta **palavras da linguagem**, sempre disponíveis, e um **módulo**, `task`, que se importa como qualquer outro (Capítulo 33):

| **Palavra**  | **Papel**                                                        | **Onde vale**                                  |
|--------------|------------------------------------------------------------------|------------------------------------------------|
| `async`      | modificador de função: ela pode esperar com `await`              | depois de `f` (e de `f const`)                 |
| `await`      | espera um resultado sem travar as outras tarefas                 | expressão; dentro de `f async` ou no topo      |
| `scope`      | abre um escopo de tarefas                                        | instrução em bloco                             |
| `with`       | abreviações de `scope`: `with parallel`, `with timeout`          | instrução em bloco                             |
| `thread`     | executa uma chamada numa thread do sistema                       | expressão                                      |
| `lock`       | região crítica com liberação automática                          | instrução em bloco                             |
| `select`     | espera por vários eventos ao mesmo tempo                         | instrução em bloco                             |
| `when`, `timeout`, `parallel`, `fair` | palavras **contextuais**: só têm sentido dentro de `select`, `with`, `for` e `scope` | nesses blocos |

As palavras contextuais continuam podendo ser usadas como nome de variável ou de função fora desses lugares. As demais seguem a regra geral do Capítulo 36: reutilizar uma palavra da linguagem como nome gera `NameReuse WARNING` (W202).

```tinypine
use task            # canais, mutex, semáforo, barreira, atômicos, all/any/map, relógio
```

Tudo que `task` oferece está no Capítulo 42.14. Os tipos dos valores que ele cria — `task`, `chan`, `mutex`, `semaphore`, `barrier`, `atomic` e `context` — são nomes de tipo como `int` ou `function` (Capítulo 6.7): servem em `var x: chan`, em asserções e em `.type`.

### Tarefas — f async e await

#### Declaração

Uma função que pode esperar é declarada com `async` logo depois de `f` (e de `const`, quando houver):

```tinypine
f async lerArquivo(caminho)
  println("lendo", caminho)
  var texto = await os.read(caminho)
  return texto

f const async fixa()
  pause 0.1
  return 1
```

A forma anônima é `f async (parâmetros)` e vale em qualquer lugar onde uma função anônima vale (Capítulo 31), inclusive como método de dicionário ou handler do Canvas. Métodos de classe também podem ser `f async` (Capítulo 32).

`async` é **só um modificador de declaração**. Não existe `async` como prefixo de chamada: quem escrevia `async trabalho()` passa a escrever `trabalho()`.

#### Chamar uma função async cria uma tarefa

Chamar uma função `async` **não executa o corpo na hora**. A chamada resolve os argumentos, cria uma **tarefa** e devolve o seu *handle*, um valor de tipo `task`. O corpo roda depois, no agendador (42.11).

```tinypine
f async somar(a, b)
  pause 0.2
  return a + b

var t = somar(1, 2)        # cria a tarefa; o corpo ainda não rodou
println(t.state)           # pending
println(await t)           # 3
println(t.state)           # done
```

Duas regras decorrem disso:

- **Argumentos são resolvidos na chamada**, na tarefa de quem chama. `somar(1)` com argumento faltando é `MissingArgument PROBLEM` (E501) *aí*, no ponto da chamada, e não dentro da nova tarefa (Capítulo 30.8).

- **O tipo de retorno declarado de uma função `async` é o tipo do resultado**, isto é, o que `await` devolve, e não `task`. Em `f async nome(): str` o resultado é `str`; a chamada `nome()` continua devolvendo uma `task`.

#### Quando a tarefa começa

Uma tarefa nova entra no fim da fila de prontas e **só começa a rodar quando quem a criou chega a um ponto de suspensão**. Por isso a ordem é sempre a mesma:

```tinypine
f async exemplo()
  println("2 - a tarefa começou")
  pause 1
  println("3 - a tarefa terminou")

var t = exemplo()
println("1 - isto sai primeiro")     # quem criou ainda não cedeu a vez
await t                              # aqui a tarefa roda
println("4 - fim")
```

*Saída: 1, 2, (1 s depois) 3, 4.*

#### await

`await expr` suspende **apenas a tarefa atual** até `expr` ter um resultado, enquanto as demais continuam. Os operandos que `await` entende:

| **Operando**                                   | **O que `await` devolve**                                                               |
|------------------------------------------------|-----------------------------------------------------------------------------------------|
| uma `task` ou a chamada de uma `f async`       | o resultado da tarefa; se ela falhou, o erro é relançado ali; se foi cancelada, `TaskCancelled` (E811) |
| um `chan` (Capítulo 42.5)                      | o próximo valor do canal                                                                |
| uma `barrier` (Capítulo 42.8)                  | o número de chegada na barreira                                                         |
| `task.all(...)`, `task.any(...)`, `task.join(...)`, `task.map(...)` | o resultado da espera coletiva (42.9)                                    |
| `task.yield()`                                 | `null`, depois de deixar as outras tarefas rodarem uma vez                              |
| função nativa **suspensível** (abaixo)         | o mesmo valor que a chamada comum devolveria                                            |

Qualquer outro operando — um número, uma `str`, uma lista — não tem o que esperar: `await` devolve o próprio valor e emite `NoopAwait WARNING` (W801), no mesmo espírito do `NoopPause` (Capítulo 26).

`await` fora de uma função `async` é `AwaitOutsideAsync PROBLEM` (E801), com **uma exceção**: no **nível de cima do programa** `await` é permitido, porque o próprio programa é uma tarefa (a *tarefa raiz*, 42.3.4). `await` não atravessa função: uma função comum chamada de uma `async` não pode usá-lo.

**Funções nativas suspensíveis.** Algumas funções da biblioteca padrão demoram por natureza: `readln`, `os.read`, `os.write`, `os.copy`, `os.move` e `computer.shell`. Chamadas **sem** `await`, elas bloqueiam o programa inteiro, como sempre bloquearam. Chamadas **com** `await`, elas rodam sem bloquear as outras tarefas:

```tinypine
var nome = await readln()                 # a janela e as outras tarefas continuam vivas
var dados = await os.read("dados.txt")
```

Dentro de uma função `async`, chamar uma suspensível sem `await` emite `BlockingCall WARNING` (W803) — é quase sempre esquecimento. As demais funções nativas (`math.sqrt`, `os.exists`, `os.env`…) são instantâneas e não precisam de `await`.

#### Pontos de suspensão

Uma tarefa **só cede a vez** nos pontos abaixo. Entre dois deles, o código roda sem interrupção:

1. `await`;
2. `pause` (dentro de uma tarefa, ver abaixo);
3. enviar para um canal com `|>`, quando o canal está cheio ou sem receptor (42.5);
4. `for` sobre um canal (42.5);
5. `select` (42.6);
6. `lock` (42.8);
7. o fim de um `scope` ou de um `with` (join das filhas, 42.3) e o fim da própria tarefa.

São também esses os **pontos de cancelamento** (42.4): é neles que um pedido de cancelamento é entregue.

#### pause dentro de tarefas

`pause` (Capítulo 26) significa "suspender **o fluxo atual** por este tempo":

| **Onde**                                          | **O que `pause n` faz**                                             |
|---------------------------------------------------|---------------------------------------------------------------------|
| programa sem tarefas, ou função comum             | espera `n` segundos; nada mais roda (o comportamento de sempre)     |
| dentro de uma tarefa (`f async` ou topo, havendo outras tarefas) | suspende **só aquela tarefa**; as outras continuam    |
| dentro de uma `thread`                            | bloqueia só aquela thread                                           |

`pause Infinity` numa tarefa suspende até ela ser cancelada, o que é uma forma simples de "ficar de pé" até o escopo terminar. Uma função **comum** chamada por uma tarefa não consegue ceder a vez: se ela fizer `pause`, as outras tarefas esperam junto, e o aviso `BlockingCall` (W803) lembra de declarar a função como `async`.

#### O handle de uma tarefa

| **Membro**     | **Tipo**   | **Significado**                                                                                  |
|----------------|------------|--------------------------------------------------------------------------------------------------|
| `t.state`      | `str`      | `"pending"` (criada, ainda não começou), `"running"` (começou e não terminou, mesmo suspensa), `"done"`, `"failed"` ou `"cancelled"` |
| `t.done`       | `bool`     | `true` quando o estado é `done`, `failed` ou `cancelled`                                        |
| `t.result`     | qualquer   | o resultado de uma tarefa `done`. Em tarefa que não terminou: `TaskNotFinished PROBLEM` (E810)  |
| `t.error`      | erro ou `null` | o erro de uma tarefa `failed`; `null` nos demais casos                                       |
| `t.cancel()`   | `null`     | pede o cancelamento (42.4); não espera por ele                                                   |
| `t.detach()`   | `task`     | torna a tarefa uma **tarefa de fundo** (42.3.5) e devolve a própria tarefa                       |

Os membros de leitura são somente leitura: gravar em `t.state` é `ReadOnlyProperty PROBLEM` (E313).

### Escopos Estruturados — scope e with

#### Regra central

Toda tarefa pertence a um **escopo**, e **um escopo só termina quando todas as suas tarefas terminam**. É isso que impede as tarefas "perdidas" (*fire and forget*): o código depois do bloco só roda quando tudo que o bloco criou acabou.

```tinypine
use task

f async calcular(n)
  pause 0.1
  return n * n

scope
  var t1 = calcular(10)
  var t2 = calcular(20)
  var t3 = calcular(30)
  println("as três já foram criadas")     # sai antes de qualquer cálculo
# aqui as três terminaram
println(t1.result, t2.result, t3.result)  # 100 400 900
```

Dentro do bloco, o corpo continua rodando até chegar a um ponto de suspensão; as filhas começam quando o corpo cede a vez, e **o fim do bloco é um ponto de suspensão**.

#### Parâmetros do scope

`scope` aceita parâmetros nomeados no mesmo estilo do `for` (`nome=valor`, Capítulo 23):

```tinypine
scope timeout=2, policy="wait"
  ...
```

| **Parâmetro** | **Padrão**   | **Efeito**                                                                                                     |
|---------------|--------------|----------------------------------------------------------------------------------------------------------------|
| `timeout`     | `Infinity`   | prazo em segundos para o escopo inteiro. Estourou: as filhas são canceladas e o escopo lança `TimeoutExceeded` (E813) |
| `policy`      | `"cancel"`   | o que fazer quando uma filha **falha**: `"cancel"` cancela as irmãs na hora; `"wait"` deixa as outras terminarem |
| `ctx`         | nenhum       | liga o escopo a um `context` (42.4.4): cancelar o contexto cancela o escopo                                    |
| `limit`       | sem limite   | **só em `with parallel`**: no máximo `limit` filhas rodando ao mesmo tempo; as outras esperam a vez, em ordem   |

`timeout` negativo ou que não seja número é `InvalidTimeout PROBLEM` (E814). `limit` que não seja inteiro positivo é `InvalidLimit PROBLEM` (E818). Parâmetro que o bloco não declara é `UnknownNamedArgument PROBLEM` (E503).

#### with — as abreviações

| **Forma**                          | **Equivale a**                                                                |
|------------------------------------|-------------------------------------------------------------------------------|
| `with timeout 2`                   | `scope timeout=2`                                                             |
| `with parallel`                    | um `scope` em que **cada instrução do corpo vira uma tarefa filha**           |
| `with parallel limit=4, timeout=10`| `with parallel` com os parâmetros acima                                       |

Em `with parallel`, o corpo só pode conter **chamadas**: de função `async` (cria uma tarefa) ou `thread chamada` (cria uma thread). Qualquer outra instrução é `InvalidParallelBody PROBLEM` (E802). As filhas são criadas na ordem em que aparecem.

```tinypine
f async baixar(nome)
  pause 0.5
  println("baixou", nome)

with parallel limit=2
  baixar("a")
  baixar("b")
  baixar("c")          # espera uma das duas primeiras terminar
println("todas baixaram")
```

Se você precisa **guardar** os handles ou fazer qualquer outra coisa além de criar tarefas, use `scope`.

#### A tarefa raiz e o escopo de cada tarefa

- O **programa** é a *tarefa raiz*, e o arquivo inteiro é o seu *escopo raiz*. Uma tarefa criada fora de qualquer bloco `scope` pertence a ele, e **o fim do arquivo espera por todas** — o programa só termina quando elas terminam.

- **Toda tarefa tem o seu escopo implícito**: o corpo de uma função `async` também só termina quando as filhas que ela criou terminam. Uma tarefa nunca sobrevive à tarefa que a criou, a não ser que seja explicitamente desligada (abaixo).

- Uma tarefa criada dentro de um `scope` pertence a esse `scope`; criada fora de bloco, pertence ao escopo implícito da tarefa em que está.

Criar uma tarefa **fora** de um bloco, **sem guardar o handle**, sem `await` e sem `detach()` é provavelmente esquecimento, pois o erro dela só apareceria no fim do escopo: `DiscardedTask WARNING` (W802). Dentro de `scope`/`with parallel` esse aviso não existe.

#### Tarefas de fundo — detach

Algumas tarefas existem para viver o programa inteiro: um log, um indicador de "carregando". `t.detach()` as passa para o escopo raiz como **tarefas de fundo**: o programa **não espera por elas** no fim; elas são **canceladas** e têm a chance de limpar (`finally`).

```tinypine
f async piscar()
  while true
    println("...")
    pause 1

f async principal()
  pause 3
  println("trabalho principal terminou")

piscar().detach()          # vive até o programa acabar
await principal()          # ao fim, 'piscar' é cancelada, não esperada
```

#### Falhas, return e break dentro do escopo

- **Uma filha falhou.** Com `policy="cancel"` (padrão), as irmãs são canceladas, o escopo espera todas desenrolarem e então lança o erro. Se mais de uma filha falhou, o erro é `AggregateError` (E812); se foi uma só, **o próprio erro dela**, sem embrulho.

- **O corpo do escopo falhou** (um erro ou `throw` no próprio bloco): as filhas são canceladas e esperadas antes de o erro continuar subindo.

- **`return`, `break` e `continue`** dentro do corpo saem do bloco normalmente, mas as filhas ainda não terminadas são **canceladas e esperadas** antes. O escopo nunca "esquece" uma tarefa ao sair.

- `try`/`catch` por fora do `scope` captura o erro propagado (42.10).

### Cancelamento e Tempo Limite

#### Como o cancelamento funciona

Cancelar é um **pedido**: `t.cancel()`, o fim de um escopo que falhou, um prazo vencido. A tarefa o recebe no **próximo ponto de cancelamento** (42.2.5):

1. o ponto de suspensão onde ela está parada, ou o próximo que ela alcançar, dispara o sinal de cancelamento naquela tarefa;
2. o sinal **sobe** pela pilha da tarefa como `return`/`break`/`continue`/`done`: **não é interceptado por `try`/`catch`** (Capítulo 24), mas **os blocos `finally` rodam**;
3. as filhas da tarefa são canceladas e esperadas;
4. a tarefa termina com estado `"cancelled"`.

```tinypine
f async trabalhador()
  try
    while true
      println("trabalhando")
      pause 1
  finally
    println("limpando")           # roda mesmo cancelada

scope
  var t = trabalhador()
  pause 2.5
  t.cancel()
# saída: trabalhando (3 vezes), limpando
```

Uma tarefa que ainda está `"pending"` e é cancelada **nunca começa**.

Dentro de um `finally` disparado por cancelamento, os pontos de suspensão deixam de ser pontos de cancelamento: a limpeza pode usar `await` e `pause` e vai até o fim.

`await t` sobre uma tarefa cancelada lança `TaskCancelled PROBLEM` (E811) **em quem espera** — quem espera não foi cancelado, só o resultado nunca virá.

#### Laços longos: yield e task.cancelled

Tarefas `async` não sofrem preempção (42.11): um laço que nunca chega a um ponto de suspensão **monopoliza o agendador**, e ninguém consegue nem cancelá-lo nem fazer a janela repintar. Num laço longo, ceda a vez de tempos em tempos com `await task.yield()`, que é um ponto de suspensão e, portanto, também de cancelamento:

```tinypine
use task

f async processar(itens)
  for item in itens
    tratar(item)
    await task.yield()      # deixa as outras tarefas rodarem; entrega o cancelamento
```

Em uma **thread** (42.7) o laço roda em paralelo com as outras tarefas e pode ser cancelado de fora, mas só **ele mesmo** consegue parar: a propriedade somente leitura `task.cancelled` diz se a tarefa atual teve o cancelamento pedido.

```tinypine
use task

f somarMuito(n)               # função comum, executada em thread
  var total = 0
  var i = 0
  while i < n
    if task.cancelled
      return total            # sai com o que tem
    total = total + i
    i = i + 1
  return total

var t = thread somarMuito(1000000000)
pause 1
t.cancel()                    # o laço vê task.cancelled na próxima volta
println(await t)              # o total parcial
```

`await t` devolve o total parcial porque a função **retornou** (a tarefa terminou `done`); só um cancelamento entregue por um ponto de suspensão termina a tarefa como `"cancelled"`. Nas threads, `pause`, os canais e `lock` são pontos de cancelamento; o laço de cálculo precisa consultar `task.cancelled`.

#### Prazo: scope timeout e with timeout

Um prazo vencido **é um erro**; um cancelamento pedido por alguém **não é**:

| **Situação**                                 | **O que o escopo faz**                                                            |
|----------------------------------------------|-----------------------------------------------------------------------------------|
| o prazo (`timeout`) venceu                   | cancela as filhas, espera elas desenrolarem e lança `TimeoutExceeded` (E813)     |
| `ctx.cancel()` ou `t.cancel()` do dono       | cancela as filhas, espera e **termina sem erro**                                  |

```tinypine
try
  with timeout 2
    var dados = await os.read("grande.txt")
    println(dados.length)
catch(err)
  println("demorou demais")
```

O prazo vale para o bloco **inteiro**, não para cada instrução, e usa o relógio da tarefa (que pode ser virtual, 42.12). `timeout=0` vence assim que o corpo cede a vez pela primeira vez; `Infinity` é "sem prazo".

#### context — um cancelamento compartilhado

Um `context` é um interruptor de cancelamento que **vários escopos** podem observar, útil quando um pedido de cancelamento vem de fora da estrutura (um botão "Cancelar", um sinal de saída):

```tinypine
use task

var ctx = task.context("timeout": 30)      # opcional: o próprio contexto tem prazo

scope ctx=ctx
  var t = trabalhar()
  ...
```

| **Membro**                  | **Significado**                                                                  |
|-----------------------------|----------------------------------------------------------------------------------|
| `ctx.cancelled`             | `true` depois de `cancel()` ou de o prazo vencer                                 |
| `ctx.cancel()`              | cancela o contexto e, com ele, todos os escopos ligados (`scope ctx=ctx`)        |
| `ctx.remaining`             | segundos que faltam para o prazo (`Infinity` se não há prazo)                    |
| `ctx.child("timeout": s)`   | um contexto derivado: é cancelado quando o pai é, e pode ter um prazo menor      |

Um escopo ligado a um contexto cujo **prazo** venceu lança `TimeoutExceeded`; se o contexto foi **cancelado** por `ctx.cancel()`, o escopo termina sem erro, como na tabela acima.

### Canais

Um **canal** é uma fila segura por onde tarefas e threads trocam valores **sem compartilhar variáveis**. É a forma preferida de comunicação: quem recebe nunca mexe nos dados de quem enviou.

#### Criar e tipar

Canais são criados pelo módulo `task` e têm o tipo `chan`:

```tinypine
use task

var a = task.chan()            # sem buffer: o envio só termina quando alguém recebe
var b = task.chan(8)           # com buffer de 8 posições
var c: chan\values: int\ = task.chan(4)    # só aceita int
```

`chan` aceita **tipo refinado** (Capítulo 6.9), com as propriedades `values` (o tipo de todo valor que passa pelo canal) e `length` (quantos valores estão guardados no buffer agora). Cada envio é validado contra `values:`: um valor de outro tipo é `RefinementViolation PROBLEM` (E316) **no ponto do envio**. Sem refinamento, o canal aceita qualquer valor.

Capacidade negativa ou que não seja inteira é `InvalidCapacity PROBLEM` (E822). `task.chan(0)` é o mesmo que `task.chan()`.

| **Membro**     | **Tipo** | **Significado**                                                                   |
|----------------|----------|-----------------------------------------------------------------------------------|
| `c.length`     | `int`    | valores guardados no buffer neste instante                                        |
| `c.capacity`   | `int`    | tamanho do buffer (0 se não tem)                                                  |
| `c.closed`     | `bool`   | `true` depois de `c.close()`                                                      |
| `c.finished`   | `bool`   | `true` quando está fechado **e** o buffer já esvaziou                             |
| `c.close()`    | `bool`   | fecha o canal; devolve `true` se fechou agora e `false` se já estava fechado      |

#### Enviar e receber

```tinypine
42 |> c               # enviar  (o destino do |> é o canal)
var x = await c       # receber
await c               # receber e descartar
```

- **Enviar** usa o `|>` do Capítulo 34.8: o destino decide o que acontece com o valor, e um canal o recebe. Quando o canal está cheio (ou sem buffer e sem ninguém esperando), o envio **suspende** a tarefa. É um ponto de suspensão.
- **Receber** é um `await`: a tarefa espera até haver um valor. Quando há vários receptores esperando, cada valor vai para **um só**, na ordem em que chegaram.
- A ordem é **FIFO**, para os valores e para as tarefas que esperam.
- **`void` não passa por canais**: `void |> c` é `InvalidChannelValue PROBLEM` (E821). Para "nenhum valor", envie `null`.

#### Fechar

Quem **envia** é quem decide quando acabou, e avisa com `c.close()`:

- enviar para um canal fechado é `SendOnClosedChannel PROBLEM` (E820);
- quem já está esperando para enviar quando o canal fecha recebe o mesmo erro;
- receber de um canal fechado **continua entregando o que sobrou no buffer**; depois que esvazia, `await c` devolve `null` na hora, sem esperar. Para distinguir esse `null` de um `null` enviado de verdade, consulte `c.finished`;
- fechar um canal que já está fechado não é erro (devolve `false`).

Fechar também serve de **sinal para todos ao mesmo tempo**: todos os receptores acordam. É o jeito mais simples de dizer "pare" a muitas tarefas.

#### for sobre um canal

A forma natural de consumir um canal é o `for`, que recebe valor a valor **até o canal fechar e esvaziar**:

```tinypine
for x in c
  println("recebeu", x)
println("acabou")          # só chega aqui depois de c.close() e do último valor
```

`break` e `continue` funcionam como em qualquer `for` (Capítulo 23). Cada volta é um ponto de suspensão.

#### Canais e geradores

O `emit` do Capítulo 23 produz um fluxo **síncrono**, sob demanda, entre uma função e quem a chama. O canal é um fluxo **entre tarefas**. Um gerador alimenta um canal com um `for`:

```tinypine
f async alimentar(c)
  for v in pares(2)          # 'pares' é um gerador (Capítulo 23)
    v |> c
  c.close()
```

#### Exemplo — produtor e consumidor

```tinypine
use task

var c: chan\values: int\ = task.chan(4)

f async produtor()
  for i in [1 to 10]
    i |> c
  c.close()                  # avisa o consumidor que acabou

f async consumidor()
  for x in c
    println("recebeu", x)

with parallel
  produtor()
  consumidor()
```

### select — Esperar por Vários Eventos

`select` espera por **vários eventos ao mesmo tempo** e executa o bloco do **primeiro que estiver pronto**:

```tinypine
select
  when c1 as x
    println("recebeu de c1:", x)
  when 99 |> c2
    println("enviou 99 para c2")
  when timeout 0.5
    println("ninguém respondeu a tempo")
```

`select` usa `when` nos seus braços, e não `case`: `case` é do `match` (Capítulo 25) e tem outro significado.

#### Os braços

| **Braço**                    | **Está pronto quando…**                                                              | **O que o bloco recebe**                          |
|------------------------------|--------------------------------------------------------------------------------------|---------------------------------------------------|
| `when c as x` · `when c`     | o canal `c` tem um valor, ou está fechado                                            | `x` é o valor (`null` se o canal acabou); `as x` é opcional |
| `when v \|> c`               | o canal `c` aceita o envio agora                                                     | nada                                              |
| `when t as r` · `when t`     | a tarefa `t` terminou                                                                | `r` é o resultado; se `t` falhou, o erro é relançado; se foi cancelada, `TaskCancelled` |
| `when timeout n`             | passaram `n` segundos desde que o `select` começou a esperar                         | nada                                              |
| `else`                       | sempre — roda **na hora**, sem esperar por ninguém                                   | nada                                              |

#### Regras

1. **Avaliação única.** Os canais, as tarefas e os valores a enviar são avaliados **uma vez**, na ordem escrita, quando o `select` começa. Só **um** braço executa, e o `select` termina — para repetir, ponha o `select` dentro de um laço.
2. **Desempate previsível.** Se vários braços estão prontos ao mesmo tempo, vence o **primeiro, na ordem em que foram escritos**. Com `select fair`, vence um deles escolhido ao acaso pelo gerador do módulo `random` (Capítulo 34.4): a escolha respeita `random.seed` e, portanto, é reproduzível.
3. **Nada pronto.** Com `else`, executa o `else`. Com `when timeout`, espera até o prazo e executa aquele braço. Sem nenhum dos dois, **suspende** até algum braço ficar pronto.
4. **`else` e `timeout` não convivem**: o `timeout` nunca seria alcançado. Dois `else`, dois `timeout`, um `select` sem braços ou um braço que não é uma das formas da tabela são `InvalidSelect PROBLEM` (E803). O `else` fica por último.
5. **`break` e `continue` dentro de um braço** valem para o laço que contém o `select`: ele não é um laço.
6. **Canal fechado** está sempre pronto para receber (entrega `null`) e, num braço de envio, o braço está "pronto" e **lança** `SendOnClosedChannel` quando escolhido.

#### Tentar sem esperar

`select` com `else` é a forma de tentar uma operação **sem bloquear**:

```tinypine
select
  when c as x
    println("havia", x)
  else
    println("nada por agora")
```

#### Exemplo — servidor com parada

```tinypine
use task

f async servidor(entrada, parar)
  while true
    select
      when entrada as msg
        println("mensagem:", msg)
      when parar
        println("parando")
        return
      when timeout 5
        println("5 s sem mensagens")
```

Quem decide parar fecha o canal: `parar.close()` acorda o `servidor` (o canal fechado está pronto).

### Threads — Paralelismo Real

#### Quando usar

Tarefas `async` dividem **um** núcleo de processador, trocando de lugar nas esperas: servem para E/S, temporizadores e interface. Se o trabalho é **cálculo pesado** e há vários núcleos, use `thread`: cada thread roda **em paralelo de verdade**, numa thread do sistema.

#### Criar

`thread` precede **uma chamada** e devolve uma `task`, como a chamada de uma função `async`, com duas diferenças: a execução **começa na hora**, em paralelo, e a função pode ser **comum ou `async`**.

```tinypine
f fib(n)
  if n < 2
    return n
  return fib(n - 1) + fib(n - 2)

var t = thread fib(40)
println("thread lançada")
println(await t)              # 102334155
```

- Função **comum**: roda do começo ao fim na thread. `pause`, `lock`, `|>` para canal, `for` sobre canal e `select` **bloqueiam só aquela thread**. Como `await` não existe em função comum, ela recebe de um canal com `for x in c` ou com `select`; quem precisa de `await` declara a função como `async`.
- Função **`async`**: a thread tem o **seu próprio agendador cooperativo**; dentro dela valem `await`, `scope`, `with parallel` e `pause` cooperativo, e as tarefas criadas ali rodam **nessa thread**.
- O operando de `thread` que não é uma chamada de função é `InvalidThreadTarget PROBLEM` (E804).
- Threads podem ser filhas de um `scope` ou de um `with parallel` e valem as mesmas regras de falha e de cancelamento (42.3 e 42.4). O handle é uma `task` comum: `await`, `cancel()`, `state`, `result`.

`thread` **não finge**: se o ambiente não tem threads, a chamada é `ThreadsUnavailable PROBLEM` (E840). Quem quer um programa portátil consulta `task.threads` (`bool`) antes; `task.cores` (`int`) diz quantos processadores lógicos existem.

#### O que atravessa a fronteira entre threads

Para que ninguém compartilhe uma lista ou um dicionário por engano, os valores são tratados assim ao **entrar** numa thread (argumentos) e ao **sair** dela (resultado e valores enviados por canal):

| **Valor**                                                              | **Ao cruzar threads**                                                      |
|------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `int`, `float`, `decim`, `num`, `str`, `bool`, `null`                  | imutáveis: iguais em todo lugar                                            |
| `tuple` e coleção declarada `const` (Capítulo 18 e 19.5)               | **compartilhadas**, pois não mudam; uma coleção mutável *dentro* delas é copiada |
| `list` e `dict` mutáveis                                               | **copiadas em profundidade**: cada thread fica com a sua                   |
| `task`, `chan`, `mutex`, `semaphore`, `barrier`, `atomic`, `context`   | **sempre compartilhados**: são feitos para isso                            |

A cópia vale **só entre threads**. Entre tarefas `async` da mesma thread nada é copiado.

Variáveis de fora, lidas ou gravadas **dentro do corpo** de uma função executada em thread, continuam sendo as mesmas variáveis: é o caso que exige `lock` (42.8) ou `task.atomic`. Gravar numa `var` de fora, sem `lock`, a partir de uma função lançada com `thread` emite `UnprotectedSharedWrite WARNING` (W804).

#### Exemplo — soma em paralelo

```tinypine
use task

f somaParcial(parte)
  var s = 0
  for x in parte
    s = s + x
  return s

var partes = [[1 to 250], [251 to 500], [501 to 750], [751 to 1000]]
var somas = await task.map(somaParcial, partes, "mode": "thread")
println(somas[0] + somas[1] + somas[2] + somas[3])      # 500500
```

### Sincronização

#### Preciso mesmo de um lock?

| **Situação**                                                                                  | **Precisa de proteção?**                                          |
|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| várias tarefas `async` mexendo na mesma variável, **sem** ponto de suspensão no meio da operação | **não**: ninguém interrompe o código entre dois pontos de suspensão |
| várias tarefas `async` e **há `await`** (ou outro ponto de suspensão) no meio da operação      | **sim**: outra tarefa pode rodar ali no meio                      |
| **threads** mexendo na mesma variável                                                         | **sim**: `lock`, `task.atomic` ou um canal                        |

A regra para escolher: **prefira canais** (ninguém compartilha nada); use `task.atomic` para um contador ou um sinalizador; use `lock` quando um grupo de variáveis precisa mudar junto.

#### lock

`lock` adquire um `mutex` (ou um `semaphore`) na entrada do bloco e o **libera na saída, mesmo em caso de erro, `return` ou cancelamento**:

```tinypine
use task

var saldo = 100
var m = task.mutex()

f async sacar(valor)
  lock m
    var atual = saldo
    await task.yield()            # outra tarefa poderia rodar aqui...
    saldo = atual - valor         # ...mas está esperando o lock

with parallel
  sacar(30)
  sacar(30)
println(saldo)                    # 40 — sem o lock, daria 70
```

| **Forma**                   | **Efeito**                                                                                      |
|-----------------------------|-------------------------------------------------------------------------------------------------|
| `lock m`                    | espera a vez (FIFO) e executa o bloco                                                           |
| `lock m, timeout=0.5`       | se não conseguir em `0.5` s, lança `TimeoutExceeded` (E813) sem executar o bloco                |

- Esperar pelo lock é um ponto de suspensão e de cancelamento.
- O `mutex` **não é reentrante**: tentar travar de novo, **na mesma tarefa**, um mutex que ela já tem é um bloqueio certo, e o erro vem na hora — `DeadlockDetected PROBLEM` (E815).
- `m.locked` (`bool`) diz se o mutex está travado.
- `lock` sobre algo que não é `mutex` nem `semaphore` é `TypeMismatch PROBLEM` (E302).

#### Semáforo

`task.semaphore(n)` tem `n` permissões (inteiro positivo; senão, `InvalidPermitCount` E831). `lock s` pega **uma** e devolve ao sair do bloco. Serve para limitar a simultaneidade de um recurso:

```tinypine
use task

var vagas = task.semaphore(3)

f async baixar(nome)
  lock vagas                      # no máximo 3 dentro do bloco ao mesmo tempo
    pause 1
    println("baixou", nome)
```

`s.available` (`int`) diz quantas permissões estão livres.

#### Barreira

`task.barrier(n)` junta `n` participantes: `await b` suspende até que `n` tenham chegado, e então **todos** seguem. A barreira é **reutilizável** (a próxima rodada começa limpa). O valor de `await b` é a ordem de chegada daquela tarefa, de `0` a `n - 1`, útil para eleger quem faz uma tarefa única.

Se um participante falha ou é cancelado **enquanto os outros esperam**, a barreira quebra e os que esperam recebem `BarrierBroken PROBLEM` (E830): ninguém fica preso para sempre. `n` precisa ser inteiro positivo (`InvalidPermitCount`, E831).

#### Atômicos

`task.atomic(valor)` guarda **um valor escalar** (`int`, `float`, `decim`, `num`, `bool`, `str` ou `null`) que pode ser lido e mudado por várias threads **sem `lock`**:

| **Membro**              | **Efeito**                                                                          |
|-------------------------|-------------------------------------------------------------------------------------|
| `a.value`               | lê o valor atual                                                                    |
| `a.set(v)`              | grava `v`; devolve `null`                                                           |
| `a.add(n)`              | soma `n` (só números) e devolve o **novo** valor                                    |
| `a.swap(v)`             | grava `v` e devolve o valor **antigo**                                              |
| `a.cas(esperado, novo)` | grava `novo` só se o valor atual `===` `esperado`; devolve `true` se gravou         |

Um valor que não é escalar, ou `a.add` com algo que não é número, é `TypeMismatch PROBLEM` (E302).

```tinypine
use task

var contador = task.atomic(0)

f conta()
  repeat 1000
    contador.add(1)

with parallel
  thread conta()
  thread conta()
  thread conta()
println(contador.value)           # 3000
```

### Espera Coletiva e Laços Paralelos

#### task.all, task.any e task.join

As funções de espera coletiva do módulo `task` **devolvem uma tarefa**, então se usam com `await`. Elas aceitam tarefas (ou chamadas de função `async`) e também uma coleção espalhada com `unpack` (Capítulo 15):

| **Função**                 | **Resultado do `await`**                                                                          | **Quando uma falha**                                                       |
|----------------------------|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `task.all(t1, t2, ...)`    | lista com os resultados, **na ordem dos argumentos**                                              | a primeira falha cancela as outras e é relançada                           |
| `task.any(t1, t2, ...)`    | o resultado da **primeira que terminar com sucesso**; as outras são **canceladas**                | falhas são ignoradas enquanto alguma puder vencer; se todas falham, `AggregateError` |
| `task.join(t1, t2, ...)`   | `null`, depois que todas terminaram                                                               | como `task.all`                                                            |

`task.all` e `task.join` aceitam `"policy": "wait"`: nenhuma é cancelada, todas terminam, e só então o erro (ou o `AggregateError`) é lançado. Um argumento que não é tarefa é `TypeMismatch PROBLEM` (E302). `task.any()` sem argumentos é `MissingArgument PROBLEM` (E501); `task.all()` sem argumentos devolve `[]`.

```tinypine
use task

var tarefas = [calcular(10), calcular(20), calcular(30)]
var resultados = await task.all(unpack tarefas)          # [100, 400, 900]

var primeiro = await task.any(buscar("a"), buscar("b"))  # a mais rápida vence; a outra é cancelada
```

#### task.map

`task.map(f, colecao)` aplica `f` a cada elemento e devolve (via `await`) **a lista de resultados na ordem da coleção**, rodando as chamadas ao mesmo tempo:

```tinypine
f async dobro(x)
  pause 0.1
  return x * 2

var r = await task.map(dobro, [1, 2, 3, 4], "limit": 2)
println(r)                         # [2, 4, 6, 8]
```

| **Parâmetro** | **Padrão**             | **Efeito**                                                                              |
|---------------|------------------------|-----------------------------------------------------------------------------------------|
| `"limit"`     | sem limite (`task.cores` com threads) | no máximo `limit` chamadas ao mesmo tempo                                 |
| `"mode"`      | `"async"`              | `"async"`: cada chamada é uma tarefa e `f` precisa ser `async`; `"thread"`: cada chamada é uma `thread` e `f` pode ser comum ou `async` |

Em caso de falha vale a regra de `task.all`. `f` comum com `"mode": "async"` é `TypeMismatch` (E302): a função nunca cederia a vez, então não haveria concorrência.

#### for paralelo

O `for` (Capítulo 23) aceita dois parâmetros a mais, que o transformam num **escopo**: cada volta vira uma tarefa filha.

```tinypine
f async baixarTodos(nomes)
  for nome in nomes, parallel=true, limit=3
    await baixar(nome)
  println("terminou tudo")
```

| **Parâmetro**     | **Efeito**                                                                                   |
|-------------------|----------------------------------------------------------------------------------------------|
| `parallel=true`   | cada volta roda como uma tarefa `async`; o `for` só termina quando todas terminarem          |
| `limit=n`         | no máximo `n` voltas ao mesmo tempo                                                          |

Também valem `timeout` e `policy` (42.3.2). Regras:

- uma variável declarada **dentro** do corpo é local de cada volta; as de fora são compartilhadas, com as mesmas regras de 42.8;
- `continue` termina só aquela volta; `break` e `return` **cancelam as voltas que ainda rodam** e saem;
- as voltas começam na ordem da coleção, e a ordem dos **resultados** não importa aqui (use `task.map` quando importar);
- só existe a forma `async`; para paralelismo real use `task.map(..., "mode": "thread")`.

### Erros em Tarefas

#### Para onde vai o erro

Um erro numa tarefa **nunca some**. A tarefa termina com estado `"failed"`, guarda o erro em `t.error`, e ele aparece em **quem espera**:

| **Quem espera**                              | **O que acontece com o erro**                                                          |
|----------------------------------------------|----------------------------------------------------------------------------------------|
| `await t`                                    | é relançado ali, com o mesmo código e a mesma mensagem                                 |
| o fim de um `scope`/`with`                   | o primeiro erro (ou `AggregateError` se houve mais de um) é lançado depois do bloco   |
| `task.all`, `task.any`, `task.join`, `task.map` | segundo a tabela de 42.9                                                            |
| ninguém (tarefa raiz ou de fundo sem espera) | o programa termina com o bloco de erro padrão (Capítulo 36.7), com a pilha **da própria tarefa** |

`try`/`catch` funcionam como sempre (Capítulo 24), em qualquer desses pontos:

```tinypine
f async fragil(n)
  if n > 2
    throw "n grande demais"
  return n

try
  var r = await fragil(5)
catch(err)
  println("falhou:", err)
```

```tinypine
try
  scope
    var a = fragil(5)
    var b = fragil(6)
catch(err)
  println("erro no escopo:", err)
```

Quando **mais de uma** filha falha no mesmo escopo (com `policy="wait"`, ou duas falhas simultâneas), o erro lançado é `AggregateError PROBLEM` (E812) e o objeto de erro do `catch` traz a lista de todos em `err.errors`. Com uma só falha, o erro chega **sem embrulho**: quem escreveu `catch` para `DivisionByZero` continua capturando `DivisionByZero`.

#### O que o try não captura

- **O cancelamento.** É um sinal de controle como `return`, `break`, `continue` e `done`: sobe pela pilha, roda os `finally`, e **não** é interceptado por `catch` (Capítulo 24).
- O erro que *chega* a quem esperava uma tarefa cancelada (`TaskCancelled`, E811) é um erro comum e **é** capturado.

#### Deadlock

Se **todas** as tarefas vivas estão suspensas esperando umas pelas outras e **nada** pode acordá-las — nenhum prazo, nenhuma E/S pendente, nenhuma thread rodando —, o programa não conseguiria continuar nunca. Em vez de travar em silêncio, o agendador lança `DeadlockDetected PROBLEM` (E815) **na tarefa raiz**, no ponto onde ela está suspensa; as demais são canceladas pelo desenrolar dos escopos.

```tinypine
use task

var c = task.chan()        # sem buffer
1 |> c                     # ninguém recebe: DeadlockDetected, em vez de esperar para sempre
```

A mensagem lista o que cada tarefa esperava. Travar o mesmo `mutex` duas vezes na mesma tarefa é detectado **na hora** (42.8). Um programa que espera por E/S real (`readln`, `os.read`) ou por uma thread **não** é deadlock.

### Ordem de Execução e Modelo de Memória

#### O agendador

Cada thread — inclusive a principal — tem **um agendador cooperativo** com estas regras, que valem para toda implementação:

1. **Uma fila de prontas, FIFO.** Uma tarefa criada entra no fim da fila; uma tarefa acordada (por canal, por lock, por `await`) entra no fim da fila.
2. **Sem preempção.** A tarefa que roda só sai nos pontos de suspensão (42.2.5) ou ao terminar. Quem sai vai para o fim da fila, ou para a espera de algo.
3. **Temporizadores em ordem.** Prazos que vencem juntos acordam as tarefas pela ordem de **vencimento** e, em empate, pela ordem de **criação** do temporizador.
4. **Determinismo.** Num programa sem threads e sem E/S real, a ordem de tudo que acontece é a mesma em toda execução. A E/S e as threads são as únicas fontes de variação, e `task.virtual` (42.12) torna o tempo previsível também.

#### Modelo de memória

- **Variáveis locais** de uma tarefa são só dela.
- **Entre tarefas `async` da mesma thread** não há corrida de dados: o código entre dois pontos de suspensão roda sem interferência. Só é preciso proteger operações que **atravessam** um ponto de suspensão (42.8).
- **Entre threads**, dados mutáveis compartilhados precisam de `lock`, `task.atomic` ou de um canal. Os valores que atravessam a fronteira de threads seguem a tabela de 42.7.
- **Garantias de ordem (*happens-before*).** Entre threads, valem somente estas, e uma implementação pode assumir nada além delas:
  1. tudo que acontece antes de criar uma tarefa ou thread acontece antes do início dela;
  2. tudo que a tarefa fez acontece antes de o `await` (ou o fim do escopo) que a espera continuar;
  3. um envio acontece antes de o recebimento correspondente terminar, e `close` acontece antes de qualquer recebimento que perceba o fechamento;
  4. liberar um `mutex` (sair do `lock`) acontece antes da próxima aquisição dele; o mesmo vale para o `semaphore`;
  5. a chegada de cada participante numa `barrier` acontece antes de a espera de qualquer um terminar;
  6. cada operação de um `atomic` é indivisível, e as operações de um mesmo `atomic` têm uma ordem total.
- **Coletor de lixo (Capítulo 41).** É transparente: um valor continua vivo enquanto qualquer tarefa, thread ou canal o referencia.

### Relógio Virtual e Testes

O tempo de `pause`, `timeout` (de `scope`, `with`, `lock` e `select`) e dos prazos de `context` pode ser **virtual**, no mesmo espírito dos testes sem tela do Canvas (Capítulo 51): em vez de esperar de verdade, o agendador **avança o relógio** até o próximo prazo quando todas as tarefas estão esperando só por tempo.

```tinypine
use task
task.virtual(true)

f async lento()
  pause 3600                       # uma hora

try
  with timeout 5
    await lento()
catch(err)
  println("estourou o prazo")      # na hora, sem esperar 5 segundos
println(task.now())                # 5
```

| **Função**              | **Efeito**                                                                                          |
|-------------------------|-----------------------------------------------------------------------------------------------------|
| `task.virtual(ligado = true)` | liga (ou, com `false`, desliga) o relógio virtual                                               |
| `task.now()`            | segundos (`num`) desde o início do programa, no relógio em uso                                      |

- `task.virtual` só pode ser chamada **pela tarefa raiz, sem temporizadores pendentes**; senão, `InvalidClockChange PROBLEM` (E817). O lugar natural é a primeira linha do teste.
- O relógio só salta quando **nenhuma** tarefa está pronta e **nenhuma** E/S real está pendente. Com E/S real pendente (`await readln()`), o tempo continua passando de verdade.
- **Threads não são virtualizadas**: usam sempre o tempo real. Testes determinísticos devem usar tarefas `async`.
- O relógio de `canvas.advance` (Capítulo 51) é **independente** do de `task.virtual` nesta versão.

### Integração com o Canvas

#### O laço do canvas hospeda o agendador

Enquanto `canvas.run()` ou `canvas.poll()` está rodando (Capítulo 49), **o laço do canvas é o agendador**. Cada rodada faz, nesta ordem: recebe os eventos e chama os handlers; roda as tarefas prontas, cada uma até o próximo ponto de suspensão; vence os temporizadores; pinta. Por isso `await` e `pause` dentro de uma tarefa **não congelam a janela**, ao contrário de `pause` e `readln()` num handler comum.

- **Handlers podem ser `async`.** Um handler declarado `f async (e)` cria uma tarefa a cada evento; ela pertence ao escopo raiz. Um erro nela termina o programa com o bloco de erro padrão, como num handler comum (Capítulo 49).

- **Fatias lentas.** O aviso `SlowHandler` (W702) vale também para uma **fatia** de tarefa — o trecho entre dois pontos de suspensão — que passa do limite: um laço longo sem `await task.yield()` congela a janela do mesmo jeito.

- **Fim do programa.** `canvas.run()` volta quando a última janela fecha; em seguida o escopo raiz espera as tarefas que ainda rodam. Tarefas de fundo (`detach()`) são canceladas.

```tinypine
use canvas
use os

const w = canvas.window("id": "main", "name": "Leitor")
const estado = w.text("pronto", "id": "estado")
const botao = w.button("Ler", "id": "ler")

botao.on("click", f async (e)
  estado.text = "lendo..."
  var texto = await os.read("dados.txt")      # a janela continua viva
  estado.text = format "{texto.length} caracteres"
)

canvas.run()
```

#### Threads e o canvas — canvas.post

O canvas só pode ser usado pela **thread principal**. Qualquer outro membro de `canvas` ou de um elemento, chamado de dentro de uma thread, é `CanvasFromThread PROBLEM` (E841), no lugar do antigo "comportamento indefinido". A única porta de entrada para a interface, a partir de uma thread, é `canvas.post`:

| **Função**            | **Retorno** | **Efeito**                                                                                                      |
|-----------------------|-------------|-----------------------------------------------------------------------------------------------------------------|
| `canvas.post(f)`      | `null`      | agenda `f` para rodar **no laço do canvas, na thread principal**, na próxima rodada. `f` recebe um evento `e` com `e.kind == "post"`. Pode ser chamada de qualquer thread e também da principal |

Se não há laço rodando, `f` fica na fila até a próxima rodada. As funções agendadas rodam na ordem em que foram postadas.

```tinypine
use canvas
use task
use os

const w = canvas.window("id": "main", "name": "Cálculo")
const estado = w.text("calculando...", "id": "estado")

f contar()                          # função comum, roda em thread
  var total = 0
  var i = 0
  while i < 50000000
    total = total + i
    i = i + 1
  canvas.post(f(e)
    estado.text = format "total: {total}"
  )

thread contar()
canvas.run()
```

Para **receber** dados de uma thread dentro de um handler sem bloquear, use um canal e `select` com `else` no handler de `canvas.every`: ele nunca suspende, então é permitido numa função comum (42.16, `SuspendInSyncFunction`).

### Módulo task — Referência

O módulo `task` é importado com `use task` (Capítulo 33). Como todo módulo, é usado **sempre com o namespace**: `task.chan()`, nunca `chan()`.

#### Criação

| **Função**                          | **Retorno**  | **Descrição**                                                                                   |
|-------------------------------------|--------------|-------------------------------------------------------------------------------------------------|
| `task.chan(capacidade = 0)`         | `chan`       | cria um canal (42.5). `InvalidCapacity` (E822) se negativa ou não inteira                       |
| `task.mutex()`                      | `mutex`      | cria um mutex, usado com `lock` (42.8)                                                          |
| `task.semaphore(n)`                 | `semaphore`  | cria um semáforo com `n` permissões; `InvalidPermitCount` (E831) se `n` não é inteiro positivo   |
| `task.barrier(n)`                   | `barrier`    | cria uma barreira de `n` participantes; `InvalidPermitCount` (E831) se `n` não é inteiro positivo |
| `task.atomic(valor)`                | `atomic`     | cria um atômico com um valor escalar (42.8); não escalar é `TypeMismatch` (E302)                 |
| `task.context("timeout": s)`        | `context`    | cria um contexto de cancelamento, com prazo opcional em segundos (42.4)                         |

#### Espera

| **Função**                                            | **Retorno** | **Descrição**                                                                         |
|-------------------------------------------------------|-------------|---------------------------------------------------------------------------------------|
| `task.all(t1, ...)`                                   | `task`      | espera todas e junta os resultados em lista (42.9)                                    |
| `task.any(t1, ...)`                                   | `task`      | o resultado da primeira que termina com sucesso; cancela as outras (42.9)             |
| `task.join(t1, ...)`                                  | `task`      | espera todas, sem coletar valores (42.9)                                              |
| `task.map(f, colecao, "limit": n, "mode": m)`         | `task`      | aplica `f` a cada elemento, em ordem de resultado (42.9)                              |
| `task.yield()`                                        | `task`      | `await task.yield()` cede a vez uma vez (42.4.2)                                      |

#### Estado e ambiente

| **Membro**         | **Tipo** | **Descrição**                                                                                    |
|--------------------|----------|--------------------------------------------------------------------------------------------------|
| `task.cancelled`   | `bool`   | `true` se a tarefa (ou thread) atual teve o cancelamento pedido (42.4)                           |
| `task.threads`     | `bool`   | `true` se o ambiente tem threads reais                                                           |
| `task.cores`       | `int`    | número de processadores lógicos (pelo menos 1)                                                   |
| `task.virtual(ligado = true)` | `null` | liga ou desliga o relógio virtual (42.12)                                                |
| `task.now()`       | `num`    | segundos desde o início do programa, no relógio em uso                                           |

Todos os membros de leitura são somente leitura (`ReadOnlyProperty`, E313, ao gravar).

#### Funções nativas suspensíveis

As funções de outros módulos que podem ser esperadas com `await` sem bloquear (42.2.4) são: `readln`, `os.read`, `os.write`, `os.copy`, `os.move` e `computer.shell`. Os módulos ainda sem funções especificadas (`web`, `time`; Apêndice A.2, B2) devem declarar, ao serem especificados, quais das suas funções são suspensíveis.

### Gramática

A gramática de concorrência complementa a de funções (Capítulo 30.7). Notação como no Capítulo 30.7: terminais entre aspas, `|` alternativas, `[ ... ]` opcional, `{ ... }` repetição.

```ebnf
(* Declaração: ver também gramatica.ebnf (Capítulo 30.7) *)
FuncDecl      = "f" [ "const" ] [ "async" ] IDENT "(" [ ParamList ] ")" [ ":" Type ] Block ;
AnonFunc      = "f" [ "async" ] "(" [ ParamList ] ")" Block ;

(* Expressões: prefixos com a precedência de "not" (Capítulo 12.1) *)
AwaitExpr     = "await" Expr ;
ThreadExpr    = "thread" CallExpr ;

(* Escopos *)
ScopeStmt     = "scope" [ BlockArgs ] Block ;
WithStmt      = "with" ( "parallel" [ BlockArgs ] | "timeout" Expr ) Block ;
BlockArgs     = BlockArg { "," BlockArg } ;
BlockArg      = IDENT "=" Expr | STRING ":" Expr ;      (* timeout, policy, ctx, limit *)

(* Região crítica *)
LockStmt      = "lock" Expr [ "," BlockArg ] Block ;    (* só timeout *)

(* select *)
SelectStmt    = "select" [ "fair" ] { WhenArm } [ ElseArm ] ;
WhenArm       = "when" ( SendArm | TimeoutArm | WaitArm ) Block ;
SendArm       = Expr "|>" Expr ;
TimeoutArm    = "timeout" Expr ;
WaitArm       = Expr [ "as" IDENT ] ;                    (* canal ou tarefa *)
ElseArm       = "else" Block ;

(* Tipos: acrescentados aos nomes de tipo do Capítulo 6 *)
ConcType      = "task" | "chan" | "mutex" | "semaphore" | "barrier" | "atomic" | "context" ;
```

Observações para um *parser*:

- **`when` é decidido pelo que vem depois.** Se, no nível mais externo da expressão, há um `|>`, é `SendArm`; se o primeiro token é a palavra contextual `timeout`, é `TimeoutArm`; senão é `WaitArm`.
- **Palavras contextuais.** `when`, `timeout`, `parallel` e `fair` só são palavras da linguagem na posição indicada; em qualquer outro lugar são identificadores comuns.
- **Cabeçalho do `for`.** Os parâmetros `parallel=true` e `limit=n` (e `timeout`, `policy`) entram na lista de parâmetros nomeados do `for` (Capítulo 23); a gramática do cabeçalho não muda.
- **`await` e `thread`** são prefixos: `await f() + 1` lê-se `(await f()) + 1`, e `thread` só aceita uma chamada como operando.
- **Blocos.** Todos os blocos acima seguem o Capítulo 4, nos dois estilos.

### Erros e Avisos

Formato igual ao do Capítulo 36.7: código, nome em PascalCase, recuperável?, mensagem (uma frase, em inglês) e dica (começa em minúscula). Os códigos usam as faixas `E8xx` e `W8xx`, reservadas à concorrência (a faixa `E7xx` é do `canvas`). Os erros de execução são **recuperáveis** com `try`/`catch`.

#### Códigos reaproveitados

| **Código** | **Nome**               | **Onde a concorrência usa**                                                                                   |
|------------|------------------------|---------------------------------------------------------------------------------------------------------------|
| `E302`     | `TypeMismatch`         | `lock` sobre algo que não é `mutex`/`semaphore`; valor não escalar em `task.atomic`; argumento de `task.all` que não é tarefa; `task.map` com `f` comum em `"mode": "async"` |
| `E313`     | `ReadOnlyProperty`     | gravar em `t.state`, `c.length`, `task.cores` e demais membros somente leitura                                |
| `E316`     | `RefinementViolation`  | enviar para um `chan\values: T\` um valor que não é `T`                                                        |
| `E501`     | `MissingArgument`      | `task.any()` sem nenhuma tarefa                                                                               |
| `E503`     | `UnknownNamedArgument` | parâmetro que `scope`, `with` ou `lock` não declara                                                           |

#### Declaração e uso (E801–E804)

| **Código** | **Nome**              | **Recup.** | **Mensagem**                                                                            | **Dica**                                                                                  |
|------------|-----------------------|------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `E801`     | `AwaitOutsideAsync`   | No         | 'await' can only be used inside an async function or at the top level of the program.   | declare the function with f async, or move the await out of the function.                 |
| `E802`     | `InvalidParallelBody` | No         | A 'with parallel' block can only contain calls: each statement becomes a task.          | keep only calls to async functions (or 'thread' calls) in the block, or use scope.        |
| `E803`     | `InvalidSelect`       | No         | A select block cannot have both 'else' and 'when timeout'.                              | remove one of them: else never waits, so the timeout would never be reached.              |
| `E803`     | `InvalidSelect`       | No         | The select block has more than one 'else'.                                              | keep a single else arm, written last.                                                     |
| `E803`     | `InvalidSelect`       | No         | The select block has no 'when' arm.                                                     | add at least one 'when' arm, for example: when c as x.                                    |
| `E804`     | `InvalidThreadTarget` | Yes        | 'thread' requires a function call; got the number 5.                                    | write thread f(args), where f is a function.                                              |

#### Tarefas e escopos (E810–E818)

| **Código** | **Nome**                 | **Recup.** | **Mensagem**                                                                             | **Dica**                                                                                  |
|------------|--------------------------|------------|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `E810`     | `TaskNotFinished`        | Yes        | The task has not finished yet, so it has no result.                                      | use await t, or check t.done first.                                                       |
| `E811`     | `TaskCancelled`          | Yes        | The awaited task was cancelled and produced no result.                                   | check t.state before awaiting, or catch the error.                                        |
| `E812`     | `AggregateError`         | Yes        | 3 tasks failed in the same scope.                                                        | catch the error and read err.errors to see each failure.                                  |
| `E813`     | `TimeoutExceeded`        | Yes        | The scope exceeded its timeout of 2 seconds.                                             | increase the timeout, or make the tasks finish sooner.                                    |
| `E813`     | `TimeoutExceeded`        | Yes        | The lock could not be acquired within 0.5 seconds.                                       | increase the timeout, or release the lock sooner.                                         |
| `E814`     | `InvalidTimeout`         | Yes        | The timeout cannot be negative; got -1.                                                  | use 0 or a positive number of seconds, or Infinity for no limit.                          |
| `E815`     | `DeadlockDetected`       | Yes        | No task can make progress: 2 tasks are waiting for each other.                           | check the order of the channel operations and locks, or add a timeout.                    |
| `E815`     | `DeadlockDetected`       | Yes        | The task already holds this mutex: locking it again would block forever.                 | take the lock only once; a mutex is not reentrant.                                        |
| `E816`     | `SuspendInSyncFunction`  | Yes        | This operation would suspend the task, but it was called from a function that is not async. | declare the function with f async and call it with await.                             |
| `E817`     | `InvalidClockChange`     | Yes        | The clock can only be changed from the main task while no timer is pending.              | call task.virtual at the start of the program, before using pause or creating tasks.      |
| `E818`     | `InvalidLimit`           | Yes        | The limit must be a positive integer; got 0.                                             | use a positive integer, for example: limit=4.                                             |

#### Canais, sincronização, threads e canvas (E820–E841)

| **Código** | **Nome**                | **Recup.** | **Mensagem**                                                                           | **Dica**                                                                                  |
|------------|-------------------------|------------|----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `E820`     | `SendOnClosedChannel`   | Yes        | Cannot send on a closed channel.                                                       | close the channel only after the last send, or check c.closed before sending.             |
| `E821`     | `InvalidChannelValue`   | Yes        | void cannot be sent through a channel.                                                 | send null to mean 'no value'.                                                             |
| `E822`     | `InvalidCapacity`       | Yes        | The channel capacity must be a non-negative integer; got -1.                           | use 0 for an unbuffered channel, or a positive integer for a buffer.                      |
| `E830`     | `BarrierBroken`         | Yes        | The barrier was broken: a participant failed or was cancelled while others were waiting. | handle the failure of the participant, or catch the error in the waiting tasks.         |
| `E831`     | `InvalidPermitCount`    | Yes        | The number of permits must be a positive integer; got 0.                               | use a positive integer, for example: task.semaphore(3).                                   |
| `E840`     | `ThreadsUnavailable`    | Yes        | Real threads are not available in this environment.                                    | check task.threads first, or run the work as an async task.                               |
| `E841`     | `CanvasFromThread`      | Yes        | The canvas can only be used from the main thread.                                      | use canvas.post(f) to run code in the event loop.                                         |

#### Avisos

Avisos nunca interrompem a execução e podem ser escondidos com `#~ hide` (Capítulo 3.1.1).

| **Código** | **Nome**                  | **Mensagem**                                                                       | **Dica**                                                                       |
|------------|---------------------------|------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `W801`     | `NoopAwait`               | await has no effect here: the value is not awaitable.                              | remove the await.                                                              |
| `W802`     | `DiscardedTask`           | The task created here is never awaited and does not belong to a scope block.       | use await, keep the handle, put it in a scope or with parallel, or call .detach(). |
| `W803`     | `BlockingCall`            | readln() blocks every task while it waits.                                         | write await readln() so the other tasks keep running.                          |
| `W803`     | `BlockingCall`            | pause blocks every task here: it was called from a function that is not async.     | declare the function with f async.                                             |
| `W804`     | `UnprotectedSharedWrite`  | The variable 'total' is shared with a thread and is written outside a lock block.  | protect the write with lock, or use task.atomic.                               |

### Resumo da Sintaxe

| **Quero…**                                   | **Escrevo**                                                          |
|----------------------------------------------|----------------------------------------------------------------------|
| declarar uma função que espera               | `f async nome(a, b)`                                                 |
| criar uma tarefa                             | `var t = nome(1, 2)`                                                 |
| esperar um resultado                         | `var r = await t`                                                    |
| cuidar para que nada fique perdido           | `scope` … ou `with parallel` com uma chamada por linha               |
| limitar o tempo de um trecho                 | `with timeout 2`                                                     |
| cancelar                                     | `t.cancel()` · `ctx.cancel()`                                        |
| deixar uma tarefa viver até o fim do programa | `t.detach()`                                                         |
| criar um canal                               | `var c = task.chan(8)`                                               |
| enviar · receber · acabar                    | `v \|> c` · `await c` · `c.close()`                                  |
| consumir um canal                            | `for x in c`                                                         |
| esperar vários eventos                       | `select` com `when … as x`, `when v \|> c`, `when timeout n`, `else` |
| esperar todas · a primeira                   | `await task.all(a, b)` · `await task.any(a, b)`                      |
| aplicar uma função a uma lista, em paralelo  | `await task.map(f, lista, "limit": 4)`                               |
| rodar uma chamada em outro núcleo            | `var t = thread f(x)`                                                |
| proteger uma região                          | `lock m`                                                             |
| limitar a simultaneidade                     | `var s = task.semaphore(3)` · `lock s`                               |
| contar com segurança entre threads           | `var n = task.atomic(0)` · `n.add(1)`                                |
| ceder a vez num laço longo                   | `await task.yield()`                                                 |
| atualizar a janela a partir de uma thread    | `canvas.post(f(e) … )`                                               |
| testar sem esperar                           | `task.virtual(true)`                                                 |

### Exemplos Completos

#### Pipeline de três estágios

```tinypine
use task

f async gerar(saida)
  for i in [1 to 5]
    i |> saida
  saida.close()

f async dobrar(entrada, saida)
  for x in entrada
    (x * 2) |> saida
  saida.close()

f async imprimir(entrada)
  for x in entrada
    println(x)

var a = task.chan(2)
var b = task.chan(2)

with parallel
  gerar(a)
  dobrar(a, b)
  imprimir(b)
# imprime 2, 4, 6, 8, 10
```

#### Grupo de trabalhadores

```tinypine
use task

f async trabalhador(id, fila, resultados)
  for n in fila
    pause 0.1
    [id, n * n] |> resultados

var fila = task.chan(10)
var resultados = task.chan(10)

scope
  for id in [1 to 3]
    trabalhador(id, fila, resultados)
  for n in [1 to 6]
    n |> fila
  fila.close()                 # os trabalhadores acabam quando a fila esvazia
resultados.close()

for r in resultados
  println("trabalhador", r[0], "calculou", r[1])
```

#### Tentar de novo com prazo

```tinypine
f async buscar(demora)
  pause demora
  return "dados"

f async tentar(vezes)
  for i in [1 to vezes]
    try
      with timeout 1
        return await buscar(2 - i * 0.6)      # 1ª tentativa: 1,4 s (estoura); 2ª: 0,8 s
    catch(err)
      println("tentativa", i, "falhou")
  throw "todas as tentativas falharam"

println(await tentar(3))
# tentativa 1 falhou
# dados
```

#### A primeira resposta vence

```tinypine
use task

f async servidor(nome, demora)
  pause demora
  return nome

var vencedor = await task.any(servidor("a", 0.3), servidor("b", 0.1), servidor("c", 0.2))
println(vencedor)               # b — as outras duas foram canceladas
```

### Pontos em Aberto

Os pontos ainda não fechados deste capítulo estão no Apêndice A.2 (B39 a B44): a validação de `values:` de um `chan` em tempo de execução, a forma do objeto de erro agregado, a lista de funções nativas suspensíveis dos módulos ainda não especificados, o relógio virtual com threads e com o canvas, a segurança do módulo `random` e da saída entre threads, e os códigos `E8xx`/`W8xx`, escolhidos nesta revisão e que podem ser trocados.
