## pause — Pausa da Execução

A instrução `pause segundos` interrompe temporariamente a execução do bloco atual durante um intervalo de tempo especificado. O parêntese é opcional, no mesmo estilo de `if`/`while`/`return`/`break`/`continue` (Capítulo 4.6) — `pause(segundos)` e `pause segundos` são equivalentes; esta especificação usa a forma sem parênteses.

```tinypine
pause 2
print("2 segundos depois")
```

**Dentro de tarefas.** `pause` suspende o **fluxo atual**: num programa sem tarefas ela espera e nada mais roda, como descrito acima; dentro de uma tarefa (função `async` ou nível de cima de um programa com outras tarefas), suspende **só aquela tarefa**, e as demais continuam; dentro de uma `thread`, bloqueia só aquela thread. É um ponto de suspensão e de cancelamento (Capítulo 42.2.5 e 42.4), e a unidade continua sendo o segundo, também no relógio virtual (Capítulo 42.12). Numa função comum chamada por uma tarefa, `pause` bloqueia todas as tarefas e emite `BlockingCall WARNING` (W803).

### Sintaxe e Parâmetros

| **Parâmetro** | **Tipo**                | **Descrição**                                                                |
|---------------|-------------------------|------------------------------------------------------------------------------|
| `segundos`    | `num`, `int` ou `float` | Tempo de pausa em segundos. Valores decimais representam frações de segundo. |

A **unidade oficial de tempo do TinyPine é o segundo**. O interpretador nunca expõe milissegundos como unidade pública da linguagem, mesmo que internamente converta o valor para a API de tempo do sistema operacional hospedeiro.

### Exemplos

```tinypine
pause 1       # aguarda 1 segundo
pause 0.5     # aguarda 0,5 segundo (500 ms)
pause 0.03    # aguarda aproximadamente 30 ms
 
var e=null
var lista = [1 to 5]
for i in lista
  e = lista[i]
  print(e, " ")
  pause 0.2
# Saída: 1 2 3 4 5, com aproximadamente 0,2 segundo entre cada impressão
```

### Precisão

O tempo informado representa o intervalo desejado, em segundos. A precisão real depende do sistema operacional, do temporizador utilizado internamente pelo interpretador e da carga de processamento do computador no momento da execução.

### Casos de Borda

Esta é a única tabela normativa de casos de borda de `pause` — o Capítulo 36 referencia esta seção em vez de repetir o conteúdo.

| **Entrada**      | **Comportamento formal**                                                                              |
|------------------|-------------------------------------------------------------------------------------------------------|
| `pause 0`        | *Noop* — a execução continua imediatamente, sem erro mas com NoopPause WARNING.                       |
| `pause -1`       | `InvalidPauseDuration PROBLEM` — o tempo de pausa não pode ser negativo.                              |
| `pause 1.5`      | Aguarda aproximadamente 1,5 segundo.                                                                  |
| `pause Infinity` | Aguarda indefinidamente, até que a execução seja interrompida externamente.                           |
| `pause NaN`      | `InvalidPauseDuration PROBLEM` — o valor informado não representa uma duração válida. ( lembrando NaN é apenas um indicador do interpreter para erro numérico |
| `pause "1"`      | `TypeError PROBLEM` — o parâmetro deve ser numérico; não há conversão implícita de string para tempo. |

**pause 0 em laço.** `pause 0` gera o `NoopPause WARNING` a cada execução — dentro de um laço, um aviso por iteração. Quando o tempo é calculado e pode ser zero, proteja o `pause`:

```tinypine
f passo(e, tempo = 0)
  if tempo > 0
    pause tempo
  return e
```

`pause` apenas suspende temporariamente a execução; não altera variáveis, escopo ou fluxo lógico do programa. `pause` nunca abre um bloco: nenhuma linha seguinte pode ser mais recuada por causa de `pause`.
