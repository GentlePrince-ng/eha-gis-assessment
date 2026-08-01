"""Build the Word style template used for every document in this submission.

Pandoc does not take fonts or margins as options for `.docx` output - it copies
them from a **reference document**. This builds that reference so every rendered
file matches the house style rather than pandoc's generic defaults.

The style is taken from `Oladimeji_CoverLetter_MiracleFeet.docx`:

    page          US Letter, portrait
    margins       0.75 inch all round  (1080 twips)
    body font     Calibri 11 pt        (sz 22 half-points)
    paragraphs    10 pt space after, left aligned, single line spacing
    headings      Calibri bold, stepped down from 16 pt

Run:  python writeup/make_reference.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PANDOC = Path(r"C:/Users/SolomonOladimeji/AppData/Local/Pandoc/pandoc.exe")
OUT = HERE / "reference.docx"

# --- House style, in Word's units --------------------------------------
FONT = "Calibri"
BODY_HALF_PT = 22          # 11 pt
SPACE_AFTER = 200          # 10 pt
PAGE_W, PAGE_H = 12240, 15840      # US Letter, twips
MARGIN = 1080                       # 0.75 inch

# Heading sizes in half-points, stepped down. Kept modest so a heading does not
# eat a fifth of a page in a document that is page-limited.
HEADINGS = {"Heading1": 32, "Heading2": 28, "Heading3": 24,
            "Heading4": 22, "Heading5": 22, "Heading6": 22}


def build() -> None:
    subprocess.run([str(PANDOC), "--print-default-data-file", "reference.docx"],
                   stdout=OUT.open("wb"), check=True)

    zin = zipfile.ZipFile(OUT)
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()

    # ---- page size and margins ----------------------------------------
    doc = items["word/document.xml"].decode("utf-8")
    page = (f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}" w:orient="portrait"/>'
            f'<w:pgMar w:top="{MARGIN}" w:right="{MARGIN}" w:bottom="{MARGIN}" '
            f'w:left="{MARGIN}" w:header="708" w:footer="708" w:gutter="0"/>')
    doc = re.sub(r"<w:sectPr>", "<w:sectPr>" + page, doc, count=1)
    items["word/document.xml"] = doc.encode("utf-8")

    sty = items["word/styles.xml"].decode("utf-8")

    # ---- document defaults: Calibri 11 pt, 10 pt after, single spacing --
    defaults = (
        "<w:docDefaults>"
        "<w:rPrDefault><w:rPr>"
        f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/>'
        f'<w:sz w:val="{BODY_HALF_PT}"/><w:szCs w:val="{BODY_HALF_PT}"/>'
        "</w:rPr></w:rPrDefault>"
        "<w:pPrDefault><w:pPr>"
        f'<w:spacing w:after="{SPACE_AFTER}" w:line="240" w:lineRule="auto"/>'
        '<w:jc w:val="left"/>'
        "</w:pPr></w:pPrDefault>"
        "</w:docDefaults>"
    )
    sty = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", defaults, sty, flags=re.S)

    # ---- every style uses the house font ------------------------------
    sty = re.sub(r'<w:rFonts[^/]*/>',
                 f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" '
                 f'w:eastAsia="{FONT}"/>', sty)

    # ---- headings: bold, stepped, tight spacing ------------------------
    for style_id, half_pt in HEADINGS.items():
        pattern = rf'(<w:style [^>]*w:styleId="{style_id}".*?</w:style>)'
        def fix(m, hp=half_pt):
            block = m.group(1)
            block = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{hp}"/>', block)
            block = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{hp}"/>', block)
            block = re.sub(r'<w:spacing[^/]*/>',
                           '<w:spacing w:before="200" w:after="100"/>', block)
            if "<w:b/>" not in block:
                block = block.replace("<w:rPr>", "<w:rPr><w:b/>", 1)
            return block
        sty = re.sub(pattern, fix, sty, flags=re.S)

    items["word/styles.xml"] = sty.encode("utf-8")

    tmp = OUT.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items.items():
            z.writestr(name, data)
    shutil.move(tmp, OUT)

    print(f"  reference.docx rebuilt to house style")
    print(f"    page      US Letter {PAGE_W}x{PAGE_H} twips, {MARGIN} twip margins")
    print(f"    body      {FONT} {BODY_HALF_PT/2:.0f} pt, {SPACE_AFTER/20:.0f} pt after")
    print(f"    headings  {FONT} bold, "
          + ", ".join(f"{k[-1]}={v/2:.0f}pt" for k, v in HEADINGS.items()))


if __name__ == "__main__":
    build()
