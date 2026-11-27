#!/usr/bin/env python3
"""Mechanical ATS checks for a resume (.docx) or cover letter (.pdf). Standard library only.

  python scripts/ats_check.py resume.docx --keywords keywords.txt --pages 2
  python scripts/ats_check.py cover-letter.pdf --pages 1
  python scripts/ats_check.py resume.docx --render qa/      # page images + layout warnings
  python scripts/ats_check.py --self-test

Prints PASS / WARN / FAIL lines and exits 1 if anything failed.
--pages is a maximum. Page counts need LibreOffice (soffice) for .docx; without it the count is reported as unverified.
Install pypdf for exact PDF page counts and the text-based PDF check.
--render needs pypdfium2 and pillow (and LibreOffice for .docx).
"""
import argparse, io, os, re, shutil, subprocess, sys, tempfile, zipfile

MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
FULL_MONTH = r"\b(January|February|March|April|June|July|August|September|October|November|December)\s+\d{4}\b"
BAD_DATES = [FULL_MONTH, r"\b\d{4}-\d{2}\b", r"\b\d{1,2}/\d{4}\b", r"\b(?:%s)\w*\s+'\d{2}\b" % MONTHS]
ICONS = re.compile("[☀-➿←-⇿■-◿─-╿\U0001F000-\U0001FAFF]")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")


def docx_text(z):
    xml = z.read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    return xml, [re.sub(r"<[^>]+>", "", "".join(re.findall(r"<w:t[^>]*>[^<]*</w:t>", p))) for p in paras]


def pdf_pages(path):
    try:
        import pypdf
        r = pypdf.PdfReader(path)
        return len(r.pages), "".join((p.extract_text() or "") for p in r.pages)
    except ImportError:
        # shortcut: regex count misses pages inside compressed object streams; install pypdf for exact counts
        data = open(path, "rb").read()
        return len(re.findall(rb"/Type\s*/Page(?![a-z])", data)), None


def docx_to_pdf(path):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None
    out = tempfile.mkdtemp()
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", out, path],
                   capture_output=True, timeout=180)
    pdf = os.path.join(out, os.path.splitext(os.path.basename(path))[0] + ".pdf")
    return pdf if os.path.exists(pdf) else None


def docx_pages(path):
    pdf = docx_to_pdf(path)
    return pdf_pages(pdf)[0] if pdf else None


def pdf_lines(path):
    """Text lines per page as (y, x, text), top to bottom, from the PDF's text positions."""
    import pypdf
    pages = []
    for page in pypdf.PdfReader(path).pages:
        segs = []

        def grab(text, cm, tm, *_):
            if text.strip():
                x = cm[0] * tm[4] + cm[2] * tm[5] + cm[4]
                y = cm[1] * tm[4] + cm[3] * tm[5] + cm[5]
                segs.append((round(y), x, text))

        page.extract_text(visitor_text=grab)
        rows = {}
        for y, x, t in segs:
            rows.setdefault(y, []).append((x, t))
        lines = [(y, min(s)[0], " ".join(t.strip() for _, t in sorted(s))) for y, s in rows.items()]
        pages.append((float(page.mediabox.height), sorted(lines, reverse=True)))
    return pages


def widows(pages):
    """A 1-word line that a wrapped line spilled onto, like 'Pino' alone under a long Tech stack line."""
    found = []
    for _, lines in pages:
        longest = max((len(t) for _, _, t in lines), default=0)
        for (_, px, prev), (_, x, t) in zip(lines, lines[1:]):
            if (len(t.split()) == 1 and len(t) <= 15 and abs(px - x) <= 20
                    and len(prev) >= 0.75 * longest and not prev.rstrip().endswith((".", ":", ";", "!", "?"))):
                found.append(t)
    return found


def layout(path, outdir):
    """Save page images for a visual check and warn about layout problems the text checks can't see."""
    res = []
    pdf = path if path.lower().endswith(".pdf") else docx_to_pdf(path)
    if not pdf:
        return [("WARN", "render skipped: no LibreOffice to turn the .docx into a PDF")]
    try:
        import pypdfium2
        os.makedirs(outdir, exist_ok=True)
        doc = pypdfium2.PdfDocument(pdf)
        names = []
        for i in range(len(doc)):
            name = os.path.join(outdir, f"page-{i + 1}.png")
            doc[i].render(scale=2).to_pil().save(name)
            names.append(name)
        res.append(("PASS", f"page images: {', '.join(names)}"))
    except ImportError:
        res.append(("WARN", "page images skipped (pip install pypdfium2 pillow)"))
    try:
        pages = pdf_lines(pdf)
    except ImportError:
        return res + [("WARN", "layout checks skipped (pip install pypdf)")]
    w = widows(pages)
    res.append(("WARN", f"one word alone on a line (reword to pull it back): {', '.join(w)}") if w else ("PASS", "no one-word lines"))
    if len(pages) > 1:
        height, lines = pages[-1]
        used = (height - min(y for y, _, _ in lines)) / height if lines else 0
        res.append(("WARN", f"last page only {used:.0%} full: trim to {len(pages) - 1} page(s) or use the space")
                   if used < 0.25 else ("PASS", f"last page {used:.0%} full"))
    return res


