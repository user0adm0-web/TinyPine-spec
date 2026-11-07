## Canvas — CSS em Texto

### Resumo

`w.css(texto)` registra uma **folha de regras escrita em CSS** (texto) na janela. É a mesma linguagem de `w.rules({...})` (Capítulo 46) em outra escrita — a que serve a quem já tem um `.css`, a quem quer o **mesmo seletor repetido** e a quem quer a **ordem de escrita**:

```tinypine
use canvas

const w = canvas.window("id": "app", "width": 400, "height": 300)

w.css("button { background: #2d6cdf; padding: 6px 14px }")     # texto CSS, uma linha
w.css(os.read("tema.css"), "source": "tema.css")                # ou um arquivo inteiro
```

### Três jeitos de entregar o texto

Só `format "…"` interpola `{ }` (Cap. 20). Uma string comum **não** muda de significado por ter chave, então o CSS cabe nela sem escapes:

```tinypine
# (A) De arquivo — a forma principal
w.css(os.read("tema.css"), "source": "tema.css")

# (B) Literal de UMA linha — string comum: as chaves são só caracteres
w.css("button { background: #2d6cdf; padding: 6px 14px }")

# (C) Literal MULTILINHA — ainda NÃO vale: """…""" não está definido na linguagem (Apêndice A, B35)
w.css("""
  .card { background: #202030; padding: 16px }
  .card:hover { background: #2a2a40 }
""")
```

- **(A)** usa o que a linguagem já tem (`os.read`, Cap. 34.6). Caminho relativo: ver Capítulo 44, "Caminhos de arquivo" — **depende de como o `os.read` resolve caminhos** (Apêndice A, B34).
- **(B)** vale para folhas curtas.
- **(C)** **não vale ainda**: `"""…"""` e `r"…"` só são *citados* (Cap. 3.1.1, na frase sobre `#~`); não há definição de literal multilinha nem cru (Apêndice A, B35). O `w.css` **não depende** dela: (A) e (B) bastam.
- Se o texto for **montado** com `format "…"`, as chaves do CSS precisam de `\{ \}` (e as de interpolação não). Para CSS, prefira (A).

### Contrato

```text
w.css(texto, "source": "<css>")  →  sheet
```

| **Item**             | **Regra**                                                                                                                                  |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `texto`              | `str` (um **valor**, não só literal). Outro tipo: `TypeMismatch` (E302). Vazio ou só espaços/comentários: folha **vazia**, sem erro.                                  |
| `"source"`           | Nome mostrado nos erros — o do arquivo `.css`. Sem ele: `"<css>"`. Quem lê de arquivo **deve** passá-lo, senão o erro não diz onde está.                              |
| Retorno              | `sheet`, o **mesmo** tipo de `w.rules` (`.remove()`, `.active`). Entra na cascata **na ordem de registro**, misturada com as de `rules` (Capítulo 46).               |
| **Tudo ou nada**     | O texto inteiro é lido e **todas** as declarações são validadas **antes** de a folha entrar. Se houver erro, **nenhuma** regra é registrada.                   |
| **Estrito**          | O **primeiro erro** interrompe. Não existe "pular a declaração inválida e seguir" do CSS de navegador. O padrão **permite** parar no primeiro erro (CSS Syntax Module Level 3); o motivo de o navegador se recuperar — sintaxe nova não quebrar navegador velho — **não vale** aqui: o conjunto é fechado e declarado. |
| Fora do subconjunto  | `@media`, `@import`, `@font-face`, `@keyframes`, `!important`, `url()`, `var()`, `calc()`, pseudo-elementos, seletores de atributo/irmãos/estruturais → `UnsupportedStyle` (E722), como no dict. |
| Forma por caminho    | **Não existe** (`w.css("tema.css")` trataria o caminho como CSS): `os.read` já lê. Um caminho **é** um texto; uma função que ora recebe texto, ora caminho, é ambígua.    |

#### Gramática

```text
folha       = { regra } ;
regra       = lista-de-seletores "{" { declaração } "}" ;
declaração  = propriedade ":" valor [ ";" ] ;     (* o último ";" é opcional, como no CSS *)
comentário  = "/*" … "*/" ;                       (* pode ocupar várias linhas; fora de string *)
```

