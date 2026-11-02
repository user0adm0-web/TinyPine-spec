## Canvas — Testes Sem Tela

### Para quê

O repositório valida exemplos com **`tinypine run` + `output`** (a saída impressa é comparada). `"headless": true` e `rect()` cobrem **estilo e layout** sem tela. Faltava a **interação**: sem usuário, ninguém clica, e um contador ou uma lista de tarefas não seriam testáveis. Três recursos, **só para janelas `headless`**, resolvem isso:

| **Recurso**                              | **Faz**                                                                                          |
|------------------------------------------|--------------------------------------------------------------------------------------------------|
| `w.dispatch(tipo, dados)` · `el.dispatch(tipo, dados)` | entrega um evento **pelo mesmo caminho** do real (captura → alvo → bolha, ações padrão). |
| `canvas.advance(segundos)`               | move o **relógio virtual**: roda `after`/`every` vencidos, sem esperar de verdade.               |
| `canvas.poll()` sem dormir               | uma rodada **instantânea** (equivale a `advance(0)`).                                            |

Em janela **não** `headless`, `dispatch` e `advance` são `HeadlessOnly PROBLEM` (E734): um teste que "clica" numa janela de verdade competiria com o usuário.

### `dispatch`

```text
alvo.dispatch(tipo, dados = {})  →  bool
```

- **Síncrono**: quando retorna, o evento já foi propagado, as **ações padrão** (a menos que canceladas) já rodaram e os handlers já terminaram. É o `dispatchEvent` do DOM.
- **Retorno**: `false` se algum handler chamou `e.prevent()` num evento **cancelável**; senão `true` (como no DOM).
- **Alvo**:
  - `el.dispatch(…)`: o alvo é `el` (não precisa estar focado; um `el.dispatch("keydown", …)` vai para `el`).
  - `w.dispatch(…)` com **evento de ponteiro** (`pointer*`, `click`, `dblclick`, `wheel`): o alvo é o elemento **sob `(x, y)`** (o mesmo *hit-test* do usuário, Capítulo 48); `"x"` e `"y"` são **obrigatórios**.
  - `w.dispatch(…)` com evento de **teclado** (`keydown`, `keyup`, `textinput`): o alvo é o **elemento focado**, ou a janela se não há foco — exatamente a regra do usuário (Capítulo 49).
- **Dados** (`dict`; o que falta recebe o padrão):

| **Tipo**                                        | **Chaves**                                                                                   |
|-------------------------------------------------|----------------------------------------------------------------------------------------------|
| `pointerdown`, `pointerup`, `click`, `dblclick`, `pointermove`, `pointerenter`, `pointerleave` | `"x"`, `"y"` (em `el.dispatch`: o **centro** da caixa da borda); `"button"` (`"left"`); `"count"` (`click`: 1, `dblclick`: 2); modificadores `"shift"`, `"ctrl"`, `"alt"`, `"meta"` (`false`) |
| `wheel`                                         | `"x"`, `"y"`, `"dx"` (0.0), `"dy"` (0.0), modificadores                                       |
| `keydown`                                       | `"key"` (**obrigatória**; os nomes de `computer.keyboard`), `"repeat"` (`false`), modificadores |
| `keyup`                                         | `"key"`, modificadores                                                                        |
| `textinput`                                     | `"text"` (**obrigatória**, `str` não vazia; Capítulo 50)                                      |
| `close`                                         | — (equivale ao usuário pedir para fechar: cancelável; se ninguém cancela, a janela fecha)    |
| `resize`, `move`, `scale`, `activate`, `deactivate` | os dados do evento (`"width"`/`"height"`, `"x"`/`"y"`, `"scale"`). **Só entrega** o evento: **não** muda `w.width`, `w.x`… (o estado vem do sistema) |

- **Não despacháveis**: `frame` e `timer` (use `advance`), `focus`/`blur` (use `el.focus()`/`el.blur()`), `input`/`change` (nascem da edição: despache `textinput`/`keydown` num `input`). Tipo desconhecido: `UnknownEventKind` (E730); tipo não despachável, chave que o tipo não tem, chave obrigatória ausente, ou valor de tipo errado: **`InvalidDispatch PROBLEM` (E735)**, com as chaves do tipo na dica.
- **Estado do ponteiro**: `pointerenter`/`pointerleave` ligam/desligam `el.hovered` (e a pseudo-classe `:hover`); `pointerdown`/`pointerup` ligam/desligam `el.pressed` (`:active`). Assim estilos de estado também são testáveis (`el.computed(…)`, Capítulo 46).
- **Um evento por chamada**: `el.dispatch("click")` entrega **só** o `click`, sem `pointerdown`/`pointerup` antes (é o `el.click()` do DOM). Para a sequência completa, despache os três.
- `dispatch` **de dentro de um handler** é permitido (headless) e roda aninhado, síncrono (Capítulo 49, "Mudar a árvore…").
- Evento digitado **não** gera evento "irmão": `dispatch("keydown", {"key": "a"})` **não** produz `textinput` (que é o que insere o texto). Quem testa digitação despacha o `textinput`.

### O relógio virtual: `advance` e `poll`

