#!/usr/bin/env python3
"""Repo test suite. Runs locally and in CI (.github/workflows/test.yml).

  npm install --no-save docx@9 && pip install pypdf reportlab pypdfium2 pillow
  python tests/run_tests.py

Needs Node with the `docx` package resolvable from the repo (or via NODE_PATH).
With LibreOffice installed, page counts are checked for real; without it they're reported as unverified.
"""
import json, os, re, subprocess, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILDER = os.path.join(ROOT, "templates", "resume_build.js")
CHECK = os.path.join(ROOT, "scripts", "ats_check.py")
OUT = tempfile.mkdtemp()
failures = []


def test(name):
    def wrap(fn):
        try:
            fn()
            print(f"ok    {name}")
        except Exception as e:  # report every failure, not just the first
            failures.append(name)
            print(f"FAIL  {name}: {e}")
        return fn
    return wrap


def sh(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, (r.stdout + r.stderr).strip()[-800:]
    return r.stdout


def read(path):
    return open(path, encoding="utf-8").read()


def build(src, name):
    out = os.path.join(OUT, name + ".docx")
    sh("node", src, out)
    return out


def paragraphs(docx):
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    return xml, paras, ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paras]


def variant(name, *subs, src=BUILDER):
    """Copy a builder with regex substitutions, kept in templates/ so dependencies resolve the same way."""
    s = read(src)
    for pat, rep in subs:
        s, n = re.subn(pat, rep, s, flags=re.S)
        assert n == 1, f"variant {name}: pattern not found: {pat[:40]}"
    path = os.path.join(ROOT, "templates", f"_test_{name}{os.path.splitext(src)[1]}")
    open(path, "w", encoding="utf-8").write(s)
    return path


@test("version is the same in SKILL.md, plugin.json and CHANGELOG.md")
def _():
    skill = re.search(r"^\s+version:\s*(\S+)", read(os.path.join(ROOT, "SKILL.md")), re.M).group(1)
    plugin = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))["version"]
    log = re.search(r"^## (\S+)", read(os.path.join(ROOT, "CHANGELOG.md")), re.M).group(1)
    assert skill == plugin == log, f"SKILL.md {skill}, plugin.json {plugin}, CHANGELOG {log}"


@test("plugin manifests parse and share the SKILL.md description")
def _():
    plugin = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
    market = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))
    desc = re.search(r"^description:\s*(.+)$", read(os.path.join(ROOT, "SKILL.md")), re.M).group(1)
    assert plugin["description"] == market["plugins"][0]["description"], "plugin.json and marketplace.json differ"
    assert desc.startswith(plugin["description"]), "manifest description isn't the start of the SKILL.md description"


@test("ats_check.py self-test")
def _():
    sh(sys.executable, CHECK, "--self-test")


@test("resume builder syntax")
def _():
    sh("node", "--check", BUILDER)


@test("example resume builds and passes the ATS check (2 pages max)")
def _():
    out = sh(sys.executable, CHECK, build(BUILDER, "default"), "--pages", "2")
    print("\n".join("      " + l for l in out.splitlines() if "page" in l or not l.startswith("PASS")))


@test("example resume keeps the house style")
def _():
    xml, paras, text = paragraphs(os.path.join(OUT, "default.docx"))
    heads = [t for p, t in zip(paras, text) if "<w:pBdr>" in p]
    assert heads == ["SUMMARY", "SKILLS", "WORK EXPERIENCE", "PROJECTS", "EDUCATION AND CERTIFICATIONS"], heads
    assert all("<w:keepNext/>" in p for p in paras if "<w:pBdr>" in p), "a section heading lost keepNext"
    assert text[0] == text[0].upper(), "name isn't in capitals"
    assert 'w:color w:val="1F4E79"' in paras[1], "headline isn't blue"
    assert xml.count("<w:hyperlink") == 4, "expected 3 contact links + 1 project link"
    assert not any(t.startswith("Tech stack") for t in text), "Tech stack line is back"


