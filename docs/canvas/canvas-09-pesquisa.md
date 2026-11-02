# canvas — Pesquisa: HTML e CSS sem navegador

> **RASCUNHO — não normativo.** Ver `canvas-00-visao-geral.md`.
> **v2:** não houve pesquisa nova na web. O que a v2 consultou foi a própria spec (no repositório do usuário, `git show HEAD:spec/…`): Cap. 3.4 (identificadores aceitam `-` e `_`), 14 (atribuição), 18/19.5 (`const`, tuplas imutáveis, `ImmutableMutation`), 29.4–29.5 (`~Program`, `load … as`), 30.3 (`nome=valor`) e 32 (classes). As seções abaixo são as da v1, sem alteração.
> **v3:** pesquisa **pontual** (só o que as decisões da v3 pediam), feita ao preparar a v3 e ao escrevê-la: **(1)** CSS Flexbox, rascunho do editor — mínimo automático do item, `flex-shrink` ponderado, margens e `%`, `align-content`, posição estática de filho absoluto num contêiner flex (fonte: `css-flexbox-1/Overview.bs`, em `w3c/csswg-drafts`, lido no GitHub, porque a página TR veio truncada); **(2)** CSS Syntax 3, rascunho do editor — o texto do próprio documento permite abortar no primeiro erro (linha 288 do arquivo lido), base do `w.css` estrito; **(3)** `winit::event::Ime` e `winit::event::KeyEvent` — texto da tecla (`text`) separado da tecla lógica (`logical_key`, que pode ser *Dead*), possível texto de dois caracteres no Windows com tecla morta, e `Ime::Commit` como evento de texto composto. **Não** pesquisei de novo os outros motores. **Não** verificado: como Linux/macOS entregam `ã`/`ç` (`canvas-15`). Fontes no fim.
> Pesquisa feita em 22/10/2026 com busca na web e leitura das páginas listadas. Os resumos abaixo vêm da leitura dessas páginas; onde a página não dizia algo, está escrito.

## A pergunta

Que partes de HTML e CSS existem **como modelo** (independentes de um navegador), e que projetos já as usaram sem navegador? A resposta orienta o que o `canvas` copia, simplifica e recusa.

## Projetos que reusam o modelo HTML/CSS sem ser um navegador

| **Projeto**       | **O que é**                                                                                                  | **O que ensina ao canvas**                                                                                          |
|-------------------|--------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| **Taffy** (Rust)  | Biblioteca de **layout**: implementa *Block*, *Flexbox* e *Grid* do CSS. Cada nó tem um `Style` (entrada) e produz um `Layout` (x, y, largura, altura). Folhas (texto, imagem) entram por uma **função de medida** fornecida pelo usuário. Tem API de alto nível (guarda a árvore e o cache) e de baixo nível (o usuário guarda a árvore). Oferece um passo de arredondamento para a grade de pixels. | **Layout é separável** de texto e de pintura. Estilo tipado como entrada, retângulos como saída. A folha é "medida", não "desenhada" pelo layout. |
| **Yoga** (Meta)   | Motor de layout *flexbox* multiplataforma, nascido do `css-layout` do React Native; núcleo em C, ligações para Java, Objective-C e C#. Mede rótulos o menor número de vezes possível; relayout só do que mudou. | **Só flexbox já cobre quase toda interface.** Relayout incremental. Existe ligação C#.                              |
| **RmlUi** (C++)   | Biblioteca de UI "baseada em HTML e CSS": XHTML1 + CSS2 + partes do CSS3 (flexbox, animações, transformações, *media queries*…), com **layout próprio**. Não é compatível por completo — prefere leveza e desempenho; documentos são escritos *para* o RmlUi. Tem DOM, eventos, *data bindings*. Não desenha: o aplicativo implementa uma **render interface**, uma **system interface** (janela, área de transferência, DPI, IME) e uma **font interface**. O aplicativo controla o laço: a biblioteca só roda quando chamada. Não define estilos padrão. | **Subconjunto é legítimo.** Separar render/system/font. **Laço controlado pelo aplicativo** → `canvas.poll()`. Ponto contrário: o canvas **define** estilos padrão (D08). |
| **litehtml** (C++)| Motor leve de HTML/CSS2/3: lê HTML (com o *gumbo-parser*) e **posiciona** os elementos, mas não desenha texto nem imagens e não depende de biblioteca de fontes ou gráficos; o hospedeiro implementa um `document_container`. Não é totalmente compatível com os padrões. | O contrato "motor posiciona, hospedeiro mede e desenha" funciona em produção. (Página lida: README de um *fork*.)       |
| **Blitz** (Rust)  | "Motor de renderização HTML/CSS modular, alternativa leve aos navegadores": `blitz-dom` (DOM *headless* que faz CSS, layout e eventos), `blitz-html` (parser), um renderizador (Vello), `blitz-shell` (janelas) e rede opcional. Interatividade vem do Dioxus; acessibilidade, do AccessKit. | **DOM headless + renderizador + shell** como peças trocáveis. Acessibilidade como camada à parte. |
| **Sciter** / **Sciter.Lite** | Motor de UI embutível com HTML, CSS e script. A versão Lite não usa *handles* de janela do SO: o hospedeiro fornece a superfície, com a mesma API. CSS serve de tema por plataforma. | Separar **dono da janela** de **motor** dá o modo embutido/headless. |

