## Canvas — Estilo

### Resumo

O estilo do canvas **tem a forma do CSS** — propriedades com os mesmos nomes (`font-size`, `flex-direction`, `border-radius`…), seletores, especificidade, cascata, herança — mas é um **subconjunto fechado**, escrito com valores do TinyPine e **checado**: o que o CSS de navegador ignora em silêncio, o canvas recusa com erro.

Uma declaração é um par `"propriedade": valor` num **dict**:

```tinypine
{"background": "#202030", "padding": 16, "border-radius": 8}
```

O mesmo dict serve para estilo inline e para o corpo de uma regra.

### Formas de aplicar estilo

| **Forma**                         | **Onde**                          | **Prioridade na cascata** | **Exemplo**                                              |
|-----------------------------------|-----------------------------------|---------------------------|----------------------------------------------------------|
| na criação, `"style": {...}`      | construtor de elemento            | inline (a maior)          | `w.text("Oi", "style": {"color": "yellow"})`             |
| `el.style({...})`                 | elemento já criado                | inline (a maior)          | `titulo.style({"font-size": 32})`                        |
| `w.rules({seletor: {...}, ...})`  | folha da janela                   | por especificidade e ordem | `w.rules({".card": {"padding": 12}})`                   |
| `w.css(texto)`                    | folha da janela, em **texto CSS** | por especificidade e ordem | `w.css(os.read("tema.css"), "source": "tema.css")` (Capítulo 47) |

`el.style(dict)` **mescla** com o estilo inline que já existe (só as chaves dadas mudam). Para remover uma declaração inline, use o valor `null`: `el.style({"color": null})` volta a deixar a cascata decidir. `w.style(dict)` age sobre a raiz. `el.style()` (sem argumento) devolve uma **cópia** `dict` do estilo inline atual — para o programa alterar e reaplicar (o dict é a forma de manipular estilo). `style` é método e não propriedade, de propósito.

`w.rules(...)` e `w.css(...)` devolvem um `sheet` (`.remove()` tira a folha; as folhas valem **na ordem em que foram registradas**, misturadas entre as duas formas). A forma em dict equivale à em texto, com uma diferença: **o dict não repete chave**, então o mesmo seletor não aparece duas vezes no mesmo `rules` (registre outro `rules`, ou use `w.css`). O contrato de `w.css`, os erros e o que fica de fora estão no Capítulo 47.

```tinypine
w.rules({
  "box.card":       {"background": "#202030", "padding": 16, "border-radius": 8},
  "box.card:hover": {"background": "#2a2a40"},
  "text":           {"font-size": 18},
  "#titulo":        {"font-size": 28, "color": "#ffd166"}
})
```

Lista de seletores com vírgula (`"a, b"`) funciona como no CSS.

### Valores

| **Tipo de valor** | **Formas aceitas**                                                                                           |
|-------------------|--------------------------------------------------------------------------------------------------------------|
| **comprimento**   | `num` = pixels lógicos (`16`); `str` com unidade (`"16px"`, `"50%"`, `"1.5em"`, `"2rem"`, `"10vw"`, `"10vh"`); `"auto"` onde couber |
| **cor**           | nome (`"white"`, `"black"`, `"red"`, … o conjunto de nomes do CSS), `"transparent"`, `"currentColor"`, `"#rgb"`, `"#rrggbb"`, `"#rrggbbaa"`, `"rgb(r,g,b)"`, `"rgba(r,g,b,a)"`, `"hsl(h,s%,l%)"`, `"hsla(...)"` |
| **palavra-chave** | `str` (`"flex"`, `"center"`, `"bold"`…)                                                                      |
| **número puro**   | `num` (`"opacity": 0.5`, `"flex-grow": 1`, `"z-index": 2`)                                                   |
| **atalho (1–4 valores)** | `num` para um valor só; **lista** para vários (`"padding": [8, 16]`, `"margin": [0, "auto"]`); ou uma `str` CSS **completa** (`"padding": "8px 16px"`) |
| **`null`**        | só em `el.style`: remove a declaração inline                                                                |

