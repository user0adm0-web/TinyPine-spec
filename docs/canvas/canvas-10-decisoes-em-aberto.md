# canvas — Decisões (v3)

> **RASCUNHO — não normativo.** Ver `canvas-00-visao-geral.md`.
> Pelo processo do projeto (ambiguidade = lista numerada, não preenchimento silencioso), toda escolha minha que você pode reverter está aqui. Cinco partes:
> **A.** o que você decidiu (v1/v2); **B.** o que a **spec atualizada** resolveu (D38, D39); **C.** as perguntas de `canvas-12` (**D40–D51**), que você **não anotou** — a v3 aplicou as recomendações ✔, **todas reversíveis**, e diz abaixo o que fez com cada uma; **D.** decisões **novas da v3** (D52–D58); **E.** as da v2 (D32–D37) e **F.** as da v1, com ajustes.
> Itens marcados **[spec]** tocam algo que a spec atual ainda não define ou define de outro jeito.

## A. Decididas por você (v1 → v2, sem mudança)

| **Item** | **Sua resposta** | **Situação na v3** |
|----------|------------------|--------------------|
| **D01** handles | "escolho (b)": propriedades graváveis | Mantida (`window`/`element`). Depende de D37 **[spec]**. |
| **D02** `update` | dict | Mantida. |
| **D03** estilo | dict | Mantida. Na v3 o `str` é CSS válido (D45) e há `w.css` (D43). |
| **D04** CSS em texto | "versão 3" | **Feito**: `canvas-13`. |
| **D05** unidades | `str` CSS | Mantida e **completada** (D45): a `str` é sempre CSS válido; atalhos por lista. |
| **D07** layout | "okay" | Mantida, **exceto uma** das seis simplificações, revogada por D49 (posição estática do absoluto). Avisei: você aprovou D07 com as seis. |
| **D10** colisões | "confirmo"; depois "me arrependi… '-' é melhor" | Hífen mantido (`min-width`, `on-top`, `scroll-x`). |
| **D23** tipos novos | "okay" | Mantida. |
| **(não é D)** | "já corrigi as coisas que impedião a v3" + o site publicado | A v3 foi feita sobre o `spec/` que você enviou (`c1e03f30-spec.zip`). Os rascunhos **não** estão no site (D50 ✔ já atendido por você). |

## B. Resolvidas pela spec atualizada

| **Item** | **O que a spec nova diz** | **O que a v3 fez** |
|----------|---------------------------|--------------------|
| **D38** interpolação | Cap. 20: "Strings formatadas (`format ""`) suportam interpolação" — **só `format`**. | Todo exemplo com `{…}` usa `format "…"` (`canvas-05`, `-06`, `-14`, `-15`). Texto CSS em string comum não precisa escapar `{ }` (`canvas-13`). |
| **D39** `const` e handles | Cap. 18.2: `const` impede a reatribuição **do identificador**. | Exemplos usam `const w`, `const botao`… e gravam propriedade (`botao.text = "x"`). **Contradição que continua**: o Cap. 19.5 diz que `const` não permite **mutação de conteúdo** (`B.add("C")` → `ImmutableMutation`), e o Cap. 19.4.2 diz o contrário (`A["x"] = 2` "válido"). Para handles, a v3 segue 18.2; onde um **dict** é mexido por dentro (`var s = caixa.style()`; `s["opacity"] = 0.5`), uso `var`, para não depender da contradição. **[spec]** |

## C. As perguntas de `canvas-12` (D40–D51) — você não anotou; a v3 aplicou ✔

