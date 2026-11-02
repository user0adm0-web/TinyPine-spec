## Canvas — Eventos e Laço

### Resumo

Um programa de janela **não termina**: espera o usuário. O canvas separa isso em duas partes:

1. o **laço**, que recebe os eventos do sistema (ponteiro, teclado, janela, relógio) — `canvas.run()` ou `canvas.poll()`;
2. os **handlers**, funções do TinyPine registradas com `on(...)`, que o laço chama.

```tinypine
use canvas

const w = canvas.window("id": "main", "name": "Clique")
const botao = w.button("Clique aqui", "id": "ok")

botao.on("click", f(e)
  println(format "clicou em {e.x}, {e.y}")
)

canvas.run()        # só volta quando todas as janelas fecharem
```

O modelo de eventos é o do DOM — captura, alvo, bolha — porque é um modelo bom e porque quem conhece HTML já o conhece (`dom.spec.whatwg.org`).

### O laço

| **Função**                          | **Retorno** | **Efeito**                                                                                          |
|-------------------------------------|-------------|-----------------------------------------------------------------------------------------------------|
| `canvas.run()`                      | `null`      | Bloqueia e despacha eventos até a **última janela fechar** (ou `canvas.quit()`). Entre eventos, dorme. **Volta na hora** se não há nenhuma janela aberta que **não** seja `headless`. |
| `canvas.poll("wait": 0)`            | `bool`      | Processa **uma rodada**: eventos pendentes, *timers*, evento `frame`, e pinta. Espera no máximo `"wait"` segundos por um evento. Devolve `false` quando não há mais janela aberta. Com janelas `headless`, **não dorme** (Capítulo 51). |
| `canvas.quit()`                     | `null`      | Fecha **todas** as janelas e faz `run()` retornar. **Não consulta** `close`: cada janela recebe `close` como **aviso não cancelável** (`e.cancelable` é `false`; `e.prevent()` → `NotCancelable WARNING`, W704), para o programa limpar o que precisa. `w.close()` (uma janela) é quem consulta. |
| `canvas.advance(segundos)`          | `null`      | **Só com janelas `headless`**: move o relógio virtual (Capítulo 51).                                |

`run()` e `poll()` são **o mesmo mecanismo** em duas formas: `run()` é o jeito de quem reage a eventos (formulários, ferramentas); `poll()` é o jeito de quem tem o seu próprio laço, como um jogo:

```tinypine
const w = canvas.window("id": "jogo", "name": "Jogo", "width": 480, "height": 320)
const bola = w.box("id": "bola", "style": {"position": "absolute", "left": 0, "top": 150,
                                           "width": 20, "height": 20, "background": "white"})
var x = 0
while not w.closed
  canvas.poll("wait": 0.016)         # ≈ 60 quadros por segundo
  x = x + 4
  bola.style({"left": x})
```

Regras:

- Chamar `canvas.run()` ou `canvas.poll()` **de dentro de um handler** é `RunReentrant PROBLEM` (E732): o laço já está rodando.
- `run()` com **zero janelas** (ou só `headless`) não é erro e não bloqueia: volta na hora — um programa de teste nunca fica pendurado.
- Handlers são **funções comuns, síncronas**, executadas uma de cada vez, na mesma execução do programa. Nada é pintado enquanto um handler roda; a janela é apresentada quando ele retorna.
- Por isso, `pause`, `readln()` e laços longos **congelam a janela**. O motor emite `SlowHandler WARNING` (W702) quando um handler demora mais de 0,1 s (limite provisório) — a dica sugere `canvas.after` ou dividir o trabalho. Concorrência de verdade (`async`, `thread`, Capítulo 42) está reservada e **fora desta versão**; usar o canvas de outra *thread* fica indefinido até lá.
- **Erro dentro de um handler** não derruba o laço em silêncio: ele sobe pela pilha até `canvas.run()`/`canvas.poll()` e, sem `try`, termina o programa com o bloco de erro padrão (Cap. 36.7), com o handler na pilha de chamadas. `try`/`catch` **dentro** do handler trata o erro ali mesmo.

### Relógio: `after` e `every`

Em JS, `setTimeout`/`setInterval`; aqui, em **segundos** (Cap. 26: a unidade de tempo da linguagem é o segundo):

