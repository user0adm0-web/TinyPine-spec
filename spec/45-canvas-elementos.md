## Canvas — Elementos

### Resumo

Uma janela vazia é só o fundo preto. Os **elementos** são o que se desenha nela. Cada elemento é uma caixa numa árvore; o programador cria um elemento **chamando o construtor do pai** — a janela ou outro elemento:

```tinypine
const w = canvas.window("id": "main")

const painel = w.box("id": "painel")                        # filho da janela
const titulo = painel.text("Olá", "id": "titulo")           # filho de `painel`
const ok     = painel.button("OK", "id": "ok")              # irmão de `titulo`
```

Pai sem filhos é uma janela vazia; pai com filhos é uma árvore. Não há `appendChild` separado: **criar é anexar**.

### Tipos de elemento

Cinco tipos, escolhidos para cobrir o que o HTML mais usa sem arrastar o resto do navegador:

| **Tipo**   | **Parecido com (HTML)** | **Aceita filhos?** | **Para quê**                                       | **`display` padrão** |
|------------|-------------------------|--------------------|----------------------------------------------------|----------------------|
| `box`      | `<div>`                 | sim                | container genérico; agrupa e organiza              | `block`              |
| `text`     | `<span>` / `<p>`        | não (folha)        | um trecho de texto, com quebra de linha            | `block`              |
| `image`    | `<img>`                 | não (folha)        | imagem de arquivo                                  | `block`              |
| `button`   | `<button>`              | não (folha)        | botão com texto; recebe foco, `click`              | `flex`               |
| `input`    | `<input type=text>`     | não (folha)        | campo de texto de uma linha                        | `block`              |

- A **janela** também é um contêiner: é a raiz, e tem os mesmos construtores de `box`.
- Folhas (`text`, `image`, `button`, `input`) **não têm** construtores: `titulo.box(...)` é membro inexistente. Um botão com ícone e texto é um `box` com `on("click", …)` e estilo — não um `button` com filhos.
- `text` **não é `inline`**: é uma caixa de bloco cujo conteúdo é um parágrafo. Texto com trechos de estilos diferentes numa mesma linha fica para depois (texto rico).

Fora desta versão: `select`, `textarea`, `checkbox`/`radio`, listas, tabelas, vídeo, e o elemento de desenho 2D (`surface`) (Apêndice A, B38).

### Construtores

Disponíveis em **janelas** e **`box`**. Retornam um `element`.

```text
pai.box   (                !, <comuns>, "focusable": false)
pai.text  ("text":  t = "", !, <comuns>)
pai.image (src,             !, <comuns>, "alt": "")
pai.button("text":  t = "", !, <comuns>, "disabled": false)
pai.input ("value": v = "", !, <comuns>, "placeholder": "", "password": false, "disabled": false)
```

Notação: a primeira posição (`"text": t = ""`, `src`, `"value": v = ""`) é o conteúdo principal e pode ser passada **por posição** (`pai.text("Olá")`) ou por nome (`pai.text("text": "Olá")`) — é um parâmetro nomeado opcional, que o Cap. 30.3 deixa ligar das duas formas. Tudo depois de `!` é só por nome. A notação é ilustrativa.

**Parâmetros comuns** (todos os tipos):

