# canvas — Análise da v2 e preparação da v3

> **RASCUNHO — não normativo.** Arquivo independente, ao lado de `canvas-00` a `canvas-11` (v2). **Não é a v3**: nenhum arquivo da v2 foi alterado. É o que precisa estar decidido e verificado **antes** de escrever a v3.
> Pelo processo do projeto (ambiguidade = lista numerada, não preenchimento silencioso), os pontos que dependem de você estão na seção 8 (D38 em diante, com recomendação ✔). Os que mexem na spec estão marcados **[spec]**.
> Nada aqui foi executado: continua não existindo interpretador do canvas.

## 1. Veredito

1. A v2 está **coerente por dentro** (as referências D/E fecham; o `check.py` do repositório passa), mas **tem 8 defeitos objetivos** (seção 3) — dois deles vêm de a spec do TinyPine se contradizer, não de erro de desenho.
2. **O achado mais importante é sobre strings**: a spec usa `format "…{x}…"` em quase todos os exemplos de interpolação, mas o texto do Cap. 20 diz que *toda* string interpola. Se só `format` interpola, **o problema que adiou o `w.css` (D04) desaparece em parte** e 4 exemplos meus estão errados (seção 3, F1; seção 7).
3. Para o **`w.css`** (sua decisão D04 → v3) há um caminho que **já funciona hoje, sem mudar a spec**: `w.css(os.read("tema.css"))`. O CSS vira um valor `str` lido de arquivo, e `{ }` só interpola em **literais**. O que exige spec é escrever CSS **literal multilinha** dentro do `.tpine` (seção 7).
4. O que **falta** na v2 está em três grupos: comportamento indefinido (seção 4.A), **teste de interface sem tela** (4.B) e **entrada de texto** com teclas mortas (`ç`, `ã`) (4.C). Recursos novos (controles, `surface`…) vêm depois (4.D), e `surface` depende de uma pergunta sobre `pen`/`scene` que você me mandou ignorar.
5. **Escopo proposto da v3** em quatro etapas (seção 6): fechar o que está indefinido → decidir os pontos de spec → `w.css` + entrada de texto + harness de teste → recursos que você escolher.
6. Para destravar: responda primeiro **D38, D39, D43, D41 e D46** (seção 8).

## 2. O que eu verifiquei, e contra quê

| **Verificação**                                                                                  | **Fonte**                                           | **Resultado** |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------|---------------|
| Corpo de função anônima por indentação dentro de `( )` (todos os exemplos de handler)            | spec Cap. 4.11, 31; `gramatica.ebnf` (`AnonFunc`)    | ✔ conforme, **exceto** a linha `f(e) do println("x") --)` do exemplo 8 (F7) |
| Código de erro `E7xx`/`W7xx` livre                                                               | spec inteira (`git grep -E '\b[EW]7[0-9]{2}\b'`)     | ✔ nenhuma ocorrência |
| Ordem de inserção de dict (a cascata de `w.rules` usa "ordem do dict")                           | spec Cap. 19.1                                       | ✔ garantida |
| Tupla imutável; `ImmutableMutation` (base de `el.classes`)                                       | spec Cap. 19.5                                       | ✔ |
| `os.read(file)` existe (base do `w.css` por arquivo)                                              | spec Cap. 34 (módulo `os`)                           | ✔ (retorno e codificação não detalhados aqui) |
| Strings de uma linha; `{ }` interpola; `\{ \}` escapam                                           | spec Cap. 3.2, 3.3, 20                               | ✔ — **mas** ver F1 |
| `r"…"` e `"""…"""` definidos?                                                                    | spec inteira (`git grep`)                            | ✘ só **citados** numa frase do Cap. 3.1.1; sem definição |
| `const` e mutação de conteúdo                                                                    | spec Cap. 18.2, 19.4.2, 19.5                         | ✘ **contraditório** (F6) |
| Flex: `flex-shrink` ponderado pelo tamanho-base; margens/paddings `%` contra a largura; margens de itens flex não colapsam; margens `auto` absorvem espaço antes do `justify-content` | W3C CSS Flexbox, **rascunho do editor** (`w3c/csswg-drafts`, `css-flexbox-1/Overview.bs`, lido no GitHub) | ✔ a v2 está certa |
| Flex: tamanho mínimo automático do item                                                          | idem                                                 | ✘ **v2 incompleta** (F4) |
| Flex: posição estática de filho absoluto                                                         | idem                                                 | ≠ a v2 **simplifica** (documentado em D07; ver D49) |
| `align-content` inicial `stretch`                                                                | idem                                                 | ✔ |
| CSS pode **abortar no primeiro erro** (base para `w.css` estrito)                                | W3C CSS Syntax 3, `css-syntax-3/Overview.bs`, linha 288 | ✔ o próprio padrão permite |
| Saída de `println` de um **dict** e de float em dict                                             | spec (busca por `# → {`)                             | ✘ não achei formato definido (F5) |
| Como o backend entrega `ç`/`ã` (teclas mortas)                                                   | doc do `winit::event::Ime` (lida)                    | **parcial**: a página separa `KeyboardInput` (teclado latino) de `Ime::Commit` (texto que exige sequência) e **não** fala de teclas mortas — hipótese em 4.C |

