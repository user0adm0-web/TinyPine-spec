"""Funções compartilhadas por build.py e check.py."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"
INCLUDE = re.compile(r"^<!--\s*include:\s*(\S+)\s*-->\s*$")
FENCE = re.compile(r"^(`{3,}|~{3,})\s*(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
APENDICE = re.compile(r"^Apêndice\s+([A-Z])\b")


def load_meta():
    """Lê meta.yaml (só 'chave: valor', sem dependência de PyYAML)."""
    meta = {}
    for line in (ROOT / "meta.yaml").read_text(encoding="utf8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    return meta


def spec_files():
    return sorted(p for p in SPEC.glob("*.md"))


def expand_includes(text, base=SPEC):
    """<!-- include: arquivo.ebnf --> vira um bloco de código com o conteúdo do arquivo."""
    out = []
    for line in text.split("\n"):
        m = INCLUDE.match(line)
        if not m:
            out.append(line)
            continue
        f = base / m.group(1)
        if not f.exists():
            raise FileNotFoundError(f"include não encontrado: {m.group(1)}")
        lang = f.suffix.lstrip(".") or "text"
        out.append(f"```{lang}")
        corpo = f.read_text(encoding="utf8").rstrip("\n")
        if corpo.startswith("(*") and "\n\n" in corpo:      # o comentário de cabeçalho do arquivo não vai pro texto
            corpo = corpo.split("\n\n", 1)[1]
        out.extend(corpo.split("\n"))
        out.append("```")
    return "\n".join(out)


class Heading:
    def __init__(self, level, number, title, file, line):
        self.level, self.number, self.title, self.file, self.line = level, number, title, file, line


def number_text(text, filename="", state=None):
    """Numera os títulos de `text`. Capítulo = '## ' (N.), seções '###' (N.k), '####' (N.k.m)...
    Apêndice = '## Apêndice X — ...' (seções X.k). '# ' (Partes) não é numerado.
    `state` carrega os contadores de um arquivo para o seguinte. Devolve (texto, [Heading])."""
    if state is None:
        state = {"cap": 0, "letter": None, "c": []}
    out, heads, infence = [], [], None
    for i, line in enumerate(text.split("\n"), 1):
        fm = FENCE.match(line)
        if fm:
            tok = fm.group(1)[0]
            if infence is None:
                infence = tok
            elif infence == tok and not fm.group(2):
                infence = None
            out.append(line)
            continue
        hm = None if infence else HEADING.match(line)
        if not hm:
            out.append(line)
            continue
        lvl, title = len(hm.group(1)), hm.group(2)
        if lvl == 1:
            out.append(line)
            heads.append(Heading(1, "", title, filename, i))
            continue
        if lvl == 2:
            am = APENDICE.match(title)
            if am:
                state["letter"] = am.group(1)
                state["c"] = []
                heads.append(Heading(2, am.group(1), title, filename, i))
                out.append(line)
                continue
            state["cap"] += 1
            state["letter"] = None
            state["c"] = []
            num = str(state["cap"])
            out.append(f"## {num}. {title}")
            heads.append(Heading(2, num, title, filename, i))
            continue
        depth = lvl - 2
        c = state["c"]
        while len(c) < depth:
            c.append(0)
        del c[depth:]
        c[depth - 1] += 1
        base = state["letter"] or str(state["cap"])
        num = base + "." + ".".join(str(x) for x in c)
        out.append(f"{'#' * lvl} {num} {title}")
        heads.append(Heading(lvl, num, title, filename, i))
    return "\n".join(out), heads


def build_numbered():
    """Junta todos os capítulos (com includes expandidos) e numera. Devolve (texto, [Heading])."""
    state = {"cap": 0, "letter": None, "c": []}
    parts, heads = [], []
    for f in spec_files():
        txt = expand_includes(f.read_text(encoding="utf8"))
        t, h = number_text(txt, f.name, state)
        parts.append(t.rstrip("\n"))
        heads += h
    return "\n\n".join(parts) + "\n", heads
