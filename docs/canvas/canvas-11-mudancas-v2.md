# canvas — Mudanças da v1 para a v2

> **RASCUNHO — não normativo.** Ver `canvas-00-visao-geral.md`.
> Lista completa do que mudou, por arquivo. O que **não** está aqui não foi tocado (por exemplo, todo o miolo de `canvas-04` e `canvas-09`).

## Origem das mudanças

Suas respostas em `canvas-10` (v1): **D01** "escolho (b)", **D02** "Alternativa aceita", **D03** "prefiro o dict", **D04** "versão 3", **D05** "`str` CSS é melhor", **D07/D10/D23** confirmados. As consequências viraram D32–D37.

## Revisão 2.1 (você reverteu parte de D10)

Você escreveu: "me arrependi da decisão do D10, é muito melhor com '-' do que com '_'". Em uma versão intermediária da v2 eu havia trocado `min-width`, `min-height`, `max-width`, `max-height`, `on-top` por `_` (e criado `scroll_x`/`scroll_y`) por causa do D10; nesta revisão **voltei ao hífen em todos os lugares** e `scroll_x`/`scroll_y` viraram `scroll-x`/`scroll-y`. Arquivos tocados: `canvas-01`, `-02`, `-04`, `-07` (dica do E716), `-10` (D10, D31, D33, resumo) e este. O resto de D10 (`e.kind`, `id`, `canvas` × `<canvas>`, `input`, `update`) continua como você confirmou. Cuidado que fica: em conta aritmética, espaço em volta do `-` (`w.width - 10`).

## Por arquivo

| **Arquivo**                       | **Mudança**                                                                                                                                                                                                                         |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `canvas-00-visao-geral.md`        | Aviso de "Versão 2". Princípio 4 reescrito (era "ler por propriedade, escrever por método"; agora "ler e gravar por propriedade"). Mapa web→canvas: linha de `el.textContent = "x"` e nota "CSS em texto: v3". Mapa dos rascunhos: `canvas-10` e `canvas-11`. `w.css` na lista "fora do v1". |
| `canvas-01-janela.md`             | **Seção "O handle `window`" reescrita:** tabela com coluna G/L (gravável/somente leitura), "Escrever" (6 regras), `update(dict)`. **Removidos** `w.show()` e `w.hide()` (agora `w.visible`; D36). **Nomes com hífen mantidos** (`min-width`, `min-height`, `max-width`, `max-height`, `on-top`) em parâmetros de `canvas.window`, propriedades e chaves de `update` (D33; veja a revisão 2.1 abaixo). **Corrigida** a frase da v1 que dizia que esses nomes "não são identificadores válidos" (eram válidos, Cap. 3.4.1): agora o texto documenta `min-width=100` e o cuidado de espaçar a subtração. Ciclo de vida: gravar em janela fechada é E706, ler continua. Tabela de erros: E313, E716, E302. |
| `canvas-02-elementos.md`          | **Seção "O handle `element`" reescrita:** tabela G/L, "Escrever", `update(dict)`, "Classes" (`el.classes` lê tupla; atribuição troca todas; `toggle`/`has` mantidos com motivo novo), "Estilo" (`el.style()` sem argumento devolve cópia; `style` continua método). **Novas propriedades** `scroll-x`/`scroll-y`. Mapa para o HTML: linhas novas (`classes =`, `update`, `scroll-y`). Obsolescência do handle: gravar é E706, ler vale. |
| `canvas-03-estilo.md`             | `el.style()` sem argumento (cópia); D04 diz "adiada para a v3"; D05 marcada como decidida; `(400)`/`(700)` → `(= 400)`/`(= 700)` (silencia dois avisos falsos do `check.py`). Nenhuma propriedade de estilo mudou.                                                                                                         |
| `canvas-04-layout.md`             | Uma frase: `el.scroll(...)` (método) → `el.scroll-x`/`el.scroll-y` (propriedades).                                                                                                                                                      |
| `canvas-05-eventos.md`            | Nota de que o objeto evento é **todo** somente leitura (D01-b vale só para `window` e `element`). Exemplo "Fechar com Esc": `aviso.update(text=…)` → `aviso.text = …`.                                                                |
| `canvas-06-exemplos.md`           | Contador, lista de tarefas e "o que dá erro": `update(text=…)`/`update(value=…)` → gravação de propriedade. Exemplo 8: trocada a linha `t.text = "x"` (que agora **é válida**) por cinco erros novos (E313, E716 ×2, E302, `ImmutableMutation`); `t.update(text="y")` → `t.text = "y"`. **Exemplo 9 novo** (propriedades + `update` + `classes`; sem tela, saída prevista, **não executado**). |
| `canvas-07-erros-e-avisos.md`     | **E716 `UnknownAttribute` novo.** Linhas reaproveitadas ajustadas: E302 (também valor gravado), E308 (só leitura de membro), E313 (somente leitura em qualquer objeto nativo — **[spec]**), E503 (não mais `update`); `ImmutableMutation` (Cap. 19.5) incluído.                         |
| `canvas-08-arquitetura.md`        | "Ponte com o interpretador" reescrita: *setter* em objeto nativo (o que o interpretador ainda não tem), tabela de atributos por tipo, `update(dict)` como função comum, `classes` e `style()` devolvem cópias novas.                      |
| `canvas-09-pesquisa.md`           | Só uma nota no cabeçalho: **a v2 não fez pesquisa nova na web**; consultou a spec no `git` do seu repositório.                                                                                                                       |
| `canvas-10-decisoes-em-aberto.md` | Reescrito em três partes: **A** decididas (com as suas palavras), **B** novas D32–D37, **C** D06…D31 inalteradas — exceto D27 (cita `w.css` na v3), D29 (E716) e D31 (`scroll-x`/`scroll-y`).                                         |
| `canvas-11-mudancas-v2.md`        | Este arquivo (novo).                                                                                                                                                                                                                 |

## O que **não** foi feito

- **Nada foi executado.** Continua não existindo interpretador do canvas; os exemplos com saída (5 e 9) são previsões.
- Os exemplos do rascunho foram escritos como ```` ```tinypine ````, **não** como ```` ```tinypine run ````, para que `tools/run_examples.py` do seu repositório não tente rodá-los.
- Nenhum arquivo do seu repositório (`spec/`, `tools/`, `meta.yaml`, `README.md`) foi alterado. A v2 é só a pasta `canvas-rascunho-v2/`.

## Atenção ao colocar em `spec/`

Você copiou os rascunhos da v1 para `spec/`. `tools/common.py` lê **todo** `spec/*.md` como capítulo. Testei numa cópia temporária do seu repositório (commit `945f346`) com a v2 dentro de `spec/`:

- `check.py` **sem** rascunhos: 0 erros, 0 avisos, **210** seções numeradas.
- `check.py` **com** a v2 em `spec/`: 0 erros, **339** seções numeradas — ou seja, `build.py` incluiria os 12 rascunhos na especificação gerada, como capítulos 43 em diante.
- Dois avisos falsos (o texto `"bold"` seguido de 700 entre parênteses, e o análogo de 400) que **já existiam na v1** foram corrigidos na v2 (agora `(= 400)`/`(= 700)`), em `canvas-03`.

Se a ideia é manter os rascunhos fora da spec (como você pediu), uma pasta ao lado de `spec/` (por exemplo `rascunhos/`) evita isso; não mudei nada no seu repositório.
