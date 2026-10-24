# PARTE V — VARIÁVEIS E DADOS ESTRUTURADOS

## Variáveis

### Declaração Local e Global

Por padrão, uma variável é local ao escopo do bloco em que é declarada. O prefixo `$` no identificador declara a variável no escopo global.

| **Escopo**     | **Sintaxe**  |
|----------------|--------------|
| Local (padrão) | `var A = 5`  |
| Global         | `var $A = 5` |

### Imutabilidade — var e const

`const` substitui `var` na declaração para impedir a reatribuição do identificador — não apenas da referência (ver Capítulo 19.5 para coleções). A regra de escopo (local/global) se combina livremente com a de mutabilidade:

| **Forma**       | **Sintaxe**    |
|-----------------|----------------|
| Local mutável   | `var A = 5`    |
| Local imutável  | `const A = 5`  |
| Global mutável  | `var $A = 5`   |
| Global imutável | `const $A = 5` |

### Inserção e Edição em Variáveis

Sobre valores numéricos, a edição in-place é feita por meio de operações do próprio valor, seguida de reatribuição:

```tinypine
var A = 5
A = A.add(6)
print(A)
# → 56
```

Sobre strings, é possível atribuir diretamente a uma posição de índice para inserir conteúdo a partir daquele ponto:

```tinypine
var A = "olá, "
A[5] = " Usuário!!"
print(A)
# → olá, Usuário!!
```

O intervalo `[início to fim]` segue a regra de fatia do Capítulo 19.2.1: as duas pontas são incluídas, e um limite negativo conta a partir do fim.

### Remoção em Variáveis

A remoção de um único caractere por índice, sobre uma string, é feita combinando o índice com o método `remove` (Capítulo 16), que remove a primeira ocorrência do valor informado:

```tinypine
var A = 56
A.remove(A[1])
print(A)
# → 5
```

Sobre um intervalo de índices, a remoção é feita atribuindo-se a string vazia ao intervalo `[início to fim]`:

```tinypine
var A = "olá, Usuário!!"
A[3 to 13] = ""
print(A)
# → olá,
 
var A = "olá, Usuário!!"
A[4 to 13] = ""
print(A)
# → olá
```
