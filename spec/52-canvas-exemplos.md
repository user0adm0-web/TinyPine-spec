## Canvas — Exemplos

Os desenhos em ASCII são esboços do resultado, não saída do programa. Todos os exemplos usam a API dos Capítulos 44 a 51.

### 1. A janela preta

O menor programa com janela: só a janela, nenhum elemento.

```tinypine
use canvas

canvas.window("id": "vazia")
canvas.run()
```

```
┌─ vazia ───────────────────────┐
│                               │
│          (tudo preto)         │
│                               │
└───────────────────────────────┘
```

800 × 600, fundo `black`, sem elementos. Fecha-se pelo botão da barra de título; `run()` retorna e o programa acaba.

### 2. Primeiro: a janela; depois: os elementos

```tinypine
use canvas

const w = canvas.window("id": "main", "name": "Olá", "width": 480, "height": 200)

w.rules({
  "#titulo": {"font-size": 32, "margin": 24},
  "#sub":    {"color": "#9aa0b4", "margin": [0, 24]}
})

w.text("Olá, TinyPine", "id": "titulo")
w.text("Uma janela, sem navegador.", "id": "sub")

canvas.run()
```

```
┌─ Olá ─────────────────────────────┐
│                                   │
│  Olá, TinyPine                    │
│  Uma janela, sem navegador.       │
│                                   │
└───────────────────────────────────┘
```

Texto branco (herdado da raiz) sobre fundo preto; o `#sub` troca só a cor.

### 3. Contador

O estado fica **no próprio elemento** (`valor.text`), então o handler só lê e grava a propriedade — sem variável global. (Versão testável por `dispatch` no Capítulo 51.)

```tinypine
use canvas

const w = canvas.window("id": "contador", "name": "Contador", "width": 320, "height": 220)

w.rules({
  ".painel":      {"display": "flex", "flex-direction": "column", "align-items": "center",
                   "gap": 16, "padding": 24},
  "#valor":       {"font-size": 48},
  "button":       {"background": "#2d6cdf"},
  "button:hover": {"background": "#4a85f0"}
})

const painel = w.box("classes": ["painel"])
const valor  = painel.text("0", "id": "valor")
const mais   = painel.button("+1", "id": "mais")
const zero   = painel.button("zerar", "id": "zero")

mais.on("click", f(e)
  const atual = valor.text: to-int
  valor.text = format "{atual + 1}"
)
zero.on("click", f(e)
  valor.text = "0"
)

canvas.run()
```

```
┌─ Contador ───────────────┐
│                          │
│            3             │
│          [ +1 ]          │
│         [ zerar ]        │
└──────────────────────────┘
```

Notas: `align-items: "center"` num contêiner em coluna centraliza os itens na horizontal; o `button` já tem `width: "fit-content"` na folha padrão (Capítulo 46), por isso não estica.

### 4. Lista de tarefas (campo + botão + lista)

```tinypine
use canvas

const w = canvas.window("id": "tarefas", "name": "Tarefas", "width": 360, "height": 420)

w.rules({
  "#barra": {"display": "flex", "gap": 8, "padding": 12},
  "#campo": {"flex-grow": 1},
  "#lista": {"display": "flex", "flex-direction": "column", "gap": 6,
             "padding": [0, 12], "height": 340, "overflow": "auto"},
  ".item":  {"padding": [8, 10], "background": "#1e1e2e", "border-radius": 4}
})

const barra = w.box("id": "barra")
const campo = barra.input("", "id": "campo", "placeholder": "nova tarefa")
const add   = barra.button("Adicionar", "id": "add")
const lista = w.box("id": "lista")

f adicionar()
  if campo.value != ""
    lista.text(campo.value, "classes": ["item"])
    campo.value = ""
    campo.focus()

add.on("click", adicionar)              # handler sem parâmetro, direto
campo.on("keydown", f(e)
  if e.key == "enter"
    adicionar()
)

canvas.run()
```

