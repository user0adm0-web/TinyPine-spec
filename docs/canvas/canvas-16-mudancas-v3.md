# canvas — Mudanças da v2 para a v3

> **RASCUNHO — não normativo.** Ver `canvas-00-visao-geral.md`.
> Lista completa do que mudou, por arquivo. O que **não** está aqui não foi tocado (por exemplo, o miolo de `canvas-04` sobre modelo de caixa e pintura, e todo o `canvas-11`).

## Origem das mudanças

1. Seu pedido: "já corrigi as coisas que impedião a v3, pode fazer a v3 agora" (com o `spec/` atualizado, `c1e03f30-spec.zip`).
2. A análise `canvas-12` (defeitos F1–F8, lacunas 4.A–4.E, melhorias M1–M9, perguntas D38–D51). **Você não anotou D40–D51**: apliquei as recomendações ✔, **todas reversíveis**, e cada uma está identificada em `canvas-10`, parte C.
3. A spec atualizada resolveu **D38** (só `format "…"` interpola, Cap. 20) e **D39** em parte (Cap. 18.2: `const` impede a reatribuição do identificador; o Cap. 19.5 continua dizendo outra coisa para conteúdo de coleção).

## Por arquivo

| **Arquivo** | **Mudança** |
|-------------|-------------|
| `canvas-00-visao-geral.md` | Aviso de "Versão 3"; base de spec atualizada; exemplo com `const`; mapa web→canvas: `w.css`, `el.computed`, `el.dispatch`; princípio novo "testável sem tela" (o antigo 7 virou 8); mapa dos rascunhos com 12–16; "Fora do v1" sem `w.css` e com a etapa 3 adiada. |
| `canvas-01-janela.md` | **F2:** `w.x`/`w.y` lidos são `int` (gravar aceita `null`); em `headless` lê `0` (**suposição minha**, sem tela não há posição). `min-*`/`max-*` lidos continuam `int` ou `null`. **Novo:** `w.css`, `w.dispatch` (só `headless`), `canvas.advance`; seção "Caminhos de arquivo" (D51); `run()` não conta janela `headless`; erros E734 e E723 na tabela. `const` nos exemplos. |
| `canvas-02-elementos.md` | **Novo:** `el.computed(nome)` (D56), `el.dispatch` (só `headless`), `NotFocusable` (W705) em `focus()`, `W701` para `scroll-x`/`scroll-y` sem `overflow`; `src` relativo ao `.tpine` (D51); linhas no mapa HTML. `const` nos exemplos, **exceto** `var s = caixa.style()` (o dict é alterado por dentro: não dependo da contradição 19.5 × 19.4.2). |
| `canvas-03-estilo.md` | **D45:** `str` de estilo é sempre CSS válido; atalhos de 2–4 valores por **lista** (`[8, 16]`, `[0, "auto"]`); `"8 16"` (que a v2 aceitava como px) agora é `E721`; folha UA reescrita sem o dialeto (`"padding": [6, 14]`, `"border": "1px solid #555"`…). **D43:** `w.css` na tabela de formas e na cascata; `w.rules` e `w.css` devolvem `sheet`. **F4:** mínimo automático de `min-width`/`min-height` (0 em contêiner de rolagem; limitado pelo tamanho especificado e por `max-*`). **D55:** `font-family` aceita lista. **D56:** seção nova "Ler o estilo" (`el.style()` × `el.computed(nome)`). Aviso de que erros de `w.css` levam posição no texto. `const` no exemplo. |
| `canvas-04-layout.md` | **F4:** parágrafo do tamanho mínimo automático reescrito (dois casos). **D49:** posição estática do filho absoluto **como no CSS** (em flex, como único item) — **revoga uma das seis simplificações de D07** e some da tabela de diferenças. **F5:** exemplos imprimem `rect()` campo a campo. `"margin": [0, "auto"]`. `W701` para `scroll-x`/`scroll-y`. `const`. A tabela "difere do CSS" não diz mais "v1". |
| `canvas-05-eventos.md` | **F1/D38:** os três `println` com `{…}` usam `format "…"`. **D40:** `run()` volta na hora sem janela real; `quit()` não consulta `close` (entrega aviso não cancelável); `canvas.advance` na tabela; `timer` pendente vira `active == false` ao fechar a última janela. **D42:** handler com 0 ou 1 parâmetro; `E731` só para 2+ ou `package`; exemplo com `f ao_clicar()`. **D41/D58:** evento `textinput`; `e.char` **removido**; `e.text`; `keydown` cancelado suprime o `textinput`; ação padrão do `input` por `textinput`; filtro de dígitos reescrito. **D52:** seção "Mudar a árvore ou os handlers durante o despacho" (5 regras); `W705`. **Tabela do evento:** `e.x`/`e.y` separados em `float` (ponteiro) e `int` (`move`); `e.width`/`e.height` `int`; `e.scale`/`e.dt` `float`. **D30:** exemplos com estado compartilhado usam `var $…` global (nenhum depende de D30). |
| `canvas-06-exemplos.md` | `const` nos handles; `format "{atual + 1}"` (F1); `"margin": [0, 24]`, `[0, 12]`, `[8, 10]` (D45); exemplo 4 passa `adicionar` **direto** a `on` (D42) e o texto explicativo mudou; exemplo 5 imprime campo a campo com a função `linha(r)` e a saída prevista mudou de formato (F5) — **removi** `w.capture("layout.png")` do exemplo; exemplo 8: `t.on("clik", …)` em várias linhas (F7), **linhas novas** `E731` e `E723`; exemplo 9 com `const`. Cabeçalho aponta `canvas-13` a `-15`. |
| `canvas-07-erros-e-avisos.md` | **Novos:** `E723 CssSyntaxError`, `E734 HeadlessOnly`, `E735 InvalidDispatch`, `W705 NotFocusable`. **Alterados:** `E731` (0 ou 1 parâmetro), `E732` (inclui `advance`), `E733` (inclui `advance`), `W701` (inclui `scroll-*`), `W704` (inclui o `close` do `quit`). Seção de estilo vira E720–E723. Exemplo de bloco completo: `const` e alinhamento das linhas (o `|>` e os números de linha estavam desalinhados). Conferido de novo: `E7xx`/`W7xx` continuam livres na spec atualizada. |
| `canvas-08-arquitetura.md` | Leitor de CSS em texto com posições (estrito, tudo ou nada); mínimo automático e posição estática no layout; caminho do evento fixado no início; `textinput` como evento separado no `IWindowSystem`; `IClock` (real × virtual) e `dispatch` do backend `headless`; aridade de handler (D42); caminhos pelo `~Program.path` (D51); marcos M0 e M3 com os testes novos. |
| `canvas-09-pesquisa.md` | Nota "v3": pesquisa **pontual** (flexbox e CSS Syntax no rascunho do editor do W3C; `winit` `Ime` e `KeyEvent`); fontes novas no fim. |
| `canvas-10-decisoes-em-aberto.md` | **Reescrito** em partes A–F: A (suas decisões), B (o que a spec nova resolveu: D38, D39), C (D40–D51: o que a v3 fez com cada uma, e o estado), D (**novas**: D52–D58), E (D32–D37, texto da v2), F (D06–D31, com ajustes em D11, D17, D20, D25, D27, D28, D29, D30). |
| `canvas-11-mudancas-v2.md` | **Não alterado.** |
| `canvas-12-analise-v2-e-preparacao-v3.md` | **Não alterado** (documento histórico). Nota: o exemplo de bloco de erro da seção 7.3 tinha as colunas deslocadas de um e não tinha o `|>`; a versão **corrigida** está em `canvas-13`. |
| `canvas-13-css-em-texto.md` | **Novo.** Contrato do `w.css`, gramática, mapa dict↔CSS, erros com linha e coluna dentro do texto (dois blocos completos). |
| `canvas-14-testes-sem-tela.md` | **Novo.** `dispatch` (síncrono; alvo, dados, estado do ponteiro), relógio virtual (`advance`, `poll`), limites de fonte, quatro exemplos com `output` previsto, erros. |
| `canvas-15-entrada-de-texto.md` | **Novo.** `textinput`, regras do `e.text`, o que foi e o que **não** foi verificado sobre teclas mortas, migração de `e.char`. |
| `canvas-16-mudancas-v3.md` | Este arquivo (novo). |