A leitura automática da página do W3C (TR) veio **truncada**; por isso conferi o texto no repositório de rascunhos do W3C. É o rascunho do editor (`main`), **não** a Recomendação/Candidata publicada: pode diferir dela em detalhes.

## 3. Defeitos da v2

**F1 — Interpolação em string comum (4 exemplos). [spec]**
`canvas-05` (3×: `"clicou em {e.x}, {e.y}"`, `"…{e.target.id}"`, `"idade: {e.value}"`) e `canvas-06` (`"{atual + 1}"`) interpolam em string **sem `format`**. A spec se contradiz: o Cap. 20 (texto de 20.1, com `print("você é muito {A} …")`) diz que strings interpolam; mas 20.2, o Cap. 30, o Cap. 38 e o Apêndice A (B28) **só** usam `format "…{x}…"`, inclusive a frase "usá-la dentro de um texto `format "{x}"`" (Cap. 38). `format` não está em `gramatica.ebnf`. **Decisão D38.** Correção na v3: usar `format "…"` nos exemplos **ou** manter, conforme a resposta.

**F2 — `w.x`/`w.y` lidos como `int ou null`.** (`canvas-01`, tabela de propriedades.) Ao **ler**, a posição é sempre um `int` (a real); `null` só faz sentido ao **gravar** ("o sistema escolhe"). O mesmo vale só parcialmente para `min-*`/`max-*` (ali `null` lido = "sem limite" é legítimo). Correção: separar "tipo lido" de "tipo aceito ao gravar".

**F3 — `canvas.run()` sem janela real.** `run()` "volta quando a última janela fecha" (`canvas-05`, D25), mas uma janela `headless` **nunca fecha sozinha** e `canvas.run()` sem nenhuma janela não está dito: bloquearia para sempre num teste. Também indefinido: `canvas.quit()` quando um handler de `close` chama `e.prevent()` (o `run()` volta ou continua?). **Decisão D40.**

**F4 — Tamanho mínimo automático de item flex, incompleto.** (`canvas-03`, `canvas-04`.) A v2 diz "o tamanho mínimo do conteúdo". Conferido no W3C (§4.5, rascunho): (a) se o item é um **contêiner de rolagem** no eixo principal (`overflow` ≠ `visible`), o mínimo automático é **zero**; (b) o mínimo do conteúdo é **limitado pelo tamanho especificado** (`width: 100` com uma palavra de 140 → mínimo 100), e pelo máximo se definido. Sem (a), um item flex com `overflow: auto` (uma coluna rolável ao lado de outra, por exemplo) **não encolhe** abaixo do conteúdo, ao contrário do navegador; sem (b), um item de `width` fixo com uma palavra longa teria mínimo maior que o `width` pedido. Nenhum exemplo da v2 depende disso, mas é regra que o motor precisa ter certa. Correção direta, sem decisão.