- **Seletores**: os do Capítulo 46: tipo, `*`, `#id`, `.classe`, composto, descendente, `>`, lista com `,`, `:hover`/`:active`/`:focus`/`:disabled`. Seletor mal escrito: `InvalidSelector` (E713), com a posição.
- **Propriedades e valores**: as do Capítulo 46, escritas como em CSS (hífen, **minúsculas**: `font-size`, não `fontSize` nem `Font-Size`). Comprimentos: `16px`, `50%`, `2em`, `1.5rem`, `10vw`; **sem unidade só o `0`** (`padding: 8 16` é `InvalidStyleValue`, E721 — a mesma regra do dict, Capítulo 46). Cores: `#rgb`, `#rrggbb`, `#rrggbbaa`, nomes, `rgb()`, `rgba()`, `hsl()`, `hsla()`. Atalhos de 2–4 valores com **espaço**: `padding: 8px 16px`, `margin: 0 auto`, `border: 1px solid #444`. Listas com **vírgula**: `font-family: sans, monospace` (nomes **sem aspas**, como no CSS).
- **Sem interpolação, sem expressões** (`calc()`, `var()` ficam fora): o texto é dado.
- **Espaço em branco** (inclusive quebras de linha) entre os elementos é livre.

#### Mapa: o mesmo estilo em CSS e em dict

| **CSS (texto)**                             | **dict**                                              |
|---------------------------------------------|-------------------------------------------------------|
| `padding: 16px`                             | `"padding": 16`                                       |
| `padding: 8px 16px`                         | `"padding": [8, 16]` ou `"padding": "8px 16px"`       |
| `margin: 0 auto`                            | `"margin": [0, "auto"]`                               |
| `width: 50%`                                | `"width": "50%"`                                      |
| `border: 1px solid #444`                    | `"border": "1px solid #444"`                          |
| `font-family: sans, monospace`              | `"font-family": ["sans", "monospace"]`                |
| `button:hover { … }` declarado 2 vezes      | **só em CSS** (o dict não repete o seletor)            |

Duas escritas, **uma** linguagem: o que o dict aceita, o CSS aceita, e vice-versa, com a mesma regra de unidade e os mesmos três erros de estilo (E720, E721, E722).

### Erros: com posição **dentro do texto CSS**

Os erros de estilo (E720, E721, E722), o de seletor (E713) e o **novo** `CssSyntaxError` (E723) apontam a **linha e as colunas dentro do texto**, no formato do Cap. 36.7 (linhas e colunas contadas a partir de 1, extremidades incluídas). A "fonte" é o `source` dado, que **não** é um `.tpine`: nesse caso o bloco do Cap. 36.7 mostra o `source` no lugar do caminho do arquivo.

`CssSyntaxError` (E723) cobre: chave sem fechar ou a mais; `;` faltando entre declarações; `:` faltando; comentário `/*` sem fechar; seletor vazio antes de `{`; propriedade ou valor vazios.

```text
=== UnknownStyleProperty (E720) PROBLEM ===

We found a problem in the file:
tema.css

   1 | /* tema do app */
|> 2 | .card { background: #202030; paddng: 16px }
                                    ^^^^^^
   3 | .card:hover { background: #2a2a40 }

Line 2, characters 30 to 35.
Recoverable error with try.

The style property "paddng" does not exist.

Hint: did you mean 'padding'?

Call stack (most recent call last):
  tema.tpine, line 7: w.css(os.read("tema.css"), "source": "tema.css")

=== END ERROR ===
```

*(Formato do Cap. 36.7: `|>` marca a linha do erro; as colunas contam a linha física.)*

```text
=== CssSyntaxError (E723) PROBLEM ===

We found a problem in the file:
tema.css

   3 | /* cartão */
|> 4 | .card { background: #202030
       ^^^^^^^
   5 | .card:hover { background: #2a2a40 }

Line 4, characters 1 to 7.
Recoverable error with try.

The block opened with "{" is never closed.

Hint: add a "}" at the end of the rule.

=== END ERROR ===
```

*(O erro aponta o **`{` que não fecha** (`.card {`, colunas 1 a 7), não o fim do texto.)*

Em todos, é um erro **recuperável com `try`**, como os demais do canvas: o programa pode capturar e cair num tema padrão.

```tinypine
try
  w.css(os.read("tema.css"), "source": "tema.css")
catch e
  println("tema inválido; usando o padrão")
  w.rules({"button": {"background": "#2d6cdf"}})
```

### Folhas de regras: remover e conferir

```tinypine
const tema = w.css("button { color: red }")
println(tema.active)     # true
tema.remove()
println(tema.active)     # false; os botões voltam à cor da folha padrão
```

### Pontos em aberto

Literais multilinha ou crus (Apêndice A, B35) e a resolução de caminhos relativos pelo `os.read` (B34). O `source` serve só para mensagens; o **caminho lido** é assunto do módulo `os`.