| **Função**                      | **Retorno** | **Efeito**                                                                  |
|---------------------------------|-------------|-----------------------------------------------------------------------------|
| `canvas.after(segundos, f)`     | `timer`     | Chama `f` **uma vez**, depois de `segundos`.                                |
| `canvas.every(segundos, f)`     | `timer`     | Chama `f` repetidamente, a cada `segundos`. Não acumula atrasos: se o laço atrasou, perde ticks em vez de rodá-los em rajada. |

`f` recebe um evento `e` com `e.kind == "timer"` e `e.dt` (segundos desde a última chamada). O `timer` tem `t.active` (`bool`) e `t.cancel()`. `segundos` < 0, ou `every` com 0, é `InvalidTimerInterval PROBLEM` (E733); `after(0, f)` é válido (roda na próxima rodada) e **não** gera `NoopPause` — não é uma pausa.

```tinypine
var $cont = 3
const t = canvas.every(1, f(e)
  println($cont)
  $cont = $cont - 1
)
canvas.after(3.5, f(e)
  t.cancel()
  println("fim")
)
```

*(O estado compartilhado entre handlers é `var $cont`, **global** (Cap. 18). Se uma função anônima pode **atribuir** uma variável **local** do escopo de fora não está definido (Apêndice A, B36); por isso os exemplos usam variáveis globais ou o próprio elemento. `t` só é **lido** dentro do handler.)*

Timers pertencem ao módulo, não a uma janela: continuam vivos enquanto houver janela aberta e acabam junto com o `run()`. Quando a **última janela fecha**, todo timer pendente é cancelado e `t.active` passa a `false` (idem depois de `quit()`).

### Registrar: `on` e `off`

```text
alvo.on(tipo, handler, "capture": false, "once": false)  →  listener
```

`alvo` é a **janela** ou qualquer **elemento**. `tipo` é uma `str` da tabela abaixo; tipo desconhecido é `UnknownEventKind PROBLEM` (E730), com *did you mean*. `handler` é uma função (nomeada ou anônima) com **0 ou 1 parâmetro**: `f(e)` recebe o evento; `f()` (ou uma função nomeada sem parâmetros) simplesmente **não o recebe** — quem ignora o evento não precisa declará-lo. **2 ou mais** parâmetros, ou um parâmetro `package` (variádico), é `InvalidHandler PROBLEM` (E731), detectável antes de rodar quando o handler é literal. Função com parâmetros **opcionais** conta todos os parâmetros que declara.

| **Opção**       | **Padrão** | **Efeito**                                                                                    |
|-----------------|------------|-----------------------------------------------------------------------------------------------|
| `"capture"`     | `false`    | `true`: o handler roda na fase de **captura** (descendo), antes do alvo.                      |
| `"once"`        | `false`    | `true`: o handler é removido depois da primeira chamada.                                      |

`on` devolve um **`listener`**:

```tinypine
f ao_clicar()                         # sem parâmetro: o evento é ignorado
  println("clicou")

const ouvinte = botao.on("click", ao_clicar)
println(ouvinte.active)    # true
ouvinte.off()              # remove; ouvinte.active passa a false
```

Há `off()` no ouvinte (e não `alvo.off(tipo, handler)`) porque o TinyPine não tem uma noção definida de "a mesma função" (por `is`, duas funções quaisquer são iguais, Cap. 6.7) — comparar `handler`s para achar o que remover seria ambíguo.

Vários handlers no mesmo alvo e tipo rodam **na ordem em que foram registrados**.

#### Mudar a árvore ou os handlers durante o despacho

Seguem o DOM:

1. **O caminho é fixado no início do despacho.** A lista de alvos (janela → … → alvo) é calculada **uma vez**, quando o evento começa. Se um handler remove o alvo ou um ancestral (`el.remove()`), os handlers dos elementos que **já estavam no caminho** ainda rodam **naquele** evento (o handle aparece com `e.target.removed == true`); o **próximo** evento usa a árvore nova.
2. **`off()` vale na hora**: um ouvinte removido durante o despacho **não** é chamado, nem no evento em curso.
3. **Registrar durante o despacho** (`on` no mesmo alvo e tipo, dentro de um handler) só vale a partir do **próximo** evento.
4. **`once`**: o ouvinte é removido **antes** de o handler rodar, então um `dispatch` do mesmo tipo feito de dentro do handler não o chama de novo.
5. **Despacho dentro de despacho** (`dispatch`; só `headless`) roda **de forma síncrona**, aninhado, como `dispatchEvent` no DOM (Capítulo 51).

