# canvas — Arquitetura do motor (notas de implementação)

> **RASCUNHO — não normativo.** Ver `canvas-00-visao-geral.md`.
> Este arquivo **não é parte do contrato da linguagem**: descreve *uma* forma de construir o módulo, para que a spec do canvas não prometa o que o motor não consegue cumprir. Nomes de bibliotecas são **sugestões a validar** — não foram testados nesta pesquisa.
> Contexto assumido: o núcleo do TinyPine é C#/.NET (Lexer/Parser/Interpreter/Runtime), roda em Windows e Linux, e já existe uma GUI separada.
> **v3:** acrescenta (1) o **leitor de CSS em texto** (`w.css`); (2) o **relógio** como interface (`IClock`: real × virtual) e o `dispatch` do backend `headless`; (3) `textinput` como evento **separado** do teclado; (4) handler com 0 ou 1 parâmetro; (5) resolução de caminhos pelo `.tpine`; (6) mínimo automático e posição estática do absoluto no layout. Lista completa em `canvas-16-mudancas-v3.md`.

## Camadas

```
┌───────────────────────────────────────────────────────────────┐
│ Ponte com o interpretador  (CanvasModule: window, get, run…)  │  objetos nativos: Window, Element,
│                                                               │  Event, Listener, Timer, Sheet
├───────────────────────────────────────────────────────────────┤
│ Núcleo (sem nenhuma dependência de SO, testável sem janela)   │
│   Árvore ─► Estilo ─► Layout ─► Lista de desenho (display list)│
│   Eventos: hit-test + despacho (captura/alvo/bolha)           │
├───────────────────────────────────────────────────────────────┤
│ Interfaces de plataforma (o SO e as bibliotecas entram aqui)  │
│   IWindowSystem · IRenderer · IFontService · IImageLoader     │
├───────────────────────────────────────────────────────────────┤
│ Backends:  janela real (Win/Linux)  ·  headless (memória)     │
└───────────────────────────────────────────────────────────────┘
```

A separação em **núcleo + interfaces de plataforma** é a lição mais repetida na pesquisa: o RmlUi expõe uma *render interface*, uma *system interface* e uma *font interface*; o litehtml pede ao hospedeiro um `document_container` (medir texto, desenhar); o Sciter.Lite deixa o hospedeiro dar a superfície; o Blitz separa DOM headless, renderizador e "shell" de janelas (`canvas-09`). Daí saem duas vantagens para o TinyPine:

1. **Modo `headless` de graça** (D20): o mesmo núcleo com um backend em memória.
2. **Testes sem tela**: estilo, layout e despacho de eventos são funções puras sobre a árvore.

## Núcleo

### Árvore
`Node { kind, id?, classes[], attrs{}, inlineStyle{}, children[], parent }`. `Window` é o nó raiz. Índice `id → Node` por janela (para `find`). Handles do TinyPine apontam para o nó por uma referência com **geração** (para detectar `StaleHandle`, E706, sem manter nós mortos vivos).

### Estilo
1. **Tradução**: dict do TinyPine **ou texto CSS** → `Declaration { prop, valor tipado }`, com validação por propriedade (E720/E721/E722). Uma tabela de propriedades (nome, tipo de valor, herda?, inicial) é a única fonte de verdade — vira também a lista do *did you mean* e da documentação. O **leitor de CSS** (`w.css`) é um *tokenizer* + parser pequeno (`folha → regra → declaração`) que **guarda a posição** (linha, coluna inicial e final) de cada token, para os erros apontarem **dentro do texto** (`canvas-13`); é **estrito** (para no primeiro erro, `CssSyntaxError` E723) e **tudo ou nada** (valida antes de registrar a folha). Dict e texto passam pela **mesma** validação de valores (D45); só o parser é novo.
2. **Seletores**: parser do subconjunto de `canvas-03` → estrutura casável; especificidade calculada uma vez por regra.
3. **Cascata** por elemento: UA < folhas < inline; herança; valor inicial → `ComputedStyle` (comprimentos já em px; `em`/`rem`/`vw`/`vh` resolvidos aqui).
4. **Invalidação**: mudança de classe/estado/estilo marca o nó; só reestiliza o que a regra pode alcançar (descendentes para seletores descendentes).