**Regra única:** número é px; qualquer outra unidade vai numa `str` que seja **CSS válido** — portanto **com unidade** (`"50%"`, `"2em"`, `"16px"`; só o `0` dispensa) e, nos atalhos, ou a lista (`[8, 16]`, cada item `num` ou `str` com unidade) ou a `str` inteira (`"8px 16px"`). `"padding": "8 16"` é `InvalidStyleValue` (E721), com a dica de usar `[8, 16]` ou `"8px 16px"`. Assim o dict e o `w.css` têm **uma** regra de unidade, e uma `str` copiada de um CSS de navegador continua válida. Em detalhe: `"width": 200` é 200 px; `"width": "50%"` é 50% do bloco contêiner. Não há funções de unidade como `pct(50)`: as `str` evitam inventar tipos novos e deixam o CSS que o programador já conhece funcionar. `em` é relativo ao `font-size` do elemento (do pai, quando usado em `font-size`); `rem` ao `font-size` da raiz; `vw`/`vh` a 1% da largura/altura da **área cliente** da janela. `%` é relativo à propriedade correspondente do bloco contêiner (regras no Capítulo 48).

As cores usam o espaço sRGB. `"currentColor"` é o valor de `color` do próprio elemento.

### Propriedades

Legenda: **herda** = herdada pelos filhos quando não definida; **atalho** = aceita 1–4 valores.

#### Caixa e tamanho

| **Propriedade**                                       | **Valores**                                         | **Padrão**       | **Obs.**                                                        |
|-------------------------------------------------------|-----------------------------------------------------|------------------|-----------------------------------------------------------------|
| `width`, `height`                                     | comprimento, `"auto"`, `"fit-content"`              | `"auto"`         | `"fit-content"`: o tamanho do conteúdo (limitado ao espaço disponível) — o "encolher para caber" que o CSS faz com `inline-block`/`float`. |
| `min-width`, `min-height`                             | comprimento, `"auto"`                               | `"auto"`         | `"auto"` vale `0`, exceto em item *flex* no **eixo principal**, onde é o tamanho mínimo do **conteúdo** — **limitado** pelo `width`/`height` definido e pelo `max-*` — e **`0` se o item tem `overflow` ≠ `visible`** (regra do CSS Flexbox, §4.5; Capítulo 48). |
| `max-width`, `max-height`                             | comprimento, `"none"`                               | `"none"`         |                                                                 |
| `padding` (`-top`, `-right`, `-bottom`, `-left`)      | comprimento ≥ 0 · atalho                            | `0`              | Sem negativos.                                                  |
| `margin` (`-top`, `-right`, `-bottom`, `-left`)       | comprimento, `"auto"` · atalho                      | `0`              | Negativos valem. Não colapsam.                            |
| `border-width`                                        | comprimento ≥ 0 · atalho                            | `0`              |                                                                 |
| `border-style`                                        | `"none"`, `"solid"`                                 | `"none"`         | Pontilhado/tracejado: `UnsupportedStyle`.                       |
| `border-color`                                        | cor                                                 | `currentColor`   |                                                                 |
| `border`                                              | `"largura estilo cor"` (ex. `"1px solid #444"`)     | —                | Atalho dos três acima; a largura leva unidade.            |
| `border-radius`                                       | comprimento · lista de 1–4 valores                  | `0`              | Raio circular (sem elíptico).                                   |
| `box-sizing`                                          | `"border-box"`, `"content-box"`                     | **`"border-box"`** | Desvio do CSS.                                          |

#### Visual