### Tipos de evento

Legenda: **bolha** = sobe pelos ancestrais; **cancel.** = `e.prevent()` tem efeito.

#### Ponteiro (mouse; caneta e toque entram no mesmo nome depois)

| **Tipo**         | **Alvo**                         | **Bolha** | **Cancel.** | **Quando**                                                  |
|------------------|----------------------------------|-----------|-------------|-------------------------------------------------------------|
| `pointerdown`    | elemento sob o ponteiro          | sim       | sim         | botão pressionado                                           |
| `pointerup`      | elemento sob o ponteiro          | sim       | sim         | botão solto                                                 |
| `click`          | elemento (down e up no mesmo)    | sim       | sim         | pressionar e soltar sobre o mesmo elemento; também Enter/Espaço em `button` focado |
| `dblclick`       | idem                             | sim       | sim         | dois cliques em sequência                                   |
| `pointermove`    | elemento sob o ponteiro          | sim       | não         | o ponteiro se moveu                                         |
| `pointerenter`   | cada elemento que o ponteiro entra | não     | não         | ponteiro entrou (ancestrais inclusive, do mais externo)     |
| `pointerleave`   | cada elemento que o ponteiro sai | não       | não         | ponteiro saiu                                               |
| `wheel`          | elemento sob o ponteiro          | sim       | sim         | roda do mouse                                               |

#### Teclado

O alvo é o **elemento focado**; sem foco, a **janela**.

| **Tipo**   | **Bolha** | **Cancel.** | **Quando**                                                                                    |
|------------|-----------|-------------|-----------------------------------------------------------------------------------------------|
| `keydown`  | sim       | sim         | tecla pressionada (repete enquanto segura, com `e.repeat` verdadeiro)                         |
| `keyup`    | sim       | não         | tecla solta                                                                                    |
| `textinput`| sim       | **sim**     | o usuário **produziu texto** (já composto: `"ç"`, `"ã"`, colagem); `e.text`. **É por ele que o `input` edita** (Capítulo 50) |

`keydown`/`keyup` descrevem a **tecla física** (`e.key`); `textinput` descreve o **texto resultante**. São separados porque `ç`, `ã`, `é` costumam vir de **duas teclas** (acento, depois letra) ou de colagem, e a tecla apertada não é o texto digitado. `e.prevent()` num `keydown` **também suprime** o `textinput` daquela tecla (como no DOM, em que cancelar `keydown` cancela o texto); `e.prevent()` no `textinput` suprime só a inserção.

#### Foco e campos

| **Tipo**   | **Alvo**       | **Bolha** | **Cancel.** | **Quando**                                                                      |
|------------|----------------|-----------|-------------|---------------------------------------------------------------------------------|
| `focus`    | o elemento     | não       | não         | recebeu o foco de teclado                                                       |
| `blur`     | o elemento     | não       | não         | perdeu o foco                                                                   |
| `input`    | `input`        | sim       | não         | o texto mudou (cada edição); `e.value` é o texto novo                           |
| `change`   | `input`        | sim       | não         | o campo perdeu o foco, ou Enter, com o texto diferente do que tinha ao receber o foco |

`focus`/`blur` não sobem; para observar o foco de uma região inteira, registre no ancestral com `"capture": true` (a captura acontece mesmo para eventos sem bolha, como no DOM).

#### Janela (alvo: a janela)

| **Tipo**       | **Cancel.** | **Dados**                    | **Quando**                                                                        |
|----------------|-------------|------------------------------|-----------------------------------------------------------------------------------|
| `resize`       | não         | `e.width`, `e.height`        | a área cliente mudou de tamanho                                                   |
| `move`         | não         | `e.x`, `e.y`                 | a janela mudou de posição                                                         |
| `activate`     | não         | —                            | a janela ganhou o foco do sistema                                                 |
| `deactivate`   | não         | —                            | perdeu                                                                            |
| `scale`        | não         | `e.scale`                    | o fator de DPI mudou (ex.: arrastada para outro monitor)                          |
| `close`        | **sim**     | —                            | o usuário (ou `w.close()`) pediu para fechar; `e.prevent()` cancela                |
| `frame`        | não         | `e.dt`                       | uma vez por quadro apresentado; `e.dt` = segundos desde o quadro anterior   |

