## Canvas — Janela

### Resumo

`canvas.window(...)` é a primeira chamada de todo programa com interface. Ela **abre uma janela preta e vazia** e devolve um **handle** (`window`). Tudo o que existe depois — elementos, estilo, eventos — é pendurado nesse handle.

```tinypine
use canvas

const w = canvas.window("id": "main", "name": "Meu app", "width": 640, "height": 360)
```

Com só `"id"`, a janela abre com 800 × 600, fundo `black`, **zero elementos** (`w.children().length` é `0`). O que o programador decide — `id`, `name`, tamanho, posição, moldura — está todo na chamada.

### Funções do módulo

| **Função**                          | **Retorno**      | **Efeito**                                                                  |
|-------------------------------------|------------------|-----------------------------------------------------------------------------|
| `canvas.window(!, "id": …, …)`      | `window`         | Cria e abre uma janela (abaixo).                                            |
| `canvas.get(id)`                    | `window`         | Devolve a janela aberta com esse `id`; `WindowNotFound PROBLEM` se não há.  |
| `canvas.windows()`                  | `list`           | Todas as janelas abertas, na ordem de criação.                              |
| `canvas.screen()`                   | `dict`           | `{"width", "height", "scale"}` da tela principal (px lógicos e fator de DPI). |
| `canvas.run()` · `canvas.poll()` · `canvas.quit()` · `canvas.after()` · `canvas.every()` | — | Laço de eventos e *timers*: ver Capítulo 49. |
| `canvas.advance(segundos)`          | `null`           | Relógio virtual, **só com janelas `headless`** (Capítulo 51).               |

O módulo **não** tem construtores de elemento. `canvas.box(...)` é erro (membro inexistente): elementos nascem dentro de uma janela ou de outro elemento (Capítulo 45).

### canvas.window

Todos os parâmetros são **exclusivamente nomeados** (seção `!` do Cap. 30.3). `"id"` é o único obrigatório: sem ele, `MissingNamedArgument PROBLEM` (E502). Chamar com argumento posicional é `PositionalForNamedOnly PROBLEM` (E504).

| **Nome externo**   | **Tipo**   | **Padrão**    | **Descrição**                                                                                                  |
|--------------------|------------|---------------|----------------------------------------------------------------------------------------------------------------|
| `"id"`             | `str`      | — (obrigatório) | Identificador da janela, **escolhido pelo programador**. Único entre as janelas abertas. Não vazio, sem espaço em branco (mesma regra do `id` do HTML). |
| `"name"`           | `str`      | o próprio `id`  | Nome da janela, mostrado na barra de título.                                                                   |
| `"width"`          | `int`      | `800`           | Largura da **área cliente**, em px lógicos (≥ 1).                                                              |
| `"height"`         | `int`      | `600`           | Altura da área cliente, em px lógicos (≥ 1).                                                                   |
| `"x"`, `"y"`       | `int`      | `null`          | Posição do canto superior esquerdo na tela. `null`: o sistema escolhe.                                         |
| `"min-width"`, `"min-height"`, `"max-width"`, `"max-height"` | `int` | `null` | Limites de redimensionamento. `null`: sem limite.                                              |
| `"resizable"`      | `bool`     | `true`          | O usuário pode redimensionar.                                                                                  |
| `"frame"`          | `bool`     | `true`          | Moldura e barra de título do sistema. `false`: janela sem borda.                                               |
| `"visible"`        | `bool`     | `true`          | Abre já visível. `false`: abre oculta; `w.visible = true` mostra.                                               |
| `"maximized"`      | `bool`     | `false`         | Abre maximizada.                                                                                               |
| `"fullscreen"`     | `bool`     | `false`         | Abre em tela cheia.                                                                                            |
| `"on-top"`         | `bool`     | `false`         | Fica acima das demais. É uma *dica*: o sistema pode ignorar.                                                   |
| `"transparent"`    | `bool`     | `false`         | Fundo com transparência real (dica; depende da plataforma).                                                    |
| `"background"`     | `str`      | `"black"`       | Cor de fundo da janela. Equivale a `w.style({"background": …})`.                                         |
| `"icon"`           | `str`      | `null`          | Caminho de um arquivo de imagem para o ícone. Relativo ao **`.tpine` em execução** (abaixo, "Caminhos de arquivo").               |
| `"headless"`       | `bool`     | `false`         | Sem janela do sistema: o motor roda estilo e layout e pinta em memória.                                  |

