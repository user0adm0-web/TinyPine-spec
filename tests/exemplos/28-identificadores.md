# Exemplos executáveis — identificadores (cap. 28)

Cada par `tinypine run` + `output` é executado por `tools/run_examples.py`
(`println(a, b)` imprime sem separador).

O exemplo do capítulo: `mais` vale o conteúdo de `id mais`, declarado depois (sem aspas e sem `@`):

```tinypine run
println(100 mais 100)

id mais
  +
```

```output
200
```

Registro antecipado: a referência vem antes da declaração, e a declaração por si só não executa nada:

```tinypine run
println("antes")
msg
id msg
  println("olá")
println("depois")
```

```output
antes
olá
depois
```

Um `id` nunca referenciado não roda:

```tinypine run
id nao
  println("não executa")
println("fim")
```

```output
fim
```

O corpo pode ter blocos aninhados e é colado no recuo de onde a referência aparece (aqui, dentro de um `if`
e dentro de uma função):

```tinypine run
id laco
  for i = 1, i <= 2
    println(i)
    i = i + 1
  println("fim do laço")
f usa()
  laco
if true
  laco
usa()
```

```output
1
2
fim do laço
1
2
fim do laço
```

Um identificador pode usar outro, na forma `do ... --`:

```tinypine run
id a do
  println("A")
--
id b do
  a
  println("B")
--
b
```

```output
A
B
```

Comentários dentro do corpo não fazem parte do conteúdo, e o texto de uma string não é expandido:

```tinypine run
id soma  # comentário na linha da declaração
  + || comentário no meio do corpo ||
println(1 soma 2)
println("soma")
```

```output
3
soma
```