| **Propriedade**    | **Valores**                                         | **Padrão**     | **Herda** |
|--------------------|-----------------------------------------------------|----------------|-----------|
| `background`       | cor (só cor; gradiente e imagem ficam para depois) | `"transparent"` | não    |
| `color`            | cor                                                 | `"white"` (raiz) | sim     |
| `opacity`          | `0` a `1`                                           | `1`            | não       |
| `visibility`       | `"visible"`, `"hidden"`                             | `"visible"`    | sim       |
| `overflow`         | `"visible"`, `"hidden"`, `"scroll"`, `"auto"`       | `"visible"`    | não       |
| `cursor`           | `"default"`, `"pointer"`, `"text"`, `"none"`        | `"default"`    | sim       |
| `z-index`          | `int`                                               | `0`            | não       |

`visibility: "hidden"` mantém o espaço e não recebe evento; `display: "none"` tira o elemento do layout.

#### Texto

| **Propriedade**    | **Valores**                                                          | **Padrão**  | **Herda** |
|--------------------|----------------------------------------------------------------------|-------------|-----------|
| `font-family`      | `"sans"`, `"serif"`, `"mono"` ou nome de família instalada; **uma lista** = ordem de preferência (`["Segoe UI", "sans"]`) | `"sans"`    | sim       |
| `font-size`        | comprimento > 0                                                      | `16`        | sim       |
| `font-weight`      | `100`…`900`, `"normal"` (= 400), `"bold"` (= 700)                        | `"normal"`  | sim       |
| `font-style`       | `"normal"`, `"italic"`                                               | `"normal"`  | sim       |
| `line-height`      | número puro (múltiplo do `font-size`), comprimento, `"normal"`       | `"normal"`  | sim       |
| `text-align`       | `"left"`, `"center"`, `"right"`                                      | `"left"`    | sim       |
| `white-space`      | `"normal"` (quebra), `"nowrap"`, `"pre"` (preserva espaços e `\n`)   | `"normal"`  | sim       |

#### Layout (resumo; o comportamento está no Capítulo 48)

| **Propriedade**    | **Valores**                                                                                   | **Padrão**     |
|--------------------|-----------------------------------------------------------------------------------------------|----------------|
| `display`          | `"block"`, `"flex"`, `"none"`                                                                 | por tipo (Capítulo 45) |
| `position`         | `"static"`, `"relative"`, `"absolute"`                                                        | `"static"`     |
| `top`, `right`, `bottom`, `left` | comprimento, `"auto"`                                                           | `"auto"`       |
| `flex-direction`   | `"row"`, `"row-reverse"`, `"column"`, `"column-reverse"`                                      | `"row"`        |
| `flex-wrap`        | `"nowrap"`, `"wrap"`, `"wrap-reverse"`                                                        | `"nowrap"`     |
| `justify-content`  | `"flex-start"`, `"flex-end"`, `"center"`, `"space-between"`, `"space-around"`, `"space-evenly"` (`"start"`/`"end"` também) | `"flex-start"` |
| `align-items`      | `"stretch"`, `"flex-start"`, `"flex-end"`, `"center"` (`"start"`/`"end"` também)              | `"stretch"`    |
| `align-self`       | `"auto"` ou como `align-items`                                                                | `"auto"`       |
| `flex-grow`, `flex-shrink` | número ≥ 0                                                                            | `0`, `1`       |
| `flex-basis`       | comprimento, `"auto"`                                                                         | `"auto"`       |
| `flex`             | atalho: `1`, `"1 1 auto"`, `"none"`, `"auto"`                                                 | —              |
| `gap`, `row-gap`, `column-gap` | comprimento ≥ 0 · `gap` aceita 1 ou 2 valores                                     | `0`            |
| `order`            | `int`                                                                                         | `0`            |

#### Fora desta versão (erro `UnsupportedStyle`, E722, com dica)

`display: grid | inline | inline-block`, `float`, `clear`, `transform`, `transition`, `animation`, `filter`, `box-shadow`, `text-shadow`, `outline`, `background-image`/gradientes, `calc()`, `var()`/propriedades `--x`, `align-content`, `text-decoration`, `text-overflow`, `letter-spacing`, `pointer-events`, `user-select`, `position: fixed | sticky`, `!important`, `@media`, `@font-face`, `@import`.

### Seletores