| **Item** | **✔ aplicado** | **Onde** | **Estado** |
|----------|----------------|----------|------------|
| **D40** laço e testes | `run()` volta na hora sem janela real; `quit()` não consulta `close`; `headless` ganha `dispatch` e `canvas.advance`; `poll()` não dorme. Detalhes novos em D53. | `canvas-05`, `-14` | aplicado, reversível |
| **D41** `textinput` | evento novo com `e.text` composto; `e.char` **removido** de `keydown`. Detalhes em D58. **Falta confirmar** em teclado real como `ã`/`ç` chegam em cada sistema. | `canvas-05`, `-15` | aplicado; **hipótese a testar** |
| **D42** handlers 0 ou 1 parâmetro | `f()` e `f(e)` válidos; 2+ ou `package` → `E731`. | `canvas-05`, `-07`, `-06` (ex. 4) | aplicado, reversível |
| **D43** escopo do `w.css` | `w.css(texto, "source")` → `sheet`, estrito, sem forma por caminho, `E723`. Detalhes em D54. | `canvas-13` | aplicado, reversível |
| **D44** literais cruos/multilinha | **Não aplicado**: é decisão da **linguagem** ([spec]). O `w.css` não depende (arquivo ou uma linha). `"""…"""` aparece só como exemplo marcado "ainda não vale". | `canvas-13` | **aberta** |
| **D45** `str` é CSS válido; atalhos por lista | aplicado: `"padding": [8, 16]`; `"8 16"` agora é `E721`; unidade obrigatória em `str`, `0` dispensa. | `canvas-03`, `-04`, `-06`, `-13` | aplicado, reversível |
| **D46** `surface` × `pen`/`scene` | **Não tratado**: você mandou ignorar `pen`/`scene`; sem resposta, o canvas segue **só interface** (✔), sem `surface`. | — | **aberta** |
| **D47** ordem da etapa 3 | **Não feita**: a etapa 3 (controles, `outline`, diálogos…) fica para a v4. | `canvas-00` | **aberta** |
| **D48** v2.1 antes da v3 | **Superada**: você pediu a v3; a v3 já inclui a etapa 0 (F1–F8, 4.A). | `canvas-16` | decidida pelo seu pedido |
| **D49** posição estática do absoluto | aplicado: como no CSS (em flex, "como se fosse o único item"). **Revoga uma simplificação de D07** (que você aprovou). | `canvas-04` | aplicado, reversível |
| **D50** onde moram rascunhos e testes | você já os mantém fora de `spec/` (site publicado sem eles). Exemplos executáveis seguiriam para `tests/exemplos/` — **não mexi** em nada do repositório. | — | atendida por você |
| **D51** caminhos relativos | aplicado para o canvas: relativo ao `.tpine` em execução (`~Program.path`). **O `os.read` é decisão do módulo `os`**, que não li em detalhe. | `canvas-01`, `-13` | aplicado; parte aberta |

## D. Decisões novas da v3 (D52–D58) — todas com ✔ aplicado

**D52 — Casos de despacho e foco que estavam indefinidos (4.A de `canvas-12`).**
✔ (1) o **caminho do evento é fixado no início** do despacho, e handlers de elementos já no caminho **ainda rodam** naquele evento mesmo que um handler os remova; (2) `off()` vale **na hora** (um ouvinte removido não é chamado nem no evento em curso); (3) `on` durante o despacho só vale no **próximo** evento; (4) `once` remove **antes** de chamar o handler; (5) `el.focus()` em elemento **não focável** não muda o foco e emite **`W705 NotFocusable`**; (6) ao fechar a **última** janela, todo `timer` pendente vira `active == false`; (7) `scroll-x`/`scroll-y` sem `overflow: scroll|auto` → `W701` (M7). Tudo como o DOM, exceto (5)–(7), que são avisos do canvas.
Alternativa: deixar indefinido (não recomendado: cada um vira bug sutil). Impacto: `canvas-05`, `-02`, `-04`, `-07`.