**F5 — Saída de dict não definida.** O exemplo 5 (`canvas-06`) e os de `canvas-04` mostram `println(rect())` como `{"x": 0.0, …}`; a spec define impressão de lista (`["w", "x"]`) e `to-float` (`3.0`), mas **não achei** o formato de impressão de dict. Para que os exemplos sejam testes, imprima campo a campo (`println(r["width"])`) ou defina o formato **[spec]**.

**F6 — `const` e handles. [spec]**
Todo exemplo usa `var`, mas `const botao = w.button(…)` é o jeito natural (a referência nunca muda). A spec diz que `const` é "imutabilidade total" (Cap. 18.2; `B.add("C")` → `ImmutableMutation`, Cap. 19.5) **e**, no Cap. 19.4.2, que `const` "permite editar uma chave/índice já existente". Com a **sua** decisão D01(b) (`botao.text = "x"`), `const botao` + gravação é ou legal ou `ImmutableMutation`. **Decisão D39.**

**F7 — Exemplo 8: `t.on("clik", f(e) do println("x") --)`.** A forma de uma linha com `do … --` existe na spec (`while true do print(1) --`), mas **`--)` colado ao parêntese** não aparece. Reescrever em várias linhas (forma por indentação, a mesma de todos os outros exemplos).

**F8 — `"padding": "8 16"` não é CSS (inconsistência entre `str` e CSS).** (`canvas-03`, folha UA e exemplos.) Em CSS, `8 16` sem unidade é inválido; na v2 é aceito como px dentro de `str`. Isso faz a `str` do dict ser um **dialeto** do CSS, e o `w.css` (v3) ficaria com duas regras de unidade. **Decisão D45.**

Menores, sem decisão: `e.x`/`e.y` são `float` no ponteiro e `int` no evento `move` (a linha final da tabela junta tudo em "`num`") — separar na tabela; `scroll-x`/`scroll-y` aparecem como propriedade de **todos** os elementos, mas só valem com `overflow: scroll|auto` — sem efeito nos outros (hoje: sem aviso; sugestão: `W701`).

## 4. O que falta

### 4.A Comportamento indefinido (fechar antes de acrescentar recursos)

| **Caso**                                                                                             | **Hoje**   | **Sugestão (✔)** |
|------------------------------------------------------------------------------------------------------|------------|------------------|
| `run()` com só janelas `headless`, ou sem janela (F3)                                                | indefinido | volta na hora, sem erro |
| `quit()` com `close` cancelado                                                                       | indefinido | `quit()` fecha **sem** consultar `close` (é "sair do programa"); `w.close()` consulta |
| Handler **remove** o elemento do próprio evento, ou um ancestral, no meio da propagação              | indefinido | como o DOM: o caminho é **fixado no início** do despacho; handlers de elementos removidos ainda rodam naquele evento; a próxima propagação usa a árvore nova |
| Handler **registra** outro handler no mesmo alvo e tipo durante o despacho                           | indefinido | só vale a partir do **próximo** evento |
| `el.focus()` num `disabled`/oculto (`display: none`)                                                 | indefinido | `W701`-estilo: aviso "não focável"; foco não muda |
| `canvas.every` quando todas as janelas fecharam                                                      | "acaba com o `run()`" | idem, e `t.active` passa a `false` |
| Gravar `w.width = 5000` acima da tela                                                                 | pergunta aberta em D35 | já em D35 |
| Caminho relativo de `image src`, `icon`, e do CSS por arquivo                                        | indefinido | relativo ao **`.tpine` em execução** (`~Program.path`, Cap. 29.4), não ao diretório atual — **D51** |
| Fonte padrão **embutida**: qual e licença (D18)                                                      | aberto     | sem ela, o `rect()` de `text` não é reproduzível entre máquinas; **bloqueia** testes com texto |

### 4.B Teste de interface sem tela (a lacuna que mais vale para o seu repositório)

O repositório já roda exemplos `tinypine run` + `output` (`tools/run_examples.py`) e compara a saída. O `headless` + `rect()` da v2 cobre **layout**, mas **não cobre interação**: sem usuário, ninguém clica. Faltam:

- **Disparar eventos por código**: `el.dispatch("click", {"x": 10, "y": 5})` e `w.dispatch("keydown", {"key": "enter"})`, (o nome é `dispatch` como no DOM, e não `emit`, que é palavra reservada de geradores — Cap. 23) passando pela **mesma** propagação (captura → alvo → bolha) e ações padrão. Sem isso, o contador (exemplo 3) e a lista de tarefas (exemplo 4) **não são testáveis**.
- **Passo do laço**: `canvas.poll()` já existe; falta dizer que, em `headless`, ele **não dorme** e processa o que foi enfileirado por `dispatch`.
- **Relógio falso** (`canvas.after`/`every`): `canvas.advance(segundos)` só em `headless`, para testar timers sem esperar.
- **Comparação de imagem** (`w.capture`): fica fora; depende da fonte embutida.

Custo no motor: baixo (o despacho já precisa existir); benefício: os exemplos 3, 4 e 6 passam a ser `tinypine run` + `output` de verdade. **D40** cobre as duas metades (laço e harness).

### 4.C Entrada de texto (importante para quem escreve em português)

A v2 define `keydown` com `e.key` e `e.char`, e D28 diz "sem IME". Mas **`ç`, `ã`, `é`, `ñ` costumam vir de teclas mortas** (acento primeiro, letra depois), e o texto digitado **não é** a tecla apertada. Se `input` for montado em cima de `keydown`+`e.char`, o campo pode errar justamente no seu idioma. O `winit` (lido) separa o teclado latino de eventos de texto (`Ime::Commit`: "texto a inserir no editor"); como ele trata teclas mortas especificamente **não consegui confirmar**. Proposta (✔) — **D41**: um evento **`textinput`** (`e.text`, uma `str` já composta) **separado** de `keydown`/`keyup` (teclas físicas); o `input` edita por `textinput`; `e.char` sai de `keydown`. Pré-edição de IME (japonês etc.) continua fora (D28).

### 4.D Recursos que não existem (candidatos; ordem sugerida na seção 6)

- **Controles**: `checkbox`/`radio`, `select`, `textarea` (várias linhas), `range`/`progress`; **barras de rolagem** visíveis e `overflow-x`/`overflow-y` separados (hoje só `overflow`).
- **Aparência**: `outline` (anel de foco), `box-shadow`, `transition`, gradientes.
- **Janela**: filha/modal (D24), **diálogos nativos** (mensagem, abrir/salvar arquivo).
- **Texto**: carregar fonte de arquivo (D18); `text-overflow`, `letter-spacing`.
- **`surface`** (desenho 2D, D27). **Atenção**: o TinyPine já tem os módulos `pen` e `scene`, que você pediu para **ignorar**. Se eles cobrem o desenho, o `surface` do canvas duplicaria; se não, é o próximo passo natural para os seus jogos. **D46.**
- **`display: grid`**, `position: fixed/sticky`, `calc()`, `var()`.
- Fora de propósito (não são lacunas): reatividade/`bind` de dados à interface, HTML.

### 4.E Integração com a spec (tudo o que a v2 supõe e a spec ainda não tem)

| **Ponto**                                                                            | **Onde**                    | **O que a spec teria de dizer** |
|--------------------------------------------------------------------------------------|-----------------------------|---------------------------------|
| *Setter* em objeto nativo (`obj.nome = valor` chama o motor) — D37                    | Cap. 14, 29                 | atribuição a membro de objeto nativo |
| `E313` para membro só leitura de qualquer objeto nativo                              | Cap. 36.7, 37               | hoje só `~Program` |
| `const` × handle (D39)                                                               | Cap. 18.2, 19.4.2, 19.5     | uma regra única |
| Interpolação: `format` ou toda string (D38)                                          | Cap. 20                     | uma regra única; B28 |
| Strings cruas e multilinha (D44)                                                     | Cap. 3                      | `r"…"`, `"""…"""` só citados no 3.1.1 |
| `w.id` depois de `.` (`id` é palavra de bloco, Cap. 28)                              | Cap. 3.4, 28                | aceitar `id` como membro |
| Tecla `meta` (D17)                                                                   | Cap. 34.7                   | a tabela de teclas não tem |
| Tipos `window`, `element`, `event`, `listener`, `timer`, `sheet` e `.type` (D23)      | Cap. 6.7, 35 (etapa 6)      | anotação `: window` e análise estática |
| Impressão de dict (F5)                                                               | Cap. 19/20                  | formato |
| Função anônima que **atribui** a variável de fora (D30)                              | Cap. 31.3                   | escopo de escrita |
| Blocos de erro com fonte **que não é `.tpine`** (erros dentro do texto CSS, seção 7)  | Cap. 36.7                   | "Line N, characters a to b" sobre outro texto |