Sintaxe de CSS, subconjunto mínimo:

| **Seletor**             | **Casa**                                                         | **Exemplo**                |
|-------------------------|------------------------------------------------------------------|----------------------------|
| tipo                    | elementos desse tipo (`box`, `text`, `image`, `button`, `input`) | `button`                   |
| `*`                     | qualquer elemento                                                | `*`                        |
| `#id`                   | o elemento com esse `id`                                         | `#titulo`                  |
| `.classe`               | quem tem a classe                                                | `.card`                    |
| composto                | todas as partes juntas, sem espaço                               | `box.card.ativo`           |
| descendente             | `A B` — B dentro de A, em qualquer profundidade                  | `.card text`               |
| filho direto            | `A > B`                                                          | `.card > text`             |
| lista                   | `A, B` — o mesmo corpo para vários                               | `button, input`            |
| pseudo-classe de estado | `:hover`, `:active`, `:focus`, `:disabled`                       | `button:hover`             |

Fica para depois: seletores de atributo (`[x=y]`), irmãos (`+`, `~`), estruturais (`:first-child`, `:nth-child`…), pseudo-elementos. Casar **o tipo do elemento** é a diferença para o CSS: em vez de `div`, `p`, `span`, os nomes são `box`, `text`, `image`, `button`, `input` (JavaFX e Qt também usam o nome do tipo de controle como seletor de tipo).

As pseudo-classes seguem o estado do elemento: `:hover` (ponteiro em cima), `:active` (pressionado), `:focus` (com foco de teclado), `:disabled`. As mesmas leituras existem como propriedades (`el.hovered`, `el.pressed`, `el.focused`, `el.disabled`).

### Cascata

Para cada propriedade de cada elemento, o valor **especificado** é o da origem mais forte que a define, na ordem (**da mais forte para a mais fraca**):

1. **estilo inline** (`"style"`, `el.style`);
2. **folhas do autor** (`w.rules`, `w.css`): vence a regra de maior **especificidade**; em empate, **a posterior vence** (as folhas valem na ordem em que foram registradas; dentro de uma folha, na ordem do dict);
3. **folha padrão do canvas (UA)** — a lista abaixo.

Se **nenhuma** origem define a propriedade: ela é **herdada** do pai, se for do tipo "herda"; senão recebe o **valor inicial** (coluna "Padrão").

**Especificidade**, como no CSS 2: o trio (nº de `#id`, nº de `.classe` + pseudo-classes, nº de tipos); `*` não conta; compara-se da esquerda para a direita. Qt e JavaFX usam a mesma regra.

Não existe `!important` (Qt também não tem): a ordem acima é a única. Se um programador precisa "vencer" uma regra, usa `el.style`.

Mudou uma classe, um estado (`:hover`) ou um estilo → o motor reavalia **só os elementos afetados**.

#### Ler o estilo: `el.style()` e `el.computed(nome)`

| **Chamada**            | **Devolve**                                                                                                                        |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `el.style()`           | **cópia** `dict` do estilo **inline** (o que foi escrito em `"style"`/`el.style({...})`), exatamente como foi dado.                  |
| `el.computed("width")` | o valor **resolvido** de uma propriedade depois da cascata, da herança e do layout.                                          |

`computed` segue o que os navegadores fazem com `getComputedStyle`: **comprimentos viram `float` em px** (`"2em"` → `32.0`, `"50%"` de largura → a largura usada); `width`/`height`/`top`/… com `auto` devolvem o valor **usado** (força o layout, como `rect()`); cores viram `"#rrggbb"` ou `"#rrggbbaa"`; palavras-chave voltam como `str`; números puros como `num`. Propriedade que não existe: `UnknownStyleProperty` (E720); fora desta versão: `UnsupportedStyle` (E722). Em elemento `display: "none"` (ou dentro de um), as propriedades de tamanho devolvem `0.0`.

```tinypine
const t = w.text("Oi", "style": {"font-size": "2em"})
println(t.computed("font-size"))    # 32.0 (2 × o font-size herdado, 16)
```