@test("builder without certifications, and a project with no link")
def _():
    src = variant("nocert", (r'certifications: \["[^\]]*\]', "certifications: []"),
                  (r'      link: \{ text: "github\.com/example/invoice-diff"[^\n]*', "      link: null,"))
    try:
        docx = build(src, "nocert")
        sh(sys.executable, CHECK, docx, "--pages", "2")
        _, _, text = paragraphs(docx)
        assert "EDUCATION" in text and "EDUCATION AND CERTIFICATIONS" not in text, "heading didn't drop 'and Certifications'"
        assert "Open-source project" in text, "project type line missing when there's no link"
        assert not any(t.startswith("Certifications") for t in text), "empty Certifications line rendered"
    finally:
        os.remove(src)


@test("builder with no projects")
def _():
    src = variant("noproj", (r"  projects: \[.*?\n  \],\n", "  projects: [],\n"))
    try:
        docx = build(src, "noproj")
        sh(sys.executable, CHECK, docx, "--pages", "2")
        assert "PROJECTS" not in paragraphs(docx)[2], "empty Projects heading rendered"
    finally:
        os.remove(src)


LETTER = os.path.join(ROOT, "templates", "cover_letter_build.py")


def letter_text(src, name):
    out = os.path.join(OUT, name + ".pdf")
    sh(sys.executable, src, out)
    import pypdf
    return out, pypdf.PdfReader(out).pages[0].extract_text()


@test("example cover letter builds as a 1-page text PDF")
def _():
    out, text = letter_text(LETTER, "letter")
    sh(sys.executable, CHECK, out, "--pages", "1")
    for want in ("Maya Tan", "maya.tan@example.com", "Application for Senior Backend Engineer, Payments", "Kind regards,"):
        assert want in text, f"missing: {want}"


@test("cover letter keeps & and < in the text")
def _():
    src = variant("amp", (r'"role": "[^"]*"', '"role": "R&D <Platform> Engineer"'), src=LETTER)
    try:
        assert "Application for R&D <Platform> Engineer" in letter_text(src, "amp")[1], "escaped text missing"
    finally:
        os.remove(src)


@test("ATS check catches a cover letter that spills onto page 2")
def _():
    src = variant("long", (r'    \],\n    "closing"', '    ] * 3,\n    "closing"'), src=LETTER)
    try:
        out, _ = letter_text(src, "long")
        r = subprocess.run([sys.executable, CHECK, out, "--pages", "1"], capture_output=True, text=True)
        assert r.returncode == 1 and "limit 1" in r.stdout, "a 2-page letter passed the 1-page check"
    finally:
        os.remove(src)


def render(path, name):
    qa = os.path.join(OUT, "qa-" + name)
    r = subprocess.run([sys.executable, CHECK, path, "--render", qa], capture_output=True, text=True, encoding="utf-8")
    return r.stdout, qa


@test("--render saves page images and passes the example letter and resume")
def _():
    out, qa = render(os.path.join(OUT, "letter.pdf"), "letter")
    assert "PASS: no one-word lines" in out, out
    assert os.path.exists(os.path.join(qa, "page-1.png")), "no page image: " + out
    out, qa = render(os.path.join(OUT, "default.docx"), "resume")
    if "no LibreOffice" in out:
        print("      WARN: resume render skipped (no LibreOffice)")
    else:
        assert "PASS: no one-word lines" in out and os.path.exists(os.path.join(qa, "page-1.png")), out


@test("--render warns about one word left alone on a line")
def _():
    from reportlab.pdfgen import canvas
    pdf = os.path.join(OUT, "widow.pdf")
    c = canvas.Canvas(pdf)
    c.drawString(72, 700, "Tech stack: Python, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, AWS Lambda, SQS,")
    c.drawString(72, 686, "Pino")
    c.drawString(72, 660, "A short line")
    c.drawString(72, 646, "Done.")
    c.save()
    out, _ = render(pdf, "widow")
    assert "WARN: one word alone on a line (reword to pull it back): Pino" in out, out


print(f"\n{len(failures)} failure(s)" if failures else "\nall tests passed")
sys.exit(1 if failures else 0)
