## Concorrência:

```tinypine
async
await
thread
parallel
```

### Funções Assíncronas — f async

Uma função pode ser declarada como assíncrona com o prefixo `async` após a palavra-chave `f`:

```tinypine
f async buscarDados()
  print("Começou a buscar...")

  var resposta = await fetch("https://jsonplaceholder.typicode.com/todos/1")
  var dados = await resposta.json()

  print("Dados recebidos:", dados)
  return dados;
```

`Funções async` podem usar o operador `await` e retornam implicitamente um valor aguardável (Promise / Future / Task).

### Operador await

O operador `await` espera o resultado de uma operação assíncrona.

**Diferença fundamental em relação a pause:**

| **Comando**       | **O que faz**                                 | **Escopo do bloqueio** | **Outras partes do programa podem continuar?** |
|-------------------|-----------------------------------------------|------------------------|------------------------------------------------|
| `pause n`         | Espera um intervalo de tempo (em segundos)    | Toda a execução        | Não                                            |
| `await expressão` | Espera o resultado de uma operação assíncrona | Apenas a função atual  | Sim                                            |

`await` só tem efeito real quando a expressão à direita é assíncrona. Usar `await` sobre uma expressão puramente síncrona (ex.: `100**9`) não produz o comportamento esperado de concorrência.

Exemplo correto:

```tinypine
f async exemplo()
  print("1 - Começou")

  var A = await tarefaPesada()     # pausa apenas esta função

  print("2 - Resultado chegou:", A)
  print("3 - Continuou depois do await")

f async tarefaPesada()
  pause 2                          # ou qualquer operação assíncrona real
  return 100**9;

exemplo()
print("Isso pode aparecer enquanto tarefaPesada ainda está em execução")
```

### Threads — thread

Threads permitem execução paralela real (em outro núcleo, quando disponível):

```tinypine
thread calcularFibonacci(n)
  var resultado = fib(n)
  return resultado;

var t = thread calcularFibonacci(40)
print("Thread lançada em paralelo...")
var valor = await t
print("Resultado:", valor)
```

O valor retornado por uma `thread` é aguardável com `await`.

### Execução Paralela — parallel

O bloco `parallel` lança múltiplas threads ou tarefas para execução simultânea:

```tinypine
parallel
  thread tarefa1()
    print("Tarefa 1 rodando")
    pause 2

  thread tarefa2()
    print("Tarefa 2 rodando")
    pause 1

print("Todas as threads foram lançadas")
```

### Resumo da Sintaxe:

| **Conceito**       | **Sintaxe TinyPine** | **Observação**                       |
|--------------------|----------------------|--------------------------------------|
| Função assíncrona  | `f async nome() ...` | Pode usar await                      |
| Aguardar resultado | `await expressão`    | Pausa só a função atual              |
| Thread             | `thread nome() ...`  | Execução paralela real               |
| Bloco paralelo     | `parallel ...`       | Lança várias tarefas simultaneamente |
