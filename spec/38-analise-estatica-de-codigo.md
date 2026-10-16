## Análise Estática de Código

### Detecção de Variáveis Não Utilizadas

O analisador estático pode identificar variáveis declaradas e nunca utilizadas, ajudando a localizar código morto ou erros de digitação em nomes de variáveis.

```tinypine
var nome = "Ana"
print("Olá")
# gera aviso:
# UnusedVariable WARNING — Variable "name" was declared but never used.
```

- **Não impede a execução do programa — é um aviso (**`Warning`**), não um erro.**

- **Variáveis usadas em qualquer ponto do escopo não geram aviso.**

- **A análise considera o escopo da variável, não o programa inteiro.**

### Autocompletar do Editor (fora do interpretador)

Recursos de autocompletar — por exemplo, inserir automaticamente o recuo esperado ao abrir um bloco, ou detectar e sinalizar mistura de TAB e espaço enquanto o programador digita — são recursos do editor/IDE do TinyPine, e não do interpretador. Eles apenas auxiliam a escrita: não alteram a lógica do programa, e podem ser desativados pelo programador.

Os capítulos desta parte documentam áreas da linguagem que ainda não possuem especificação fechada. Eles são mantidos separados do restante do documento justamente para deixar explícito, à primeira vista do índice, quais partes da linguagem são normativas hoje e quais ainda estão em desenho.