## O que **não** foi feito

- **Nada foi executado.** Continua não existindo interpretador do canvas; os blocos com `output` (em `canvas-06` e `canvas-14`) são **previsões**. Estão escritos como ```` ```tinypine ```` e ```` ```output ````, **não** como ```` ```tinypine run ````, para que `tools/run_examples.py` não os execute.
- **Etapa 3 de `canvas-12`** (controles novos, barras de rolagem, `outline`/`transition`, diálogos, fonte de arquivo, `surface`): fica para a v4 (D46, D47 abertas).
- **D44** (literais `"""…"""`/`r"…"`): não é do canvas; o `w.css` não depende dela.
- **Não verificado:** como Linux e macOS entregam `ã`/`ç` (só li a documentação do `winit`: ver `canvas-15`); como o `os.read` resolve caminho relativo; o flexbox além dos cinco pontos de `canvas-12`; se atribuir a variável **global** `$x` dentro de função anônima funciona (a spec não diz; `canvas-10`, D30).
- **Contradição da spec que continua:** Cap. 19.5 (`const` não permite mutação de conteúdo) × Cap. 19.4.2 (permite). A v3 evita depender dela.

## Verificação feita

- Referências cruzadas: todo `Dnn` citado tem entrada em `canvas-10`; todo `E7xx`/`W7xx` citado existe em `canvas-07`; nenhum resto de `e.char` fora das notas de migração, nem de `"8 16"`, `min_width`, `scroll_x`, "exatamente um parâmetro" ou string comum com `{…}` sem `format`.
- Numa **cópia temporária** do seu repositório, com os 17 arquivos dentro de `spec/` (só para testar; **nada seu foi alterado**): `tools/check.py` → 0 erros, 0 avisos, com a spec antiga (commit `945f346`) **e** com a spec atualizada. Sem os rascunhos: 210 seções; com eles: 393 — por isso devem ficar **fora** de `spec/` (D50).
