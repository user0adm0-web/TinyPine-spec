## Análise Estática de Código

### Detecção de Variáveis Não Utilizadas

O analisador estático identifica variáveis declaradas e nunca utilizadas, ajudando a localizar código morto ou erros de digitação em nomes de variáveis.

```tinypine
var nome = "Ana"
print("Olá")
# gera aviso:
# UnusedVariable (W201) WARNING — Variable "nome" was declared but never used.
```

- **Não impede a execução do programa — é um aviso (**`Warning`**), não um erro.**

- **A análise considera o escopo da variável, não o programa inteiro.** Cada leitura é ligada à declaração visível naquele ponto, e só essa conta como usada: o mesmo nome em outro escopo não "salva" uma variável que nunca é lida.

- **Só leituras contam como uso.** Atribuir a uma variável (`x = 2`) não a usa; ler o seu valor, usá-la dentro de um texto `format "{x}"` ou chamá-la (quando guarda uma função) usa.

- **Não gera aviso:** parâmetros de função, a variável de um `for`, a variável do `catch`, campos de classe, e variáveis de um programa que usa `import` (Capítulo 29.3), cujo escopo global é compartilhado com outros arquivos. O terminal interativo também não avisa, porque cada entrada é analisada sozinha.

- **Na dúvida, não avisa.** Uma leitura que não encontra declaração visível naquele ponto (por exemplo, uma função escrita antes da variável global que ela lê) conta como uso de toda variável com aquele nome.

```tinypine
var x = 1            # UnusedVariable: este x nunca é lido
f usa()
  var x = 5          # UnusedVariable: este também (o x de fora não é o dele)
  var y = 7
  println(y)         # usa y
```

### Detecção de Código que Nunca é Executado

O analisador também avisa de código que, pela estrutura do programa, nunca roda. Todos os casos abaixo emitem `UnreachableCode (W203) WARNING` ou `UnusedFunction (W204) WARNING`, não interrompem a execução e podem ser escondidos com `#~ hide the W203` / `#~ hide the W204` (Capítulo 3.1.1).

**Código depois de uma saída (`UnreachableCode`).** A primeira instrução depois de `return`, `throw`, `break` ou `continue` incondicionais, no mesmo bloco, nunca é executada. O mesmo vale depois de um `if` com `else` em que **todo** ramo termina em uma dessas instruções. `break` e `continue` com condição (`break x > 3`) só saem às vezes e não encerram o fluxo. Só a primeira instrução morta é marcada.

```tinypine
f a()
  return 1
  println("nunca")   # UnreachableCode: it comes after a return
```

**Condição constante (`UnreachableCode`).** Quando a condição é o literal `false`, o bloco de `if false` e o de `while false` nunca executam; quando é o literal `true`, o `else` de `if true` nunca executa. `while true` não gera aviso: laço infinito é uma escolha comum.

```tinypine
if false
  println("nunca")   # UnreachableCode: the condition is always false
```

**Função nunca chamada (`UnusedFunction`).** Uma função declarada fora de classe, que não é chamada nem usada como valor (`var g = f`, `aplica(f, 3)`, `x |> f`) em nenhum ponto do programa, gera o aviso. Uma chamada a si mesma, dentro do próprio corpo, não conta como uso. Métodos de classe nunca geram o aviso; e, como em `UnusedVariable`, ele não é emitido em programas com `import` nem no terminal interativo.

```tinypine
f nunca(n)           # UnusedFunction: Function 'nunca' was declared but never called
  return n * 2
```

### Verificações de Concorrência

O analisador também confere o uso das construções do Capítulo 42. Como as demais verificações, **na dúvida não avisa**, e todo aviso pode ser escondido com `#~ hide`.

| **Verificação**                                                                                                  | **Resultado**                      |
|------------------------------------------------------------------------------------------------------------------|------------------------------------|
| `await` dentro de uma função que não é `async` (e fora do nível de cima do programa)                             | `AwaitOutsideAsync PROBLEM` (E801) |
| `with parallel` com uma instrução que não é uma chamada                                                          | `InvalidParallelBody PROBLEM` (E802) |
| `select` com `else` e `when timeout`, com mais de um `else`, ou sem braços                                       | `InvalidSelect PROBLEM` (E803)     |
| `await` sobre um valor que, pelo texto, não é aguardável (um literal, uma `str`, uma lista)                      | `NoopAwait WARNING` (W801)         |
| criar uma tarefa fora de `scope`/`with parallel`, sem guardar o handle, sem `await` e sem `detach()`              | `DiscardedTask WARNING` (W802)     |
| `readln()` ou `os.read(...)` (e as demais suspensíveis, 42.14.4) **sem** `await` dentro de função `async`        | `BlockingCall WARNING` (W803)      |
| escrever numa `var` de fora, sem `lock`, dentro de uma função lançada com `thread`                               | `UnprotectedSharedWrite WARNING` (W804) |
| braços de `select` escritos depois de um `else`                                                                  | `UnreachableCode WARNING` (W203)   |

```tinypine
var total = 0
f soma(n)
  repeat n
    total = total + 1       # UnprotectedSharedWrite: escrita sem lock numa função lançada com thread

var t = thread soma(1000)
```

A verificação de `UnprotectedSharedWrite` é uma heurística sobre o texto: considera apenas atribuições e métodos de mutação diretos sobre uma variável de fora do corpo da função, e não acompanha a variável por dentro de outras funções.

### Autocompletar do Editor (fora do interpretador)

Recursos de autocompletar — por exemplo, inserir automaticamente o recuo esperado ao abrir um bloco, ou detectar e sinalizar mistura de TAB e espaço enquanto o programador digita — são recursos do editor/IDE do TinyPine, e não do interpretador. Eles apenas auxiliam a escrita: não alteram a lógica do programa, e podem ser desativados pelo programador.

Os capítulos desta parte documentam áreas da linguagem que ainda não possuem especificação fechada. Eles são mantidos separados do restante do documento justamente para deixar explícito, à primeira vista do índice, quais partes da linguagem são normativas hoje e quais ainda estão em desenho.
