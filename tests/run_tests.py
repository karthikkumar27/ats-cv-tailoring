#!/usr/bin/env python3
"""Repo test suite. Runs locally and in CI (.github/workflows/test.yml).

  npm install --no-save docx@9 && pip install pypdf
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


def variant(name, *subs):
    """Copy the builder with regex substitutions, kept in templates/ so `docx` resolves the same way."""
    s = read(BUILDER)
    for pat, rep in subs:
        s, n = re.subn(pat, rep, s, flags=re.S)
        assert n == 1, f"variant {name}: pattern not found: {pat[:40]}"
    path = os.path.join(ROOT, "templates", f"_test_{name}.js")
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
    print("      " + "\n      ".join(l for l in out.splitlines() if not l.startswith("PASS")) or "      all PASS")


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


print(f"\n{len(failures)} failure(s)" if failures else "\nall tests passed")
sys.exit(1 if failures else 0)
