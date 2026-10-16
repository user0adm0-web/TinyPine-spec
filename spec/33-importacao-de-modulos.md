## Importação de Módulos

### Sintaxe — use

A importação de módulos é feita através da palavra chave `use`, informando um ou mais módulos como parâmetros.

```tinypine
use json
use pen, system, random
use math.PI     # importa apenas o submódulo PI, pertencente a math
```

### Namespaces Obrigatórios

Os módulos da biblioteca padrão devem ser utilizados através de seus respectivos namespaces. Chamadas diretas de uma função pertencente a um módulo, sem o prefixo do módulo, não são permitidas.

```tinypine
use math
math.sin()
math.cos()
math.PI
math.E
```

*^- Correto*

```tinypine
sin()   # não permitido — sin() pertence ao namespace math
```

*^- Incorreto*

### Função len()

O TinyPine disponibiliza uma função nativa `len()`, fora do sistema de módulos, para obter o comprimento de uma coleção ou string. A assinatura completa — comportamento sobre cada tipo suportado (`str`, coleção, `tuple`) e casos de borda — ainda não está fechada (ver Histórico, Apêndice A).
