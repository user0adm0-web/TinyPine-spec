## Sistema de Identificadores (id)

Identificadores permitem declarar um bloco de forma nomeada; a resolução de nomes acontece numa etapa de **Registro de IDs** que precede a etapa de Execução (ver Capítulo 35), o que permite que um identificador seja registrado independentemente da ordem textual em que aparece.

### Declaração

```tinypine
id("msg")
  print("olá")
# print executa normalmente
```

### Referência a um Identificador

```tinypine
id-do("msg")
  print("olá")
# print executa normalmente
```

### Registro de IDs

O interpretador registra todo identificador durante o *parsing*, antes da etapa de Execução — por isso um identificador pode, em princípio, ser referenciado a partir de qualquer ponto do programa, independentemente da ordem textual da declaração. Essa etapa de registro independe de o bloco correspondente ser efetivamente executado.

### Propriedades dos Identificadores

- **Identificadores são imutáveis após a criação.**

- **Identificadores são registrados durante o *parsing*, independentemente de o bloco correspondente ser efetivamente executado.**

- **Identificadores duplicados geram** `IdDuplicate PROBLEM`**.**

- **Referenciar um identificador inexistente interrompe a execução.**

- **A sintaxe para referenciar um identificador já declarado está pendente de nova definição (28.2).**

```tinypine
|| ID duplicado ||
id("spawn")
  print("A")
id("spawn")
  print("B")
# → IdDuplicate PROBLEM
```