**D53 — Detalhes de `dispatch`, `advance`, `poll` e `quit` (completa D40).**
✔ (1) `dispatch` é **síncrono** (como `dispatchEvent`) e devolve `bool` (`false` se um handler cancelou um evento cancelável) — **mudei** o que `canvas-12` descrevia ("enfileirado e processado pelo `poll`"), porque um teste de uma linha só é previsível se o evento já foi tratado quando a chamada volta; (2) `w.dispatch` de ponteiro faz *hit-test* em `(x, y)`; de teclado vai ao focado; `el.dispatch` vai ao elemento; (3) um evento por chamada (`click` não gera `pointerdown`/`pointerup`; `keydown` não gera `textinput`); (4) `advance(s)` roda `after`/`every` vencidos em ordem e entrega **um** `frame` com `dt = s`; `poll()` em `headless` ≡ `advance(0)`; (5) `dispatch`/`advance` com janela real aberta → `E734`; dados inválidos → `E735`; (6) `quit()` entrega `close` **como aviso não cancelável** (`canvas-12` dizia só "sem consultar"; a notificação para limpeza é acréscimo meu).
Alternativas: `dispatch` enfileirado; `quit()` sem entregar `close`. Impacto: `canvas-14`, `-05`, `-07`.

**D54 — Detalhes do `w.css`.**
✔ (1) **tudo ou nada** (valida o texto inteiro antes de registrar); (2) propriedades e palavras-chave em **minúsculas** (`Color` → E720 com dica), como o dict; (3) o último `;` do bloco é opcional; (4) comentários `/* */` fora de string; (5) `"source"` padrão `"<css>"`; (6) texto vazio é folha vazia, sem erro; (7) o erro aponta linha e colunas **dentro do texto** (**[spec]**, Cap. 36.7: hoje só descreve arquivos `.tpine`). Alternativa para (2): aceitar maiúsculas como o CSS de navegador (não recomendado: um jeito só de escrever).
Impacto: `canvas-13`, `-07`.

**D55 — `font-family` como lista.**
✔ `"font-family": ["Segoe UI", "sans"]` (família preferida, depois alternativas) e, em CSS texto, `font-family: sans, monospace`. Um `str` único continua valendo. Já aplicado em `canvas-03`; em D45 a lista é o mesmo mecanismo dos atalhos.

**D56 — `el.computed(nome)`.**
✔ devolve o valor **resolvido**: comprimentos como `float` em px; `auto` dá o valor **usado** (força o layout, como `rect()`); cores em `"#rrggbb"`/`"#rrggbbaa"`; palavra-chave como `str`; número puro como `num`; `display: none` → tamanhos `0.0`. Erro: E720 (nome), E722 (fora do v1). Pergunta aberta dentro dele: normalizar cores (`"red"` → `"#ff0000"`) ou devolver como escrito? ✔ normalizar (comparável). Impacto: `canvas-03`.

**D57 — Impressão de `dict`. [spec]**
Não achei na spec o formato de `println` de um dict (F5). ✔ a v3 **evita** (imprime campo a campo). Se você definir (provavelmente `{"x": 0.0, …}` em ordem de inserção, Cap. 19.1), os exemplos podem voltar a `println(r.rect())`.

**D58 — `textinput`: regras (completa D41).**
✔ (1) `e.text` nunca vazio e **sem caractere de controle** (Enter/Tab/Backspace são `keydown`); (2) pode ter **mais de um caractere**; (3) `e.prevent()` num `keydown` suprime o `textinput` da tecla; no `textinput`, só a inserção; (4) `dispatch("keydown")` não sintetiza `textinput`; (5) `e.char` removido (**mudança incompatível com a v2**, tabela de migração em `canvas-15`); (6) sem seleção/colar/pré-edição de IME no v1.
Alternativa: manter `e.char` em `keydown` **além** de `textinput` (dois jeitos; não recomendado). Impacto: `canvas-05`, `-15`.

## E. Decisões da v2 (consequências de D01 e D02) — seguem como estavam

*(D32–D36 você não anotou; seguem valendo as recomendações. **D37 continua em aberto** e é a condição para D01-b funcionar de verdade. Textos inalterados da v2, salvo nota.)*