## 5. Melhorias propostas

| **#** | **Melhoria**                                                                                                                                         | **Por quê**                                                                                                                       | **Custo** |
|-------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|-----------|
| M1    | **Handler aceita 0 ou 1 parâmetro** (`ok.on("click", adicionar)` direto, sem `f(e) adicionar()`) — **D42**                                           | o exemplo 4 precisou de um *wrapper* só por causa da aridade; quem ignora o evento não deveria declará-lo. Erro continua para 2+ parâmetros | baixo; é uma regra de `on`, não da linguagem |
| M2    | **`textinput`** separado de `keydown` (4.C) — D41                                                                                                      | `ç`/`ã` corretos                                                                                                                  | médio |
| M3    | **`dispatch` + `advance`** em `headless` (4.B) — D40                                                                                                       | interação testável por `tinypine run`                                                                                              | baixo |
| M4    | **Posição estática de filho absoluto como no CSS** — D49                                                                                               | verificado no W3C: no flex, o filho absoluto sem `top/left` fica onde estaria se fosse o **único item** (respeita `justify-content`/`align-items`). A v2 o põe no canto, e numa raiz centralizada (`justify-content: center`) o resultado difere do navegador | baixo (o flex já calcula a posição) |
| M5    | **Estilo: `str` sempre CSS válido; atalhos por lista** (`"padding": [8, 16]`, `"margin": [0, "auto"]`) — D45                                            | uma regra de unidade para dict **e** `w.css`; lista é natural em TinyPine                                                          | baixo; muda `canvas-03` e a folha UA |
| M6    | **`el.computed("width")`**: valor resolvido de uma propriedade                                                                                          | hoje só `rect()` e `style()` (que devolve o inline); para depurar a cascata ou ler `font-size` herdado                            | baixo |
| M7    | **Aviso `W701` também para `scroll-x`/`scroll-y` sem `overflow`**                                                                                      | consistente com D09 (nenhum erro silencioso)                                                                                       | trivial |
| M8    | **Enxugar os rascunhos antes de entrarem na spec**: hoje ~2 000 linhas; a spec usa um capítulo por tema e `tinypine run` + `output`                      | os rascunhos repetem tabelas e justificativas; a spec precisa só da regra e de exemplos executáveis                               | só edição |
| M9    | **Mover os exemplos `headless` para `tests/exemplos/`** (como `30-parametros.md`) e os rascunhos para fora de `spec/` — D50                              | `tools/common.py` lê **todo** `spec/*.md` como capítulo (medi: 210 → 339 seções com a v2 dentro); `run_examples.py` já lê `tests/exemplos/` | só mover |

Não proponho: reatividade, HTML, `async` (D11 continua), mais seletores.

## 6. Escopo proposto da v3

**Etapa 0 — Correções (sem recurso novo).** F1–F8 e os menores; tabela 4.A; M7. *Pode ser uma v2.1 curta* (pergunta D48).

**Etapa 1 — Decisões de spec** (nada se escreve antes): D38 (interpolação), D39 (`const`), D37 (*setters*, já aberta), D44 (strings cruas/multilinha), D51 (caminhos).

**Etapa 2 — Núcleo da v3.**
1. `w.css` (seção 7).
2. Entrada de texto: `textinput` (D41).
3. Harness de teste: `dispatch`, `advance`, `run()` sem janela (D40).
4. M1, M4, M5.

**Etapa 3 — Recursos, na ordem que você escolher** (D47). Sugestão, por custo/benefício para ferramentas e jogos: (1) barras de rolagem + `overflow-x/y`; (2) `checkbox`, `textarea`, `range`; (3) `outline` + `transition`; (4) fonte de arquivo (D18); (5) diálogos; (6) `surface`, **só** se D46 disser que `pen`/`scene` não cobrem.

