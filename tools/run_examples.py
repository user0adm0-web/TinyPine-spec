#!/usr/bin/env python3
"""Roda os exemplos executáveis dos .md e compara a saída.

Um exemplo é um bloco ```tinypine run seguido, logo depois, de um bloco ```output:

    ```tinypine run
    println("oi")
    ```
    ```output
    oi
    ```

Procura em tests/exemplos/*.md e em spec/*.md. O interpretador vem de $TINYPINE
(ex.: TINYPINE="dotnet C:/TinyPine/TinyPine.dll"); padrão: "tpine".

    python tools/run_examples.py
"""
import os, re, shlex, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^(`{3,})\s*(.*)$")


def blocos(path):
    lines = path.read_text(encoding="utf8").split("\n")
    i, out = 0, []
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        info, ini = m.group(2).strip(), i
        j = i + 1
        while j < len(lines) and not (FENCE.match(lines[j]) and not FENCE.match(lines[j]).group(2)):
            j += 1
        out.append((info, "\n".join(lines[i + 1:j]), ini + 1))
        i = j + 1
    return out


def main():
    cmd = shlex.split(os.environ.get("TINYPINE", "tpine"))
    arquivos = sorted((ROOT / "tests" / "exemplos").glob("*.md")) + sorted((ROOT / "spec").glob("*.md"))
    total = falhas = 0
    for f in arquivos:
        bs = blocos(f)
        for k, (info, code, line) in enumerate(bs):
            if info.split()[:2] != ["tinypine", "run"]:
                continue
            esperado = bs[k + 1][1] if k + 1 < len(bs) and bs[k + 1][0] == "output" else None
            if esperado is None:
                print(f"AVISO {f.name}:{line}: bloco 'run' sem bloco 'output' logo depois")
                continue
            total += 1
            with tempfile.NamedTemporaryFile("w", suffix=".tpine", delete=False, encoding="utf8") as tmp:
                tmp.write(code + "\n")
            try:
                r = subprocess.run(cmd + [tmp.name], capture_output=True, text=True, timeout=20)
                obtido = r.stdout
            except FileNotFoundError:
                sys.exit(f"interpretador não encontrado: {cmd[0]} (defina a variável TINYPINE)")
            finally:
                os.unlink(tmp.name)
            if obtido.strip() == esperado.strip():
                print(f"ok     {f.name}:{line}")
            else:
                falhas += 1
                print(f"FALHOU {f.name}:{line}\n  esperado: {esperado.strip()!r}\n  obtido:   {obtido.strip()!r}")
                if r.stderr.strip():
                    print("  stderr:", r.stderr.strip().splitlines()[0])
    print(f"\n{total - falhas}/{total} exemplos passaram")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