| **Nome externo** | **Tipo**                        | **Padrão** | **Descrição**                                                                           |
|------------------|---------------------------------|------------|-----------------------------------------------------------------------------------------|
| `"id"`           | `str`                           | `null`     | Identificador do elemento. Opcional. Único **dentro da janela**. **Imutável.**         |
| `"classes"`      | `list\values: str\`             | `[]`       | Nomes de classe, para os seletores `.nome`.                                             |
| `"style"`        | `dict\keys: str\`               | `{}`       | Estilo inline (Capítulo 46). Equivale a chamar `el.style({...})` logo depois de criar.  |
| `"label"`        | `str`                           | `null`     | Texto para leitores de tela / dica de acessibilidade.                              |

**Parâmetros por tipo:**

| **Tipo**  | **Parâmetro**       | **Tipo**  | **Padrão** | **Descrição**                                                         |
|-----------|---------------------|-----------|------------|-----------------------------------------------------------------------|
| `box`     | `"focusable"`       | `bool`    | `false`    | Entra na ordem de Tab e recebe foco de teclado.                       |
| `text`    | `"text"`            | `str`     | `""`       | O conteúdo. `\n` quebra linha.                                        |
| `image`   | `src` (posicional)  | `str`     | —          | Caminho do arquivo (PNG ou JPEG). Obrigatório. Relativo, é resolvido a partir do **`.tpine` em execução** (Capítulo 44, "Caminhos de arquivo"). |
| `image`   | `"alt"`             | `str`     | `""`       | Descrição, usada como `label` se este faltar.                         |
| `button`  | `"text"`            | `str`     | `""`       | Rótulo do botão.                                                      |
| `button`  | `"disabled"`        | `bool`    | `false`    | Desabilitado: não recebe foco nem `click`; casa com `:disabled`.      |
| `input`   | `"value"`           | `str`     | `""`       | Texto atual do campo (edição básica de uma linha; sem pré-edição de IME). |
| `input`   | `"placeholder"`     | `str`     | `""`       | Texto-dica, mostrado enquanto `value` está vazio.                     |
| `input`   | `"password"`        | `bool`    | `false`    | Mostra `•` no lugar de cada caractere; `value` continua o texto real.  |
| `input`   | `"disabled"`        | `bool`    | `false`    | Como em `button`.                                                     |

Erros: `id` repetido na janela → `ElementIdDuplicate PROBLEM` (E710); `id` vazio ou com espaço → `InvalidElementId PROBLEM` (E711); argumento que o tipo não declara (`pai.text("x", "src": "a.png")`) → `UnknownNamedArgument PROBLEM` (E503); imagem ilegível → `ImageLoadError PROBLEM` (E714, recuperável com `try`).

### O handle `element`

Mesma política da janela: lê-se por `.`, grava-se por `=`; só o que é estado do motor é somente leitura.

#### Propriedades

**G** = gravável (`titulo.text = "x"`), **L** = somente leitura.

| **Membro**          | **Tipo**         |     | **Existe em**        | **Descrição**                                                        |
|---------------------|------------------|-----|----------------------|----------------------------------------------------------------------|
| `el.id`             | `str` ou `null`  | L   | todos                | Dado na criação; `null` se não houve. Imutável.                      |
| `el.kind`           | `str`            | L   | todos                | `"box"`, `"text"`, `"image"`, `"button"`, `"input"`.                 |
| `el.type`           | `str`            | L   | todos                | `"element"` — o `.type` do Cap. 6.7.                      |
| `el.window`         | `window`         | L   | todos                | A janela dona.                                                       |
| `el.classes`        | `tuple` | G | todos              | Ao **ler**, uma **tupla** (imutável, Cap. 19.5). Ao **gravar**, aceita lista ou tupla e **troca todas** as classes. |
| `el.label`          | `str` ou `null`  | G   | todos                | Texto para leitores de tela.                                   |
| `el.text`           | `str`            | G   | `text`, `button`     |                                                                      |
| `el.value`          | `str`            | G   | `input`              | O texto do campo (ver "Escrever", item 4).                           |
| `el.placeholder`    | `str`            | G   | `input`              |                                                                      |
| `el.password`       | `bool`           | G   | `input`              |                                                                      |
| `el.src`            | `str`            | G   | `image`              | Gravar recarrega a imagem (falha → `ImageLoadError`, E714, e o valor antigo fica). |
| `el.alt`            | `str`            | G   | `image`              |                                                                      |
| `el.disabled`       | `bool`           | G   | `button`, `input`    |                                                                      |
| `el.focusable`      | `bool`           | G   | `box`                |                                                                      |
| `el.scroll-x`, `el.scroll-y` | `float` | G   | todos                | Deslocamento de rolagem em px lógicos; só tem efeito com `overflow: scroll\|auto` — **sem** isso, ler dá `0.0` e gravar não faz nada **e** emite `StyleHasNoEffect WARNING` (W701). |
| `el.hovered`        | `bool`           | L   | todos                | O ponteiro está sobre o elemento (ou um descendente).                |
| `el.focused`        | `bool`           | L   | todos                | O elemento tem o foco de teclado (para mover o foco: `el.focus()`).  |
| `el.pressed`        | `bool`           | L   | todos                | Botão do ponteiro pressionado sobre ele.                             |
| `el.removed`        | `bool`           | L   | todos                | `true` depois de `el.remove()` ou de a janela fechar.                |

`id` é só leitura (como todo identificador, Cap. 28.4) e `focused`/`hovered`/`pressed` também: são **estado que o motor decide** (foco e ponteiro vêm do usuário), e há método para pedir a ação (`el.focus()`).

Ler um membro que o tipo não tem (`titulo.value`) é `IdNotFound PROBLEM` (E308) com dica do tipo; **gravar** um membro que o tipo não tem é `UnknownAttribute PROBLEM` (E716).

#### Escrever

Mesmas regras da janela (Capítulo 44, "Escrever"), com as particularidades dos elementos:

```tinypine
titulo.text = "Placar: 3"
campo.value = ""
ok.disabled = true
painel.classes = ["painel", "ativo"]