Os nomes têm o **mesmo formato** que as propriedades da janela (abaixo): com hífen (`min-width`, `on-top`), como no CSS e nas funções da biblioteca (`to-int`). O `-` no meio do nome é válido em identificador (Cap. 3.4.1), então além da forma `"min-width": 100` vale também `min-width=100` (Cap. 30.3) e `w.min-width = 100` é um membro comum. Em contas, escreva **com espaços**: `w.width - 10` é subtração; colado, vale a regra do Cap. 3.4.1 (`a-b` colado é nome; se os dois lados são variáveis, o parser dá erro).

Os atributos são o conjunto comum às plataformas (título, tamanho interno, mínimo/máximo, redimensionável, decorações, visível, maximizada, tela cheia, nível da janela, transparente, ícone); os que só existem em uma plataforma ficam de fora.

#### Caminhos de arquivo

Todo caminho **relativo** que o canvas recebe — `"icon"`, `src` de `image`, e o CSS por arquivo (Capítulo 47) — é resolvido a partir da **pasta do arquivo `.tpine` em execução** (`~Program.path`, Cap. 29.4: caminho absoluto do programa), **não** do diretório de trabalho: o programa abre igual de qualquer pasta. Caminho absoluto vale como está. Com `~Program.path` vazio (sem arquivo, p. ex. entrada interativa) o diretório de trabalho é o de referência. *(O `os.read` (Capítulo 34.6) não diz como resolve caminhos relativos; se resolver pelo diretório de trabalho, quem lê CSS monta o caminho a partir de `~Program.path` — Capítulo 47. Ponto em aberto: Apêndice A, B34.)*

#### A janela preta

A janela é, ao mesmo tempo, a **raiz** da árvore. Seus padrões de estilo (UA, Capítulo 46):

| **Propriedade**  | **Valor da raiz**                 |
|------------------|-----------------------------------|
| `background`     | `black`                           |
| `color`          | `white` (herdada pelos filhos)    |
| `font-family`    | `"sans"`                          |
| `font-size`      | `16`                              |
| `display`        | `block`                           |

`color: white` sobre `background: black` não é capricho: sem isso o primeiro `w.text(...)` seria preto sobre preto, invisível — um erro silencioso por outro caminho.

### O handle `window`

O handle é um **objeto nativo** com **propriedades graváveis**: os membros são lidos com `.` e, quando não são estado do motor, **também gravados com `=`**. Gravar valida na hora e o motor aplica a mudança (ver "Escrever" abaixo; o Capítulo 45 tem a mesma política para elementos). A atribuição a um membro de objeto nativo chama o motor, e não vincula um identificador (nota no Capítulo 14).

#### Propriedades

**G** = gravável (`w.name = "x"`), **L** = somente leitura.

| **Membro**        | **Tipo**         |       | **Descrição**                                                                  |
|-------------------|------------------|-------|--------------------------------------------------------------------------------|
| `w.id`            | `str`            | L     | O `id` dado na criação. Imutável.                                              |
| `w.kind`          | `str`            | L     | Sempre `"window"`.                                                             |
| `w.type`          | `str`            | L     | `"window"` — o `.type` do Cap. 6.7.                                 |
| `w.name`          | `str`            | G     | Nome (barra de título).                                                        |
| `w.width`, `w.height` | `int`        | G     | Tamanho da **área cliente**, em px lógicos (≥ 1). Muda também quando o usuário redimensiona. |
| `w.x`, `w.y`      | **lê** `int`; **grava** `int` ou `null` | G | Posição do canto superior esquerdo na tela. Ao **ler**, é sempre a posição real (um `int`; em `headless`, que não tem tela, `0`). Gravar `null` devolve a escolha ao sistema. |
| `w.min-width`, `w.min-height`, `w.max-width`, `w.max-height` | `int` ou `null` | G | Limites de redimensionamento; `null` = sem limite (aqui `null` lido **é** informação: "sem limite"). |
| `w.resizable`     | `bool`           | G     | O usuário pode redimensionar.                                                  |
| `w.visible`       | `bool`           | G     | Janela mostrada ou oculta (`false` oculta; os elementos continuam existindo).  |
| `w.maximized`, `w.fullscreen` | `bool` | G   | Estado da janela.                                                              |
| `w.on-top`        | `bool`           | G     | Fica acima das demais (dica; o sistema pode ignorar).                          |
| `w.icon`          | `str` ou `null`  | G     | Caminho da imagem do ícone.                                                    |
| `w.scale`         | `float`          | L     | Fator de DPI (1.0, 1.25, 2.0…).                                                |
| `w.focused`       | `bool`           | L     | A janela tem o foco do sistema (para pedir foco: `w.focus()`).                 |
| `w.closed`        | `bool`           | L     | `true` depois que a janela fechou.                                             |
| `w.frame`, `w.transparent`, `w.headless` | `bool` | L | Só valem na criação.                                                      |