**D32 — Gravar em membro que não existe: que erro?**
✔ **`UnknownAttribute` (E716)**, novo, com *did you mean* e a lista de atributos do tipo — vale para `el.valor = "x"` e para a chave desconhecida de `update({...})`. **Ler** o mesmo nome continua `IdNotFound` (E308, já existente).
Alternativas: (a) reaproveitar `IdNotFound` (E308) também na gravação — um erro a menos, mas a mensagem "não encontrado" descreve mal "tentou criar atributo novo"; (b) deixar gravar e criar o membro (como num dict) — **não recomendado**: `botao.txet = "x"` seria um erro silencioso, o contrário do Cap. 36.
Impacto: `canvas-07` ganha E716.

**D33 — Nomes de atributo com hífen. (decidida por você: hífen; reverte parte de D10)**
✔ **Com hífen**, como no CSS e como `to-int`: `min-width`, `min-height`, `max-width`, `max-height`, `on-top` (janela) e `scroll-x`, `scroll-y` (elemento) — **o mesmo nome** nas **propriedades** (`w.min-width = 100`), nas **chaves de `update`** (`{"min-width": 100}`) e nos **parâmetros de `canvas.window`** (`"min-width": 100` ou `min-width=100`, Cap. 30.3). Isso volta aos nomes da v1; a v2 tinha trocado por `min_width` etc. por causa do D10 que você confirmou e agora reverteu. Os nomes de **estilo** (`"font-size"`) já tinham hífen.
Custo que fica (não é erro, é cuidado): em conta aritmética, escreva **com espaços** — `w.width - 10` é subtração; `w.width-10` colado segue o Cap. 3.4.1 (número depois do `-` não continua o nome, e `a-b` colado com os dois lados variáveis é erro do parser), mas ler isso exige saber a regra. Vale a pena um aviso no `check`/análise estática para `membro-membro` colado? **[spec]** — pergunta aberta, não pedida.
Correção da v1 mantida: eu havia escrito que `"min-width"` "não é identificador válido" para `nome=valor`; **estava errado** (Cap. 3.4.1), e agora a forma `min-width=100` vale e está documentada.
Alternativas que descartei por sua escolha: `min_width` (a v2 inicial), agrupar em dicts (`w.min_size = {...}`) ou `minwidth`.
Impacto: `canvas-01`, `canvas-02`, `canvas-04`, `canvas-07`.

**D34 — `style` e `classes` com propriedades graváveis.**
✔ (1) **`style` é método** (`el.style({...})` mescla; `el.style()` devolve cópia), **não** propriedade, porque "mesclar" e "substituir" são operações diferentes e `el.style = {...}` só diria uma; atribuir a `style` é `ReadOnlyProperty` (E313) com dica. (2) **`classes` é propriedade**: lê uma **tupla** imutável (assim `el.classes.add("x")` falha com `ImmutableMutation`, Cap. 19.5, em vez de alterar uma cópia em silêncio) e, ao gravar, **troca todas** (aceita lista ou tupla). (3) `toggle`/`has` **ficam** por conveniência (mexer numa classe só).
Alternativas: (a) `style` também propriedade — gravar **substitui** o estilo inline inteiro, e a mesclagem vira `el.style = {**atual, ...}` (a spec descreve `unpack` de dict de forma ambígua, Cap. 19.4) ou um método à parte (`el.restyle`); (b) `classes` devolver `list` (cópia): `el.classes.add("x")` funcionaria e **não** mudaria o elemento — erro silencioso; (c) remover `toggle`/`has` (a v1 os justificava por a lista ser cópia; com tupla imutável e atribuição, sobra só a conveniência).
**[spec]** (2) assume que uma propriedade pode devolver `tuple` e que `ImmutableMutation` vale para ela.

