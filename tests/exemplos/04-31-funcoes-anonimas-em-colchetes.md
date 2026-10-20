# Exemplos executáveis — função anônima em colchetes (caps. 4.11, 19.2.2, 30.6, 31.3)

Cada par `tinypine run` + `output` é executado por `tools/run_examples.py`.

Objeto "console" em um dicionário: corpo por indentação dentro de `{ }` (4.11), `package` + `unpack` (30.6),
leitura da função por índice e por ponto (19.2.2) e chamada pela variável (31.3):

```tinypine run
var console = {"log": f(package ARGS)
  print(unpack ARGS)
}
const write = console["log"]
var Write = console.log
write(1, 2, 3)
print(" ")
write(2 ** 6)
print(" ")
Write(2 ** 6)
```

```output
123 64 64
```

Dois membros: a linha do `f` está no recuo 2, o corpo no recuo 4, e a linha da vírgula encerra o primeiro corpo:

```tinypine run
var ops = {
  "soma": f (a, b)
    return a + b
  ,
  "dobro": f (x)
    return x * 2
}
var soma = ops["soma"]
var dobro = ops.dobro
println(soma(2, 3))
println(dobro(4))
```

```output
5
8
```

Estilo `do` ... `--` dentro do dicionário, e leitura por ponto (19.2.2):

```tinypine run
var D = {"dobro": f (x) do return x * 2 --}
var F = D["dobro"]
var G = D.dobro
print(F(4), G(5))
```

```output
810
```

Função como argumento, com mais argumentos depois do corpo (a linha da vírgula volta ao recuo do `f`):

```tinypine run
f aplica(fn, a, b) do return fn(a, b) --
println(aplica(f (x, y)
  var t = x * y
  return t + 1
, 3, 4))
```

```output
13
```

Repasse de argumentos com `package` + `unpack` (30.6), fora de qualquer coleção:

```tinypine run
f repassar(package ARGS)
  print(unpack ARGS)
repassar(1, 2, 3)
```

```output
123
```
