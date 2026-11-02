## Laços de Repetição

Além dos blocos especiais `repeat()` (Capítulo 27) e `loop()` (Capítulo 29.3), o TinyPine define as construções clássicas de repetição `while()` e `for()`, além das instruções de controle de fluxo `break()` e `continue()`.

### while

Executa o bloco repetidamente enquanto a condição informada permanecer verdadeira.

```tinypine
var ativo = true
while ativo
  print("rodando")
  ativo = false
```

### for — Iteração sobre Coleções e Intervalos

O `for` itera sobre uma coleção ou intervalo. Diferente do `while`, ele avança sozinho: a cada ciclo a variável de iteração recebe o próximo elemento.

Sintaxe básica:

```tinypine
for i in lista
  print(i)
```

Para intervalos numéricos usa-se a forma `[início to fim]`:

```tinypine
for i in [1 to 10]
  print(i, " ")
# Saída: 1 2 3 4 5 6 7 8 9 10
```

#### Parâmetros

O `for` aceita parâmetros nomeados no mesmo estilo das funções (`nome=value` ou `"nome": value`). Os parâmetros oficiais são:

| Parâmetro | Padrão | Efeito |
|-----------|--------|--------|
| `start`   | início da coleção/intervalo | Valor inicial da iteração |
| `end`     | fim da coleção/intervalo    | Valor final (inclusive) |
| `step`    | `1`                         | Incremento entre elementos |

Exemplos:

```tinypine
|| passo de 2 ||
for i in [1 to 10], step=2
  print(i, " ")
# Saída: 1 3 5 7 9

|| contagem regressiva ||
for i in [10 to 1], step=-1
  print(i, " ")
# Saída: 10 9 8 7 6 5 4 3 2 1

|| start e end explícitos sobre lista ||
var lista = ["a", "b", "c", "d", "e"]
for i in lista, start=1, end=3
  print(i)
# Saída: b c d
```

Quando `start`, `end` ou `step` são usados sobre uma lista, eles atuam sobre os índices (0-based). Quando usados sobre um intervalo `[a to b]`, atuam diretamente sobre os valores.

#### Modo Gerador (Stream / Generator)

Quando `for` é usado dentro de uma função combinado com a instrução `emit`, ele assume o comportamento de um produtor de fluxo (*stream*). `emit` não encerra a função no primeiro ciclo: emite o valor atual e aguarda o próximo passo do laço. Quando o `for` esgota os elementos, o interpretador emite um sinal interno de finalização, e o chamador encerra graciosamente.

```tinypine
f contagem()
  for i in [1 to 100]
    emit(i)
print(contagem(), "last": " ")
# Saída: 1 2 3 ... 99 100 (em série, ciclo a ciclo)
```

Fluxo do modo gerador:

- **O chamador (por exemplo,** `print`**) inicia uma escuta ativa sobre a função geradora.**

- `emit(A)` **emite o valor para o chamador, que o consome imediatamente.**

- **Esse processo se repete até que o** `for` **esgote os elementos.**

- **Condição de parada: ao esgotar a coleção/intervalo,** `for` **emite o sinal interno** `done`**, encerrando a execução do chamador de forma graciosa.**

**emit não depende do tipo de laço.** O que torna a função um gerador é a presença de `emit` no seu corpo, não o laço usado: `emit` funciona com `for`, com `while` e fora de qualquer laço. A função é executada sob demanda, e cada `emit` entrega um valor ao chamador.

```tinypine
f pares(e)
  while e < 12
    e = e + 2
    emit e
print(pares(2), "last": " ")   # 4 6 8 10 12
```

**Como print e println consomem o fluxo.** Os dois leem o fluxo em série, valor a valor, e escrevem cada valor seguido do `last`. Em `print` o `last` padrão é vazio, por isso, sem `"last"`, os valores saem colados; em `println` o padrão é a quebra de linha, um valor por linha.

```tinypine
print(pares(2))                  # 4681012 — sem separador, os valores saem colados
println(pares(2))                # um valor por linha: 4, 6, 8, 10, 12
```

**Quando o fluxo não é consumido em série.** O consumo em série só vale quando a chamada do gerador é o **único argumento posicional** de `print` ou `println`; os nomeados `last`, `sep` e `flush` podem acompanhá-la. Em qualquer outro uso — outros argumentos posicionais, atribuição, argumento de outra função — a função roda até o fim e a chamada devolve a lista dos valores emitidos (regra registrada em Apêndice A.2, B23).

```tinypine
var L = pares(2)                        # [4, 6, 8, 10, 12]
print("| ", pares(2), "last": " | ")    # imprime: | [4, 6, 8, 10, 12] | 
```

### break() e continue()

`break(condição)` e `continue(condição)` aceitam o parêntese opcional, no mesmo estilo de `if`/`while`/`return`/`pause`/`repeat` (Capítulo 4.6): `break condição` e `continue condição`. Sem argumento, o efeito é incondicional: `break` sozinho equivale a `break true`.

| **Instrução** | **Efeito**                                                                                                                                                      |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `break()`     | Interrompe imediatamente o laço atual. Quando chamado com o argumento `true`, o efeito é aplicado condicionalmente (equivalente a `if condição: break() --`).   |
| `continue()`  | Interrompe a iteração atual e avança para a próxima. Quando chamado com o argumento `true`, o efeito é aplicado condicionalmente, no mesmo padrão de `break()`. |
