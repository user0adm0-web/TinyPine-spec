# PARTE X — MÓDULO CANVAS

## Canvas — Visão Geral

### Resumo

`canvas` é um módulo da biblioteca padrão que dá ao TinyPine o que o navegador dá ao JavaScript: **uma janela, uma árvore de elementos, um sistema de estilo no formato do CSS e um laço de eventos** — sem navegador, sem HTML, sem motor de JavaScript.

A ideia em uma frase: **TinyPine está para `canvas` como JS está para o navegador.**

```tinypine
use canvas

const w = canvas.window("id": "main", "name": "Meu app")   # 1º: a janela (preta, vazia)
w.text("Olá, TinyPine", "id": "titulo")                  # 2º: os elementos
canvas.run()                                             # 3º: o laço de eventos
```

A regra central é a **ordem**: primeiro o programador faz a janela, depois os elementos. Isso não é convenção — é estrutural: os construtores de elemento (`box`, `text`, `image`, `button`, `input`) existem **somente dentro de um handle** (a janela ou outro elemento). O módulo `canvas` em si não tem `canvas.box(...)`. Não dá para criar um elemento "solto".

### O que o canvas pega do HTML e do CSS (e o que deixa)

O HTML e o CSS são, antes de tudo, **modelos**: uma árvore de elementos, caixas com *content/padding/border/margin*, regras com seletores e cascata, layout por *block* e *flex*, eventos que descem e sobem pela árvore. Nada disso exige navegador: vários motores de interface reusam só esse modelo (Taffy, Yoga, RmlUi, litehtml, Blitz, Sciter).

| **Fica (modelo)**                                    | **Sai (navegador)**                                      |
|------------------------------------------------------|----------------------------------------------------------|
| árvore de elementos com `id` e `classes`             | parser de HTML (a árvore é construída por chamadas) |
| modelo de caixa (content, padding, border, margin)   | JavaScript, `<script>`, `eval`                           |
| seletores, especificidade, cascata, herança          | rede, cookies, abas, `iframe`, `<a href>`                |
| layout *block*, *flex* e posicionamento absoluto     | layout *inline* (fluxo de texto misturado), tabelas, `float` |
| eventos com captura → alvo → bolha                   | `!important`, folhas externas por URL, `@import`         |
| unidades `px`, `%`, `em`, `rem`, `vw`, `vh`          | `calc()`, `var()`, media queries                    |

### Mapa web → canvas

| **Na web**                              | **No canvas**                                | **Diferença que importa**                                              |
|-----------------------------------------|----------------------------------------------|------------------------------------------------------------------------|
| `window` / aba                          | `canvas.window(...)` → `window`              | não existe até ser criada; `id` e `name` escolhidos pelo programador   |
| `document` + DOM                        | a árvore da janela                           | construída por chamadas; sem parser                                    |
| `createElement` + `appendChild`         | `pai.box(...)`, `pai.text(...)`…             | cria e anexa num passo só                                              |
| `el.textContent = "x"`                  | `el.text = "x"`                              | quase igual ao JS; o motor valida e repinta no próximo quadro    |
| `getElementById`                        | `w.find("id")`                               | `id` é imutável depois de criado                                       |
| `querySelector` / `querySelectorAll`    | `w.query(sel)` / `w.select(sel)`             | subconjunto de seletores                                         |
| folha CSS e atributo `style`            | `w.rules({...})`, `w.css("…")` e `el.style({...})` | dict **ou texto CSS**; subconjunto fechado; CSS inválido **é erro** (o primeiro interrompe), não é ignorado |
| `getComputedStyle(el).width`            | `el.computed("width")`                       | valor resolvido; comprimentos em px (`float`)                          |
| `el.dispatchEvent(...)` (testes)        | `el.dispatch("click", {...})`                | só em janela `headless`; síncrono (Capítulo 51)                        |
| `addEventListener`                      | `el.on("click", f(e) ...)`                   | o *handler* é uma função do TinyPine                                   |
| `setTimeout` / `setInterval`            | `canvas.after(...)` / `canvas.every(...)`    | tempo em **segundos** (Cap. 26)                                        |
| `requestAnimationFrame`                 | evento `frame` com `dt`                      | um por quadro apresentado, com `dt` em segundos |
| event loop do navegador                 | `canvas.run()` / `canvas.poll()`             | `run()` bloqueia; `poll()` deixa o laço com o programa |
| `<canvas>` (superfície 2D)              | *fora desta versão*                 | o nome do módulo **não** é a `<canvas>` do HTML                        |

### Princípios

