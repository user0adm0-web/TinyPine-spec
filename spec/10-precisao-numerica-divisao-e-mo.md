## Precisão Numérica, Divisão e Modificadores Rígidos de Tipo

O operador de divisão (`/`) tem comportamento dependente do contexto da expressão, dos casts explícitos e da precedência dos modificadores de tipo. Esta seção formaliza esse comportamento.

### Divisão Padrão (Dinâmica)

Quando dois valores numéricos são divididos sem modificador ou prefixo de tipo, o interpretador realiza a operação em ponto flutuante de precisão padrão, segundo a seguinte tabela de resultado:

| **Operandos**               | **Tipo do resultado**                                 |
|-----------------------------|-------------------------------------------------------|
| `int / int`                 | `num`                                                 |
| `int / float`               | `float`                                               |
| `float / int`               | `float`                                               |
| `num / num`                 | `num`                                                 |
| Operação envolvendo `decim` | `decim` (ou `float`, se o outro operando for `float`) |

Se o resultado possuir casas decimais, o valor flutuante é preservado integralmente no tipo `num` — não há truncamento implícito na divisão padrão.

```tinypine
var resultado = 10 / 100   # resultado armazena 'num' com valor 0.1
```

### Conversão Explícita para Inteiro — : to-int

Quando o resultado de uma expressão precisa ser forçado a inteiro (descartando a parte fracionária), usa-se `: to-int`, que tem precedência máxima e se aplica apenas ao termo imediatamente à sua esquerda. O resultado é truncado em direção a zero, independentemente do sinal ou do valor decimal — para converter o resultado de uma divisão inteira, a expressão precisa estar entre parênteses:

```tinypine
var r1 = (10 / 19): to-int   # 10/19 = 0.526... → truncado para 0
var r2 = 1.5: to-int         # truncamento puro → 1
```

### Asserção Rígida de Tipo — Sufixo : int

Como sufixo pós-fixado (colado ao termo imediatamente anterior), `: int` tem **precedência máxima** no analisador sintático: captura e valida imediatamente apenas o termo diretamente à sua esquerda, antes de qualquer operação aritmética ainda pendente.

```tinypine
var resultado = 10: int / 100
# "10: int" valida 10 (é int), depois calcula 10 / 100 = 0.1 (tipo num)
 
var resultado = (10 / 100): int
# resolve (10 / 100) = 0.1 primeiro, depois aplica "0.1: int" → TypeMismatch PROBLEM (resíduo decimal)
```

### Asserção Rígida — Sufixo : decim (Alta Precisão)

`: decim`, como sufixo pós-fixado, possui a mesma precedência máxima de `: int`: instrui o analisador sintático a interceptar apenas o termo imediatamente anterior, para que a operação ocorra em base decimal de alta precisão desde o início do cálculo.

```tinypine
var taxa = 10: decim / 100   # aplica alta precisão ao termo 10 antes da divisão
```

### Conversão Tardia — : to-decim

Para envelopar o resultado sob o tipo `decim` **após** o cálculo ter sido realizado em precisão comum de hardware (ou seja, sem alta precisão desde o início), usa-se `: to-decim` sobre a expressão entre parênteses, já que o sufixo tem precedência máxima e se aplica apenas ao termo imediatamente à sua esquerda.

```tinypine
var taxa = (10 / 100): to-decim   # calcula em precisão comum; o resultado é rotulado
                          # 'decim', mas sem alta precisão
```
