## Filosofia de Design

O TinyPine foi desenvolvido seguindo um conjunto de princípios fundamentais, descritos nesta seção. Esses princípios orientam toda decisão de projeto documentada no restante desta especificação.

### Princípios Centrais

| **Princípio**                      | **Descrição**                                                                                                                                                                                                                                       |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ausência de delimitadores de chave | A linguagem não utiliza `{` e `}` para delimitar blocos.                                                                                                                                                                                            |
| Escopo definido por indentação     | O escopo léxico é determinado pela indentação: 2 espaços ou 1 TAB por nível, nunca os dois tipos misturados no mesmo escopo.                                                                                                                        |
| Delimitação explícita de blocos    | Blocos abrem na quebra de linha após a assinatura e fecham por `indentação` (recuo): o corpo é toda linha mais recuada que a assinatura, e o bloco termina na primeira linha que volta ao recuo da assinatura ou a um nível menor (ver Capítulo 4). |
| Modificação pós-declaração         | Blocos podem ser referenciados e modificados por identificadores, inclusive antes de sua declaração textual (referência antecipada).                                                                                                                |
| Blocos especiais controlados       | Determinadas construções (`debug`, `js`, `loop`) são controladas diretamente pelo interpretador, fora do modelo geral de funções.                                                                                                                   |

Complementarmente, o projeto adota os seguintes princípios de mais alto nível:

- **Sintaxe simples — evitar símbolos sintáticos e construções complexas sempre que uma alternativa mais legível for viável.**

- **Leitura natural — aproximar a forma do código da forma como uma pessoa descreveria o algoritmo em linguagem corrente.**

- **Comportamento previsível — reduzir ambiguidades e efeitos colaterais inesperados; toda regra tem comportamento determinístico e documentado.**

- **Especificação formal — permitir que implementações independentes apresentem exatamente o mesmo comportamento observável.**

- **Biblioteca modular — organizar funcionalidades por responsabilidade, através de módulos importados explicitamente (ver Capítulo 33).**

### Modelo Interno

A linguagem converge para um modelo conceitual com três elementos centrais:

- **Blocos são a unidade principal de execução.**

- **Identificadores constituem o sistema de referência e modificação pós-declaração de blocos (ver Capítulo 28).**

### Objetivos e Casos de Uso

O TinyPine é projetado para ser simples de aprender, consistente de ler e suficientemente poderoso para desenvolver desde pequenos scripts até aplicações de maior porte. Seu objetivo não é substituir linguagens já consolidadas, mas oferecer uma experiência de programação que prioriza clareza, previsibilidade e facilidade de expansão.

A linguagem busca ser adequada, em particular, para:

- **aprendizado de programação;**

- **automação de tarefas;**

- **desenvolvimento de jogos;**

- **criação de ferramentas;**

- **experimentação em design de linguagens;**

- **ensino de compiladores e interpretadores.**

### Relação com Outras Linguagens

O TinyPine possui inspirações declaradas em Python, JavaScript, Lua e outras linguagens, mas não pretende ser um clone de nenhuma delas. Sempre que uma decisão de projeto estiver em conflito com o comportamento de uma linguagem de referência, prevalece o critério de consistência interna, simplicidade e facilidade de evolução da própria especificação do TinyPine.

### Natureza Experimental da Especificação

O TinyPine é um projeto em evolução contínua. Recursos podem ser adicionados, modificados ou removidos conforme o amadurecimento da linguagem, sob o compromisso de que toda decisão seja documentada formalmente nesta especificação — incluindo decisões que revertem ou substituem uma regra anterior. O registro dessas decisões vive no Histórico da Especificação (Apêndice A).