## CSS fora da web (nos *toolkits*)

| **Toolkit**                | **O que adaptou**                                                                                                                                          | **O que ensina ao canvas**                                                                                          |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| **Qt Style Sheets (QSS)**  | Seletores: universal, **tipo**, propriedade, classe, id, descendente, filho; pseudo-estados (`:hover`, `:pressed`…) e subcontroles; especificidade como no CSS 2; **sem `!important`**; a folha do próprio elemento vence a herdada. Por padrão **não** herda fonte/cor dos pais. | CSS é adaptável a controles nativos; o **tipo do controle** serve de seletor de tipo; abrir mão de `!important`. (O canvas **herda** `color` e fontes, como a web.) |
| **JavaFX CSS**             | Mantém a sintaxe do CSS, prefixa propriedades próprias com `-fx-`; cada nó tem `styleClass` e `id`; seletor de tipo = nome do tipo do nó; unidade padrão `px`; pseudo-classes `hover`, `pressed`, `focused`, `disabled`; **descarta** pseudo-classes estruturais e *media queries*; precedência: padrão do toolkit < código < folhas < `setStyle` inline. | O conjunto de pseudo-classes do v1 e a ordem da cascata; o `px` como unidade padrão. O prefixo `-fx-` não é necessário aqui: as propriedades do canvas **são** CSS. |

## Janelas, acessibilidade e eventos

| **Fonte**                         | **O que a página diz**                                                                                                                                       | **Uso no canvas**                                                       |
|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| **winit** (`WindowAttributes`)    | Atributos de uma janela nativa: `title`, `inner_size`, `min/max_inner_size`, `position`, `resizable`, `decorations`, `maximized`, `fullscreen`, `visible`, `transparent`, `blur`, `window_level`, `window_icon`, `preferred_theme`, `active`, `cursor`…; a maioria tem um `set_*` para mudar depois. | Base dos parâmetros de `canvas.window` (`canvas-01`), com nomes mais simples (`frame` em vez de `decorations`). |
| **AccessKit**                     | Infraestrutura de acessibilidade para *toolkits*: a interface é uma **árvore de nós**, cada um com **id inteiro**, papel e atributos; ações pedidas pelas tecnologias assistivas voltam ao *toolkit*; envia a árvore inteira e depois **atualizações incrementais**. Windows (UIA), macOS, iOS, Android, Linux (AT-SPI). | Por isso todo elemento tem papel derivado do tipo e `label`; o `id` estável já existe (D22). |
| **DOM — eventos** (WHATWG)        | Caminho do alvo à raiz; fases de **captura**, **alvo** e **bolha**; `stopPropagation`, `stopImmediatePropagation`, `preventDefault` (só se `cancelable`); `bubbles`; `target` × `currentTarget`; opções `capture`, `once`, `passive` ao registrar. | O modelo de eventos de `canvas-05`. `passive` não foi adotado (não há rolagem assíncrona no v1). |
| **CSS Box Model Level 3** (W3C)   | Caixas de conteúdo, preenchimento, borda e margem; margens podem ser negativas, preenchimento não; margens adjacentes podem colapsar; margens são sempre transparentes; o módulo **não** define `box-sizing` nem as bordas. | O modelo de caixa de `canvas-04`.                                       |
| **CSS Flexbox Level 1** (W3C)     | Contêiner/itens flex; eixo principal e cruzado; `flex-direction`, `flex-wrap`, `order`, alinhamento, `flex` (grow/shrink/basis), margens `auto`; algoritmo em 9 passos. A leitura da página trouxe **só o índice e os exemplos**, não as definições completas. | O conjunto de propriedades de flex do v1; o texto dos passos em `canvas-04` é o resumo do algoritmo conhecido, não uma citação. |

