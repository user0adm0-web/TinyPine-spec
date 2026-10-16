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