(`activate`/`deactivate` são da janela; `focus`/`blur` são de elemento — nomes diferentes de propósito, para não haver evento de dois significados.)

### O objeto evento

O argumento `e` é um objeto nativo **inteiramente somente leitura**: um evento descreve algo que já aconteceu, então não há o que gravar (`e.x = 3` é `ReadOnlyProperty`, E313). O que se faz com ele é por método (`stop`, `prevent`). Propriedades graváveis valem para `window` e `element`, não para `event`, `listener`, `timer` e `sheet`.

| **Membro**        | **Tipo**         | **Existe em**                | **Descrição**                                                                       |
|-------------------|------------------|------------------------------|-------------------------------------------------------------------------------------|
| `e.kind`          | `str`            | todos                        | O tipo (`"click"`…). Não se chama `type` porque `.type` é a propriedade de tipo da linguagem (Cap. 6.7). |
| `e.target`        | `window`/`element` | todos exceto `timer`/`frame` | Onde o evento começou.                                                              |
| `e.current`       | `window`/`element` | todos                      | O alvo cujo handler está rodando agora (muda durante a propagação).                 |
| `e.phase`         | `str`            | todos                        | `"capture"`, `"target"` ou `"bubble"`.                                              |
| `e.time`          | `float`          | todos                        | Segundos desde o início do programa.                                                |
| `e.bubbles`, `e.cancelable` | `bool` | todos                        | Da tabela acima.                                                                    |
| `e.prevented`     | `bool`           | todos                        | `true` depois de `e.prevent()`.                                                     |
| `e.x`, `e.y`      | `float`          | ponteiro (`pointer*`, `click`, `dblclick`, `wheel`) | Posição na **área cliente** da janela.                         |
| `e.local`         | `dict`           | ponteiro                     | `{"x", "y"}` relativos à caixa da borda do `e.target`.                              |
| `e.button`        | `str`            | `pointerdown/up`, `click`, `dblclick` | `"left"`, `"middle"`, `"right"`.                                      |
| `e.count`         | `int`            | `click`, `dblclick`          | 1 ou 2.                                                                             |
| `e.dx`, `e.dy`    | `float`          | `wheel`                      | Rolagem (positivo = para baixo/direita).                                      |
| `e.key`           | `str`            | `keydown`, `keyup`           | Nome da tecla, **o mesmo de `computer.keyboard`** (Cap. 34.7): `"a"`, `"enter"`, `"space"`, `"up"`, `"f1"`…. |
| `e.text`          | `str`            | `textinput`                  | O texto **já composto** produzido. Nunca vazio. |
| `e.repeat`        | `bool`           | `keydown`                    | Repetição por tecla segurada.                                                       |
| `e.shift`, `e.ctrl`, `e.alt`, `e.meta` | `bool` | ponteiro e teclado    | Modificadores no momento do evento.                                                 |
| `e.value`         | `str`            | `input`, `change`            | O texto do campo.                                                                   |
| `e.width`, `e.height` | `int`        | `resize`                     | Nova área cliente, em px lógicos.                                                   |
| `e.x`, `e.y`      | `int`            | `move`                       | Nova posição da janela na tela. *(No ponteiro, `e.x`/`e.y` são `float`: a mesma letra, dois tipos, **separados** pelo tipo de evento.)* |
| `e.scale`         | `float`          | `scale`                      | Novo fator de DPI.                                                                  |
| `e.dt`            | `float`          | `frame`, `timer`             | Segundos desde o quadro / a chamada anterior.                                       |

Ler um membro que o evento não tem (`e.key` num `click`) é `IdNotFound PROBLEM` (E308) com a dica de quais membros aquele tipo tem — nunca `void`/`null` silencioso.