**Fica fora da v3**: `grid`, `calc()`/`var()`, `@media`, IME/bidi, janelas filhas (a menos que você peça), HTML.

**Pronto quando**: cada decisão da seção 8 respondida; todos os exemplos executáveis (`headless`) rodando como `tinypine run` + `output`; `check.py` sem erro/aviso com os rascunhos **fora** de `spec/`; nenhum exemplo depende de D30.

## 7. `w.css` preparado (D04 → v3)

### 7.1 O que dizia o adiamento, e o que muda

O D04 adiou por dois motivos: (1) strings cruas/multilinha não são especificadas; (2) `{ }` do CSS colide com a interpolação. **Revisão:**

- **(2) é só um problema de _literal_.** A interpolação acontece quando o lexer lê um literal `"…"`. Um `str` **lido de arquivo** (`os.read`) ou montado em tempo de execução pode ter `{ }` à vontade. E, se a resposta de D38 for "só `format` interpola", **nem o literal comum** tem o problema.
- **(1) é só um problema de literal multilinha.** Strings terminam no fim da linha (Cap. 3.3: "String não fechada"). CSS de uma linha cabe; CSS de verdade não.

### 7.2 Três jeitos de entregar o texto

```tinypine
# (A) De arquivo — funciona com o que a spec já tem (os.read, Cap. 34)
w.css(os.read("tema.css"), "source": "tema.css")

# (B) Literal de UMA linha — depende de D38
#   se SÓ `format` interpola:     w.css("button { color: red }")
#   se TODA string interpola:     w.css("button \{ color: red \}")      # legível? não

# (C) Literal MULTILINHA — exige spec (D44): `"""…"""` ou r"…" (citados no Cap. 3.1.1, sem definição)
w.css("""
  .card { background: #202030; padding: 16px }
  .card:hover { background: #2a2a40 }
""")
```

✔ **(A) como forma principal** (zero mudança de spec, arquivo editável por quem não programa, e é o uso real de CSS); (B) segue de D38; (C) fica para quando você decidir D44 — **não bloqueia** o `w.css`.

### 7.3 Contrato proposto

```text
w.css(text, "source": "<css>")  →  sheet
```

| **Item**             | **Proposta (✔)**                                                                                                                                              |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `text`               | `str` (valor, não só literal). Qualquer outro tipo: `TypeMismatch` (E302).                                                                                    |
| `"source"`           | nome mostrado nos erros (o nome do arquivo `.css`); sem ele, `"<css>"`. Quem lê de arquivo **precisa** passá-lo, senão o erro não diz onde está.              |
| Retorno              | `sheet`, o **mesmo** tipo de `w.rules` (`.remove()`, `.active`); entra na cascata **na ordem de registro**, misturada com as de `rules`.                      |
| Gramática            | `lista-de-seletores "{" declaração* "}"`; declaração = `propriedade ":" valor ";"`; comentários `/* … */`. Mesmos seletores de D26, mesmas propriedades de `canvas-03`. |
| **Estrito**          | **o primeiro erro interrompe**: sem "pular a declaração e seguir". O CSS Syntax 3 permite parar no primeiro erro (linha 288 do rascunho do W3C lido), e é a regra do Cap. 36. O motivo do CSS para recuperar-se (sintaxe nova não quebrar navegador velho) **não vale aqui**: o conjunto é fechado e declarado. |
| Fora (E722)          | `@media`, `@import`, `@font-face`, `@keyframes`, `!important`, `url()`, `var()`, `calc()`, pseudo-elementos, seletores de atributo/irmãos/estruturais.          |
| **Vantagem sobre dict** | **repetir o mesmo seletor** (o dict não repete chave, `canvas-03`) e **ordem de escrita preservada**.                                                       |
| Erros                | os de estilo já existentes (E720 desconhecida, E721 valor inválido, E722 não suportado) e E713 (seletor), **com linha e coluna dentro do texto CSS**; **um novo**: `CssSyntaxError` (E723) para chave sem fechar, `;` faltando, comentário aberto. |
| Unidades             | em texto CSS, `16px`, `50%`, `2em`; **sem unidade só o `0`**. Casa com D45 (se aprovado, o dict também fica assim).                                           |