def check(path, keywords=None, pages=None, page_counter=docx_pages):
    res = []
    add = lambda level, msg: res.append((level, msg))
    text = None
    if path.lower().endswith(".docx"):
        z = zipfile.ZipFile(path)
        xml, paras = docx_text(z)
        text = "\n".join(paras)
        for name, pat in [("tables", "<w:tbl>"), ("text boxes", "txbxContent"), ("images", "<w:drawing"),
                          ("legacy shapes", "<w:pict")]:
            add("FAIL" if pat in xml else "PASS", f"no {name}" if pat not in xml else f"contains {name}")
        cols = re.search(r'<w:cols [^>]*w:num="([2-9])"', xml)
        add("FAIL" if cols else "PASS", "multi-column layout" if cols else "single column")
        hf = [n for n in z.namelist() if re.match(r"word/(header|footer)\d*\.xml", n)
              and re.search(r"<w:t[^>]*>[^<]*\S", z.read(n).decode("utf-8"))]
        add("FAIL" if hf else "PASS", f"text in {', '.join(hf)}" if hf else "no text in header or footer")
        top = "\n".join(paras[:8])
        add("PASS" if EMAIL.search(top) else "FAIL", "email near the top" if EMAIL.search(top) else "no email in the first lines of the body")
        add("PASS" if PHONE.search(top) else "WARN", "phone near the top" if PHONE.search(top) else "no phone in the first lines of the body")
        bad = sorted({m.group(0) for p in BAD_DATES for m in re.finditer(p, text)})
        add("FAIL" if bad else "PASS", f"non-standard dates: {', '.join(bad)}" if bad else "dates use Mon YYYY")
        hyphen = re.search(r"\b(?:%s) \d{4} - " % MONTHS, text)
        add("WARN" if hyphen else "PASS", "date range uses '-' instead of '–'" if hyphen else "date ranges consistent")
        icons = sorted(set(ICONS.findall(text)))
        add("FAIL" if icons else "PASS", f"icons or box characters: {' '.join(icons)}" if icons else "no icons or symbols")
        if pages:
            n = page_counter(path)
            add("WARN", "page count unverified (no LibreOffice)") if n is None else \
                add("PASS" if n <= pages else "FAIL", f"{n} page(s), limit {pages}")
    elif path.lower().endswith(".pdf"):
        n, text = pdf_pages(path)
        if pages:
            add("PASS" if 0 < n <= pages else "FAIL", f"{n} page(s), limit {pages}")
        if text is None:
            add("WARN", "text-based PDF check skipped (install pypdf)")
        else:
            add("PASS" if text.strip() else "FAIL", "text-based PDF" if text.strip() else "no extractable text (scanned or image PDF?)")
    else:
        add("FAIL", "expected a .docx or .pdf file")
    if keywords and text is not None:
        flat = re.sub(r"\s+", " ", text).lower()
        missing = [k for k in keywords if k.lower() not in flat]
        add("FAIL" if missing else "PASS", f"keywords missing: {', '.join(missing)}" if missing else f"all {len(keywords)} keywords found")
        if not 25 <= len(keywords) <= 35:
            add("WARN", f"{len(keywords)} keywords listed; the guide aims for 25 to 35 (fewer is fine if that's all you have)")
    return res


def _docx(body, header=""):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", "<w:document><w:body>%s</w:body></w:document>" % body)
        if header:
            z.writestr("word/header1.xml", "<w:hdr><w:p><w:r><w:t>%s</w:t></w:r></w:p></w:hdr>" % header)
    path = os.path.join(tempfile.mkdtemp(), "t.docx")
    open(path, "wb").write(buf.getvalue())
    return path


def self_test():
    p = lambda t: "<w:p><w:r><w:t>%s</w:t></w:r></w:p>" % t
    good = _docx(p("Maya Tan") + p("Singapore | +65 8000 0000 | maya@example.com") + p("Engineer | Acme | Mar 2022 – Present") + p("Python and AWS"))
    r = check(good, ["Python", "AWS"], pages=2, page_counter=lambda _: 2)
    assert not [m for l, m in r if l == "FAIL"], r
    bad = _docx("<w:tbl></w:tbl>" + p("No contact here") + p("June 2020 – 2021-03 ☎"), header="maya@example.com")
    fails = " | ".join(m for l, m in check(bad, ["Kafka"], pages=2, page_counter=lambda _: 3) if l == "FAIL")
    for want in ["tables", "header", "email", "non-standard dates", "icons", "3 page(s), limit 2", "Kafka"]:
        assert want in fails, (want, fails)
    assert ("WARN", "page count unverified (no LibreOffice)") in check(good, pages=2, page_counter=lambda _: None)
    print("self-test passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--keywords", help="text file, one keyword per line")
    ap.add_argument("--pages", type=int, help="expected page count")
    ap.add_argument("--render", metavar="DIR", help="save page images (PNG) to DIR and check the layout")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.file:
        ap.error("give a .docx or .pdf file")
    kws = [l.strip() for l in open(a.keywords, encoding="utf-8") if l.strip()] if a.keywords else None
    res = check(a.file, kws, a.pages) + (layout(a.file, a.render) if a.render else [])
    for level, msg in res:
        print(f"{level}: {msg}")
    sys.exit(1 if any(l == "FAIL" for l, _ in res) else 0)


if __name__ == "__main__":
    main()
