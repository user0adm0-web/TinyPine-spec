#!/usr/bin/env python3
"""Gera templates/reference.docx (o "visual" do docx) a partir do reference.docx padrão do pandoc.

Rode de novo só quando quiser mudar fontes, cores ou margens:
    python tools/make_reference.py
"""
import re, subprocess, zipfile, io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "templates" / "reference.docx"
AZUL = "1F3B57"


def style_xml(sid, name, ppr="", rpr="", based="Normal", nxt="BodyText", kind="paragraph"):
    nx = f'<w:next w:val="{nxt}"/>' if nxt else ""
    return (f'<w:style w:type="{kind}" w:styleId="{sid}"><w:name w:val="{name}"/><w:basedOn w:val="{based}"/>{nx}<w:qFormat/>'
            f'{"<w:pPr>" + ppr + "</w:pPr>" if ppr else ""}{"<w:rPr>" + rpr + "</w:rPr>" if rpr else ""}</w:style>')


def replace_style(styles, sid, new):
    pat = re.compile(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % re.escape(sid), re.S)
    return pat.sub(lambda m: new, styles) if pat.search(styles) else styles.replace("</w:styles>", new + "</w:styles>")


def main():
    default = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], capture_output=True, check=True).stdout
    zin = zipfile.ZipFile(io.BytesIO(default))
    files = {n: zin.read(n) for n in zin.namelist()}
    st = files["word/styles.xml"].decode("utf8")

    font = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'
    st = re.sub(r"<w:docDefaults>.*?</w:docDefaults>",
                f'<w:docDefaults><w:rPrDefault><w:rPr>{font}<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="pt-BR"/></w:rPr></w:rPrDefault><w:pPrDefault/></w:docDefaults>',
                st, flags=re.S)
    cor = f'<w:color w:val="{AZUL}"/>'
    st = replace_style(st, "BodyText", style_xml("BodyText", "Body Text", '<w:spacing w:before="0" w:after="160" w:line="288" w:lineRule="auto"/>', nxt="BodyText"))
    st = replace_style(st, "Compact", style_xml("Compact", "Compact", '<w:spacing w:before="0" w:after="100" w:line="276" w:lineRule="auto"/>', based="BodyText"))
    st = replace_style(st, "Heading1", style_xml("Heading1", "heading 1", '<w:keepNext/><w:pageBreakBefore/><w:spacing w:before="0" w:after="280"/><w:outlineLvl w:val="0"/>', f'<w:b/><w:bCs/>{cor}<w:sz w:val="40"/><w:szCs w:val="40"/>'))
    st = replace_style(st, "Heading2", style_xml("Heading2", "heading 2", '<w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="160"/><w:outlineLvl w:val="1"/>', f'<w:b/><w:bCs/>{cor}<w:sz w:val="30"/><w:szCs w:val="30"/>'))
    st = replace_style(st, "Heading3", style_xml("Heading3", "heading 3", '<w:keepNext/><w:keepLines/><w:spacing w:before="280" w:after="140"/><w:outlineLvl w:val="2"/>', f'<w:b/><w:bCs/>{cor}<w:sz w:val="24"/><w:szCs w:val="24"/>'))
    st = replace_style(st, "Heading4", style_xml("Heading4", "heading 4", '<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="3"/>', f'<w:b/><w:bCs/><w:i/><w:iCs/>{cor}<w:sz w:val="22"/><w:szCs w:val="22"/>'))
    st = replace_style(st, "Title", style_xml("Title", "Title", '<w:keepNext/><w:spacing w:before="2400" w:after="240"/><w:jc w:val="center"/>', f'<w:b/><w:bCs/>{cor}<w:sz w:val="72"/><w:szCs w:val="72"/>'))
    st = replace_style(st, "Subtitle", style_xml("Subtitle", "Subtitle", '<w:spacing w:before="120" w:after="120"/><w:jc w:val="center"/>', '<w:color w:val="555555"/><w:sz w:val="30"/><w:szCs w:val="30"/>', based="Title"))
    mono = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Consolas" w:cs="Consolas"/>'
    st = replace_style(st, "SourceCode", style_xml("SourceCode", "Source Code",
                       '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/><w:spacing w:before="0" w:after="0" w:line="264" w:lineRule="auto"/><w:ind w:left="200" w:right="200"/>',
                       f'{mono}<w:sz w:val="20"/><w:szCs w:val="20"/>', nxt="BodyText"))
    st = replace_style(st, "VerbatimChar", style_xml("VerbatimChar", "Verbatim Char", rpr=f'{mono}<w:color w:val="1F5C99"/>', based="DefaultParagraphFont", nxt=None, kind="character"))
    st = replace_style(st, "BlockText", style_xml("BlockText", "Block Text",
                       '<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="1F3B57"/></w:pBdr><w:spacing w:before="100" w:after="100"/><w:ind w:left="460" w:right="200"/>', based="BodyText"))
    borders = ''.join(f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>' for e in ("top", "left", "bottom", "right", "insideH", "insideV"))
    st = re.sub(r'(<w:style [^>]*w:styleId="Table".*?<w:tblPr>)(.*?)(</w:tblPr>)',
                lambda m: m.group(1) + '<w:tblInd w:w="0" w:type="dxa"/><w:tblBorders>' + borders + '</w:tblBorders>'
                '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>' + m.group(3),
                st, count=1, flags=re.S)
    files["word/styles.xml"] = st.encode("utf8")

    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    rp = '<w:rPr><w:color w:val="888888"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {ns}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
              f'<w:r>{rp}<w:fldChar w:fldCharType="begin"/></w:r><w:r>{rp}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              f'<w:r>{rp}<w:fldChar w:fldCharType="separate"/></w:r><w:r>{rp}<w:t>1</w:t></w:r><w:r>{rp}<w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
    files["word/footer1.xml"] = footer.encode("utf8")
    rels = files["word/_rels/document.xml.rels"].decode("utf8")
    files["word/_rels/document.xml.rels"] = rels.replace("</Relationships>", '<Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>').encode("utf8")
    ct = files["[Content_Types].xml"].decode("utf8")
    files["[Content_Types].xml"] = ct.replace("</Types>", '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>').encode("utf8")
    doc = files["word/document.xml"].decode("utf8")
    sect = '<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter1"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1300" w:right="1300" w:bottom="1300" w:left="1300" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
    doc = re.sub(r"<w:sectPr.*?</w:sectPr>", sect, doc, flags=re.S) if "<w:sectPr" in doc else doc.replace("</w:body>", sect + "</w:body>")
    files["word/document.xml"] = doc.encode("utf8")

    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", files.pop("[Content_Types].xml"))
        for n, b in files.items():
            z.writestr(n, b)
    print("gerado:", OUT)


if __name__ == "__main__":
    main()
