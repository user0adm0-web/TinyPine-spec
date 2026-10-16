## Conversão Explícita de Tipos — : to-

Cada tipo primitivo aceita conversão explícita no formato `valor: to-tipo`, responsável por converter explicitamente um valor para o tipo indicado. Diferentemente da asserção (Capítulo 6), a conversão **transforma** o valor de entrada quando necessário e possível.

### : to-str — Conversão para Texto

```tinypine
var frase = "olá mundo": to-str
123: to-str    # "123"
true: to-str   # "true"
false: to-str  # "false"
```

### : to-num — Conversão para Numérico Genérico

```tinypine
var idade = 20: to-num
var altura = 1.75: to-num
"123": to-num   # 123
"15.7": to-num  # 15.7
"abc": to-num   # falha de conversão
true: to-num     # 1
false: to-num    # 0
```

### : to-int — Conversão para Inteiro

```tinypine
var n = 42: to-int
3.9: to-int     # 3 — gera PrecisionLoss WARNING (truncamento)
"10": to-int   # 10
```

### : to-float — Conversão para Ponto Flutuante

```tinypine
var x = 3.14159: to-float
3.14159: to-float # 3.14159 — Mantém a precisão dupla IEEE 754
"2.7": to-float # 2.7
3: to-float # 3.0 — Coerção explícita para float
```

### : to-decim — Conversão para Decimal de Alta Precisão

```tinypine
var pi = 3.14159265: to-decim
3.14159265: to-decim # 3.14159265 — Aloca dinamicamente o tamanho exato do literal
```

### : to-bool — Conversão para Lógico

```tinypine
var ativo = true: to-bool
var vazio = false: to-bool
1: to-bool         # true
0: to-bool         # false
"true": to-bool    # true
"": to-bool        # false
var A
A: to-bool       # InvalidConversion PROBLEM — void não pode ser convertido
```