titulo.id = "outro"       # ReadOnlyProperty PROBLEM (E313)
titulo.value = "x"        # UnknownAttribute PROBLEM (E716): text não tem 'value'
titulo.text = 3           # TypeMismatch PROBLEM (E302)
```

1. **Valida na hora**: E716 (não existe neste tipo), E313 (somente leitura), E302 (tipo errado). Em elemento removido: `StaleHandle` (E706).
2. **Efeito no próximo quadro**; ler de volta devolve o valor novo imediatamente. Várias gravações num handler viram um quadro só.
3. **`null` é aceito só onde a tabela diz `ou null`** (`label`); nos demais é E302. Para voltar ao padrão de `placeholder`, grave `""`.
4. **Gravar não dispara evento**, como no DOM: `campo.value = ""` **não** dispara `input` nem `change` (esses são do usuário editando). Quem precisa reagir a uma gravação do próprio programa já sabe que gravou.
5. Gravar o valor que já está lá não faz nada (nem invalida o layout).
6. `\n` gravado em `value` de um `input` (campo de uma linha): comportamento **indefinido** nesta versão (Apêndice A, B37).

#### update — várias propriedades de uma vez

`el.update(dict)` grava **só as chaves do dict** (o argumento é um **dict**). O mesmo contrato de `w.update` (Capítulo 44): tudo ou nada, `null` é valor, chave ausente = não mexe.

```tinypine
titulo.update({"text": "Placar: 3"})
campo.update({"value": "", "placeholder": "Digite o nome"})
ok.update({"disabled": true, "label": "Confirmar"})
ok.update({"label": null})                  # null explícito: remove o label

