## Canvas — Layout

### Resumo

Layout é a etapa que transforma **estilo + árvore** em **retângulos**: para cada elemento, onde ele fica e de que tamanho é. No canvas isso é feito **pelo próprio motor**, sem navegador, com um subconjunto pequeno e bem definido do layout do CSS:

- **`block`** — filhos empilhados na vertical;
- **`flex`** — o *flexbox* do CSS (linha ou coluna, quebra, crescer/encolher, alinhar, `gap`);
- **`absolute`** — fora do fluxo, posicionado por `top/right/bottom/left`;
- texto, imagem e campos são **folhas medidas** (o motor pergunta ao sistema de fontes/imagens "de que tamanho você fica?").

Isso segue o que Taffy e Yoga fazem (árvore de nós com estilo + função de medida para folhas) e deixa de fora o que RmlUi e litehtml fazem a mais (texto em fluxo, CSS2 completo). Esta versão fica no primeiro grupo de propósito: o difícil do CSS não é o *flex*, é o fluxo de texto *inline* e o colapso de margens.

### O modelo de caixa

Todo elemento gera **uma caixa** com quatro camadas, de dentro para fora:

```
┌───────────────────────── margem ─────────────────────────┐
│  ┌─────────────────────── borda ──────────────────────┐  │
│  │  ┌───────────────── preenchimento ───────────────┐ │  │
│  │  │  ┌───────────── conteúdo ──────────────────┐  │ │  │
│  │  │  │            (filhos / texto)             │  │ │  │
│  │  │  └─────────────────────────────────────────┘  │ │  │
│  │  └───────────────────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

| **Camada**      | **Propriedade**           | **Pinta?**                                  |
|-----------------|---------------------------|---------------------------------------------|
| conteúdo        | `width`, `height`         | texto, imagem, filhos                       |
| preenchimento   | `padding`                 | recebe o `background`                       |
| borda           | `border-*`                | recebe a cor da borda; o `background` também passa por baixo dela |
| margem          | `margin`                  | **nunca** pinta (sempre transparente)       |

Esse é o modelo do *CSS Box Model* (W3C): conteúdo, preenchimento, borda e margem, com margem negativa permitida e preenchimento não. O canvas muda **uma coisa**: `box-sizing` é `border-box` por padrão — `"width": 200` é a largura da **borda externa**, e o conteúdo é o que sobra. Quem quiser o comportamento do CSS clássico escreve `"box-sizing": "content-box"`.

Se `padding` + `border` já passam do `width` pedido, a largura usada é a soma deles e o conteúdo fica com 0 (a caixa nunca fica menor que as próprias camadas).

### Tamanhos

#### Valores

| **Valor**        | **Significado**                                                                                          |
|------------------|----------------------------------------------------------------------------------------------------------|
| `16` / `"16px"`  | pixels lógicos                                                                                           |
| `"50%"`          | 50% da dimensão correspondente do **bloco contêiner** (ver abaixo)                                       |
| `"auto"`         | calculado pelo layout (abaixo)                                                                           |
| `"fit-content"`  | o tamanho do conteúdo, no máximo o espaço disponível (substitui `inline-block`/`float`)             |
| `em`, `rem`, `vw`, `vh` | resolvidos antes do layout, a partir do estilo (Capítulo 46) e da janela                          |

#### `auto`

- **Largura em bloco**: ocupa a largura do conteúdo do contêiner, descontadas as margens.
- **Altura em bloco**: soma das alturas (com margens) dos filhos em fluxo.
- **Largura/altura em *flex*** e de elemento absoluto: ver as seções abaixo.
- **Folhas** (`text`, `image`, `button`, `input`): vêm da medida do conteúdo.

#### Porcentagens

- `%` em largura, margem e preenchimento refere-se à **largura do conteúdo** do bloco contêiner.
- `%` em **altura** só tem sentido se a altura do contêiner for **definida** (um comprimento fixo, uma porcentagem de contêiner definido, ou a raiz — a janela tem altura definida: a área cliente). Se não for, a porcentagem se comporta como `auto` e o motor emite `StyleHasNoEffect WARNING` (W701) — o CSS de navegador faz o mesmo em silêncio.

#### Limites

`min-*` e `max-*` limitam o tamanho calculado: `usado = max(min, min(calculado, max))`. Se `min` > `max`, **o `min` vence** (regra do CSS).

### Layout *block*

Padrão de `box`, `text`, `image`, `input` e da **raiz** (janela).

1. Os filhos em fluxo (`display` ≠ `none`, `position` ≠ `absolute`) são empilhados de cima para baixo, na ordem da árvore.
2. Cada filho ocupa a largura do contêiner (menos margens), salvo `width` definido.
3. Margens verticais adjacentes **somam** — não colapsam. Em compensação, isso é o mesmo comportamento que o CSS já tem dentro de contêineres *flex*.
4. Margem horizontal `"auto"` com `width` definido **centraliza** (`"margin": [0, "auto"]`).
5. `position: "relative"` desloca a caixa *depois* do layout, por `top/left/…`, sem mexer nos vizinhos.

```tinypine
const lista = w.box("id": "lista", "style": {"padding": 16})
lista.text("um",   "style": {"margin-bottom": 8})
lista.text("dois", "style": {"margin-bottom": 8})
lista.text("três")
```

### Layout *flex*

`display: "flex"` faz do elemento um **contêiner flex**; seus filhos em fluxo são **itens flex**. Segue o algoritmo do *CSS Flexible Box Layout* (W3C), nesta ordem:

1. **Coleta** dos itens (`display: none` fora; absolutos saem do fluxo); `order` define a ordem visual.
2. **Tamanho do contêiner** no eixo principal (definido, ou o disponível, ou o do conteúdo).
3. **Tamanho-base** de cada item (`flex-basis`, senão `width`/`height` do eixo, senão conteúdo) e **tamanho hipotético** (limitado por `min-*`/`max-*`).
4. **Linhas**: com `flex-wrap: "nowrap"` há uma linha; com `"wrap"`, itens vão para a linha seguinte quando não cabem.
5. **Resolução dos comprimentos flexíveis** por linha: se sobra espaço, ele é dividido entre os itens por `flex-grow`; se falta, o excesso é tirado por `flex-shrink` ponderado pelo tamanho-base; itens que batem em `min`/`max` são congelados e o resto recalculado.
6. **Tamanho cruzado** de cada linha e de cada item; `align-items`/`align-self: "stretch"` estica itens sem altura (largura, em coluna) definida.
7. **Distribuição no eixo principal** (`justify-content`) com `gap` entre itens; margens `"auto"` absorvem o espaço livre antes do `justify-content`.
8. **Alinhamento no eixo cruzado** (`align-items`/`align-self`). Linhas múltiplas se esticam para preencher o contêiner (equivale ao `align-content` padrão do CSS; a propriedade em si fica para depois).

**Tamanho mínimo automático** (`min-width: "auto"` / `min-height: "auto"`, Capítulo 46). Como no CSS (W3C, *CSS Flexible Box Layout*, "automatic minimum size"), um item flex **não encolhe abaixo** do seu mínimo automático no eixo principal, que vale:

1. **0**, se o item é um **contêiner de rolagem** nesse eixo (`overflow` ≠ `visible`): uma coluna com `overflow: "auto"` ao lado de outra **encolhe** normalmente e rola;
2. senão, o **tamanho mínimo do conteúdo** (para `text`: a palavra mais longa), **limitado** pelo tamanho especificado no eixo (`width: 100` com uma palavra de 140 → mínimo 100) e pelo `max-*`, se houver.

`"min-width": 0` escrito explicitamente desliga a regra. É a regra que mais surpreende no CSS — mas é a que faz o texto não sumir; o canvas a mantém.

```tinypine
const linha = w.box("id": "linha", "style": {"display": "flex", "gap": 10, "padding": 20, "width": 400})
const a = linha.box("id": "a", "style": {"width": 100, "height": 50})
const b = linha.box("id": "b", "style": {"width": 100, "height": 50, "flex-grow": 1})