`visible`, `maximized` e `fullscreen` são propriedades, e **não há `w.show()`/`w.hide()`**: `w.visible = false` diz a mesma coisa, com um jeito só de fazer.

```tinypine
println(w.id)         # main
println(w.width)      # 640
w.width = 900         # grava: pede ao sistema uma janela de 900 px de largura
w.visible = false     # oculta
w.id = "outro"        # ReadOnlyProperty PROBLEM (E313)
w.cor = "red"         # UnknownAttribute PROBLEM (E716)
w.width = 0           # InvalidWindowSize PROBLEM (E703)
w.width = "900"       # TypeMismatch PROBLEM (E302)
```

#### Escrever

Gravar uma propriedade (ou usar `update`, abaixo) segue **as mesmas regras**:

1. **Valida na hora**, na linha do `=`: nome que não existe → `UnknownAttribute` (E716); somente leitura → `ReadOnlyProperty` (E313); tipo errado → `TypeMismatch` (E302); valor fora do domínio → o erro do próprio atributo (`InvalidWindowSize`, E703).
2. **Efeito**: a mudança entra na fila do motor e aparece no próximo quadro (várias gravações dentro de um mesmo handler viram um quadro só — Capítulo 48). **Ler de volta devolve o valor novo na hora.**
3. **Tamanho e posição são pedidos ao sistema**, que pode ajustar (limites, tela menor): se ajustar, o evento `resize`/`move` chega com o valor real e a propriedade passa a refleti-lo. Logo após gravar, a leitura devolve o valor **pedido**, e passa a refletir o valor real quando o evento chega (Apêndice A, B37).
4. **Gravar não dispara evento de usuário**, como no DOM (gravar o texto de um `input` não dispara `input`; Capítulo 45). Dispara só o que o próprio sistema reporta (`resize`, `move`).
5. Gravar o valor que já está lá não faz nada.
6. Em janela fechada, gravar é `StaleHandle` (E706); ler continua valendo (abaixo).

#### update — várias propriedades de uma vez

`w.update(dict)` grava **só as chaves do dict** (o argumento é um **dict**, não argumentos nomeados). O dict distingue por si "não mencionado" de `null`: `{"x": null}` é "o sistema escolhe a posição"; chave ausente é "não mexe".

```tinypine
w.update({"name": "Meu app — salvo"})
w.update({"width": 900, "height": 500})
w.update({"x": null})                    # null é um valor: volta a deixar o sistema escolher

const tamanho = {"width": 1024, "height": 768}
w.update(tamanho)                        # o dict pode vir de uma variável
```

- Aceita as chaves **graváveis** da tabela acima. Chave só de leitura (`"id"`, `"frame"`…) → `ReadOnlyProperty` (E313); chave que não existe → `UnknownAttribute` (E716), com *did you mean*; valor de tipo errado → `TypeMismatch` (E302).
- **Tudo ou nada**: todas as chaves são validadas antes de gravar a primeira; se uma falha, nenhuma é gravada.
- Argumento que não é `dict`, ou dict com chave que não é `str` → `TypeMismatch` (E302). Dict vazio: não faz nada. Devolve `null`.
- Por que existe se há propriedades: (1) validação **atômica** de um grupo de mudanças; (2) aceita um dict montado pelo programa (guardado, mesclado, vindo de um arquivo) — o mesmo motivo do estilo em dict (Capítulo 46).

A **cor de fundo** não é propriedade da janela depois de criada: é estilo, e se muda como estilo (`w.style({"background": "#101018"})`).

#### Métodos