## O que a pesquisa mudou no desenho

1. **Núcleo separado do SO**, com interfaces de render/janela/fonte → `canvas-08` e o modo `headless`.
2. **Subconjunto fechado e declarado** (RmlUi, JavaFX): o v1 não promete "CSS", promete uma lista.
3. **Folhas medidas, não desenhadas pelo layout** (Taffy, litehtml): o `text` é uma folha de bloco; o fluxo *inline* fica de fora (D07).
4. **Laço do aplicativo** (RmlUi): além de `run()`, `poll()` (D11).
5. **Seletor de tipo = tipo do elemento**, sem `!important`, pseudo-classes mínimas (Qt, JavaFX).
6. **Acessibilidade como modelo desde o início**, ponte depois (AccessKit): papéis e `label` já no v1.
7. **Janela**: o conjunto de atributos vem do `WindowAttributes` do winit (lido); nomes como `frame` seguem o hábito de outros toolkits (conhecimento geral, não pesquisado).

## O que **não** foi verificado

- Detalhes do Taffy e do Yoga além do que as páginas lidas dizem (por exemplo, a forma exata da função de medida e se ela recebe espaço *min-content/max-content*): `canvas-04` e `canvas-08` descrevem as "três perguntas de medida" como **conhecimento geral** sobre layout flex, não como citação do Taffy.
- O algoritmo flexbox completo, a ordem de empilhamento do CSS e os valores iniciais das propriedades: escritos de **conhecimento geral** do CSS; a página do W3C lida só trouxe o índice. Devem ser conferidos contra a especificação e contra testes de referência antes de o v1 ser fechado.
- Os resumos de página vieram de leitura automática; a página do JavaFX foi lida só até os primeiros ~100 mil caracteres; a do litehtml é o README de um *fork*, não do projeto original.
- Nomes de bibliotecas sugeridos em `canvas-08` (Avalonia, SDL/GLFW, SkiaSharp, HarfBuzz) **não** foram pesquisados.
- Nada foi testado: não há código nem protótipo, só rascunho de design.

## Fontes

- Taffy — <https://docs.rs/taffy/latest/taffy>
- Yoga — <https://engineering.fb.com/2016/12/07/android/yoga-a-cross-platform-layout-engine/>
- RmlUi — <https://github.com/mikke89/RmlUi/blob/master/readme.md>
- litehtml (README de um fork) — <https://github.com/Arkarit/litehtml/blob/master/README.md>
- Blitz (documentação via docsearch) — <https://docsearch.algolia.com/mcp/docs/repo/dioxuslabs/blitz>
- Sciter e Sciter.Lite — <https://terrainformatica.com/2019/11/20/sciter-and-sciter-lite-universal-ui-solution/>
- Qt Style Sheets — <https://doc.qt.io/QT-6/stylesheet-syntax.html>
- JavaFX CSS Reference Guide — <https://docs.Oracle.com/javase/8/javafx/api/javafx/scene/doc-files/cssref.html>
- winit `WindowAttributes` — <https://doc.servo.org/winit/window/struct.WindowAttributes.html>
- AccessKit — <https://github.com/AccessKit/accesskit>
- DOM Standard, eventos — <https://dom.spec.whatwg.org/#events>
- CSS Box Model Module Level 3 — <https://www.w3.org/TR/2024/REC-css-box-3-20240411/>
- CSS Flexible Box Layout Module Level 1 — <https://www.w3.org/TR/css-flexbox-1/>
- (v3) CSS Flexible Box Layout, rascunho do editor — <https://github.com/w3c/csswg-drafts/blob/main/css-flexbox-1/Overview.bs>
- (v3) CSS Syntax Module Level 3, rascunho do editor — <https://github.com/w3c/csswg-drafts/blob/main/css-syntax-3/Overview.bs>
- (v3) winit, `event::Ime` — <https://doc.servo.org/winit/event/enum.Ime.html>
- (v3) winit, `event::KeyEvent` — <https://doc.servo.org/winit/event/struct.KeyEvent.html>
- Artigo sobre motores "seletivos" (opinião, fonte fraca; só contexto) — <https://dev.to/hejhdiss/rethinking-embedded-web-frameworks-the-smart-selective-engine-developers-actually-need-583p>