#### Folha padrão (UA)

Mínima e deliberadamente visível — o programador pode ler tudo o que o canvas aplica sozinho (RmlUi parte do extremo oposto: nenhum estilo padrão):

```tinypine
{
  "button": {"display": "flex", "justify-content": "center", "align-items": "center",
             "width": "fit-content", "padding": [6, 14], "background": "#3a3a3a",
             "color": "white", "border-radius": 4, "cursor": "pointer"},
  "button:hover":    {"background": "#4a4a4a"},
  "button:active":   {"background": "#2a2a2a"},
  "button:disabled": {"opacity": 0.5, "cursor": "default"},
  "input":  {"width": 200, "padding": [6, 8], "background": "#1e1e1e", "color": "white",
             "border": "1px solid #555", "border-radius": 4, "cursor": "text"},
  "input:focus": {"border-color": "#4a85f0"}
}
```

Mais os valores da raiz da janela (Capítulo 44) e o `display` por tipo (Capítulo 45). O anel de foco para `box`/`text` focáveis **não** existe nesta versão (precisaria de `outline`).

### Erros de estilo

Três erros distintos, para o programador saber se **errou**, se **digitou errado** ou se **pediu algo que ainda não existe**:

| **Caso**                                                | **Erro**                                  | **Exemplo**                                   |
|---------------------------------------------------------|-------------------------------------------|-----------------------------------------------|
| nome não existe no CSS nem no canvas                    | `UnknownStyleProperty PROBLEM` (E720)     | `{"colour": "red"}` → *did you mean 'color'?* |
| o nome existe, mas o valor tem tipo/forma errados       | `InvalidStyleValue PROBLEM` (E721)        | `{"width": "wide"}` · `{"opacity": 2}`        |
| CSS válido, fora desta versão                                  | `UnsupportedStyle PROBLEM` (E722)         | `{"display": "grid"}` · `{"transform": …}`    |
| propriedade válida que não tem efeito nesse contexto    | `StyleHasNoEffect WARNING` (W701)         | `flex-grow` num filho de `display: block`     |

Os erros de estilo são **erros** (não avisos) porque um navegador que os ignora produz exatamente a classe de bug que o TinyPine se propõe a evitar (Cap. 36). `StyleHasNoEffect` é aviso e pode ser escondido com `#~ hide W701` (Cap. 3.1.1), como qualquer aviso.

A verificação é feita **quando o estilo é aplicado** (execução, etapa 8). Em `w.css`, o erro leva também **a posição dentro do texto CSS** (Capítulo 47). Dicts de estilo escritos como literais podem ser verificados antes, na Análise Estática de Tipos (etapa 6), quando todo valor é literal — uma melhoria possível, não requisito.

### Exemplo

```tinypine
use canvas

const w = canvas.window("id": "demo", "name": "Estilo", "width": 480, "height": 240)

w.rules({
  ".linha":        {"display": "flex", "gap": 12, "padding": 16},
  ".caixa":        {"width": 80, "height": 80, "border-radius": 8},
  "#a":            {"background": "#ef476f"},
  "#b":            {"background": "#ffd166"},
  ".caixa:hover":  {"opacity": 0.7}
})

const linha = w.box("classes": ["linha"])
linha.box("id": "a", "classes": ["caixa"])
linha.box("id": "b", "classes": ["caixa"])
linha.box("id": "c", "classes": ["caixa"], "style": {"background": "#06d6a0"})

canvas.run()
```

```
┌─ Estilo ─────────────────────────────┐
│ (fundo preto)                        │
│  ┌──────┐  ┌──────┐  ┌──────┐        │
│  │  A   │  │  B   │  │  C   │        │
│  └──────┘  └──────┘  └──────┘        │
└──────────────────────────────────────┘
```
A = rosa, B = amarelo, C = verde. Três caixas de 80 × 80, em linha, com 12 px de espaço entre elas e 16 px de margem interna.
