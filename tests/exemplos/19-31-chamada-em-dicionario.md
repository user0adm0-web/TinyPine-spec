# Exemplos executáveis — chamada de função guardada em dicionário (caps. 19.2.2, 31.3)

Cada par `tinypine run` + `output` é executado por `tools/run_examples.py`.

`D.chave(...)` chama a função anônima guardada na chave (o objeto "console" do Capítulo 31.3):

```tinypine run
var console = {"log": f(package ARGS)
  print(unpack ARGS)
}
console.log("Hello World!")
```

```output
Hello World!
```

Parâmetros, retorno e escopo de criação (a função enxerga `base`, que existe onde ela foi escrita):

```tinypine run
var base = 10
var calc = {
  "soma": f (a, b)
    return a + b
  ,
  "mais_base": f (x)
    return x + base
}
println(calc.soma(2, 3))
println(calc.mais_base(5))
```

```output
5
15
```

Chave ausente e valor que não é função são erros tratáveis:

```tinypine run
var d = {"x": 1}
try do
  d.nada()
--
catch(e) do
  println("sem a chave")
--
try do
  d.x()
--
catch(e) do
  println("nao e funcao")
--
```

```output
sem a chave
nao e funcao
```
