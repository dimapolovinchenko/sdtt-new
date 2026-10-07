"""Check that every relative href/src in the generated HTML points to an existing file
and that every #fragment exists on the target page. Usage: python tools/check_links.py"""

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKIP = (".claude", "tools", ".git")

pages = [p for p in ROOT.rglob("*.html") if not any(part in SKIP for part in p.relative_to(ROOT).parts)]
ids = {p.resolve(): set(re.findall(r'\sid="([^"]+)"', p.read_text(encoding="utf-8"))) for p in pages}

errors = 0
for page in pages:
    html = page.read_text(encoding="utf-8")
    for attr, url in re.findall(r'\s(href|src)="([^"]+)"', html):
        if url.startswith(("http:", "https:", "mailto:", "tel:", "data:")):
            continue
        parts = urlsplit(url)
        if url.startswith("/"):
            target = ROOT / parts.path.lstrip("/")
        elif parts.path:
            target = (page.parent / parts.path)
        else:
            target = page
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            print(f"MISSING  {page.relative_to(ROOT)} -> {url}")
            errors += 1
            continue
        if parts.fragment and target.suffix == ".html" and parts.fragment not in ids.get(target.resolve(), set()):
            print(f"NO ANCHOR {page.relative_to(ROOT)} -> {url}")
            errors += 1

print(f"{len(pages)} pages checked, {errors} problem(s).")
sys.exit(1 if errors else 0)
