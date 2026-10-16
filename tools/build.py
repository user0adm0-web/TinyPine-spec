#!/usr/bin/env python3
"""Gera a especificação TinyPine a partir de spec/*.md.

    python tools/build.py            # docx + html (padrão)
    python tools/build.py all        # docx + html + pdf + md único
    python tools/build.py html       # só HTML
    python tools/build.py html --watch   # refaz o HTML a cada gravação
    python tools/build.py docx --no-check

Requer: Python 3.8+ e pandoc 3.x. PDF: LibreOffice (soffice) instalado.
A saída vai para dist/ (não versionada).
"""
import argparse, shutil, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, SPEC, load_meta, build_numbered

DIST = ROOT / "dist"


def need(cmd):
    if shutil.which(cmd) is None:
        sys.exit(f"erro: '{cmd}' não encontrado no PATH. Veja o README (seção 'Instalação').")


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"erro ao rodar {args[0]}:\n{r.stderr}")
    if r.stderr.strip():
        print(r.stderr.strip())


def build(formats, check=True):
    need("pandoc")
    if check:
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "check.py")])
        if r.returncode:
            sys.exit("check.py encontrou erros; corrija antes de gerar (ou use --no-check).")
    meta = load_meta()
    DIST.mkdir(exist_ok=True)
    text, _ = build_numbered()
    stem = f"TinyPine-spec-v{meta.get('version', '0')}"
    md = DIST / f"{stem}.md"
    md.write_text(text, encoding="utf8")
    common = ["-f", "gfm", str(md), "--toc", "--toc-depth=3", "--no-highlight",
              "-M", f"title={meta.get('title', 'TinyPine')}",
              "-M", f"subtitle={meta.get('subtitle', '')} — versão {meta.get('version', '')}",
              "-M", "lang=pt-BR", "-M", "toc-title=Sumário"]
    if "docx" in formats or "pdf" in formats:
        out = DIST / f"{stem}.docx"
        run(["pandoc", *common, "-t", "docx", "--reference-doc", str(ROOT / "templates" / "reference.docx"), "-o", str(out)])
        print("gerado:", out.relative_to(ROOT))
    if "pdf" in formats:
        need("soffice")
        try:  # caminho bom: atualiza o sumário antes de exportar
            run([sys.executable, str(ROOT / "tools" / "docx2pdf.py"), str(DIST / f"{stem}.docx"), str(DIST / f"{stem}.pdf")])
        except (Exception, SystemExit):
            print("aviso: não consegui atualizar o sumário (módulo uno ausente?); PDF sai com sumário vazio")
            run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(DIST), str(DIST / f"{stem}.docx")])
        print("gerado:", (DIST / f"{stem}.pdf").relative_to(ROOT))
    if "html" in formats:
        out = DIST / f"{stem}.html"
        run(["pandoc", *common, "-t", "html5", "-s", "--embed-resources", "--css", str(ROOT / "templates" / "style.css"), "-o", str(out)])
        shutil.copyfile(out, DIST / "index.html")
        print("gerado:", out.relative_to(ROOT))
    if "md" in formats:
        print("gerado:", md.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("formats", nargs="*", default=["docx", "html"], help="docx html pdf md all")
    ap.add_argument("--no-check", action="store_true", help="não roda check.py antes")
    ap.add_argument("--watch", action="store_true", help="refaz a cada alteração em spec/ (útil com html)")
    a = ap.parse_args()
    fmts = {"docx", "html", "pdf", "md"} if "all" in a.formats else set(a.formats)
    build(fmts, check=not a.no_check)
    if a.watch:
        print("observando spec/ ... (Ctrl+C para sair)")
        last = None
        while True:
            cur = [(p.name, p.stat().st_mtime) for p in sorted(SPEC.iterdir())]
            if last is not None and cur != last:
                try:
                    build(fmts, check=False)
                except SystemExit as e:
                    print(e)
            last = cur
            time.sleep(1)


if __name__ == "__main__":
    main()