**D35 — Semântica de gravar.**
✔ (1) valida **na hora**, na linha do `=` (E716/E313/E302/erro do próprio atributo); (2) o efeito aparece no **próximo quadro**, mas **ler de volta devolve o valor novo imediatamente**; (3) gravar **nunca dispara evento de usuário** (`input`, `change`, `click`…), como no DOM; só o que o sistema reporta (`resize`, `move`); (4) gravar valor igual não faz nada; (5) em handle obsoleto (janela fechada, elemento removido), gravar é `StaleHandle` (E706) e ler continua valendo; (6) `update` aplica as mesmas regras a um grupo, **tudo ou nada**.
Abertos dentro dele: (a) **tamanho e posição da janela** são *pedidos* ao sistema, que pode ajustar: logo após `w.width = 5000`, `w.width` devolve 5000 (pedido) ou o último valor real? ✔ o pedido, corrigido quando o evento `resize` chegar — mais simples de programar, mas pode mentir por um quadro; (b) **`\n` gravado em `value` de um `input`** (campo de uma linha): erro, trocar por espaço ou aceitar e mostrar numa linha? ✔ erro (sem alteração silenciosa); **não decidido nos rascunhos** (hoje indefinido no v1); (c) gravar durante a propagação de um evento (handler troca `el.text` de um elemento do caminho): vale na hora para leitura, e o quadro sai depois do handler.

**D36 — `show()`/`hide()` da janela.**
✔ **Removidos**: `w.visible = true/false` (propriedade gravável) faz o mesmo, e `maximized`/`fullscreen` já eram estado. `w.focus()` e `w.close()` ficam porque são **ações**, não estado.
Alternativa: manter `show()`/`hide()` como açúcar sobre `visible` — dois jeitos de fazer a mesma coisa (preferência minha por um só; não é uma regra que eu tenha achado na spec).
Impacto: `canvas-01`.

**D37 — Atribuição a membro de objeto nativo que executa código. [spec]**
✔ A linguagem passa a aceitar que, para objetos **nativos** (`window`, `element`), `obj.nome = valor` chame o motor (um *setter*), com tabela de atributos por tipo (nome, tipo, gravável?, validador). Hoje a spec só define `=` como "vincula um valor a um identificador" (Cap. 14); `Y.A = 5` em `load` (29.5) é variável comum, e `~Program` (29.4) é o contraexemplo: tudo somente leitura, `E313`. A v2 assume: (1) `E313` passa a cobrir membros somente leitura de **qualquer** objeto nativo (o catálogo diz só `~Program`); (2) `E716` é novo; (3) `update` é função nativa comum (não precisa mais inspecionar argumentos, ao contrário da v1).
Pergunta de fundo: o mesmo mecanismo vale para **classes do usuário** (Cap. 32)? Hoje o capítulo não mostra atribuição de fora (`p.nome = x`) nem *setters*; se virar regra geral, o `canvas` é só um caso. ✔ para o canvas só (objetos nativos); classes ficam para quando o Cap. 40 (Sistema de Objetos) for fechado.
Impacto: `canvas-08` (ponte com o interpretador).

## F. Decisões da v1 que seguem como estavam (com os ajustes da v3)

### C.1 Estilo e layout

**D06 — `box-sizing`.** ✔ padrão `border-box` (desvio do CSS). Alternativa: `content-box` como o CSS — "mais fiel", mas `width: 200` + `padding` deixa de medir 200.

**D08 — Padrões de janela e do canvas.** ✔ janela `black`, `color: white`; folha padrão mínima e **visível** para `button` e `input` (`canvas-03`). Alternativa (RmlUi): nenhum estilo padrão — mais "puro", mas uma janela com um `button` mostraria um botão invisível.

**D09 — Estilo inválido.** ✔ três erros distintos (E720 desconhecida / E721 valor inválido / E722 não suportado) e um aviso (W701 sem efeito). Alternativa: tudo aviso, ou ignorar como o CSS. Contraria o Cap. 36.