| **Método**                  | **Retorno** | **Efeito**                                                                                              |
|-----------------------------|-------------|---------------------------------------------------------------------------------------------------------|
| `w.update(dict)`            | `null`      | Grava várias propriedades de uma vez (acima).                                                           |
| `w.focus()`                 | `null`      | Pede foco do sistema para a janela (dica).                                                              |
| `w.close()`                 | `bool`      | Fecha. Dispara `close` (cancelável); devolve `false` se um handler cancelou, `true` se fechou. `canvas.quit()`, ao contrário, **não consulta** (Capítulo 49). |
| `w.clear()`                 | `null`      | Remove **todos** os elementos: a janela volta a ser preta e vazia. Handles dos elementos ficam obsoletos. |
| `w.capture(caminho)`        | `null`      | Salva a imagem atual da janela em PNG. Funciona também em `headless`. Caminho relativo: ver "Caminhos de arquivo". |
| `w.dispatch(tipo, dados)`   | `bool`      | **Só `headless`**: entrega um evento como se o usuário o tivesse produzido (Capítulo 51). Em janela real: `HeadlessOnly PROBLEM` (E734). |
| `w.rect()`                  | `dict`      | `{"x": 0, "y": 0, "width": …, "height": …}` da área cliente.                                            |
| `w.on(tipo, handler, …)`    | `listener`  | Registra um *handler* de evento (Capítulo 49).                                                          |
| `w.box(…)` `w.text(…)` `w.image(…)` `w.button(…)` `w.input(…)` | `element` | Cria um elemento **filho direto da raiz** (Capítulo 45). |
| `w.find(id)` · `w.query(sel)` · `w.select(sel)` | `element` / `list` | Consulta na árvore inteira (Capítulo 45). |
| `w.rules({…})`              | `sheet`     | Folha de regras da janela, em dict (Capítulo 46).                                                       |
| `w.css(texto, "source": …)` | `sheet`     | Folha de regras da janela, em **texto CSS** (Capítulo 47).                                         |
| `w.style({…})`              | `null`      | Estilo inline da raiz (Capítulo 46).                                                                    |
| `w.children()`              | `list`      | Filhos diretos da raiz, em ordem.                                                                       |

### Ciclo de vida

```
 canvas.window(...) ─► aberta ─► (visível ⇄ oculta) ─► close ─► fechada
                          │
                          └─ eventos, elementos, estilo
```

- Depois de `closed`, todo método e toda **gravação** é `StaleHandle PROBLEM` (E706). **Ler** propriedades de uma janela fechada devolve o último valor conhecido, **sem** erro — ler nunca quebra.
- O `id` de uma janela fechada fica livre: `canvas.window("id": "main")` de novo é permitido.
- Duas janelas abertas com o mesmo `id`: `WindowIdDuplicate PROBLEM` (E702).

### Várias janelas

Cada janela tem **sua própria árvore, suas folhas de estilo e seus eventos**; elementos de uma janela não podem ser movidos para outra (`el.move` entre janelas é `CrossWindowMove PROBLEM`, E707). `canvas.run()` só retorna quando **todas** fecharam. Janelas filhas e modais ficam fora desta versão (Apêndice A, B38). Uma janela `headless` **não conta** para o `run()`: sem janela real aberta, `canvas.run()` volta na hora.

```tinypine
const a = canvas.window("id": "editor", "name": "Editor", "x": 100, "y": 100)
const b = canvas.window("id": "ferramentas", "name": "Ferramentas", "width": 240, "height": 400, "x": 20, "y": 100)
println(canvas.windows().length)   # 2
```

### Coordenadas

- Origem no **canto superior esquerdo da área cliente**, `x` cresce para a direita, `y` cresce para baixo.
- Unidade: **px lógico**. O fator `w.scale` converte para pixels do dispositivo; o programador não precisa tratá-lo.
- `w.width`/`w.height` são da área cliente — não incluem barra de título nem borda.

### Erros desta seção

| **Caso**                                                    | **Erro**                                  |
|-------------------------------------------------------------|-------------------------------------------|
| `canvas.window()` sem `"id"`                                | `MissingNamedArgument PROBLEM` (E502)     |
| `"id"` vazio, com espaço, ou não `str`                      | `InvalidWindowId PROBLEM` (E701)          |
| `"id"` já usado por janela aberta                           | `WindowIdDuplicate PROBLEM` (E702)        |
| `"width"`/`"height"` < 1, ou `min` > `max`                  | `InvalidWindowSize PROBLEM` (E703)        |
| `canvas.get("x")` sem janela `x`                            | `WindowNotFound PROBLEM` (E704)           |
| usar handle de janela fechada                               | `StaleHandle PROBLEM` (E706)              |
| `w.id = "x"`, `w.update({"id": "x"})` (só leitura)          | `ReadOnlyProperty PROBLEM` (E313)         |
| `w.cor = "red"`, `w.update({"cor": 1})` (não existe)         | `UnknownAttribute PROBLEM` (E716)         |
| `w.width = "900"` (tipo errado)                             | `TypeMismatch PROBLEM` (E302)             |
| sem sistema de janelas (servidor sem tela) e sem `headless` | `NoDisplay PROBLEM` (E705)                |
| `w.dispatch(…)` / `canvas.advance(…)` com janela **não** `headless` | `HeadlessOnly PROBLEM` (E734)        |
| `w.css("…")` com texto que não é CSS válido                 | `CssSyntaxError PROBLEM` (E723)           |

Mensagens e dicas completas: Capítulo 53.
