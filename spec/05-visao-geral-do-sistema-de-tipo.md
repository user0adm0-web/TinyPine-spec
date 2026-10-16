# PARTE III — SISTEMA DE TIPOS

## Visão Geral do Sistema de Tipos

O TinyPine expõe dois mecanismos distintos e não intercambiáveis para lidar com tipos:

| **Mecanismo**              | **Sintaxe**      | **Efeito**                                                                                                                                                                                                            | **Capítulo** |
|----------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| **Asserção de tipo por :** | `valor: tipo`    | Verifica se o valor à esquerda já pertence ao tipo indicado. **Não converte** — se o valor não pertencer ao tipo, o interpretador interrompe a execução com erro. Caso for compatível, força ele a ficar nesse estado | 6            |
| **Conversão explícita**    | `valor: to-tipo` | Converte o valor informado para o tipo indicado, aplicando as regras de conversão de cada tipo. Pode falhar (ver 8) quando a conversão não é definida para a entrada informada.                                       | 8            |

O uso do : de asserção de tipo não é obrigatório quando o tipo pode ser inferido automaticamente pelo interpretador; ele é útil para documentação, validação de entrada e restrição de comportamento em pontos críticos do programa.

A partir da 0.7, essa distinção é formalizada como princípio central da linguagem: **tudo pode ser tipado explicitamente ou ter seu tipo inferido**. Quando um identificador — var/const (Cap. 18.2), parâmetro de função (Cap. 30.3) ou retorno de função (Cap. 30.4) — declara um tipo explicitamente, toda atribuição a ele, na declaração e em qualquer reatribuição posterior, é verificada estaticamente contra esse tipo (Cap. 35, etapa de Análise Estática de Tipos); uma atribuição incompatível é erro de verificação estática, não erro de execução. Sem tipo declarado, o identificador permanece dinamicamente tipado e pode receber, a qualquer momento, um valor de outro tipo:

```tinypine
var A = 10
A = "a"          # válido — sem tipo declarado
var A: int = 10
A = "a"          # StaticTypeMismatch PROBLEM — incompatível com A: int
```