### Layout
Árvore de caixas (nós com `display: none` ficam de fora) com três algoritmos: *block*, *flex*, *absolute*; folhas chamam `Measure(espaço disponível)`. O algoritmo do flex é o do W3C (oito passos listados em `canvas-04`; o mínimo automático do item, com a regra do contêiner de rolagem e o limite pelo tamanho especificado, foi corrigido na v3). A **posição estática** de um filho absoluto sem `top/left/…` (D49) é calculada **pelo próprio contêiner**: em *block*, o ponto onde o filho estaria no fluxo; em *flex*, como se fosse o único item. Resultado: `Rect` em px lógicos fracionários por nó.

- **Escrever vs. reaproveitar.** O subconjunto do v1 (sem grid, sem inline, sem colapso de margem) é pequeno o bastante para escrever dentro do projeto — e assim os desvios do CSS (`border-box`, margens somando) ficam sob controle. Reaproveitar é possível: Yoga tem ligações para C#; Taffy é Rust (exigiria FFI). **Recomendação**: escrever, usando os exemplos numéricos de `canvas-04`/`canvas-06` como primeiros testes e comparando com Taffy/Yoga em casos de flex quando houver dúvida.
- **Medida de texto** (`Measure`): três perguntas — com largura definida, **mínima** (palavra mais longa) e **máxima** (uma linha só). O flex precisa das três.

### Pintura
O layout vira uma **lista de desenho**: retângulos (com raio), bordas, *runs* de texto já posicionados, imagens, `PushClip`/`PopClip`, `PushOpacity`/`PopOpacity`. A lista não sabe de SO nem de biblioteca gráfica; o `IRenderer` a executa. Benefícios: cache por janela (só refaz o que mudou), e um backend de teste pode **comparar a lista**, não pixels.

### Eventos
`IWindowSystem` entrega eventos crus (posição, botões, teclas, resize, foco). O núcleo traduz em eventos do canvas: *hit-test* na lista de desenho ao contrário, `pointerenter/leave` por diferença de caminho entre quadros, `click` por par down/up, foco e Tab, edição de `input`. O despacho monta o caminho alvo→raiz **uma vez, no início** (e o conserva, mesmo que um handler remova nós) e chama os handlers em captura/alvo/bolha (`canvas-05`). **Texto**: `IWindowSystem` entrega a **tecla** (`KeyDown`/`KeyUp`) e o **texto produzido** (da tecla ou de uma composição do sistema) como duas coisas; o núcleo gera `keydown`/`keyup` e `textinput` (D41, `canvas-15`). A forma exata com que cada sistema entrega `ã`/`ç` **não foi verificada** (`canvas-15`).

**Teste sem tela.** O backend `headless` é um `IWindowSystem` que **não tem laço de verdade**: `dispatch(tipo, dados)` chama **o mesmo** despachador do núcleo (hit-test, captura/alvo/bolha, ações padrão), de forma síncrona. O tempo vem de um **`IClock`**: o relógio real (monotônico) nas janelas reais; um **relógio virtual** (começa em 0, só anda por `advance`) no `headless` (`canvas-14`). Um só `IClock` por programa; misturar os dois é `HeadlessOnly` (E734).

## Interfaces de plataforma

| **Interface**    | **Responsabilidade**                                                                                          | **Notas**                                                           |
|------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `IWindowSystem`  | criar/fechar janelas com os atributos de `canvas-01`; bombear eventos (com *timeout* — é o `poll("wait")`); DPI; cursor; área de transferência do `input` | A janela deve ser criada e bombeada **na mesma *thread*** (exigência comum do Windows e de várias bibliotecas). |
| `IRenderer`      | executar a lista de desenho numa superfície; `Capture(png)`                                                   | há versão em memória (software) para `headless`.                    |
| `IFontService`   | achar família, métricas, **quebrar linhas**, medir e posicionar *glyphs*, fallback de fonte                   | o ponto mais difícil de ser igual entre plataformas (D18).          |
| `IImageLoader`   | decodificar PNG/JPEG para bitmap                                                                              | SVG e GIF animado fora do v1 (D19).                                  |

Como candidatos (a validar, não verificados aqui): janela e entrada via **Avalonia** (já usada na GUI do projeto — mas só como *host* de uma superfície, sem usar os controles dela, que trariam um segundo layout) ou via biblioteca de janelas como SDL/GLFW; desenho e texto via **SkiaSharp** com **HarfBuzz** para formatar texto. O backend `headless` pode usar o próprio Skia em bitmap, com uma fonte embutida para resultados reproduzíveis.

## Ponte com o interpretador