**D18 — Fontes.** ✔ famílias genéricas `"sans"`, `"serif"`, `"mono"` mais famílias instaladas; fonte padrão **embutida** (Windows e Linux dão tamanhos diferentes de texto sem isso); `W703 FontFallback`. Aberto: carregar fonte de arquivo (`canvas.font("name": …, "path": …)`?), e qual fonte embutir (licença).

**D19 — Imagens.** ✔ PNG e JPEG, carga síncrona (`E714` se falhar); SVG, GIF animado, carga assíncrona e `object-fit` depois.

**D21 — DPI e coordenadas.** ✔ tudo em px lógicos; `w.scale` só leitura; arredondamento na pintura, `rect()` sem arredondar. Aberto: permitir forçar a escala por janela.

**D26 — Seletores v1.** ✔ tipo, `*`, `#id`, `.classe`, composto, descendente, filho, lista, `:hover :active :focus :disabled`. Fora: atributo, irmãos, estruturais, pseudo-elementos.

**D27 — Fora do v1.** ✔ `grid`, `inline`, `transform`, `transition`/`animation`, gradiente e imagem de fundo, `box-shadow`, `outline`, `calc()`, `var()`, `@media`, `@font-face`, `text-decoration`, `align-content` (comportamento padrão sim, propriedade não), `pointer-events`, `position: fixed/sticky`, texto rico, RTL/bidi, `select`/`textarea`/`checkbox`/listas/tabelas/vídeo, **elemento de desenho 2D (`surface`)**, parser de HTML (`w.html("…")`), **texto CSS com `@…`/`url()`/`var()`/`calc()` (o `w.css` simples existe na v3, `canvas-13`)**, janelas modais/filhas. Observação: para jogos (Signal Lost, Célula Primordial…), `surface` provavelmente é o próximo passo natural; foi deixado de fora para não misturar dois modelos (árvore de elementos × pintura imediata) no v1.

**D31 — Rolagem.** ✔ `overflow: scroll|auto` + roda do mouse/teclado; `el.scroll-x` / `el.scroll-y` são propriedades graváveis (v2; na v1 era o método `el.scroll(...)`, que pelo D01/D02 deixou de combinar com o resto); `e.dx/e.dy` em px lógicos. Aberto: barras de rolagem visíveis e arrastáveis (v1: só indicador), rolagem suave.


### C.2 Eventos e laço

**D11 — Laço.** ✔ `canvas.run()` (bloqueante; **volta na hora** sem janela real aberta — D40) **e** `canvas.poll("wait": s)` (laço do programa); handlers síncronos; `E732` se reentrar; `W702` se um handler passar de 0,1 s (limite provisório). `async`/`thread` (Cap. 42) fora do v1 **[spec]**: uma `f async` como handler seria o caminho natural quando houver runtime.

**D12 — Relógio.** ✔ `canvas.after/every` em **segundos** com `timer.cancel()`; `every` não acumula atraso. Alternativa: só o evento `frame` + o programa conta o tempo — mais simples, pior para quem só quer "daqui a 2 s".

**D13 — `frame`.** ✔ evento da janela com `e.dt` (segundos), um por quadro apresentado. Alternativa: `canvas.every(1/60, …)`; perde a sincronia com a tela.

**D14 — Propagação.** ✔ DOM: captura → alvo → bolha; `stop()`, `stop("immediate": true)`, `prevent()`; `focus`/`blur`/`pointerenter`/`pointerleave` não sobem. Sem `passive` e sem `focusin/focusout` (use captura no ancestral).

**D15 — `on` devolve `listener` com `off()`.** ✔ porque comparar funções para remover é ambíguo (`is` entre duas funções é sempre verdadeiro, Cap. 6.7). Alternativa: `off(tipo, handler)` exigiria definir igualdade de função **[spec]**.

**D16 — Erro dentro de handler.** ✔ sobe até `run()`/`poll()`; sem `try`, encerra o programa com o bloco padrão e o handler na pilha. Alternativas: capturar, imprimir e **continuar** (pior: esconde bugs), ou fechar só aquela janela.