```
┌─ Tarefas ─────────────────────┐
│ [ nova tarefa________ ][Adic.]│
│ ┌───────────────────────────┐ │
│ │ comprar café              │ │
│ ├───────────────────────────┤ │
│ │ escrever a spec           │ │
│ └───────────────────────────┘ │
└───────────────────────────────┘
```

`adicionar` não recebe nada e é passada **direto** a `on` (um handler pode ter 0 ou 1 parâmetro). O de `keydown` usa `e` (para ler `e.key`). O `input` tem largura padrão 200, mas `flex-grow: 1` faz o campo ocupar o que sobra ao lado do botão.

### 5. Layout com barra lateral — e teste sem janela

Com `"headless": true` o motor roda estilo e layout sem abrir janela; `rect()` devolve números **exatos**, então o exemplo serve de teste automático (como os `tinypine run` + `output` da spec).

```tinypine
use canvas

const w = canvas.window("id": "app", "width": 640, "height": 400, "headless": true)
w.style({"display": "flex"})                                   # raiz em linha

const lateral   = w.box("id": "lateral",   "style": {"width": 160, "padding": 12, "background": "#16213e"})
const principal = w.box("id": "principal", "style": {"flex-grow": 1, "padding": 16})

f linha(r)
  const x = r["x"]
  const y = r["y"]
  const largura = r["width"]
  const altura = r["height"]
  return format "{x} {y} {largura} {altura}"

println(linha(lateral.rect()))
println(linha(principal.rect()))
println(linha(principal.rect("box": "content")))
```

```output
0.0 0.0 160.0 400.0
160.0 0.0 480.0 400.0
176.0 16.0 448.0 368.0
```

Cada `rect()` é um `dict`; esta especificação ainda não define como um dict é **impresso** (Apêndice A, B35), então `linha` monta o texto campo a campo. (`w.capture("layout.png")` saiu do exemplo: gravar um arquivo não é saída verificável. Saída **prevista**, não executada: Apêndice A, B33.)

Conta: a raiz tem 640 × 400 (definidos). `lateral` tem `width: 160` e `principal` ocupa o resto (`640 − 160 = 480`); as alturas esticam para 400 (`align-items: stretch`). O conteúdo de `principal` é a caixa menos 16 px de preenchimento de cada lado (`160 + 16 = 176`; `480 − 32 = 448`; `400 − 32 = 368`).

### 6. Jogo mínimo: laço próprio com `poll`

```tinypine
use canvas

const w = canvas.window("id": "jogo", "name": "Nave", "width": 480, "height": 320, "resizable": false)

const nave = w.box("id": "nave", "style": {"position": "absolute", "left": 220, "top": 280,
                                         "width": 40, "height": 20, "background": "#06d6a0"})
const alvo = w.box("id": "alvo", "style": {"position": "absolute", "left": 100, "top": 0,
                                         "width": 30, "height": 30, "background": "#ef476f",
                                         "border-radius": 15})

w.on("keydown", f(e)
  const r = nave.rect()
  if e.key == "left"
    nave.style({"left": r["x"] - 10})
  else if e.key == "right"
    nave.style({"left": r["x"] + 10})
)

w.on("frame", f(e)
  const r = alvo.rect()
  alvo.style({"top": r["y"] + 80 * e.dt})        # 80 px por segundo, independente do FPS
)

while not w.closed
  canvas.poll("wait": 0.016)
```

```
┌─ Nave ───────────────────────────┐
│       ●                          │
│                                  │
│                                  │
│                ▬▬▬               │
└──────────────────────────────────┘
```

O movimento usa `e.dt` (segundos desde o quadro anterior), não "um passo por quadro": roda igual a 30 ou 144 quadros por segundo. As duas formas de laço (`run` com handlers, ou `poll` com laço próprio) podem ser misturadas: os handlers registrados valem em ambas.

### 7. Duas janelas