| **Método**                         | **Efeito**                                                                                      |
|------------------------------------|-------------------------------------------------------------------------------------------------|
| `e.stop()`                         | Para a propagação: nenhum **outro elemento** do caminho recebe o evento (os handlers do elemento atual terminam). |
| `e.stop("immediate": true)`        | Idem, e também **não chama** os handlers restantes do mesmo elemento.                           |
| `e.prevent()`                      | Cancela a **ação padrão** (abaixo). Em evento não cancelável: `NotCancelable WARNING` (W704).   |

### Propagação

Quando o evento tem alvo `A`, o caminho vai da raiz (a janela) até `A`:

```
 janela ─► box.painel ─► box.linha ─► button#ok          (caminho)
   │          │              │            │
   1 captura ─┴──────────────┘            │            (desce: só quem registrou "capture": true)
                                      2 alvo           (todos os handlers do alvo)
   ┌──────────┬──────────────┐            │
   3 bolha ◄──┘◄─────────────┘◄───────────┘            (sobe: handlers normais, se bubbles)
```

1. **Captura** — da janela até o pai do alvo, só handlers com `"capture": true`.
2. **Alvo** — todos os handlers do alvo (captura ou não), na ordem de registro.
3. **Bolha** — do pai do alvo até a janela, só handlers sem `"capture"`, se o evento sobe.

```tinypine
painel.on("click", f(e)
  println(format "painel: clique veio de {e.target.id}")      # e.current é o painel
)
ok.on("click", f(e)
  println("botão")
  e.stop()                                              # o painel não vai receber
)
```

Teclado sem foco chega à **janela**: `w.on("keydown", …)` é o jeito de ouvir o teclado inteiro.

### Ações padrão (o que acontece se ninguém cancela)

| **Evento**                          | **Ação padrão**                                                                          |
|-------------------------------------|------------------------------------------------------------------------------------------|
| `pointerdown` em elemento focável   | move o foco para ele                                                                     |
| `click` em `button`                 | nada além do evento (o botão só avisa)                                                   |
| `keydown` `"enter"` / `"space"` num `button` focado | gera `click`                                                             |
| `keydown` `"tab"` / `"shift"+"tab"` | move o foco para o próximo / anterior elemento focável                                   |
| `textinput` num `input` focado      | insere `e.text` no cursor, dispara `input`                                          |
| `keydown` `"backspace"`/`"delete"`/setas/`"home"`/`"end"` num `input` | edita/move o cursor                                    |
| `wheel` sobre `overflow: scroll|auto` | rola o conteúdo                                                                        |
| `close`                             | fecha a janela                                                                           |

`e.prevent()` num `textinput` de `input` impede a inserção — **a forma de filtrar o que se digita** (e num `keydown` impede também o `textinput` daquela tecla, acima).

#### Foco

- **Focáveis**: `button` e `input` (se não `disabled`), e `box` com `"focusable": true`. A **ordem de Tab** é a ordem da árvore.
- `el.focus()` / `el.blur()` movem o foco; `el.focused` lê.
- `el.focus()` num elemento **não focável** (`disabled`, `display: "none"`, ou `box` sem `focusable`) **não muda o foco** e emite `NotFocusable WARNING` (W705).
- Ao fechar/remover o elemento focado, o foco vai para a janela.
- `:focus` (Capítulo 46) estiliza; não há anel de foco automático nesta versão.

### Exemplos

#### Filtrar um campo (só dígitos)

```tinypine
const campo = w.input("", "id": "idade", "placeholder": "idade")
campo.on("textinput", f(e)
  if not (e.text in "0123456789")
    e.prevent()                     # uma colagem "12a" também é recusada inteira
)
campo.on("change", f(e)
  println(format "idade: {e.value}")
)
```

#### Fechar com Esc, confirmando

```tinypine
w.on("keydown", f(e)
  if e.key == "escape"
    w.close()
)
w.on("close", f(e)
  if sujo
    e.prevent()                     # cancela o fechamento
    aviso.text = "Salvar antes de sair?"
)
```

#### Arrastar

```tinypine
var $arrastando = false
alca.on("pointerdown", f(e)
  $arrastando = true
)
w.on("pointermove", f(e)
  if $arrastando
    alca.style({"left": e.x - 10, "top": e.y - 10})
)
w.on("pointerup", f(e)
  $arrastando = false
)
```

*(Estado entre handlers em `var $…` global; ver a nota do exemplo de `every`. `sujo` e `aviso` do exemplo anterior vêm do programa em volta.)*