const estado = {"text": "Pronto", "disabled": false}
ok.update(estado)                            # o dict pode vir de uma variável
```

- Chaves aceitas = as propriedades **G** que o tipo tem: `box` (`classes`, `label`, `focusable`, `scroll-x`, `scroll-y`) · `text` (`text`, `classes`, `label`, …) · `image` (`src`, `alt`, …) · `button` (`text`, `disabled`, …) · `input` (`value`, `placeholder`, `password`, `disabled`, …); todos aceitam também `classes`, `label`, `scroll-x`, `scroll-y`.
- `"id"` (ou outra só de leitura) → `ReadOnlyProperty` (E313); chave que o tipo não tem → `UnknownAttribute` (E716) com *did you mean* e a lista de chaves do tipo; valor de tipo errado → `TypeMismatch` (E302). **Nenhuma** chave é gravada se uma falhar.
- **`"style"` não é chave de `update`**: o estilo tem método próprio (abaixo).
- Devolve `null`.

#### Classes

`el.classes` lê uma **tupla**: tentar mexer nela (`painel.classes.add("x")`) é `ImmutableMutation PROBLEM` (Cap. 19.5) — em vez de alterar uma cópia em silêncio. Há três jeitos de mudar as classes:

```tinypine
painel.classes = ["painel", "ativo"]     # troca todas
painel.toggle("ativo")                   # liga/desliga uma → bool (estado novo)
painel.toggle("ativo", true)             # força ligada
println(painel.has("ativo"))             # true
```

`toggle` e `has` ficam para o caso mais comum — mexer **numa** classe sem reescrever a lista inteira (a tupla não aceita `add`/`remove`; trocar uma só classe por atribuição exigiria montar a lista nova à mão).

#### Estilo

`el.style({...})` **mescla** o dict no estilo inline do elemento; `el.style()` (sem argumento) devolve uma **cópia** `dict` do estilo inline atual, para o programa alterar e reaplicar. `style` continua **método** — e não propriedade — porque "mesclar" e "substituir" são operações diferentes e uma atribuição (`el.style = {...}`) só diria uma delas. `el.rules({...})` não existe (regras são da janela). Detalhes no Capítulo 46.

```tinypine
var s = caixa.style()           # cópia: {"background": "#202030", ...}  (var: o conteúdo do dict é alterado abaixo; Apêndice A, B36)
s["opacity"] = 0.5
caixa.style(s)                  # reaplica (mescla); alterar só `s` não muda o elemento
caixa.style = {"color": "red"}  # ReadOnlyProperty PROBLEM (E313): style é método; use el.style({...})
```

#### Árvore

| **Método**                       | **Retorno**          | **Efeito**                                                                                      |
|----------------------------------|----------------------|-------------------------------------------------------------------------------------------------|
| `el.parent()`                    | `window`/`element`   | O pai. Para um filho direto da raiz, o pai é a janela. Para a janela, `null`.                    |
| `el.children()`                  | `list`               | Filhos diretos, em ordem (folhas: `[]`).                                                         |
| `el.remove()`                    | `null`               | Tira o elemento **e todos os descendentes** da árvore. Os `id`s ficam livres; os handles ficam obsoletos. |
| `el.clear()`                     | `null`               | Remove todos os filhos (só em `box`).                                                            |
| `el.move(novo_pai, "before": ref = null)` | `null`      | Muda o elemento de pai (ou de posição). Sem `"before"`, vai para o fim. `novo_pai` na mesma janela. |
| `el.rect()`                      | `dict`               | Caixa de layout atual (Capítulo 48).                                                             |
| `el.computed(nome)`              | valor                | Valor **resolvido** de uma propriedade de estilo, depois de cascata, herança e layout (Capítulo 46). |
| `el.dispatch(tipo, dados)`       | `bool`               | **Só `headless`**: entrega um evento ao elemento como se o usuário o tivesse produzido (Capítulo 51). Em janela real: `HeadlessOnly PROBLEM` (E734). |
| `el.find(id)` · `el.query(sel)` · `el.select(sel)` | `element` / `list` | Consulta **na subárvore** do elemento. |
| `el.on(tipo, handler, …)`        | `listener`           | Registra *handler* (Capítulo 49).                                                                |
| `el.focus()` · `el.blur()`       | `null`               | Move o foco para o elemento / tira dele. `focus()` num elemento **não focável** (`disabled`, `display: "none"`, `box` sem `focusable`): o foco **não muda** e sai `NotFocusable WARNING` (W705). |

- Mover um elemento para dentro de si mesmo ou de um descendente: `CyclicMove PROBLEM` (E715).
- Mover para outra janela: `CrossWindowMove PROBLEM` (E707).
- Usar um handle depois de `remove()` (ou de a janela fechar): `StaleHandle PROBLEM` (E706) em **métodos e gravações**; **ler** propriedades devolve o último valor conhecido, sem erro.

### Identidade e consulta

O `id` é a identidade estável do elemento **dentro da janela** — não precisa ser guardado em variável:

```tinypine
w.box("id": "painel")
# … em outro ponto do programa
const p = w.find("painel")           # ElementNotFound PROBLEM (E712) se não existir
```

| **Método**        | **Resultado**                                                              |
|-------------------|----------------------------------------------------------------------------|
| `find(id)`        | O elemento com esse `id` na subárvore; senão `ElementNotFound PROBLEM`.    |
| `query(seletor)`  | O **primeiro** casado (em ordem de árvore), ou `null` se nenhum.           |
| `select(seletor)` | **Lista** de todos os casados, em ordem de árvore; `[]` se nenhum.         |

`find` devolve erro quando falta e `query` devolve `null` de propósito: procurar por `id` conhecido que não existe é bug do programa; procurar por seletor que pode não casar é pergunta legítima. Seletor mal escrito: `InvalidSelector PROBLEM` (E713). Seletores aceitos: Capítulo 46.

Sobre o nome `id`: este `id` é um **valor de execução** (uma `str` que o programador dá ao elemento), **diferente** dos identificadores de bloco do Cap. 28 (`id msg`, resolvidos antes da execução). Os dois compartilham a ideia — nome único, imutável depois de criado — mas moram em lugares diferentes.

### Acessibilidade

Cada elemento tem um **papel** derivado do tipo (`box` → *grupo*, `text` → *texto*, `image` → *imagem*, `button` → *botão*, `input` → *campo de texto*), um **nome acessível** (`label`, senão `text`/`alt`/`value`) e o estado (`disabled`, `focused`). O `id` já dá o identificador estável que as camadas de acessibilidade de outros toolkits pedem (AccessKit: árvore de nós com id, papel e ações). Nesta versão isso é só o modelo de dados; a ponte com leitores de tela fica para depois.

### Mapa para o HTML

| **HTML**                          | **canvas**                                   |
|-----------------------------------|----------------------------------------------|
| `<div id="a" class="b c">`        | `pai.box("id": "a", "classes": ["b", "c"])`  |
| `<p>` / `<span>`                  | `pai.text("…")`                              |
| `<img src="x.png">`               | `pai.image("x.png")`                         |
| `<button disabled>`               | `pai.button("OK", "disabled": true)`         |
| `<input value="a" placeholder="b">` | `pai.input("a", "placeholder": "b")`       |
| `el.textContent = "x"`            | `el.text = "x"`                              |
| `el.classList = …` / `className`  | `el.classes = ["a", "b"]`                    |
| `Object.assign(el, {...})`        | `el.update({"text": "x", "disabled": true})`  |
| `el.scrollTop = n`                | `el.scroll-y = n`                            |
| `el.classList.toggle("on")`       | `el.toggle("on")`                            |
| `el.remove()`                     | `el.remove()`                                |
| `el.getBoundingClientRect()`      | `el.rect()`                                  |
| `getComputedStyle(el).width`      | `el.computed("width")`                       |
| `el.dispatchEvent(new Event(…))`  | `el.dispatch("click", {…})` (só `headless`)  |
