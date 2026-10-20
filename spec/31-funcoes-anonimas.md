## Funções Anônimas

### Sintaxe e Regras

```tinypine
f (parâmetros)
  statements...
```

> **1.** Uma função anônima não possui identificador próprio: é tratada como um valor de primeira classe (*first-class function*).
>
> **2.** Pode ser atribuída a variáveis, passada como argumento para outras funções, ou retornada por outras funções.
>
> **3.** O bloco segue as mesmas regras de escopo das funções nomeadas (Capítulo 4).
>
> **4.** Assim como nas funções nomeadas (Capítulo 30.2), não há retorno implícito da última expressão: o uso de `return` é obrigatório para devolver um valor. Sem `return` explícito, o valor retornado é `Null`.
>
> **5.** Quando atribuída a uma variável, a variável passa a referenciar a função criada.
>
> **6.** A lista de parâmetros segue as mesmas categorias, a mesma gramática e as mesmas regras de resolução de argumentos das funções nomeadas (Capítulos 30.3 a 30.9).

### Exemplos

```tinypine
var dobro = f (x)
  return x * 2;
```

*Atribuição a variável*

```tinypine
map(lista,
  f (x)
    return x * 2;
)
```

*Uso como argumento*

### Funções Anônimas em Coleções

Como a função anônima é um valor de primeira classe (Capítulo 31.1), ela pode ser guardada em uma lista ou em um dicionário e lida de volta (Capítulo 19.2.2). O corpo por indentação dentro de `{ }` ou `[ ]` segue o Capítulo 4.11; o estilo `do` ... `--` (Capítulo 4.8) também vale. Combinada com `package`/`unpack` (Capítulo 30.6), a função guardada pode repassar argumentos — um objeto "console" em poucas linhas:

```tinypine
var console = {"log": f(package ARGS)
  print(unpack ARGS)
}
const write = console["log"]    # lê a função; não a chama
# ou
var Write = console.log         # leitura por ponto (Capítulo 19.2.2)

write(1, 2, 3)                  # 123
write(2 ** 6)                   # 64
Write(2 ** 6)                   # 64
```

**Chamada direta com ponto.** `console.log(...)` chama a função guardada na chave `"log"` (Capítulo 19.2.2). O exemplo acima funciona também sem a variável intermediária:

```tinypine
console.log("Hello World!")     # Hello World!
console.log(1, 2, 3)            # 123
```

Uma chave ausente é `KeyNotFound PROBLEM`; uma chave que guarda outra coisa que não uma função (`{"x": 1}.x()`) é `TypeMismatch PROBLEM`. Um dicionário de funções serve como objeto leve, mas não é uma instância de classe (Capítulo 32): não há `self`, e as funções guardadas só enxergam o escopo onde foram escritas e os seus parâmetros.

**Ainda não definida.** `console["log"](...)` (índice seguido de parênteses) e a chamada direta de uma função guardada em **lista** continuam sem efeito: o primeiro é `ParserError PROBLEM`; leia o elemento para uma variável e chame a variável. Pendência B26 do Apêndice A.