Mapa dict ↔ CSS (a mesma linguagem, duas escritas):

| **CSS (texto)**                             | **dict**                                              |
|---------------------------------------------|-------------------------------------------------------|
| `padding: 16px`                             | `"padding": 16`                                       |
| `padding: 8px 16px`                         | `"padding": [8, 16]` (D45) ou `"padding": "8px 16px"` |
| `margin: 0 auto`                            | `"margin": [0, "auto"]`                               |
| `width: 50%`                                | `"width": "50%"`                                      |
| `border: 1px solid #444`                    | `"border": "1px solid #444"`                          |
| `button:hover { … }` (declarada 2 vezes)    | só em CSS texto (dict não repete o seletor)           |

Exemplo de erro (formato do Cap. 36.7, a fonte é o `.css`, **[spec]**):

```text
=== UnknownStyleProperty (E720) PROBLEM ===

We found a problem in the file:
tema.css

   2 | .card { background: #202030; paddng: 16px }
                                    ^^^^^^
Line 2, characters 31 to 36.
Recoverable error with try.

The style property "paddng" does not exist.

Hint: did you mean 'padding'?

=== END ERROR ===
```

### 7.4 Perguntas específicas

Respondidas em D43 (escopo), D44 (literais), D45 (unidades), D51 (caminhos). Mais uma, **sem recomendação firme**: `w.css` deve também aceitar um **caminho** (`w.css("tema.css")`)? ✔ **não** — `os.read` já faz, e uma função que ora recebe texto ora caminho é ambígua (um caminho **é** um texto).

## 8. Perguntas para fechar (D38–D51)

**D38 — Quem interpola: toda string ou só `format "…"`? [spec]** (F1)
Evidência: texto do Cap. 20 e `print("… {A} …")` (toda string) **×** 20.2, Cap. 30, Cap. 38, Apêndice A e B28 (só `format`). `format` não está na gramática.
✔ **só `format "…"`**: um literal comum nunca muda de significado por conter `{`; CSS, caminhos e expressões regulares ficam seguros; D04 perde metade do problema. Contra: o código fica mais longo, e é você quem decide o que a spec quer dizer. **Impacto:** 4 exemplos meus (trocar por `format "…"`); `w.css` (B).

**D39 — `const` e handles. [spec]** (F6)
✔ **permitido**: `const botao = w.button(…)` e `botao.text = "x"` valem — o `const` protege a **referência** (o handle é uma identidade, não "conteúdo de coleção"); a regra do Cap. 19.5 (`ImmutableMutation`) fica para coleções e tuplas. Alternativa: tudo só leitura sob `const` (então `const` nunca serve para handle, e os exemplos usam `var`). Precisa de uma frase na spec.

**D40 — Laço e testes.** (F3, 4.B)
✔ (1) `run()` volta na hora se não há janela **não `headless`**; (2) `quit()` não consulta `close`; (3) `headless` ganha `dispatch(kind, dados)` e `canvas.advance(segundos)`; (4) em `headless`, `poll()` não dorme.

**D41 — `textinput`.** (4.C)
✔ evento **`textinput`** com `e.text` composto, separado de `keydown`/`keyup`; `input` edita por ele. Antes de fechar, **confirmar** no backend escolhido como `ç`/`ã` chegam (a doc do `winit` que li não diz).

**D42 — Handlers com 0 ou 1 parâmetro.** (M1)
✔ aceitar `f()` e `f(e)`; 2+ ou `package` (variádico) → `InvalidHandler` (E731). Alternativa: manter exatamente 1.

**D43 — Escopo do `w.css`.** (seção 7)
✔ `w.css(text, "source")` → `sheet`, **estrito**, mesmos erros de estilo com linha/coluna, `CssSyntaxError` (E723) novo; sem forma por caminho.

**D44 — Literais cruos e multilinha. [spec]**
O Cap. 3.1.1 **já cita** `r"…"` e `"""…"""`. ✔ especificar **`"""…"""`** (multilinha, **sem** interpolação, sem escapes) — serve ao CSS e a qualquer texto; `r"…"` (uma linha, sem escapes) opcional. É decisão **da linguagem**, não do canvas; o `w.css` não depende dela (jeito A).

