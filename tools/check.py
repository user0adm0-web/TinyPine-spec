#!/usr/bin/env python3
"""Confere a especificação antes de gerar os arquivos.

Erros (código de saída 1):
  - bloco de código sem fechamento; include que não existe;
  - capítulo cujo número no nome do arquivo (07-...) não bate com a ordem real;
  - título que pula nível (## seguido de ####);
Avisos (use --strict para tratar como erro):
  - referência cruzada ("Capítulo 30.3", "(34.8)", "Apêndice A.2") que não aponta para nenhuma seção.
Referências antigas aceitas ficam em tools/known-refs.txt (uma por linha: arquivo:referência).
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, FENCE, HEADING, spec_files, expand_includes, number_text

NUM = r"\d+(?:\.\d+)*"
LISTA = rf"{NUM}(?:\s*(?:,|e|a|ou|/|–|—|-|--)\s*{NUM})*"
REF_CAP = re.compile(rf"(?:Cap(?:ítulos?|s?\.)|Seç(?:ão|ões))\s+({LISTA})")
REF_PAR = re.compile(rf"\((?:ver\s+)?({LISTA})\)")
REF_APE = re.compile(r"Apêndice\s+([A-Z](?:\.\d+)?)|\((?:ver\s+)?([A-Z]\.\d+)\)")
CODE_SPAN = re.compile(r"`[^`]*`")


def main(strict=False):
    erros, avisos = [], []
    known = set()
    kf = ROOT / "tools" / "known-refs.txt"
    if kf.exists():
        known = {l.strip() for l in kf.read_text(encoding="utf8").splitlines() if l.strip() and not l.startswith("#")}
    state = {"cap": 0, "letter": None, "c": []}
    validos, textos = set(), []
    for f in spec_files():
        raw = f.read_text(encoding="utf8")
        try:
            txt = expand_includes(raw)
        except FileNotFoundError as e:
            erros.append(f"{f.name}: {e}")
            continue
        n = 0
        for line in txt.split("\n"):
            m = FENCE.match(line)
            if m and (n % 2 == 0 or not m.group(2)):
                n += 1
        if n % 2:
            erros.append(f"{f.name}: bloco de código sem fechamento")
        antes = state["cap"]
        t, heads = number_text(txt, f.name, state)
        m = re.match(r"(\d+)-", f.name)
        if m and state["cap"] != antes and int(m.group(1)) != state["cap"]:
            erros.append(f"{f.name}: o prefixo do arquivo é {m.group(1)}, mas este é o capítulo {state['cap']} pela ordem dos títulos")
        prev = 0
        for h in heads:
            if h.level > 1:
                if prev and h.level > prev + 1:
                    erros.append(f"{f.name}:{h.line}: título pula nível ({'#' * prev} → {'#' * h.level}) em '{h.title}'")
                prev = h.level
            if h.number:
                validos.add(h.number)
        textos.append((f.name, t))
    for nome, t in textos:
        infence = None
        for i, line in enumerate(t.split("\n"), 1):
            fm = FENCE.match(line)
            if fm:
                infence = None if infence else fm.group(1)[0]
                continue
            if infence or HEADING.match(line):
                continue
            plain = CODE_SPAN.sub("", line)
            achados = set()
            for rx in (REF_CAP, REF_PAR):
                for m in rx.finditer(plain):
                    for tok in re.findall(NUM, m.group(1)):
                        if tok.split(".")[0] != "0":
                            achados.add(tok)
            for m in REF_APE.finditer(plain):
                achados.add(m.group(1) or m.group(2))
            for tok in sorted(achados):
                if tok not in validos and f"{nome}:{tok}" not in known:
                    avisos.append(f"{nome}:{i}: referência a '{tok}' não aponta para nenhuma seção")
    for e in erros:
        print("ERRO  ", e)
    for a in avisos:
        print("aviso ", a)
    print(f"\n{len(erros)} erro(s), {len(avisos)} aviso(s); {len(validos)} seções numeradas.")
    return 1 if erros or (strict and avisos) else 0


if __name__ == "__main__":
    sys.exit(main("--strict" in sys.argv))