- **Objetos nativos** (`window`, `element`, `event`, `listener`, `timer`, `sheet`): `window` e `element` têm **propriedades graváveis** (D01, decidida); `event`, `listener`, `timer` e `sheet` são só leitura. Isso exige uma capacidade que o interpretador **ainda não tem**: *atribuição a membro de objeto nativo que executa código* (um *setter*). A spec tem precedentes parciais — `Y.A = 5` em `load` (Cap. 29.5) e as variáveis de instância de `class` (Cap. 32 — que **não** mostra atribuição de fora, `p.nome = x`, então nem isso está definido) — e um contraprecedente, `~Program` (Cap. 29.4, tudo somente leitura, E313). O ponto de extensão é: o avaliador de `obj.nome = valor`, ao ver um objeto nativo, chama `SetMember(nome, valor)` do objeto em vez de gravar numa tabela de símbolos. Cada objeto nativo declara uma tabela `nome → (tipo, gravável?, validador)`, que também alimenta *did you mean*, `E716` e as listas de dica.
- **`update(dict)`** (D02, decidida) é uma função nativa comum: recebe um `dict`, valida **todas** as chaves contra a mesma tabela e só então grava (tudo ou nada). Como o dict já distingue chave ausente de `null`, não precisa inspecionar argumentos (a v1 precisava, por causa de `update(text="x")`).
- **`el.classes`** devolve uma tupla nova a cada leitura (barata: lista pequena); **`el.style()`** devolve um dict novo.
- **Chamada de handler**: o interpretador é de uma *thread* só; o laço do canvas roda **nessa** *thread* e chama a função do TinyPine como qualquer chamada. Erros do handler sobem como exceções do TinyPine até `run()`/`poll()` (D16). **Aridade (D42)**: ao registrar, o motor lê o número de parâmetros da função; com 1, passa o evento; com 0, chama sem argumento; 2 ou mais (ou `package`), `InvalidHandler` (E731).
- **Caminhos** (`image`, `icon`, `capture`): relativos à pasta de `~Program.path` (Cap. 29.4) — o núcleo recebe um *resolvedor* de caminhos do interpretador (D51).
- **Tipagem**: os tipos novos precisam de lugar na análise estática (Cap. 35, etapa 6) para que `f(e)` e `: window` signifiquem algo; enquanto isso, a checagem é em tempo de execução (D23).
- **Tempo**: `canvas.after/every` usam um relógio monotônico; unidade pública em segundos.

## Ordem sugerida de construção

Cada marco termina com algo **testável**:

| **Marco** | **Entrega**                                                                                  | **Como testar**                                                |
|-----------|----------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| M0        | árvore + `canvas.window(headless)` + estilo (cascata, seletores) + *block* + `rect()` + **`dispatch`/`advance`** + leitor de `w.css` | exemplos `output` de `canvas-04/06/14` (sem tela, sem fonte)   |
| M1        | *flex* + `absolute` + medida de texto com fonte embutida                                     | os mesmos, mais casos de flex (crescer/encolher/quebra/gap)    |
| M2        | janela real + pintura + eventos de ponteiro/teclado + `run`/`poll`/`after`/`every`           | exemplos 1–3 e 6 à mão; despacho testado sem tela             |
| M3        | `button`, `input` (edição por `textinput`), foco/Tab, rolagem                                | exemplos 3–4; teste de `ç`/`ã` **num teclado real** (ABNT2)     |
| M4        | `capture`, imagens, vários monitores/DPI, acessibilidade (ponte de leitor de tela)           | comparação de imagens; testes manuais                          |

O **M0 não depende de nenhuma biblioteca gráfica**: dá para validar o desenho da API e do layout — a parte mais cara de mudar depois — antes de decidir janela e renderizador.

## Riscos

- **Texto**: quebra de linha, fontes diferentes por sistema e *kerning* fazem o mesmo programa ter tamanhos diferentes em Windows e Linux. Mitigação: fonte padrão embutida e modo `headless` determinístico (D18, D20).
- **Fidelidade ao CSS**: cada desvio documentado (`canvas-04`) é uma promessa; o que não está na lista deve se comportar como o CSS. Casos de borda do flex (mínimo automático, `shrink` com limites) são a parte onde reimplementações costumam divergir.
- **Escopo**: a tentação de "só mais uma propriedade" — o v1 fechado (D27) e o erro `UnsupportedStyle` existem para tornar cada adição uma decisão visível.
