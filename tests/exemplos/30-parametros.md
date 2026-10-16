# Exemplos executáveis — parâmetros (cap. 30)

Cada par `tinypine run` + `output` é executado por `tools/run_examples.py`
(`println(a, b)` imprime sem separador).

Nomeados obrigatórios depois de `!`, com valor padrão opcional:

```tinypine run
f GP(!, "A": e = 5, "B": k)
  println(e, k)
GP("B": 1)
GP("B": 2, "A": 9)
```

```output
51
92
```

Marcador `?` (posicionais ligados por tipo, em qualquer ordem) combinado com `!`:

```tinypine run
f T(?, e: str, u: int, !, "nome": N)
  println(e, u, N)
T(7, "oi", "nome": "x")
T("oi", 7, "nome": "x")
```

```output
oi7x
oi7x
```