1. **Janela primeiro, elementos depois.** Construtores só existem em handles (acima).
2. **Nada de navegador.** O módulo não embute WebView, não lê HTML, não executa JS.
3. **Nenhum erro silencioso** (Cap. 36). O CSS de navegador ignora propriedade desconhecida; o canvas não: propriedade desconhecida, valor inválido e recurso "ainda não suportado" são três erros distintos (Capítulo 53).
4. **Ler e gravar por propriedade.** `botao.text` lê; `botao.text = "x"` grava; `botao.update({"text": "x", "disabled": true})` grava várias de uma vez, tudo ou nada. Só é somente leitura o que é estado do motor (`id`, `kind`, `hovered`, `focused`…); gravar nele é `ReadOnlyProperty PROBLEM` (E313, já existente para `~Program`). Gravar valida na hora e nunca dispara evento de usuário.
5. **Subconjunto pequeno e fechado, que só cresce.** Tudo o que não está listado nesta versão é erro explícito (`UnsupportedStyleValue`), nunca comportamento improvisado.
6. **Unidades**: tamanhos em **pixels lógicos** (independentes de DPI), tempo em **segundos**, cores como `str`.
7. **Testável sem tela.** Estilo, layout e despacho de eventos rodam em janela `headless`, com `dispatch` e relógio virtual (`advance`): exemplos viram `tinypine run` + `output` (Capítulo 51).
8. **Defaults de CSS onde for possível.** `display: block`, `flex-direction: row`, `align-items: stretch`… seguem o CSS. Os desvios são poucos e listados (Capítulo 48).

### Modelo de execução

```
 programa TinyPine
    │ constrói / altera                         ▲ handlers  f(e)
    ▼                                           │
 árvore de elementos ─► estilo ─► layout ─► pintura ─► superfície da janela
    ▲                                                       │
    └──────── eventos (ponteiro, teclado, janela, frame) ◄──┘  sistema operacional
```

- **Estilo**: cascata (UA < folhas < `style()` inline), herança, resolução de unidades → valores em px. As gravações de propriedade (`el.text = …`) e `update` marcam o elemento como sujo; o motor refaz o que depende dele, no máximo uma vez por quadro.
- **Layout**: caixas posicionadas por *block*, *flex* ou *absolute*; texto é uma folha medida pelo motor de fonte.
- **Pintura**: lista de desenho (fundo → borda → filhos → texto), com recorte por `overflow`/`border-radius`.
- **Eventos**: o motor faz o *hit-test*, monta o caminho alvo → raiz e chama os handlers em captura → alvo → bolha.
- O motor só refaz estilo/layout/pintura do que mudou, no máximo uma vez por quadro.

### Organização

| **Capítulo** | **Conteúdo**                                                                                  |
|--------------|-----------------------------------------------------------------------------------------------|
| 43           | Visão geral (este capítulo)                                                                   |
| 44           | A janela: `canvas.window(...)`, propriedades, ciclo de vida, métodos                          |
| 45           | Elementos: tipos, árvore, `id`/`classes`, consulta, remoção                                   |
| 46           | Estilo: propriedades, unidades, cores, seletores, cascata, herança                            |
| 47           | CSS em texto: `w.css(texto)`                                                                  |
| 48           | Layout: modelo de caixa, *block*, *flex*, *absolute*, texto, pintura, `rect()`                |
| 49           | Eventos e laço: `run`/`poll`, tipos de evento, propagação, foco, *timers*                     |
| 50           | Entrada de texto: o evento `textinput`                                                        |
| 51           | Testes sem tela: `headless`, `dispatch`, `advance`                                            |
| 52           | Exemplos completos                                                                            |
| 53           | Erros e avisos do módulo (`E7xx`/`W7xx`)                                                      |

**Situação.** Os Capítulos 43 a 53 definem a interface do módulo, mas o interpretador de referência ainda **não o implementa**. Por isso os blocos com `output` desta parte são escritos como ```` ```tinypine ```` e ```` ```output ````, e **não** como ```` ```tinypine run ````: `tools/run_examples.py` não os executa, e as saídas são **previsões** (Apêndice A, B33). Os pontos em aberto do módulo estão no Apêndice A (B33 a B38). Os documentos de trabalho do módulo (arquitetura do motor, pesquisa, decisões e histórico) ficam em `docs/canvas/`, fora desta especificação.

### Fora desta versão

`display: grid`, `inline`, `transform`, `transition`/`animation`, gradientes e imagem de fundo, `box-shadow`, `outline`, texto rico (vários estilos num parágrafo), parser de HTML, texto CSS com `@…`, `url()`, `var()` e `calc()`, media queries, pseudo-elementos, pré-edição de IME, janelas modais ou filhas, elemento de desenho 2D (`surface`), controles novos (`checkbox`, `textarea`, `range`…), barras de rolagem visíveis e diálogos nativos. Pedir em estilo algo de CSS que está fora é `UnsupportedStyle` (E722), nunca comportamento improvisado. O que fica para depois está em Apêndice A, B38.
