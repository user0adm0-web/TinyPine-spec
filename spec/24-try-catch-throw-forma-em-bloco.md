## try / catch / throw — Forma em Bloco

O TinyPine trata erros de execução recuperáveis (divisão por zero, falha de conversão de tipo, acesso inválido a coleção, entre outros) através de um único modelo, em bloco, usado para proteger uma ou várias instruções sob a mesma política de recuperação — um operador equivalente por expressão chegou a existir (Capítulo 17), mas foi removido na 0.5. As três palavras-chave seguem o mesmo padrão estrutural do restante da linguagem: parênteses para parâmetros, quando aplicável, e delimitação por indentação, como qualquer outro bloco (Capítulo 4).

| **Palavra-chave** | **Papel**                                                                                                                                                                                      |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `try`             | Inicia um bloco cujas instruções internas terão erros de execução recuperáveis interceptados.                                                                                                  |
| `catch`           | Captura e trata uma exceção gerada dentro do bloco `try` correspondente. Pode declarar um parâmetro (`catch(err)`) para acessar o objeto de erro — normalmente uma string descrevendo a falha. |
| `throw`           | Gera uma exceção manualmente, interrompendo o fluxo normal até o `catch` mais próximo que a intercepte.                                                                                        |

### Fechamento Automático de catch/finally

Assim como ocorre entre `if`/`elif`/`else` (Capítulo 4.5), o fechamento de `try` antes de `catch`, e de `catch` antes de `finally`, pode ser omitido — o interpretador fecha automaticamente o bloco compatível imediatamente anterior.

### Modelo de Erros Único

Até a v0.4, a forma em bloco e o operador `.try` (removido na 0.5 — ver Capítulo 17) compartilhavam o mesmo modelo de erros e o mesmo objeto de erro. Com a remoção de `.try`, esse modelo de erros e o objeto de erro passam a pertencer exclusivamente ao bloco `try` / `catch`, sem mais nenhuma equivalência a documentar.

### try sem catch

Um bloco `try` sem cláusula `catch` não descarta erros silenciosamente. Qualquer exceção capturada nessas condições emite o aviso `UncaughtInTry WARNING`. Sinais de controle de fluxo (`return`, `break`, `continue`, `done`) nunca são interceptados por `try` — apenas erros de execução.
