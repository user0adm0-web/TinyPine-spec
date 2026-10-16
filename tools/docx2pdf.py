#!/usr/bin/env python3
"""docx -> pdf pelo LibreOffice, ATUALIZANDO o sumário (a conversão simples deixa-o vazio).

    python tools/docx2pdf.py entrada.docx saida.pdf

Usa a API UNO (módulo `uno`, que vem com o LibreOffice). Se não estiver disponível,
build.py cai para a conversão simples (sumário vazio no PDF).
"""
import subprocess, sys, time, os, tempfile
from pathlib import Path


def main(src, dst):
    import uno
    from com.sun.star.beans import PropertyValue

    def pv(n, v):
        p = PropertyValue(); p.Name, p.Value = n, v; return p

    porta = 2002 + os.getpid() % 500
    perfil = tempfile.mkdtemp(prefix="lo-")
    proc = subprocess.Popen(["soffice", "--headless", "--norestore", f"-env:UserInstallation=file://{perfil}",
                             f"--accept=socket,host=localhost,port={porta};urp;"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ctx = uno.getComponentContext()
        resolver = ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", ctx)
        for _ in range(60):
            try:
                remoto = resolver.resolve(f"uno:socket,host=localhost,port={porta};urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError("LibreOffice não respondeu")
        desktop = remoto.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", remoto)
        doc = desktop.loadComponentFromURL(Path(src).resolve().as_uri(), "_blank", 0, (pv("Hidden", True),))
        idx = doc.getDocumentIndexes()
        for i in range(idx.getCount()):
            idx.getByIndex(i).update()
        doc.storeToURL(Path(dst).resolve().as_uri(), (pv("FilterName", "writer_pdf_Export"),))
        doc.close(True)
        try:
            desktop.terminate()
        except Exception:
            pass
    finally:
        proc.terminate()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
