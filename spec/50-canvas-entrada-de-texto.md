## Canvas — Entrada de Texto

### O problema

Para quem escreve em português, `ç`, `ã`, `é`, `ê` costumam vir de **duas teclas** (um acento "morto", depois a letra) ou de uma **composição** do sistema. A tecla que se aperta **não é** o texto que se digita. Se o campo editasse por `keydown`, ele poderia errar exatamente no idioma do programador.

### Dois eventos para duas perguntas

Dois eventos diferentes, para duas perguntas diferentes:

| **Evento**           | **Responde**                  | **Dado**                                | **Quando**                                                      |
|----------------------|-------------------------------|-----------------------------------------|-----------------------------------------------------------------|
| `keydown` / `keyup`  | "qual **tecla física**?"      | `e.key` (nome de `computer.keyboard`), `e.repeat`, modificadores | a tecla desce / sobe (inclusive Enter, Tab, setas, F1…) |
| **`textinput`**      | "que **texto** foi produzido?" | `e.text` (`str`, **já composta**)       | o usuário produziu texto; **é o que o `input` insere**          |

- Alvo e propagação: os do teclado (elemento focado; sem foco, a janela; sobe pela árvore). **Cancelável.**
- **`e.text` nunca é vazio e nunca contém caractere de controle** (`\n`, `\t`, `\b`, escape, `\x7f`): Enter, Tab, Backspace e Delete são **teclas** (`keydown`), não texto.
- **`e.text` pode ter mais de um caractere**: uma composição de IME, ou — no Windows — o caso em que a tecla morta não combina com a seguinte e o sistema entrega os dois caracteres. Um filtro deve olhar o texto **inteiro**, não o primeiro caractere.
- Um `keydown` que produz texto é seguido (se o alvo é focável e ninguém cancelou) pelo `textinput` correspondente. Teclas que não produzem texto (setas, Enter, F1, uma tecla morta sozinha) **não** geram `textinput`.
- **`e.prevent()` num `keydown` suprime o `textinput` daquela tecla** (como no DOM, em que cancelar `keydown` cancela o texto). `e.prevent()` no `textinput` suprime só a **inserção**.

```tinypine
use canvas

const w = canvas.window("id": "form", "name": "Idade")
const campo = w.input("", "id": "idade", "placeholder": "idade")

campo.on("textinput", f(e)
  if not (e.text in "0123456789")
    e.prevent()                 # "12a" colado também é recusado inteiro
)
campo.on("change", f(e)
  println(format "idade: {e.value}")
)
canvas.run()
```

### O que o `input` faz

| **Evento no `input` focado**                    | **Ação padrão**                                                                                |
|-------------------------------------------------|------------------------------------------------------------------------------------------------|
| `textinput`                                     | insere `e.text` no cursor; dispara `input` (com `e.value` novo)                               |
| `keydown` `"backspace"` / `"delete"`            | apaga antes / depois do cursor; dispara `input`                                                |
| `keydown` `"left"` / `"right"` / `"home"` / `"end"` | move o cursor                                                                              |
| `keydown` `"enter"`                             | dispara `change` se o texto mudou desde que o campo ganhou o foco                             |

Seleção por teclado e copiar/colar via área de transferência fazem parte do `input`; **o texto colado chega como um `textinput`** (e por isso o filtro de dígitos acima recusa uma colagem `12a` inteira). **Fora desta versão**: **pré-edição de IME** (o sublinhado do japonês/chinês enquanto se compõe) e texto bidirecional. Teclas de seleção e atalhos (Shift+setas, Ctrl+A/C/V) são ações padrão do `keydown` no `input` e **não** geram `textinput`, salvo o Ctrl+V.

### Origem do texto

O texto composto pode chegar do sistema por caminhos diferentes: o texto da própria tecla, uma composição de IME confirmada, uma colagem. O motor os junta em **um único** evento `textinput`, de modo que o programa não depende do caminho. Como cada sistema entrega `ã`/`ç` (Windows, Linux, macOS) ainda precisa ser conferido em teclados reais, por exemplo o ABNT2 (Apêndice A, B33).

Um teste **sem tela** não simula tecla morta: `w.dispatch("textinput", {"text": "ã"})` entrega o texto já composto (Capítulo 51).