**D45 — `str` é sempre CSS válido; atalhos por lista.** (F8, M5)
✔ dentro de `str`, **unidade obrigatória** (`"8px 16px"`), exceto `0`; número puro = px; atalhos de 2–4 valores também como lista (`"padding": [8, 16]`). Muda `canvas-03` (D05 já decidida **não muda**: número = px e `str` com unidade — isto só tira o dialeto `"8 16"`). Alternativa: manter `"8 16"` e aceitar o mesmo em CSS texto (perde a fidelidade ao CSS).

**D46 — `surface` × `pen`/`scene`.**
Você mandou ignorar `pen` e `scene`. Antes de planejar desenho 2D, **o que eles já cobrem**? ✔ o canvas fica **só** interface (árvore de elementos); desenho livre é do que já existe, e o canvas oferece, no máximo, uma **ponte** (um elemento que hospeda uma superfície dos outros módulos).

**D47 — Ordem dos recursos da etapa 3.** ✔ a da seção 6; diga o que sobe ou desce (você sabe o que os seus programas pedem; eu só estou supondo ferramentas e jogos).

**D48 — Correções (etapa 0).** ✔ publicar como **v2.1** curta (F1–F8 + 4.A) **antes** da v3, para a v3 partir de uma base sem defeito conhecido. Alternativa: já dentro da v3.

**D49 — Posição estática do filho absoluto.** (M4)
✔ seguir o CSS (verificado): no flex, o filho absoluto sem `top/left/…` fica onde estaria se fosse o único item. Revoga **uma** das seis simplificações de D07 (que você aprovou); por isso pergunto.

**D50 — Onde moram os rascunhos e os testes.** (M9)
✔ rascunhos em `rascunhos/` (fora de `spec/`), exemplos `headless` em `tests/exemplos/canvas-*.md`. Alternativa: manter em `spec/` e excluir `canvas-*` do `common.py` (mexe nas suas ferramentas; não tocarei sem pedido).

**D51 — Caminho relativo.** (4.A)
✔ relativo ao **arquivo `.tpine` em execução** (`~Program.path`), **não** ao diretório atual — um programa abre igual de qualquer pasta. Vale para `image`, `icon` e o CSS por arquivo; verificar se `os.read` já faz o mesmo (decisão do `os`, não do canvas).

**Para responder primeiro:** D38 → D39 → D43 → D41 → D46. O resto segue as recomendações.

## 9. O que **não** foi verificado

- Nenhum código existe; **nada foi executado**. Todo exemplo da v2 e deste arquivo é escrito à mão.
- Flexbox: conferi só os cinco pontos da seção 2, no **rascunho do editor**. O algoritmo inteiro (9 passos), `flex-basis: content`, `align-self` com margens `auto` e a ordem de pintura continuam **de conhecimento geral**; a v2 já avisava isso em `canvas-09`.
- Teclas mortas (D41): **hipótese**, não confirmada na fonte.
- Se `os.read` devolve `str` em UTF-8 e como trata caminho relativo: não li o capítulo do módulo `os` em detalhe.
- Não pesquisei de novo os outros motores (Taffy, Yoga, RmlUi…); a v2/v1 já tinham essa seção.
- A leitura do CSS Syntax foi do rascunho do editor, e a frase "pode abortar no primeiro erro" vem do **texto do próprio documento** (linha 288), não de uma Recomendação publicada.

## 10. Fontes

- W3C CSS Flexible Box Layout (rascunho do editor) — <https://github.com/w3c/csswg-drafts/blob/main/css-flexbox-1/Overview.bs>
- W3C CSS Syntax Module Level 3 (rascunho do editor) — <https://github.com/w3c/csswg-drafts/blob/main/css-syntax-3/Overview.bs>
- winit, `event::Ime` — <https://doc.servo.org/winit/event/enum.Ime.html>
- TinyPine-spec (seu repositório, commit `945f346`): Cap. 3, 4, 14, 18, 19, 20, 28, 29, 30, 31, 34, 35, 36.7, 37, 38, Apêndice A.
