## Operadores Aritméticos e Precedência Geral

A precedência geral segue a convenção matemática padrão — multiplicação e divisão antes de adição e subtração:

```tinypine
1 + 2 * 3
# Resultado: 7 — a multiplicação possui prioridade maior que a soma
```


O comportamento de precedência dos operadores aritméticos (`+`, `-`, `*`, `/`, `%`, `**`) está consolidado no Capítulo 12.1 (ver Histórico, Apêndice A). Suas interações com os tipos primitivos da linguagem seguem a matriz de tipos abaixo, destacando que o `tpine` rejeita coerções automáticas perigosas e prioriza a preservação da precisão matemática.

| Operador | Operando A | Operando B | Resultado Esperado | Exemplo no `tpine` |
| :--- | :--- | :--- | :--- | :--- |
| **`+` , `-` , `*`** | `num` (Inteiro/Fracionário) | `num` (Inteiro/Fracionário) | **`num`** (Preserva precisão exata / dízima) | `0.33 + 0.33` &rarr; `0.66` |
| **`/`** | `num` | `num` | **`num`** (Gera dízima exata `*∞` se aplicável) | `1/2` &rarr; `0.5` |
| **`**`** | `num` (Base) | `num` (Expoente) | **`num`** (Raízes mantêm identidade algébrica) | `math.sqrt(0.1) ** 2` &rarr; `0.1` |
| **`%`** | `num` | `num` | **`num`** (Resto da divisão) | `5 % 2` &rarr; `1` |
| **`+`** | `str` | `num` ou `str` | **`TypeMismatch PROBLEM`** (Sem coerção) | `print("ç" + 1)` &rarr; **Erro** |
| **`*`** | `str` ou `array` | `num` (Inteiro) | **Repetição Literal** (Expansão do padrão) | `[3] * 2` &rarr; `[3, 3]` |

*Nota de Implementação (Capítulo 9.2):* Para misturar strings e números, a coerção deve ser explicitada pelo desenvolvedor utilizando os modificadores `: to-str` ou `: to-num` (ex: `(1/3 : to-str).length`).
