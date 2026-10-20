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

### Propriedade .length

A partir da pós-0.7, o comprimento de um valor é lido pela propriedade `.length`, somente leitura e fora do sistema de módulos — da mesma forma que `.type` (Capítulo 6.7). `.length` **substitui** a antiga função `len()`: `len(A)` passa a ser `A.length`, com o mesmo comportamento.

```tinypine
var lista = ["a", "b", "c"]
print(lista.length)     # 3
print("Serpente".length) # 8
```

`.length` vale para `str`, `list`, `dict` e `tuple` e é a mesma medida usada pela propriedade `length` dos tipos refinados (Capítulo 6.9). O comportamento detalhado sobre cada tipo e os casos de borda ainda não estão fechados (ver Histórico, Apêndice A).