const r = b.rect()
println(r["x"])         # 130.0
println(r["width"])     # 250.0
println(linha.rect()["height"])   # 90.0
```

(`rect()` devolve um `dict`; como esta especificação ainda não define como um `dict` é **impresso** — Apêndice A, B35 —, os exemplos imprimem campo a campo.)

Conta: largura do conteúdo = 400 − 2·20 = 360; menos o `gap` (10) = 350 para os itens; bases 100 + 100 = 200; sobram 150, todos para `b` (`flex-grow: 1`) → `b` = 250. `a` começa em `x = 20` (preenchimento), `b` em `20 + 100 + 10 = 130`, e termina em `380 = 400 − 20`. Altura da linha = 50 + 2·20 = 90.

#### Centralizar na janela

A raiz tem tamanho definido (a área cliente), então ela mesma pode ser um contêiner flex:

```tinypine
const w = canvas.window("id": "c", "width": 400, "height": 300)
w.style({"display": "flex", "justify-content": "center", "align-items": "center"})
const caixa = w.box("id": "caixa", "style": {"width": 100, "height": 50, "background": "#06d6a0"})

const r = caixa.rect()
println(r["x"])         # 150.0
println(r["y"])         # 125.0
```

### Posicionamento absoluto

`position: "absolute"` tira o elemento do fluxo e o posiciona por `top`/`right`/`bottom`/`left`:

- **Bloco de referência**: a caixa de preenchimento do ancestral mais próximo com `position` ≠ `"static"`; se não há, a **raiz** (área cliente).
- `left` + `right` com `width: "auto"` esticam; `top` + `bottom` com `height: "auto"` esticam.
- **Posição estática** (**como no CSS**): num eixo em que `left`/`right` (ou `top`/`bottom`) são `auto`, o elemento fica onde **estaria se fosse `position: "static"`**. Em contêiner *block*: `left` = início do conteúdo do pai, `top` = logo abaixo dos irmãos em fluxo que o precedem. Em contêiner *flex*: onde ficaria se fosse o **único item** — respeita `justify-content`, `align-items` e `flex-direction` do pai (numa raiz com `justify-content: "center"; align-items: "center"`, um filho absoluto sem `top/left` fica no **centro**).
- **Não** ocupa espaço no pai. Pinta acima dos irmãos não posicionados (`z-index`, abaixo).

Serve para sobreposições, marcadores, mira e personagens de jogo:

```tinypine
const arena = w.box("id": "arena", "style": {"position": "relative", "width": 400, "height": 300})
const bola  = arena.box("id": "bola", "style": {
  "position": "absolute", "left": 50, "top": 80, "width": 20, "height": 20,
  "background": "white", "border-radius": 10
})
```

### Texto, imagem e campos (folhas)

Folhas não têm filhos; o layout **pergunta o tamanho** a elas dado o espaço disponível:

| **Folha** | **Medida**                                                                                                                                  |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `text`    | quebra nas **lacunas de espaço** (e em `\n`) até caber na largura disponível; altura = nº de linhas × `line-height`; largura = a linha mais larga (em `fit-content`/flex) ou a largura disponível (em bloco). Palavra mais longa que a largura **transborda** (sem `overflow-wrap` nesta versão). `white-space: "nowrap"` = uma linha só; `"pre"` preserva espaços e `\n`. |
| `image`   | tamanho **intrínseco** do arquivo; só `width` dado → mantém a proporção; os dois dados → estica. (`object-fit` fica para depois.)           |
| `button`  | texto + `padding` + `border`; é um contêiner *flex* centralizando o texto.                                                                   |
| `input`   | altura = `line-height` + `padding` + `border`; largura = `width` (UA: 200).                                                                  |

A medida precisa de **três perguntas** ao sistema de fontes: tamanho com espaço disponível *definido*, tamanho **mínimo** (a palavra mais longa) e tamanho **máximo** (tudo em uma linha). São as mesmas três que o layout flex usa — e as que Taffy chama de função de medida e RmlUi de interface de fonte.

Resultado depende da fonte instalada: para exemplos **reprodutíveis**, o modo `headless` usa uma fonte embutida fixa (qual fonte: Apêndice A, B38).

### Estouro e rolagem

| **`overflow`** | **Efeito**                                                                                            |
|----------------|-------------------------------------------------------------------------------------------------------|
| `visible`      | filhos podem pintar fora da caixa (padrão)                                                            |
| `hidden`       | recorta na caixa de preenchimento (com `border-radius`, recorte arredondado)                          |
| `scroll`       | recorta e **sempre** permite rolar (roda do mouse, teclado)                                           |
| `auto`         | como `scroll`, só quando o conteúdo passa do tamanho                                                  |

`el.scroll-x` e `el.scroll-y` leem e gravam o deslocamento, em px lógicos (propriedades graváveis). Rolar não refaz layout, só a pintura. Ler ou gravar `scroll-x`/`scroll-y` num elemento **sem** `overflow: "scroll"|"auto"` devolve `0.0`/ignora a gravação **e** emite `StyleHasNoEffect WARNING` (W701). O `scroll` interno de um `input` (texto mais longo que o campo) é da própria folha.

### Ordem de pintura e empilhamento

Cada janela é pintada a cada quadro sujo, de trás para frente:

1. Raiz: `background`.
2. Para cada elemento, em **ordem de árvore**: `background` → borda → (conteúdo da folha: texto, imagem) → filhos.
3. Filhos **posicionados** (`position` ≠ `"static"`) pintam **depois** dos não posicionados do mesmo pai, ordenados por `z-index` (negativos primeiro) e, em empate, pela ordem da árvore.
4. `opacity` < 1 pinta o elemento e seus descendentes **como um grupo**, depois compõe com a opacidade (não por elemento).
5. `overflow` ≠ `visible` recorta os descendentes.

No CSS, só `z-index` ≠ `auto` cria contexto de empilhamento; no canvas **todo elemento posicionado cria** — mais simples, e cobre o uso real.

**Hit-test** é a pintura de trás para frente ao contrário: o ponteiro pertence ao **elemento mais de cima**, entre os que não têm `display: none`, `visibility: hidden` nem estão fora do recorte de um ancestral.

### Pixels, DPI e arredondamento

O layout é calculado em **px lógicos fracionários** (`float`). Na pintura, as bordas das caixas são **arredondadas para pixels do dispositivo** (`px lógico × w.scale`), para evitar linhas borradas e frestas entre vizinhos (Taffy oferece um passo de arredondamento para isso). `rect()` devolve os valores **antes** do arredondamento.

### Invalidação e quadros

- Mudou estilo, classe, texto, árvore ou tamanho da janela → o elemento é marcado **sujo**.
- Só o que depende dele é reestilizado/relayoutado; uma mudança que não afeta tamanho (cor, opacidade) só repinta.
- Várias mudanças dentro de um mesmo handler viram **um** quadro, apresentado depois do handler.
- Ler `el.rect()` com algo sujo **força** layout na hora (como `getBoundingClientRect`): barato uma vez, caro em laço. Dica de uso: leia depois de mudar, não alternando.

### `el.rect()`

```text
el.rect("box": "border")  →  {"x": float, "y": float, "width": float, "height": float}
```

| **`"box"`**     | **Retorna**                                |
|-----------------|--------------------------------------------|
| `"border"` (padrão) | caixa da borda (a "caixa" do elemento) |
| `"padding"`     | caixa de preenchimento                     |
| `"content"`     | caixa de conteúdo                          |
| `"margin"`      | caixa de margem                            |

Coordenadas na **área cliente** da janela, incluindo o deslocamento de rolagem dos ancestrais. Elemento com `display: none` (ou dentro de um): `{"x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}`.

### Onde o canvas **difere** do CSS

| **Assunto**                       | **CSS**                                  | **canvas**                                      | **Por quê**                          |
|-----------------------------------|------------------------------------------|-------------------------------------------------|--------------------------------------|
| `box-sizing` padrão               | `content-box`                            | **`border-box`**                                | `width: 200` mede o que se vê  |
| margens verticais adjacentes      | colapsam                                 | **somam**                                       | regra mais simples e previsível|
| texto                             | fluxo *inline* com trechos misturados    | **folha de bloco**, um estilo por `text`        | o *inline* é a parte mais cara |
| `display`                         | muitos                                   | `block`, `flex`, `none`                         | subconjunto fechado            |
| encolher para caber               | `inline-block`, `float`                  | **`"fit-content"`**                             | uma ferramenta, não duas             |
| contexto de empilhamento          | `z-index` ≠ `auto` etc.                  | todo elemento posicionado                       | simplicidade                   |
| `%` de altura com pai indefinido  | vira `auto`, sem aviso                   | vira `auto` **com** `W701`                      | sem erro silencioso            |
| direção do texto                  | bidi, `direction`, `writing-mode`        | só esquerda→direita, horizontal                 | fora desta versão                     |
| propriedade inválida              | ignorada                                 | **erro**                                        | Cap. 36                        |

Todo o resto — `flex`, `gap`, `min/max`, margens `auto`, `%`, `em/rem` — segue o CSS.
