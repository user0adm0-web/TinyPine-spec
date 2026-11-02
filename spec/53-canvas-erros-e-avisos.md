## Canvas — Erros e Avisos

Formato igual ao do Cap. 36.7: código, nome em PascalCase, recuperável?, mensagem (uma frase, em inglês) e dica (começa em minúscula). Os códigos usam as faixas `E7xx` e `W7xx`, reservadas ao canvas (a faixa `E6xx` é de `random` e `computer`). Os erros do canvas são **recuperáveis** com `try`, salvo indicação.

### Códigos reaproveitados

| **Código** | **Nome**                    | **Onde o canvas usa**                                                          |
|------------|-----------------------------|--------------------------------------------------------------------------------|
| `E302`     | `TypeMismatch`              | argumento, **valor gravado** (`w.width = "900"`) ou valor num dict de `update` com tipo errado; `update` com algo que não é `dict` |
| `E308`     | `IdNotFound`                | **ler** membro que o handle/evento não tem (gravar é E716)                      |
| `E313`     | `ReadOnlyProperty`          | gravar um membro **somente leitura** (`el.id = "x"`, `w.scale = 2`, `e.x = 1`, `el.style = {…}`) ou pôr uma chave só de leitura em `update`. A entrada do catálogo (Cap. 36.7 e 37) cobre também membros somente leitura de objetos nativos. |
| (Cap. 19.5) | `ImmutableMutation`      | `el.classes.add("x")`: `classes` lê uma tupla                                  |
| `E502`     | `MissingNamedArgument`      | `canvas.window()` sem `"id"`                                                   |
| `E503`     | `UnknownNamedArgument`      | argumento que um **construtor** (ou função do módulo) não declara — **não** mais o `update`, que recebe dict |
| `E504`     | `PositionalForNamedOnly`    | `canvas.window("main")`                                                        |

### Erros

Todos acontecem na **execução** (etapa 8) e, portanto, são **recuperáveis** com `try`/`catch`.

#### Janela (E701–E707)

| **Código** | **Nome**             | **Recup.** | **Mensagem**                                                              | **Dica**                                                                   |
|------------|----------------------|------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `E701`     | `InvalidWindowId`    | Yes        | The window id "meu app" is not valid: it cannot be empty or contain spaces. | use a non-empty text without spaces, for example: "meu-app".             |
| `E702`     | `WindowIdDuplicate`  | Yes        | A window with the id "main" is already open.                              | choose another id, or close the first window before creating a new one.    |
| `E703`     | `InvalidWindowSize`  | Yes        | The window width must be at least 1; got 0.                               | use a positive size, for example: "width": 800.                            |
| `E704`     | `WindowNotFound`     | Yes        | There is no open window with the id "main".                               | check the id, or create the window with canvas.window first.               |
| `E705`     | `NoDisplay`          | Yes        | No display is available to open a window.                                 | run in a desktop session, or create the window with "headless": true.      |
| `E706`     | `StaleHandle`        | Yes        | This element was removed (or its window was closed) and can no longer be used. | create the element again, or keep using the handle only while it exists. |
| `E707`     | `CrossWindowMove`    | Yes        | An element cannot be moved to a different window.                         | create a new element in the target window instead.                         |

#### Elementos e consulta (E710–E715)

| **Código** | **Nome**             | **Recup.** | **Mensagem**                                                              | **Dica**                                                                   |
|------------|----------------------|------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `E710`     | `ElementIdDuplicate` | Yes        | An element with the id "t" already exists in this window.                 | choose another id; ids must be unique inside a window.                     |
| `E711`     | `InvalidElementId`   | Yes        | The element id "a b" is not valid: it cannot be empty or contain spaces.  | use a non-empty text without spaces, for example: "a-b".                   |
| `E712`     | `ElementNotFound`    | Yes        | No element with the id "nada" was found.                                  | check the id, or use query(...) when the element may not exist.            |
| `E713`     | `InvalidSelector`    | Yes        | The selector "box >" is not valid: a selector is missing after '>'.       | write a selector such as ".card > text"; see the supported selectors.      |
| `E714`     | `ImageLoadError`     | Yes        | The image "logo.png" could not be loaded: file not found.                 | check the path and the file format (PNG or JPEG).                          |
| `E715`     | `CyclicMove`         | Yes        | An element cannot be moved inside itself or one of its descendants.       | move it to an element that is not part of its own subtree.                 |

#### Atributos: gravação e `update` (E716)

| **Código** | **Nome**             | **Recup.** | **Mensagem**                                                              | **Dica**                                                                   |
|------------|----------------------|------------|---------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `E716`     | `UnknownAttribute`   | Yes        | The element kind "text" has no attribute "value".                         | did you mean 'text'? Attributes of "text": text, classes, label, scroll-x, scroll-y. |

Vale para `el.value = …` e para a chave desconhecida em `update({...})` (em elemento, janela). Para a janela a mensagem diz *The window has no attribute "cor"*. A **leitura** do mesmo nome continua `IdNotFound` (E308): a spec já tem esse erro para leitura, e a gravação é o caso novo.

Exemplo de `ReadOnlyProperty` (E313) adaptado a este uso: *The attribute "id" is read-only and does not accept assignment.* — dica: *read the value instead; an id cannot change after creation.* Para membros que o motor controla (`focused`): *use el.focus() to move the focus.*