```tinypine
use canvas

const a = canvas.window("id": "principal", "name": "Principal", "width": 400, "height": 300, "x": 100, "y": 100)
const b = canvas.window("id": "paleta", "name": "Paleta", "width": 160, "height": 300, "x": 520, "y": 100)

f cor_botao(hex)
  const bt = b.button(hex, "style": {"background": hex, "margin": 8})
  bt.on("click", f(e)
    a.style({"background": hex})
  )

cor_botao("#ef476f")
cor_botao("#ffd166")
cor_botao("#06d6a0")

canvas.run()          # volta quando as DUAS janelas fecharem
```

```
┌─ Principal ────────────┐   ┌─ Paleta ──┐
│                        │   │ [#ef476f] │
│   (cor escolhida)      │   │ [#ffd166] │
│                        │   │ [#06d6a0] │
└────────────────────────┘   └───────────┘
```

Cada clique na paleta muda o fundo da janela `a`: handlers de uma janela podem agir em outra, porque os handles são valores comuns. O que **não** se pode é mover um *elemento* de uma janela para a outra (`CrossWindowMove`, E707).

### 8. O que dá erro — de propósito

```tinypine
use canvas

const w = canvas.window("id": "teste")
canvas.window("id": "teste")                 # WindowIdDuplicate PROBLEM (E702)
canvas.window()                              # MissingNamedArgument PROBLEM (E502)
canvas.box("id": "x")                        # membro inexistente: elementos só nascem em janela/elemento

const t = w.text("oi", "id": "t")
w.text("de novo", "id": "t")                 # ElementIdDuplicate PROBLEM (E710)
t.id = "outro"                               # ReadOnlyProperty PROBLEM (E313): id é imutável
t.value = "x"                                # UnknownAttribute PROBLEM (E716): text não tem 'value'
t.text = 3                                   # TypeMismatch PROBLEM (E302)
t.update({"txt": "x"})                      # UnknownAttribute PROBLEM (E716) — did you mean 'text'?
t.classes.add("x")                           # ImmutableMutation PROBLEM (Cap. 19.5): classes lê uma tupla
t.box("id": "filho")                         # membro inexistente: text é folha
t.style({"colour": "red"})                   # UnknownStyleProperty PROBLEM (E720) — did you mean 'color'?
t.style({"width": "wide"})                   # InvalidStyleValue PROBLEM (E721)
t.style({"display": "grid"})                 # UnsupportedStyle PROBLEM (E722)
w.find("nada")                               # ElementNotFound PROBLEM (E712)
t.on("clik", f(e)                            # UnknownEventKind PROBLEM (E730) — did you mean 'click'?
  println("x")
)
t.on("click", f(a, b)                        # InvalidHandler PROBLEM (E731): 0 ou 1 parâmetro
  println("x")
)
w.css("button { color: red")                 # CssSyntaxError PROBLEM (E723): chave sem fechar (Capítulo 47)
t.remove()
t.text = "y"                                 # StaleHandle PROBLEM (E706): gravar em elemento removido
```

Cada linha é um erro **independente** (o programa para no primeiro; o exemplo lista todos para consulta). Mensagens e dicas completas: Capítulo 53.

### 9. Gravar e atualizar em lote (propriedades e `update`)

Exemplo sem tela (`headless`), com a saída prevista. *(Saída **prevista**: o módulo ainda não tem implementação (Apêndice A, B33). O bloco é escrito como `tinypine` e não como `tinypine run`, de propósito: `tools/run_examples.py` executaria os blocos `run` e falharia.)*

```tinypine
use canvas

const w = canvas.window("id": "t", "headless": true)
const b = w.button("OK", "id": "ok")

b.text = "Enviar"                                          # uma propriedade
b.update({"disabled": true, "label": "Enviar formulário"})  # várias, tudo ou nada
b.classes = ["primario"]

println(b.text)
println(b.disabled)
println(b.has("primario"))
println(b.classes.length)
```

```output
Enviar
true
true
1
```
