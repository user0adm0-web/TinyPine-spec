## Operador de Atribuição

| **Símbolo** | **Nome**   | **Semântica**                                                                                                                                                        |
|-------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `=`         | Atribuição | Vincula um valor a um identificador. Cria a variável, se ainda não existir no escopo corrente, ou atualiza seu valor, caso já exista e não seja imutável (ver 18.2). |

> ***Nota:** dentro da lista de parâmetros de uma declaração de função,* `=` *não é atribuição: separa o parâmetro do seu valor padrão (Capítulo 30.5).*

> ***Nota:** a atribuição a um membro de um objeto **nativo** (`objeto.nome = valor`), como os handles `window` e `element` do módulo `canvas` (Capítulo 45), não vincula um identificador: chama o motor, que valida o valor e o aplica, ou recusa (`ReadOnlyProperty`, E313, para membro somente leitura; `TypeMismatch`, E302, para tipo errado; o Capítulo 53 traz o erro de membro inexistente). Para objetos do usuário (classes, Capítulo 32) essa forma não está definida — Apêndice A, B36.*