#### Estilo (E720–E723)

Acontecem **quando o estilo é aplicado** (`style`, `rules`, `css`, ou o parâmetro `"style"`). Não valem para `update`, que não aceita `"style"`. A análise estática pode antecipá-los quando o dict é literal. Em **`w.css`**, o bloco de erro traz a **linha e as colunas dentro do texto CSS** e o nome dado em `"source"` (Capítulo 47); `w.css` é **estrito**: o primeiro erro interrompe e **nenhuma** regra é registrada.

| **Código** | **Nome**                | **Recup.** | **Mensagem**                                                       | **Dica**                                                                          |
|------------|-------------------------|------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| `E720`     | `UnknownStyleProperty`  | Yes        | The style property "colour" does not exist.                        | did you mean 'color'? Otherwise check the list of supported properties.           |
| `E721`     | `InvalidStyleValue`     | Yes        | The value "wide" is not valid for the property "width".            | use a number (pixels), a text such as "50%", or "auto".                           |
| `E722`     | `UnsupportedStyle`      | Yes        | The value "grid" for "display" is valid CSS but not supported yet. | use "block" or "flex"; see what is outside this version in the style chapter.     |
| `E723`     | `CssSyntaxError`        | Yes        | The block opened with "{" is never closed.                         | add a "}" at the end of the rule. *(só `w.css`: chave sem fechar ou a mais, `;` ou `:` faltando, comentário `/*` aberto, seletor/propriedade/valor vazio)* |

#### Eventos e laço (E730–E735)

| **Código** | **Nome**               | **Recup.** | **Mensagem**                                                       | **Dica**                                                                          |
|------------|------------------------|------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| `E730`     | `UnknownEventKind`     | Yes        | The event kind "clik" does not exist.                              | did you mean 'click'? Otherwise check the list of event kinds.                    |
| `E731`     | `InvalidHandler`       | Yes        | A handler must be a function with 0 or 1 parameter; got 2 parameters. | write f(e) to receive the event, or f() to ignore it, for example: el.on("click", f(e) ...). |
| `E732`     | `RunReentrant`         | Yes        | canvas.run(), canvas.poll() or canvas.advance() was called while the loop is already running. | do not call the loop from inside a handler; use canvas.after for delayed work. |
| `E733`     | `InvalidTimerInterval` | Yes        | The timer interval must be positive for every(); got 0.            | use a positive number of seconds, for example: canvas.every(0.5, ...). *(também `advance` com segundos < 0)* |
| `E734`     | `HeadlessOnly`         | Yes        | dispatch() is only available in headless windows; the window "main" is not headless. | create the window with "headless": true to test it without a screen. *(Capítulo 51)* |
| `E735`     | `InvalidDispatch`      | Yes        | The event data for "keydown" has no key "chr"; keys of "keydown": key, repeat, shift, ctrl, alt, meta. | check the keys of the event kind; "frame" and "timer" cannot be dispatched, use canvas.advance. |

### Avisos (W701–W705)

Avisos **não interrompem** o programa e podem ser escondidos com `#~ hide Wnnn` (Cap. 3.1.1).

| **Código** | **Nome**           | **Mensagem**                                                                 | **Dica**                                                                          |
|------------|--------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| `W701`     | `StyleHasNoEffect` | "flex-grow" has no effect here: the parent is not a flex container.           | set "display": "flex" on the parent, or remove the property. *(também `scroll-x`/`scroll-y` num elemento sem `overflow: scroll\|auto`: "scroll-y" has no effect here: the element does not scroll. — dica: set "overflow": "auto".)* |
| `W702`     | `SlowHandler`      | The handler for "click" took 0.8 s; the window was frozen meanwhile.          | avoid pause, readln and long loops in handlers; split the work or use canvas.after. |
| `W703`     | `FontFallback`     | The font family "Comic" was not found; "sans" was used instead.               | install the font, or use "sans", "serif" or "mono".                               |
| `W704`     | `NotCancelable`    | e.prevent() has no effect: "pointermove" events cannot be canceled.           | remove the call, or listen to an event that can be canceled. *(também o `close` entregue por `canvas.quit()`, que não é cancelável)* |
| `W705`     | `NotFocusable`     | The element "campo" cannot receive focus: it is disabled.                     | enable it, make it visible, or set "focusable": true on a box. *(o foco não muda)* |

### Exemplo de bloco completo

No mesmo formato do Cap. 36.7:

```text
=== UnknownStyleProperty (E720) PROBLEM ===

We found a problem in the file:
C:\Projetos\app.tpine

    9 | const t = w.text("oi", "id": "t")
|> 10 | t.style({"colour": "red"})
                 ^^^^^^^^
   11 | canvas.run()

Line 10, characters 10 to 17.
Recoverable error with try.

The style property "colour" does not exist.

Hint: did you mean 'color'? Otherwise check the list of supported properties.

=== END ERROR ===
```

A dica *did you mean* usa o mesmo mecanismo de distância de edição (≤ 2) que a spec já define para `IdNotFound` (Cap. 36.7), aplicada à lista de propriedades de estilo, de tipos de evento e de nomes de argumento.
