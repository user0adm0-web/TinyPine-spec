## case e match — Controle de Fluxo em Cascata

A estrutura `case`, aberta por `match`, permite avaliar uma expressão contra múltiplos padrões estruturais, eliminando a necessidade de quedas de fluxo (*fallthrough*) ou do uso obrigatório de `break`. Por focar na relação estrutural entre padrões, blocos `case`/`match` podem ser aninhados para formar árvores de checagem profunda e filtragem em cascata.

### Sintaxe Básica

```tinypine
var estadoTerminal = "seguranca": to-str
case estadoTerminal
  is "seguranca"
    print("Monitores ativos. Modo normal.")
  is "pesadelo"
    print("ALERTA: Modo NIGHTMARE!")
  else
    print("Terminal offline.")
```

### Aninhamento Estrutural (Filtragem em Cascata)

Quando um bloco `case` é inserido dentro de um escopo `match`, o interpretador altera o contexto de avaliação para a nova expressão fornecida, permitindo validações compostas sem poluição visual adicional.

```tinypine
|| Exemplo de validação combinada em árvore ||
case "t"
  is "t"
    case ""
      ""
        print("BLZ")
```

### Regras de Execução e Escopo

- **Sem fallthrough: a execução de um bloco** `match` **é isolada. Ao atingir o final do bloco (o recuo volta ao nível do case pai), o interpretador salta automaticamente para o fim do bloco** `case` **pai, impedindo a execução acidental dos casos seguintes.**

- **Omissão de else: o bloco** `else` **é opcional. Caso nenhum padrão corresponda e** `else` **não esteja presente, o bloco** `match` **é encerrado de forma segura, como uma operação neutra (*Noop*) — mas o interpretador emite um** `MatchWithoutElse WARNING`**.**

### Casos de Borda

| **Caso**                          | **Comportamento formal**                                                                   |
|-----------------------------------|--------------------------------------------------------------------------------------------|
| Múltiplos `else` no mesmo `match` | `MultipleElseMatch PROBLEM` — um bloco lógico `case` aceita no máximo uma cláusula padrão. |

### Múltiplos Operadores

```tinypine
case estadoTerminal
  is "pesadelo"
    print("ALERTA: Modo NIGHTMARE!")
  in ["seguranca", "normal", "padrao"]
    print("Monitores ativos. Modo normal.")
  in [1 to 5]
    print("Código de manutenção emergencial.")
  < 0
    print("Valor negativo detectado!")
  else
    print("Terminal offline.")
```
