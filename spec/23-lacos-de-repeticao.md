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

### for — Iteração com Índice e Passo Manual

Leitura de referência: "para cada valor de 1 até 10, envie para A".

A forma padrão é `for i = 0, i < 10`, sem parênteses (mesmo estilo de `if`/`while`/`return`, Capítulo 4.6). A terceira cláusula (passo) do cabeçalho é opcional: o normal é escrever o passo como *statement* comum na primeira ou última linha do corpo. A forma com passo no cabeçalho também continua válida (Capítulo 23.2.1) — as duas coexistem.

**O** `for` **nunca avança sozinho:** se nada dentro do corpo reatribuir a variável de controle, o laço não termina. Isso vale tanto para a forma com passo no corpo quanto para a forma com passo no cabeçalho.

```tinypine
|| índice simples ||
for i = 0, i < 10
  print(i, " ")
  i = i + 1
# Saída: 0 1 2 3 4 5 6 7 8 9
|| índice + elemento derivado ||
var lista = ["a", "b", "c"]
for i = 0, i < len(lista)
  var e = lista[i]
  print(i, e)
  i = i + 1
|| passo customizado (dois em dois) ||
for i = 0, i < len(lista)
  var e = lista[i]
  print(i, e)
  i = i + 2
|| reverso ||
for i = len(lista) - 1, i >= 0
  var e = lista[i]
  print(i, e)
  i = i - 1
```

#### Forma Avançada — Regra de Passo Customizada

A regra de passo é a terceira cláusula do cabeçalho do `for`. O interpretador usa a expressão informada como fórmula para calcular o próximo valor a cada iteração — permitindo passos não lineares.

```tinypine
var x = 0
for x <= 10, x = x + 2
  print(x)
# Saída: 2 4 6 8 10
 
var B = 0
for B <= 64, B = B * 2: print(x) --
# Saída: 1 2 4 8 16 32 64
 
x = 0
for x <= 91, x = x + 10: print(x) --
# Saída: 1 11 21 31 41 51 61 71 81 91
```

#### Modo Gerador (Stream / Generator)

Quando `for` é usado dentro de uma função combinado com a instrução `emit`, ele assume o comportamento de um produtor de fluxo (*stream*). `emit` não encerra a função no primeiro ciclo: emite o valor atual e aguarda o próximo passo do laço. Quando `for` ultrapassa o limite definido, o interpretador emite um sinal interno de finalização, e o chamador encerra graciosamente.

```tinypine
var A = 0
f contagem(A)
  for A <= 100, A = A + 1
    emit(A)
print(contagem(A), “last”:' ')
# Saída: 1 2 3 ... 99 100 (em série, ciclo a ciclo)
```

Fluxo do modo gerador:

- **O chamador (por exemplo,** `print`**) inicia uma escuta ativa sobre a função geradora.**

- `emit(A)` **emite o valor para o chamador, que o consome imediatamente.**

- **Esse processo se repete até que o limite do** `for` **seja ultrapassado.**

- **Condição de parada: ao ultrapassar o limite,** `for` **emite o sinal interno** `done`**, encerrando a execução do chamador de forma graciosa.**

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