**D17 — Teclas.** ✔ os nomes de `computer.keyboard` (Cap. 34.7) + modificadores (**v3: `e.char` saiu**; o texto vem de `textinput`, D41/D58), incluindo `meta` (que a tabela do 34.7 **não** tem: acrescentar lá ou omitir aqui) **[spec]**.

**D24 — Várias janelas.** ✔ independentes (cada uma com árvore, folhas e eventos próprios); filhas/modais fora do v1. Aberto: janela-pai (`"parent"`), diálogo modal, posição relativa ao pai.

**D25 — Encerramento.** ✔ `run()` volta quando a última janela fecha; `close` é cancelável; `w.close()` também dispara `close` e devolve `false` se cancelado; **`canvas.quit()` não consulta** (entrega `close` como aviso não cancelável; D40/D53). Aberto: se `close()` programático deveria poder ser cancelado (no navegador, `window.close()` não passa por `beforeunload`).


### C.3 Outros

**D20 — `headless` e `capture`.** ✔ `"headless": true` roda estilo/layout/pintura em memória; `w.capture(caminho)` salva PNG; os exemplos da spec podem usar `rect()` como saída determinística (`canvas-06`, ex. 5) e, na v3, **eventos por `dispatch`** e relógio virtual (`canvas-14`). Aberto: a fonte embutida precisa ser fixa para o resultado de `text` ser reproduzível — **bloqueia** testes com `rect()` de texto.

**D22 — Acessibilidade.** ✔ papel por tipo + `label` já no modelo; ponte com leitores de tela depois (AccessKit é um exemplo de camada pronta). Custo no v1: só o atributo e o papel.

**D28 — Edição de texto do `input`.** ✔ v1: uma linha, cursor, seleção por teclado, copiar/colar via área de transferência do sistema, `password`. **v3:** a inserção de texto é por **`textinput`** (D41); o texto colado também chega como um `textinput`. Sem **pré-edição** de IME (japonês/chinês/coreano) e sem texto bidirecional — **isso exclui alguns idiomas**, a confirmar se é aceitável. Texto **composto** (acento + letra, `ç`, `ã`) **é** coberto por `textinput`.

**D29 — Códigos de erro.** ✔ `E701–E735` (v2: `E716`; v3: `E723`, `E734`, `E735`) e `W701–W705` (v3: `W705`) provisórios (`canvas-07`); só valem se a faixa `E7xx` ficar reservada ao canvas (conferido na spec atualizada: livre).

**D30 — Função anônima que atribui a variável de fora.** **[spec]** O Cap. 31.3 diz que funções guardadas "só enxergam o escopo onde foram escritas", mas não diz se podem **atribuir** a uma variável desse escopo. **Na v3 nenhum exemplo depende disso**: o estado compartilhado entre handlers é `var $global` (Cap. 18) e o resto fica no próprio elemento. Continua aberta, e atribuir a **global** de dentro de função anônima também é suposição (Cap. 18 não fala de funções anônimas).

## Resumo: o que eu preciso de você para fechar

1. **D37** continua sendo a condição para D01-b: o interpretador aceita *setters* em objetos nativos? E **D39/Cap. 19.5** (a contradição sobre `const` e conteúdo, que não é do canvas).
2. **D41**: testar `ã`/`ç` num teclado ABNT2 real antes de aceitar o `textinput` (hipótese, `canvas-15`).
3. **D44** (literais `"""…"""`/`r"…"`) e **D57** (impressão de dict): são da linguagem.
4. **D46** (`surface`), **D47** (ordem da etapa 3): abrem a v4. **D18** (fonte embutida) bloqueia testes com `rect()` de texto.
5. Se algum ✔ aplicado (D40–D45, D49, D51–D58) **não** serve, diga o número: cada um está isolado em poucos arquivos (`canvas-16`).
