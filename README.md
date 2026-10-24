# TinyPine — Especificação da Linguagem

Fonte da especificação em Markdown (um arquivo por capítulo). Os documentos finais
(docx, HTML, PDF e um .md único) são **gerados** — nunca edite a saída.

## Estrutura

```
spec/            capítulos (NN-nome.md), apêndices (ap-x-nome.md) e gramatica.ebnf
meta.yaml        título, subtítulo, versão e codinome
tools/           build.py, check.py, run_examples.py, make_reference.py
templates/       reference.docx (visual do Word) e style.css (visual do HTML)
tests/exemplos/  exemplos executáveis (tinypine run + output)
dist/            saída gerada (não versionada)
```

## Regras de escrita

- Títulos **sem número**: `## Funções`, `### Parâmetros`. A numeração (1., 3.2, 30.4.1…) é automática.
  Apêndices: `## Apêndice A — Título`.
- Referências cruzadas continuam em texto ("ver 10.3") e são validadas por `tools/check.py`.
- Código em blocos ```` ```tinypine ````. Para virar teste: ```` ```tinypine run ```` seguido de ```` ```output ````.
- A gramática fica em `spec/gramatica.ebnf` e entra no texto com `<!-- include: gramatica.ebnf -->`.
- UTF-8, quebras LF, uma frase/ideia por linha (diffs melhores).

## Uso

Requisitos: Python 3.8+, pandoc 3.x; LibreOffice só para PDF.

```
python tools/check.py                 # valida referências/numeração
python tools/build.py                 # docx + html
python tools/build.py all             # + pdf + md único
python tools/build.py html --watch    # refaz o HTML a cada gravação
TINYPINE="dotnet caminho/TinyPine.dll" python tools/run_examples.py
```

## Versões

Cada versão é uma **tag** git (`v0.7`, `v0.8`…). Ao subir a tag, o GitHub Actions gera e anexa
o docx/PDF/md à release. O site (HTML) é publicado no GitHub Pages a partir da `main`.