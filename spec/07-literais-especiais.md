## Literais Especiais

Além dos seis tipos primitivos escalares, o TinyPine define quatro literais especiais, com semântica própria.

### Null — Valor Nulo

Representa a ausência intencional de valor, atribuída explicitamente pelo programador.

```tinypine
var valor = null
f A(ee)
  print(ee) # retorno não especificado é null

f B(d): void
  print(d ** d) # retorno especificado como void, não é preciso return
```

### void — Valor Não Definido pelo Usuário

`void` é distinto de `Null`: representa a ausência de valor gerada **implicitamente** pelo interpretador, quando o programador não forneceu um valor onde um era esperado. Toda ocorrência implícita de `void` é acompanhada de um aviso (*ImplicitVoid WARNING*), para tornar visível que o programa depende de um comportamento implícito, e não de uma escolha explícita — a linguagem prefere o uso de `Null` explícito nesses casos.

```tinypine
var valor    # gera void implicitamente, com ImplicitVoid WARNING
             # (preferir "var valor = Null" quando a ausência de valor for intencional)

print()      # gera void implicitamente, com ImplicitVoid WARNING

f A(ee)
  print(ee) # retorno não especificado
```

### NaN — Valor Não Numérico

Representa o resultado de uma operação numericamente indefinida. Ocorre principalmente como resultado de erros e comparações, não como um valor tipicamente atribuído pelo programador.

```tinypine
var valor = 0/0  # DivisionByZero PROBLEM
```
