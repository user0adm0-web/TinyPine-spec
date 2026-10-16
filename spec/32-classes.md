## Classes

Classes usam a palavra-chave `class` para abrir um bloco principal, herdando a estrutura de blocos por indentação já existente na linguagem.

### Sintaxe

```tinypine
class Pessoa()
  || Atributos (variáveis de escopo da classe) ||
  var nome = ""
  var idade = 0
 
  || Construtor (método de inicialização) ||
  f iniciar(n, i)
    nome = n
    idade = i
 
  || Um método da classe ||
  f saudar()
    print("Olá, meu nome é ", nome)
```

### Instanciação e Uso

```tinypine
var p1 = Pessoa("Dhavi", 19)
p1.saudar()
```

### Modelo de Execução

Internamente, uma classe é um molde de escopos associados. Quando o programa executa `Pessoa("Dhavi", 19)`, o interpretador segue quatro passos:

> **1.** Cria uma nova tabela de símbolos para o objeto, e adiciona um ponteiro de referência oculto, apontando de volta para a classe `Pessoa`.
>
> **2.** Inicializa apenas as variáveis (`nome`, `idade`) dentro dessa nova tabela. As funções (`iniciar`, `saudar`) permanecem exclusivamente na classe `Pessoa`, para poupar memória — não são copiadas para cada instância.
>
> **3.** Executa a função `iniciar`, localizada na classe `Pessoa`, aplicando os argumentos recebidos diretamente sobre as variáveis do novo objeto.
>
> **4.** Retorna a tabela do objeto. Quando `p1.saudar()` é chamado, o interpretador não encontra `saudar` em `p1`; segue então o ponteiro oculto até a classe `Pessoa`, e executa a função de lá, usando o escopo de `p1`.
