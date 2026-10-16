## repeat — Bloco de Repetição

`repeat n` é sempre um bloco autônomo, que abre seu próprio escopo pela indentação e repete a execução do seu próprio conteúdo *n* vezes, agindo somente para frente (ver Capítulo 23). O parêntese é opcional, no mesmo estilo já adotado em `if`/`while`/`return`/`break`/`continue`/`pause` (Capítulo 4.6) — `repeat(n)` e `repeat n` são equivalentes; esta especificação usa a forma sem parênteses.

```tinypine
repeat 3
  print("oi")
```

### Aninhamento de repeat (Multiplicação)

Quando um bloco `repeat` é aninhado dentro de outro, a repetição do bloco interno ocorre a cada iteração do bloco externo — o total de execuções é o produto dos dois valores.

```tinypine
repeat 2
  repeat 3
    print("A")
# Resultado: 2 × 3 = 6 execuções
```