- O tempo de um programa com janelas `headless` é **virtual**: começa em `0.0` e só anda por `canvas.advance(segundos)`. `e.time` e `e.dt` usam esse relógio. **Nada** dorme nem consulta o relógio do sistema.
- `canvas.advance(s)`: roda, **em ordem de vencimento**, os `after`/`every` que vencem em `s` segundos (cada um vê o relógio no seu instante de vencimento); depois entrega **um** evento `frame` por janela, com `e.dt = s`. `s` < 0: `InvalidTimerInterval` (E733). `advance(0)`: só o `frame`.
- Um `every(1, f)` dentro de `advance(3.5)` roda **3** vezes (em 1, 2 e 3); o resto, 0,5 s, fica no relógio. (Não há "perda de ticks" aqui: o passo é exato, sem atraso real — a perda de ticks do Capítulo 49 vale para janelas reais.)
- `canvas.poll()` com janela `headless` **não dorme** e equivale a `advance(0)`; devolve `true` enquanto houver janela aberta. `canvas.run()` **volta na hora** (não há usuário a esperar; Capítulo 49).
- `canvas.advance` com **qualquer** janela real aberta: `HeadlessOnly` (E734): o relógio precisa ser de um tipo só.

### Texto e fontes: o que dá e o que não dá para testar

`rect()` de **caixas sem texto** (tamanhos fixos, flex, `%`) é **exato** e reproduzível. O tamanho de um `text` depende da **fonte**; sem uma fonte **embutida e fixa** no motor (Apêndice A, B38) o resultado muda de máquina para máquina. Por isso os exemplos abaixo **evitam** `rect()` de texto: imprimem `text`, `value`, contagens e estados. `w.capture(caminho)` (PNG) existe em `headless`, mas **comparar imagens** fica fora: depende da mesma fonte.

### Exemplos

#### O contador (exemplo 3 do Capítulo 52), testado

```tinypine
use canvas

const w = canvas.window("id": "contador", "width": 320, "height": 220, "headless": true)
const valor = w.text("0", "id": "valor")
const mais  = w.button("+1", "id": "mais")
const zero  = w.button("zerar", "id": "zero")

mais.on("click", f(e)
  const atual = valor.text: to-int
  valor.text = format "{atual + 1}"
)
zero.on("click", f(e)
  valor.text = "0"
)

mais.dispatch("click")
mais.dispatch("click")
println(valor.text)
zero.dispatch("click")
println(valor.text)
```

```output
2
0
```

#### A lista de tarefas (exemplo 4), com `ç` e `ã`

```tinypine
use canvas

const w = canvas.window("id": "tarefas", "width": 360, "height": 420, "headless": true)
const barra = w.box("id": "barra")
const campo = barra.input("", "id": "campo", "placeholder": "nova tarefa")
const add   = barra.button("Adicionar", "id": "add")
const lista = w.box("id": "lista")

f adicionar()
  if campo.value != ""
    lista.text(campo.value, "classes": ["item"])
    campo.value = ""
    campo.focus()

add.on("click", adicionar)
campo.on("keydown", f(e)
  if e.key == "enter"
    adicionar()
)

campo.focus()
w.dispatch("textinput", {"text": "ação"})      # o alvo é o campo (tem o foco)
w.dispatch("keydown", {"key": "enter"})
println(lista.children().length)
println(lista.children()[0].text)
println(campo.value == "")
add.dispatch("click")                           # campo vazio: não adiciona
println(lista.children().length)
```

```output
1
ação
true
1
```

#### Timers sem esperar

```tinypine
use canvas

const w = canvas.window("id": "t", "headless": true)
var $n = 0
canvas.every(1, f(e)
  $n = $n + 1
)
canvas.advance(3.5)
println($n)
canvas.advance(0.5)
println($n)
```

```output
3
4
```

(O segundo `advance` completa 4,0 s: o quarto disparo cai exatamente em `t = 4`.)

#### Propagação e `stop`

```tinypine
use canvas

const w = canvas.window("id": "p", "width": 200, "height": 100, "headless": true)
const painel = w.box("id": "painel", "style": {"width": 200, "height": 100})
const ok = painel.button("OK", "id": "ok", "style": {"width": 80, "height": 30})

painel.on("click", f()
  println("painel")
)
ok.on("click", f(e)
  println("botão")
  e.stop()
)

ok.dispatch("click")
ok.dispatch("click")
```

```output
botão
botão
```

(O `stop()` impede o painel de receber; o `f()` sem parâmetro é um handler válido.)

### Erros e avisos desta parte

| **Caso**                                                                                          | **Erro**                                  |
|---------------------------------------------------------------------------------------------------|-------------------------------------------|
| `dispatch`/`advance` com janela **não** `headless`                                                | `HeadlessOnly PROBLEM` (E734)             |
| `dispatch` com tipo não despachável, chave desconhecida/ausente, valor de tipo errado               | `InvalidDispatch PROBLEM` (E735)          |
| `dispatch` com tipo que não existe                                                                | `UnknownEventKind PROBLEM` (E730)         |
| `advance` com segundos < 0                                                                        | `InvalidTimerInterval PROBLEM` (E733)     |
| `advance`/`poll` **de dentro de um handler**                                                      | `RunReentrant PROBLEM` (E732)             |
| `dispatch` num elemento removido / janela fechada                                                 | `StaleHandle PROBLEM` (E706)              |

### O que ficou de fora

- **Comparar imagem** (`capture`) e **medir texto** de forma reproduzível: dependem de uma fonte embutida fixa (Apêndice A, B38).
- **Gravar e reproduzir** uma sessão de eventos (macro).
- **`dispatch` assíncrono** (fila que só roda no `poll`): o `dispatch` é **síncrono**, como o `dispatchEvent` do DOM, para que o resultado de uma linha de teste (`println(valor.text)`) seja previsível.
