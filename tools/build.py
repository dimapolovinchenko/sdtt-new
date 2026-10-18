"""Static site generator for sdtt.de (DE default, EN under /en/).

Usage:  python tools/build.py

Writes plain HTML files into the project root (DE) and /en (EN), plus
placeholder images, placeholder PDFs, sitemap.xml and robots.txt.
Only the Python standard library is used. Pages are fully static —
edit content here or in site_data.py, never in the generated .html files.
"""

import datetime
import hashlib
import posixpath
from urllib.parse import quote
import random
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_data as D  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
YEAR = datetime.date.today().year
LANGS = ("de", "en")

ROUTES = {
    "home": {"de": "index.html", "en": "en/index.html"},
    "projects": {"de": "oeffentliche-projekte.html", "en": "en/public-projects.html"},
    "standards": {"de": "normen-zertifikate.html", "en": "en/standards-certificates.html"},
    "company": {"de": "unternehmen.html", "en": "en/company.html"},
    "tenders": {"de": "ausschreibungen.html", "en": "en/tenders.html"},
    "contact": {"de": "kontakt.html", "en": "en/contact.html"},
    "imprint": {"de": "impressum.html", "en": "en/imprint.html"},
    "privacy": {"de": "datenschutz.html", "en": "en/privacy.html"},
    "terms": {"de": "agb.html", "en": "en/terms.html"},
}
for _p in D.PROJECTS:
    ROUTES["p:" + _p["slug"]] = {"de": f"projekte/{_p['slug']}.html", "en": f"en/projects/{_p['slug']}.html"}

CAT = {c["key"]: c for c in D.CATEGORIES}

written = []


def esc(s):
    return escape(s, quote=True)


def rel(from_path, target):
    base = posixpath.dirname(from_path) or "."
    return posixpath.relpath(target, base)


def abs_url(path):
    if path.endswith("index.html"):
        path = path[: -len("index.html")]
    return f"{D.SITE_URL}/{path}"


def write(path, text, binary=False):
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        out.write_bytes(text)
    else:
        out.write_text(text, encoding="utf-8", newline="\n")
    written.append(path)


_versions = {}


def version(path):
    """Short content hash, appended to CSS/JS URLs so browsers never keep a stale copy."""
    if path not in _versions:
        try:
            _versions[path] = hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]
        except FileNotFoundError:
            _versions[path] = "0"
    return _versions[path]


class Ctx:
    def __init__(self, lang, pid):
        self.lang = lang
        self.pid = pid
        self.path = ROUTES[pid][lang]
        self.alt_lang = "en" if lang == "de" else "de"

    def t(self, de, en):
        return de if self.lang == "de" else en

    def url(self, pid, frag="", query="", lang=None):
        return rel(self.path, ROUTES[pid][lang or self.lang]) + query + frag

    def asset(self, target):
        url = rel(self.path, target)
        if target.endswith((".css", ".js")):
            url += "?v=" + version(target)
        return url

    def doc(self, key):
        d = next(x for x in D.DOCS if x["key"] == key)
        return self.asset(f"downloads/{self.lang}/{d['file'][self.lang]}")


# ---------------------------------------------------------------- icons
ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "close": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "alert": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "experience": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 12 9 5 9-5"/><path d="m3 16 9 5 9-5"/>',
    "standards": '<path d="M12 3 4 6v6c0 4.5 3.2 8 8 9 4.8-1 8-4.5 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "team": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14.2c2.4.3 4 2.4 4 4.8"/>',
    "schedule": '<rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m9 15 2 2 4-4"/>',
    "transparency": '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/>',
    "education": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "health": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 8v8"/><path d="M8 12h8"/>',
    "landmark": '<path d="M3 22h18"/><path d="M6 18v-7"/><path d="M10 18v-7"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="M12 2 20 7H4z"/>',
    "culture": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "infrastructure": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
}


def icon(name, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


def logo_header(c):
    """Official SDTT logo (brand handbook ch. 4): main version with tagline from 640px up,
    small version (no tagline) below. Files are used unchanged from the logo package."""
    return (f'<img class="brand-logo brand-logo--main" src="{c.asset("assets/img/logo/SDTT_Logo_Haupt_Marineblau.svg")}" '
            f'width="188" height="50" alt="SDTT – Generalunternehmer">'
            f'<img class="brand-logo brand-logo--small" src="{c.asset("assets/img/logo/SDTT_Logo_Klein_Marineblau.svg")}" '
            f'width="132" height="35" alt="SDTT – Generalunternehmer">')


def logo_footer(c):
    return (f'<img class="footer-logo" src="{c.asset("assets/img/logo/SDTT_Logo_Haupt_Weiss.svg")}" '
            f'width="220" height="58" alt="SDTT – Generalunternehmer">')


# ---------------------------------------------------------------- shared fragments
def tel(pair, cls=""):
    display, number = pair
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="tel:{number}">{esc(display)}</a>'


def mailto(addr):
    return f'<a href="mailto:{quote(addr, safe="@")}">{addr}</a>'


def period(p):
    return str(p["start"]) if p["start"] == p["end"] else f"{p['start']}–{p['end']}"


def h(level, inner, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<h{level}{c}>{inner}</h{level}>"


def head(c, title, desc, extra_head=""):
    alt = {lang: abs_url(ROUTES[c.pid][lang]) for lang in LANGS}
    robots = "" if D.INDEXABLE else '\n<meta name="robots" content="noindex, nofollow">'
    full_title = title if c.pid == "home" else f"{title} | SDTT"
    return f"""<!doctype html>
<html lang="{c.lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">{robots}
<link rel="canonical" href="{alt[c.lang]}">
<link rel="alternate" hreflang="de" href="{alt['de']}">
<link rel="alternate" hreflang="en" href="{alt['en']}">
<link rel="alternate" hreflang="x-default" href="{alt['de']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SDTT GmbH">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{alt[c.lang]}">
<meta property="og:locale" content="{c.t('de_DE', 'en_GB')}">
<meta name="theme-color" content="#1a3d66">
<link rel="icon" href="{c.asset('assets/img/logo/SDTT_Bildzeichen_Marineblau.svg')}" type="image/svg+xml">
<link rel="preload" href="{c.asset('assets/fonts/hanken-grotesk-latin-wght-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{c.asset('assets/fonts/public-sans-latin-wght-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{c.asset('assets/css/tokens.css')}">
<link rel="stylesheet" href="{c.asset('assets/css/main.css')}">
<script>document.documentElement.className = "js"; setTimeout(function () {{ if (!window.__rv) document.documentElement.classList.add("rv-fail"); }}, 4000);</script>
<script src="{c.asset('assets/js/main.js')}" defer></script>{extra_head}
</head>"""


def header(c, section):
    def cur(pid):
        return ' aria-current="page"' if section == pid else ""

    cats = "".join(
        f'<li><a href="{c.url("projects", query="?type=" + k["key"], frag="#projects")}">{esc(k["label"][c.lang])}</a></li>'
        for k in D.CATEGORIES
    )
    tender_sub = "".join(
        f'<li><a href="{c.url("tenders", frag=f)}">{label}</a></li>'
        for f, label in [
            ("#process", c.t("Ablauf der Zusammenarbeit", "How we work with you")),
            ("#downloads", c.t("Unterlagen zum Download", "Documents for download")),
            ("#contacts", c.t("Ansprechpartner", "Contacts")),
            ("#faq", c.t("Häufige Fragen", "FAQ")),
        ]
    )
    alt_href = rel(c.path, ROUTES[c.pid][c.alt_lang])
    if c.lang == "de":
        lang_html = (f'<span aria-current="true" lang="de"><span aria-hidden="true">DE</span><span class="visually-hidden">Deutsch</span></span>'
                     f'<span class="lang-sep" aria-hidden="true">|</span>'
                     f'<a href="{alt_href}" hreflang="en" lang="en"><span aria-hidden="true">EN</span><span class="visually-hidden">English</span></a>')
    else:
        lang_html = (f'<a href="{alt_href}" hreflang="de" lang="de"><span aria-hidden="true">DE</span><span class="visually-hidden">Deutsch</span></a>'
                     f'<span class="lang-sep" aria-hidden="true">|</span>'
                     f'<span aria-current="true" lang="en"><span aria-hidden="true">EN</span><span class="visually-hidden">English</span></span>')

    return f"""
<body>
<a class="skip-link" href="#main">{c.t("Zum Inhalt springen", "Skip to content")}</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{c.url('home')}" aria-label="{c.t('SDTT – zur Startseite', 'SDTT – home page')}">
      {logo_header(c)}
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      {icon("menu", "icon icon-menu")}{icon("close", "icon icon-close")}<span>{c.t("Menü", "Menu")}</span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="{c.t('Hauptnavigation', 'Main navigation')}">
      <ul class="nav-list">
        <li class="nav-item--has-sub">
          <div class="nav-item-row">
            <a class="nav-link" href="{c.url('projects')}"{cur('projects')}>{c.t("Öffentliche Projekte", "Public Projects")}</a>
            <button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-projects"><span class="visually-hidden">{c.t("Untermenü Öffentliche Projekte", "Public Projects submenu")}</span>{icon("chevron-down")}</button>
          </div>
          <ul class="sub-menu" id="sub-projects">
            <li><a href="{c.url('projects', frag='#projects')}">{c.t("Alle Projekte", "All projects")}</a></li>
            {cats}
          </ul>
        </li>
        <li><a class="nav-link" href="{c.url('standards')}"{cur('standards')}>{c.t("Normen &amp; Zertifikate", "Standards &amp; Certificates")}</a></li>
        <li><a class="nav-link" href="{c.url('company')}"{cur('company')}>{c.t("Unternehmen", "Company")}</a></li>
        <li class="nav-item--has-sub">
          <div class="nav-item-row">
            <a class="nav-link" href="{c.url('tenders')}"{cur('tenders')}>{c.t("Ausschreibungen", "Tenders")}</a>
            <button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-tenders"><span class="visually-hidden">{c.t("Untermenü Ausschreibungen", "Tenders submenu")}</span>{icon("chevron-down")}</button>
          </div>
          <ul class="sub-menu" id="sub-tenders">{tender_sub}</ul>
        </li>
        <li><a class="nav-link" href="{c.url('contact')}"{cur('contact')}>{c.t("Kontakt", "Contact")}</a></li>
      </ul>
      <div class="lang-switch" role="group" aria-label="{c.t('Sprache wählen', 'Choose language')}">{lang_html}</div>
    </nav>
  </div>
</header>"""


def footer(c):
    co = D.COMPANY
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <p class="footer-brand">{logo_footer(c)}</p>
        <p>{c.t("Generalunternehmer für öffentliche und kommunale Bauprojekte in Stuttgart und Baden-Württemberg.",
                "General contractor for public and municipal construction projects in Stuttgart and Baden-Württemberg.")}</p>
        <p>{c.t("Qualitätsmanagement nach ISO 9001:2015. Ausführung nach VOB/B und DIN.",
                "Quality management to ISO 9001:2015. Execution according to VOB/B and DIN.")}</p>
        <p class="mb-0">{c.t("Partner zahlreicher Kommunen in Baden-Württemberg.", "Partner to many municipalities in Baden-Württemberg.")}</p>
      </div>
      <div>
        <p class="footer-title">{c.t("Schnellzugriff", "Quick links")}</p>
        <ul class="footer-list">
          <li><a href="{c.url('projects')}">{c.t("Öffentliche Projekte", "Public projects")}</a></li>
          <li><a href="{c.url('standards')}">{c.t("Normen &amp; Zertifikate", "Standards &amp; certificates")}</a></li>
          <li><a href="{c.url('company')}">{c.t("Unternehmen", "Company")}</a></li>
          <li><a href="{c.url('tenders', frag='#downloads')}">{c.t("Unterlagen", "Documents")}</a></li>
          <li><a href="{c.url('contact')}">{c.t("Kontakt", "Contact")}</a></li>
        </ul>
        <p class="footer-title">{c.t("Rechtliches", "Legal")}</p>
        <ul class="footer-list">
          <li><a href="{c.url('imprint')}">{c.t("Impressum", "Imprint")}</a></li>
          <li><a href="{c.url('privacy')}">{c.t("Datenschutz", "Privacy policy")}</a></li>
          <li><a href="{c.url('terms')}">{c.t("AGB", "Terms and conditions")}</a></li>
        </ul>
      </div>
      <div>
        <p class="footer-title">{c.t("Kontakt", "Contact")}</p>
        <!-- PLATZHALTER: Kontaktdaten -->
        <ul class="footer-list footer-contact">
          <li>{icon("file")}<span>{c.t("Ausschreibungen", "Tenders")}: {mailto(D.PEOPLE[0]["email"])}</span></li>
          <li>{icon("phone")}<span>{c.t("Telefon", "Phone")}: {tel(co["phone"])}</span></li>
          <li>{icon("chat")}<span>WhatsApp: <a href="https://wa.me/{co["whatsapp"][1]}" rel="noopener">{esc(co["whatsapp"][0])}</a></span></li>
          <li>{icon("alert")}<span>{c.t("Notfall 24/7", "Emergency 24/7")}: {tel(co["emergency"])}</span></li>
          <li>{icon("pin")}<span>{co["street"]}<br>{co["zip_city"]}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2024–{YEAR} SDTT GmbH. {c.t("Alle Rechte vorbehalten.", "All rights reserved.")}</span>
      <span><a href="{c.url('imprint')}">{c.t("Impressum", "Imprint")}</a> · <a href="{c.url('privacy')}">{c.t("Datenschutz", "Privacy")}</a> · <a href="{c.url('terms')}">{c.t("AGB", "Terms")}</a></span>
    </div>
  </div>
</footer>"""


def render(c, title, desc, body, section=None, scripts=(), jsonld=None):
    extra = ""
    for s in scripts:
        extra += f'\n<script src="{c.asset(s)}" defer></script>'
    if jsonld:
        extra += f'\n<script type="application/ld+json">{jsonld}</script>'
    html = (head(c, title, desc, extra) + header(c, section or c.pid)
            + f'\n<main id="main" tabindex="-1">\n{body}\n</main>' + footer(c)
            + f'\n<script src="{c.asset("assets/js/lenis.min.js")}"></script>'
            + f'\n<script src="{c.asset("assets/js/smooth-scroll.js")}"></script>'
            + f'\n<script src="{c.asset("assets/js/reveal.js")}"></script>\n</body>\n</html>\n')
    # Never break a line between "§" and its number.
    write(c.path, html.replace("§ ", "§&nbsp;"))


def page_header(c, h1, lead=None, crumbs=(), eyebrow=None, extra=""):
    bc = ""
    if crumbs:
        items = [f'<li><a href="{c.url("home")}">{c.t("Startseite", "Home")}</a></li>']
        for label, href in crumbs:
            items.append(f'<li><a href="{href}">{label}</a></li>' if href else f'<li aria-current="page">{label}</li>')
        bc = f'<nav class="breadcrumbs" aria-label="{c.t("Brotkrumen-Navigation", "Breadcrumb")}"><ol>{"".join(items)}</ol></nav>'
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    return f"""<div class="page-header">
  <div class="container">
    {bc}{eb}
    <h1>{h1}</h1>
    {ld}{extra}
  </div>
</div>"""


# ---------------------------------------------------------------- components
def img_paths(p):
    """Before / after pictures. Projects with real photos list them under "photos";
    all others get generated placeholder drawings (.svg)."""
    ext = p.get("photos", {}).get("ext", "svg")
    return f"assets/img/projects/{p['slug']}-vorher.{ext}", f"assets/img/projects/{p['slug']}-nachher.{ext}"


def img_size(p):
    ph = p.get("photos")
    return (ph["w"], ph["h"]) if ph else (600, 400)


def ba_pair(c, p, eager=False):
    before, after = img_paths(p)
    iw, ih = img_size(p)
    loading = "" if eager else ' loading="lazy"'
    title = p["title"][c.lang]
    return f"""<div class="ba-pair">
  <figure><a class="zoom" href="{c.asset(before)}" data-lightbox aria-label="{esc(c.t('Vorher-Bild vergrößern', 'Enlarge before picture'))}"><img src="{c.asset(before)}" width="{iw}" height="{ih}"{loading} decoding="async" alt="{esc(c.t(f'{title}: Zustand vor der Sanierung', f'{title}: condition before the works'))}"></a><figcaption>{c.t("Vorher", "Before")}</figcaption></figure>
  <figure><a class="zoom" href="{c.asset(after)}" data-lightbox aria-label="{esc(c.t('Nachher-Bild vergrößern', 'Enlarge after picture'))}"><img src="{c.asset(after)}" width="{iw}" height="{ih}"{loading} decoding="async" alt="{esc(c.t(f'{title}: Zustand nach Fertigstellung', f'{title}: condition after completion'))}"></a><figcaption>{c.t("Nachher", "After")}</figcaption></figure>
</div>"""


def project_table(c, p):
    scope = "".join(f"<li>{esc(s)}</li>" for s in p["scope"][c.lang])
    return f"""<table class="data-table">
  <caption class="visually-hidden">{c.t("Projektdaten", "Project data")}: {esc(p["title"][c.lang])}</caption>
  <tbody>
    <tr><th scope="row">{c.t("Zeitraum", "Period")}</th><td><span class="mono">{period(p)}</span> · {esc(p["duration"][c.lang])}</td></tr>
    <tr><th scope="row">{c.t("Auftragsvolumen", "Contract value")}</th><td>{esc(p["budget"][c.lang])}</td></tr>
    <tr><th scope="row">{c.t("Auftraggeber", "Client")}</th><td>{esc(p["client"][c.lang])}</td></tr>
    <tr><th scope="row">{c.t("Leistungsumfang", "Scope of works")}</th><td><ul class="bullet-list">{scope}</ul></td></tr>
    <tr><th scope="row">{c.t("Team", "Team")}</th><td>{esc(p["team"][c.lang])}</td></tr>
  </tbody>
</table>"""


def cert_tags(p):
    return '<div class="tag-row">' + "".join(f'<span class="tag">{esc(x)}</span>' for x in p["certs"]) + "</div>"


def ref_letter_path(p):
    return f"downloads/referenzen/referenzschreiben-{p['slug']}.pdf"


def ref_box(c, p):
    lang_note = "" if c.lang == "de" else " (in German)"
    letter = (f'<p><strong>{c.t("Referenzschreiben", "Reference letter")}:</strong> '
              f'<a href="{c.asset(ref_letter_path(p))}" download>{c.t("PDF herunterladen", "Download PDF")}{lang_note}</a></p>')
    if p.get("contact"):
        ct = p["contact"]
        name = ct["name"] if c.lang == "de" else ct["name"].replace("Herr ", "Mr ").replace("Frau ", "Ms ")
        person = (f'<p><strong>{c.t("Ansprechpartner beim Auftraggeber", "Client contact")}:</strong> {esc(name)}</p>'
                  f'<p>{c.t("E-Mail", "Email")}: {mailto(ct["email"])} · {c.t("Telefon", "Phone")}: {tel(ct["phone"])}</p>')
    else:
        person = f'<p>{c.t("Ansprechpartner beim Auftraggeber auf Anfrage.", "Client contact available on request.")}</p>'
    return f'<div class="ref-box"><!-- PLATZHALTER: Referenzkontakt -->{letter}{person}</div>'


def ba_slider(c, p):
    """Before/after comparison: drag the handle (or use the keyboard) to wipe between the two photos."""
    before, after = img_paths(p)
    iw, ih = img_size(p)
    title = p["title"][c.lang]
    alt_b = esc(c.t(f"{title}: Zustand vor der Sanierung", f"{title}: condition before the works"))
    alt_a = esc(c.t(f"{title}: Zustand nach Fertigstellung", f"{title}: condition after completion"))
    return f"""<div class="ba-slider" style="--pos:50%">
  <img class="ba-img" src="{c.asset(before)}" width="{iw}" height="{ih}" loading="lazy" decoding="async" alt="{alt_b}">
  <img class="ba-img ba-img--after" src="{c.asset(after)}" width="{iw}" height="{ih}" loading="lazy" decoding="async" alt="{alt_a}">
  <span class="ba-label ba-label--before" aria-hidden="true">{c.t("Vorher", "Before")}</span>
  <span class="ba-label ba-label--after" aria-hidden="true">{c.t("Nachher", "After")}</span>
  <input class="ba-range" type="range" min="0" max="100" step="1" value="50" aria-label="{c.t('Vorher-Nachher-Vergleich: Regler verschieben', 'Before and after comparison: move the slider')}">
  <span class="ba-handle" aria-hidden="true"><span class="ba-grip">{icon("arrow-left")}{icon("arrow-right")}</span></span>
</div>"""


def featured_project(c, p):
    """Home page reference: comparison slider flush on the left half, facts on the right."""
    facts = [
        (c.t("Zeitraum", "Period"), f'<span class="mono">{period(p)}</span> · {esc(p["duration"][c.lang])}', False),
        (c.t("Auftragsvolumen", "Contract value"), esc(p["budget"][c.lang]), False),
        (c.t("Auftraggeber", "Client"), esc(p["client"][c.lang]), False),
        (c.t("Team", "Team"), esc(p["team"][c.lang]), False),
        (c.t("Leistungsumfang", "Scope of works"), bullet_list([esc(s) for s in p["scope"][c.lang]]), True),
    ]
    items = "".join(
        f'<li class="fp-item{" fp-item--wide" if wide else ""}"><span class="fp-num" aria-hidden="true">{i:02d}.</span>'
        f'<h4 class="fp-label">{label}</h4>{value if wide else f"<p>{value}</p>"}</li>'
        for i, (label, value, wide) in enumerate(facts, 1)
    )
    return f"""<article class="featured-project">
  <div class="fp-media">{ba_slider(c, p)}</div>
  <div class="fp-body">
    <h3 class="fp-title"><a href="{c.url('p:' + p['slug'])}">{esc(p["title"][c.lang])}</a></h3>
    <p class="fp-sub">{esc(p["summary"][c.lang])}</p>
    <ol class="fp-list">{items}</ol>
    <p class="fp-more"><a class="link-arrow" href="{c.url('p:' + p['slug'])}">{c.t("Projektdetails und Referenzschreiben", "Project details and reference letter")} {icon("arrow-right")}</a></p>
  </div>
</article>"""


def project_card(c, p, level=3):
    _, after = img_paths(p)
    iw, ih = img_size(p)
    badge = f'<span class="tag tag--sample badge-sample">{c.t("Musterdaten", "Sample data")}</span>' if p["sample"] else ""
    return f"""<article class="project-card" data-type="{p['type']}" data-city="{esc(p['city'])}" data-size="{p['size']}" data-year="{p['end']}">
  <div class="project-card-media"><img src="{c.asset(after)}" width="{iw}" height="{ih}" loading="lazy" decoding="async" alt="">{badge}</div>
  <div class="project-card-body">
    <div class="tag-row"><span class="tag">{esc(CAT[p["type"]]["label"][c.lang])}</span></div>
    {h(level, f'<a href="{c.url("p:" + p["slug"])}">{esc(p["title"][c.lang])}</a>')}
    <p class="meta"><span class="mono">{period(p)}</span> · {esc(p["city"])} · {esc(p["budget"][c.lang])}</p>
    <p class="meta">{esc(p["summary"][c.lang])}</p>
    <a class="link-arrow" href="{c.url('p:' + p['slug'])}" aria-hidden="true" tabindex="-1">{c.t("Projektdetails", "Project details")} {icon("arrow-right")}</a>
  </div>
</article>"""


def contact_card(c, person, level=3):
    """One contact: portrait, role, name, e-mail and phone, focus and tasks.
    The parts are direct children of the card so that a CSS subgrid can line the rows up."""
    sub = f'<p class="contact-role-de" lang="de">({person["role_de"]})</p>' if c.lang == "en" else '<p class="contact-role-de">&nbsp;</p>'
    lines = [
        f'<li>{icon("mail")}<span><span class="visually-hidden">{c.t("E-Mail", "Email")}: </span>{mailto(person["email"])}</span></li>',
        f'<li>{icon("phone")}<span><span class="visually-hidden">{c.t("Telefon", "Phone")}: </span>{tel(person["phone"])}</span></li>',
    ]
    focus = ""
    if person["focus"]:
        focus = f'<p class="contact-focus"><strong>{c.t("Schwerpunkt", "Specialisation")}:</strong> {esc(person["focus"][c.lang])}</p>'
    alt = f'{person["name"]}, {person["role"][c.lang]}'
    photo = ""
    if person.get("photo"):
        photo = (f'<div class="contact-photo"><img src="{c.asset(person["photo"])}" width="800" height="1072" '
                 f'loading="lazy" decoding="async" alt="{esc(alt)}"></div>')
    return f"""<article class="contact-card">
  {photo}
  <!-- PLATZHALTER: Kontaktdaten prüfen -->
  <div class="contact-head">{h(level, esc(person["role"][c.lang]), "contact-role")}{sub}</div>
  <p class="contact-name">{esc(person["name"])}</p>
  <ul class="contact-lines">{"".join(lines)}</ul>
  {focus}
  <p class="contact-fn"><strong>{c.t("Aufgabe", "Role")}:</strong> {esc(person["fn"][c.lang])}</p>
</article>"""


def emergency_block(c):
    return f"""<div class="emergency">
  {icon("alert")}<strong>{c.t("Notfallkontakt (24/7)", "Emergency contact (24/7)")}</strong>
  {tel(D.COMPANY["emergency"])}
  <span class="text-muted">{c.t("Für laufende Baustellen – rund um die Uhr erreichbar.", "For active construction sites – available around the clock.")}</span>
</div>"""


def doc_table(c, level=None):
    rows = []
    for d in D.DOCS:
        rows.append(f"""<tr>
  <td><div class="doc-name">{icon("file")}<div><strong>{esc(d["title"][c.lang])}</strong><small>{esc(d["note"][c.lang])}</small></div></div></td>
  <td class="doc-format">PDF</td>
  <td><a class="btn btn--outline" href="{c.doc(d['key'])}" download>{icon("download")}{c.t("Herunterladen", "Download")}<span class="visually-hidden">: {esc(d["title"][c.lang])}</span></a></td>
</tr>""")
    return f"""<table class="doc-table">
  <caption class="visually-hidden">{c.t("Dokumente zum Download", "Documents for download")}</caption>
  <thead><tr><th scope="col">{c.t("Dokument", "Document")}</th><th scope="col">{c.t("Format", "Format")}</th><th scope="col"><span class="visually-hidden">{c.t("Aktion", "Action")}</span></th></tr></thead>
  <tbody>{"".join(rows)}</tbody>
</table>
<p class="doc-note">{c.t("Alle Dokumente ohne Registrierung abrufbar – zum Ausdrucken und Beifügen zu Ihren Vergabeunterlagen.",
                         "All documents are available without registration – ready to print and attach to your tender files.")}</p>"""


def figures_block(c):
    """Strengths in words, no statistics: icon, one- or two-word title, short text."""
    items = [
        ("experience", c.t("Erfahrung", "Experience"),
         c.t("Langjährige Zusammenarbeit mit Kommunen und öffentlichen Einrichtungen in Baden-Württemberg.",
             "Long-standing work for municipalities and public institutions in Baden-Württemberg.")),
        ("standards", c.t("Normen", "Standards"),
         c.t("Ausführung nach VOB/B, DIN und GEG mit zertifiziertem Qualitätsmanagement nach ISO.",
             "Execution according to VOB/B, DIN and GEG with ISO-certified quality management.")),
        ("team", c.t("Eigenes Personal", "Own staff"),
         c.t("Fest angestellte Fachkräfte und feste Teams über die gesamte Projektdauer.",
             "Permanently employed specialists and stable teams for the full project duration.")),
        ("schedule", c.t("Termintreue", "Reliability"),
         c.t("Verbindliche Bauzeitenpläne mit Pufferzeiten und wöchentlicher Berichterstattung.",
             "Binding construction schedules with buffers and weekly reporting.")),
        ("transparency", c.t("Transparenz", "Transparency"),
         c.t("Schriftliche Freigabe jeder Änderung und wöchentlicher Soll-Ist-Kostenbericht.",
             "Written approval of every change and a weekly budget-versus-actual cost report.")),
    ]
    cells = "".join(
        f'<li class="hl-item">{icon(ic, "icon icon--xl")}<p class="hl-title">{title}</p><p class="hl-text">{text}</p></li>'
        for ic, title, text in items
    )
    return f'<ul class="highlights">{cells}</ul>'


def check_list(items):
    return '<ul class="check-list">' + "".join(f"<li>{icon('check')}<span>{x}</span></li>" for x in items) + "</ul>"


def bullet_list(items):
    return '<ul class="bullet-list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def competence(c):
    """Competence slider: one picture per slide, short text inside the picture (bottom left)."""
    slides = [
        (c.t("Erfahrung", "Experience"),
         c.t("Erfahrung und Historie", "Experience and track record"),
         c.t("Langjährige Zusammenarbeit mit Kommunen und öffentlichen Einrichtungen: viele abgeschlossene Projekte, zuverlässig eingehaltene Termine und ein hoher Anteil an Folgeaufträgen.",
             "Long-standing work for municipalities and public institutions: many completed projects, reliably met deadlines and a high share of repeat orders."),
         c.t("Langjährige Praxis im öffentlichen Bau.", "Long-standing practice in public construction.")),
        (c.t("Normen", "Standards"),
         c.t("Zertifizierung und Normen", "Certification and standards"),
         c.t("Qualitätsmanagement nach ISO 9001:2015, Ausführung nach VOB/B, DIN und GEG, Arbeitsschutz nach DGUV und fünf Jahre Mängelhaftung. Nachweise durch TÜV und DEKRA.",
             "Quality management to ISO 9001:2015, execution to VOB/B, DIN and GEG, occupational safety to DGUV and five years' liability for defects. Proof issued by TÜV and DEKRA."),
         c.t("Geprüfte Standards, belegt durch unabhängige Stellen.", "Verified standards, proven by independent bodies.")),
        (c.t("Ressourcen", "Resources"),
         c.t("Ressourcen und Kapazitäten", "Resources and capacity"),
         c.t("Fest angestelltes Fachpersonal, ein Netzwerk qualifizierter Nachunternehmer und gesicherte Kapazität für parallele Projekte, mit eigenem Materiallager und Pufferressourcen.",
             "Permanently employed specialists, a network of qualified subcontractors and guaranteed capacity for parallel projects, with its own material store and buffer resources."),
         c.t("Gesicherte Kapazität auch für parallele Projekte.", "Guaranteed capacity, including for parallel projects.")),
    ]
    alts = [
        c.t("Bauleiter mit Schutzhelm und Vertreter der Kommune prüfen Pläne vor einem sanierten Schulgebäude.",
            "A site manager in a hard hat and a municipal representative review drawings in front of a refurbished school building."),
        c.t("Ein unabhängiger Prüfer und der Bauleiter kontrollieren mit Wasserwaage und Tablet ein eingebautes Fenster.",
            "An independent inspector and the site manager check an installed window with a spirit level and a tablet."),
        c.t("Mehrere Teams arbeiten parallel in einem Rohbau an Fenstern, Trockenbau und Installation, ein Polier koordiniert.",
            "Several teams work in parallel in a building shell on windows, drywall and installations while a foreman coordinates."),
    ]
    total = len(slides)
    items = ""
    for i, (chip, title, text, caption) in enumerate(slides, 1):
        items += f"""<li class="cs-slide" role="group" aria-roledescription="{c.t('Folie', 'slide')}" aria-label="{i} / {total}" data-caption="{esc(caption)}">
  <img class="cs-img" src="{c.asset(f'assets/img/competence/slide-{i}.jpg')}" width="1800" height="1004" loading="lazy" decoding="async" alt="{esc(alts[i - 1])}">
  <span class="cs-chip">{chip}</span>
  <div class="cs-text"><h3>{title}</h3><p>{text}</p></div>
</li>"""
    first_caption = slides[0][3]
    return f"""<div class="cs" role="group" aria-roledescription="carousel" aria-labelledby="credentials-title">
  <div class="cs-head">
    <div class="cs-head-left">
      <h2 id="credentials-title">{c.t("Warum Kommunen und öffentliche Auftraggeber uns vertrauen", "Why municipalities and public authorities trust us")}</h2>
    </div>
    <p class="cs-intro">{c.t("Erfahrung, geprüfte Standards und gesicherte Kapazitäten – die drei Grundlagen unserer Arbeit für die öffentliche Hand.",
                             "Experience, verified standards and guaranteed capacity – the three foundations of our work for the public sector.")}</p>
  </div>
  <div class="cs-main">
    <div class="cs-side">
      <div class="cs-status" aria-live="polite" aria-atomic="true">
        <p class="cs-count"><span class="cs-num">01</span><span class="cs-total">/{total:02d}</span></p>
        <p class="cs-caption">{esc(first_caption)}</p>
      </div>
      <div class="cs-controls">
        <button class="cs-btn cs-prev" type="button" aria-label="{c.t('Vorherige Folie', 'Previous slide')}">{icon("arrow-left")}</button>
        <button class="cs-btn cs-next" type="button" aria-label="{c.t('Nächste Folie', 'Next slide')}">{icon("arrow-right")}</button>
      </div>
    </div>
    <div class="cs-viewport" tabindex="0" aria-label="{c.t('Kompetenzen, mit den Pfeiltasten blättern', 'Credentials, use the arrow keys to browse')}">
      <ul class="cs-track">{items}</ul>
    </div>
  </div>
</div>"""


def requirements(c):
    reqs = [
        (c.t("VOB/DIN-Konformität", "VOB/DIN compliance"), [
            c.t("Ausführung aller Leistungen nach VOB/B, VOB/C und den einschlägigen DIN-Normen", "All works carried out according to VOB/B, VOB/C and the relevant DIN standards"),
            c.t("Uneingeschränkter Zugang für die Bauüberwachung des Auftraggebers", "Unrestricted access for the client's site supervision"),
            c.t("Baufortschrittsberichte mindestens wöchentlich", "Progress reports at least weekly"),
            c.t("Vollständige Dokumentation: Bestandspläne, Materialnachweise, Prüfprotokolle", "Complete documentation: as-built drawings, material certificates, test reports"),
            c.t("Vertragsstrafen bei Terminüberschreitung gemäß Ausschreibung (§ 11 VOB/B)", "Contractual penalties for delays as set out in the tender (§ 11 VOB/B)"),
        ]),
        (c.t("Qualitätsmanagement", "Quality management"), [
            c.t("Prozesse nach ISO 9001:2015", "Processes according to ISO 9001:2015"),
            c.t("Abnahmebegleitung durch unabhängige Prüfer (TÜV oder DEKRA)", "Acceptance supported by independent inspectors (TÜV or DEKRA)"),
            c.t("Mindestens zwei interne oder externe Audits pro Monat", "At least two internal or external audits per month"),
            c.t("Nachweise für alle Materialien (CE-Kennzeichnung, Prüfzeugnisse)", "Certificates for all materials (CE marking, test certificates)"),
            c.t("Mängelhaftung bis zu 5 Jahre gemäß § 634a BGB", "Liability for defects of up to 5 years under § 634a BGB"),
        ]),
        (c.t("Arbeitssicherheit", "Site safety"), [
            c.t("Sicherheitskoordination nach DGUV Regel 100-001 und Baustellenverordnung", "Safety coordination according to DGUV Rule 100-001 and the Construction Site Ordinance"),
            c.t("Jährliche, dokumentierte Unterweisung aller Beschäftigten", "Annual documented safety training for all employees"),
            c.t("Notfallplan für jede Baustelle", "Emergency plan for every site"),
            c.t("Unfall- und Ereignisbuch, für den Auftraggeber einsehbar", "Accident and incident log, open to the client"),
            c.t("Null-Unfall-Ziel mit dokumentierter Gefährdungsbeurteilung", "Zero-accident target with documented risk assessment"),
        ]),
        (c.t("Kostenkontrolle", "Cost control"), [
            c.t("Detaillierte Kostenaufstellung 30 Tage vor Baubeginn", "Detailed cost breakdown 30 days before construction starts"),
            c.t("Nachträge nur nach schriftlicher Beauftragung durch den Auftraggeber", "Change orders only after written instruction by the client"),
            c.t("Wöchentlicher Soll-Ist-Kostenbericht", "Weekly budget-versus-actual cost report"),
            c.t("Keine versteckten Kosten", "No hidden costs"),
            c.t("Abweichung höchstens ±5 % von der Ausgangskalkulation", "Deviation of no more than ±5% from the initial estimate"),
        ]),
    ]
    blocks = "".join(f"""<article class="req">
  <span class="req-label">{c.t("Anforderung", "Requirement")} {i}</span>
  <h3>{title}</h3>
  {bullet_list(items)}
</article>""" for i, (title, items) in enumerate(reqs, 1))
    return f'<div class="grid grid--2">{blocks}</div>'


def faq(c):
    qa = [
        (c.t("Arbeiten Sie nach VOB/B?", "Do you work according to VOB/B?"),
         c.t("Ja. Grundlage unserer Verträge mit öffentlichen Auftraggebern sind die VOB/B und VOB/C sowie die jeweiligen Vergabeunterlagen. Abweichende Vertragsbedingungen des Auftraggebers haben Vorrang.",
             "Yes. Our contracts with public clients are based on VOB/B and VOB/C and the relevant tender documents. The client's own contract conditions take precedence.")),
        (c.t("Welche Auftragsgrößen übernehmen Sie?", "What contract sizes do you take on?"),
         c.t("In der Regel Projekte von 0,5 bis 5 Mio. € netto. Größere Vorhaben realisieren wir auf Anfrage auch in einer Arbeitsgemeinschaft (ARGE).",
             "Typically projects from €0.5 m to €5 m net. On request we also deliver larger projects as part of a joint venture (ARGE).")),
        (c.t("Wie schnell erhalten wir Eignungsnachweise?", "How quickly can we receive proof of eligibility?"),
         c.t("Die Standardunterlagen stehen auf dieser Seite zum Download bereit. Projektspezifische Nachweise senden wir in der Regel innerhalb von zwei Werktagen.",
             "The standard documents are available for download on this page. We usually send project-specific proof within two working days.")),
        (c.t("Können wir Referenzen direkt beim Auftraggeber prüfen?", "Can we verify references directly with the client?"),
         c.t("Ja. Zu jedem Referenzprojekt nennen wir – mit deren Einverständnis – eine Ansprechperson beim Auftraggeber sowie das Referenzschreiben als PDF.",
             "Yes. For every reference project we name a contact person at the client – with their consent – and provide the reference letter as a PDF.")),
        (c.t("Arbeiten Sie im laufenden Betrieb von Schulen und Kliniken?", "Do you work while schools and hospitals stay open?"),
         c.t("Ja. Bauabschnitte, Lärmzeiten, Staubschutz und Hygienekonzepte stimmen wir vorab mit der Einrichtung ab.",
             "Yes. Construction phases, noisy work periods, dust protection and hygiene concepts are agreed with the facility in advance.")),
        (c.t("Welche Gewährleistung gilt?", "Which warranty applies?"),
         c.t("Für Bauwerke gilt die fünfjährige Verjährungsfrist für Mängelansprüche nach § 634a BGB. Bei VOB/B-Verträgen vereinbaren wir auf Wunsch ebenfalls fünf Jahre anstelle der Regelfrist von vier Jahren.",
             "For buildings, claims for defects become time-barred after five years under § 634a BGB. For VOB/B contracts we also agree five years on request instead of the standard four years.")),
        (c.t("Stellen Sie Sicherheitsleistungen?", "Do you provide security bonds?"),
         c.t("Ja. Vertragserfüllungs- und Mängelansprüchebürgschaften stellen wir über Banken und Kreditversicherer.",
             "Yes. We provide performance and warranty bonds through banks and credit insurers.")),
        (c.t("In welcher Region sind Sie tätig?", "Which region do you cover?"),
         c.t("Schwerpunkt sind die Landeshauptstadt Stuttgart, die Region Stuttgart und Baden-Württemberg.",
             "Our focus is the city of Stuttgart, the Stuttgart region and Baden-Württemberg.")),
    ]
    items = "".join(f"""<details>
  <summary><span>{q}</span>{icon("chevron-down")}</summary>
  <div class="faq-body"><p>{a}</p></div>
</details>""" for q, a in qa)
    return f'<div class="faq">{items}</div>'


def section_head(title, intro=None, eyebrow=None, hid=None, level=2):
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    idattr = f' id="{hid}"' if hid else ""
    p = f"<p>{intro}</p>" if intro else ""
    return f'<div class="section-head">{eb}<h{level}{idattr}>{title}</h{level}>{p}</div>'


def cta_band(c):
    return f"""<section class="section section--cta" aria-labelledby="cta-title">
  <div class="container cta-band">
    <div>
      <h2 id="cta-title">{c.t("Unterlagen für Ihre Ausschreibung", "Documents for your tender")}</h2>
      <p>{c.t("Projektarchiv, Zertifikate und Referenzschreiben – ohne Registrierung.", "Project archive, certificates and reference letters – no registration required.")}</p>
    </div>
    <div class="btn-row">
      <a class="btn btn--primary" href="{c.url('tenders', frag='#downloads')}">{icon("download")}{c.t("Zu den Unterlagen", "Go to documents")}</a>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- pages
def page_home(lang):
    c = Ctx(lang, "home")
    featured = [p for p in D.PROJECTS if p["featured"]]
    co = D.COMPANY
    body = f"""
<div class="hero-track">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-media" aria-hidden="true">
    <img class="hero-poster" src="{c.asset('assets/video/hero-poster.jpg')}" width="1920" height="1080" fetchpriority="high" decoding="async" alt="">
    <video class="hero-video" muted playsinline preload="none" tabindex="-1" width="1280" height="720"
           data-src="{c.asset('assets/video/hero-scrub.mp4')}" data-src-small="{c.asset('assets/video/hero-scrub-sm.mp4')}"></video>
  </div>
  <div class="container hero-inner">
    <div class="hero-grid">
      <div class="hero-copy">
        <h1 id="hero-title">{c.t("Zuverlässiger Partner für öffentliche und kommunale Bauprojekte", "A reliable partner for public and municipal construction projects")}</h1>
        <p class="lead">{c.t("Langjährige Erfahrung. Zahlreiche abgeschlossene Projekte. Unterschiedliche Größenordnungen. VOB/DIN-konform.",
                             "Long-standing experience. Numerous completed projects. Every scale. VOB/DIN compliant.")}</p>
        <div class="btn-row">
          <a class="btn btn--primary btn--lg" href="{c.doc('archive')}" download>{icon("download")}{c.t("Projektarchiv herunterladen (PDF)", "Download project archive (PDF)")}</a>
        </div>
      </div>
    </div>
  </div>
</section>
</div>

<section class="section" aria-label="{c.t('Unsere Stärken', 'Our strengths')}" style="padding-bottom:0">
  <div class="container">{figures_block(c)}</div>
</section>

<section class="section">
  <div class="container">
    {competence(c)}
  </div>
</section>

<section class="section section--grey" aria-labelledby="portfolio-title">
  <div class="container">
    {section_head(c.t("Referenzen: öffentliche Bauprojekte", "References: public construction projects"),
                  c.t("Ausschließlich öffentliche Auftraggeber. Zu jedem Projekt: Zeitraum, Auftragsvolumen, Auftraggeber und Leistungsumfang. Referenzschreiben finden Sie auf den Projektseiten.",
                      "Public clients only. For every project: period, contract value, client and scope of works. Reference letters are on the project pages."),
                  hid="portfolio-title")}
    {"".join(featured_project(c, p) for p in featured)}
    <div class="btn-row mt-7">
      <a class="btn btn--outline" href="{c.url('projects')}">{c.t("Alle öffentlichen Projekte ansehen", "View all public projects")} {icon("arrow-right")}</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="standards-title">
  <div class="container">
    {section_head(c.t("Unsere Zusagen für öffentliche Projekte", "Our commitments for public projects"),
                  c.t("Verbindliche Standards, die wir in jedem Vertrag mit öffentlichen Auftraggebern einhalten.",
                      "Binding standards we meet in every contract with public clients."),
                  hid="standards-title")}
    {requirements(c)}
    <div class="btn-row mt-7">
      <a class="btn btn--primary" href="{c.doc('methodology')}" download>{icon("download")}{c.t("Projektmanagement-Methodik herunterladen (PDF)", "Download project management methodology (PDF)")}</a>
      <a class="link-arrow" href="{c.url('standards')}">{c.t("Alle Normen und Zertifikate", "All standards and certificates")} {icon("arrow-right")}</a>
    </div>
  </div>
</section>

<section class="section section--grey" aria-labelledby="tender-contacts">
  <div class="container">
    {section_head(c.t("Ansprechpartner für Ausschreibungen und Vergabe", "Contacts for public procurement and tenders"),
                  c.t("Feste Ansprechpartner für Vergabestellen – von der Angebotsphase bis zur Abnahme.",
                      "Dedicated contacts for contracting authorities – from the bidding phase to acceptance."),
                  hid="tender-contacts")}
    <div class="grid grid--3 grid--contacts">{"".join(contact_card(c, p) for p in D.PEOPLE)}</div>
    {emergency_block(c)}
  </div>
</section>

<section class="section" aria-labelledby="downloads-title">
  <div class="container">
    {section_head(c.t("Unterlagen zum Download", "Documents for download"),
                  c.t("Alle Nachweise für Ihre Eignungsprüfung an einem Ort.", "All proof for your eligibility assessment in one place."),
                  hid="downloads-title")}
    {doc_table(c)}
  </div>
</section>
"""
    jsonld = ('{"@context":"https://schema.org","@type":"GeneralContractor","name":"SDTT GmbH",'
              f'"logo":"{D.SITE_URL}/assets/img/logo/SDTT_Logo_Haupt_Marineblau.svg",'
              f'"url":"{D.SITE_URL}/","email":"{co["email"]}","telephone":"{co["phone"][1]}",'
              f'"address":{{"@type":"PostalAddress","streetAddress":"{co["street"]}","postalCode":"40474","addressLocality":"Düsseldorf","addressRegion":"Nordrhein-Westfalen","addressCountry":"DE"}},'
              '"areaServed":"Baden-Württemberg"}')
    render(c,
           c.t("SDTT – Generalunternehmer für öffentliche Bauprojekte in Stuttgart und Baden-Württemberg",
               "SDTT – General contractor for public construction projects in Stuttgart and Baden-Württemberg"),
           c.t("Zuverlässiger Partner für öffentliche und kommunale Bauprojekte: Schulen, Kliniken, Verwaltungsgebäude. ISO 9001, VOB/DIN, GEG. Unterlagen für Ausschreibungen ohne Registrierung.",
               "A reliable partner for public and municipal construction projects: schools, hospitals, administrative buildings. ISO 9001, VOB/DIN, GEG. Tender documents without registration."),
           body, scripts=["assets/js/hero-scrub.js", "assets/js/ba-slider.js", "assets/js/slider.js"], jsonld=jsonld)


def page_projects(lang):
    c = Ctx(lang, "projects")
    counts = {k["key"]: sum(1 for p in D.PROJECTS if p["type"] == k["key"]) for k in D.CATEGORIES}
    tiles = "".join(f"""<a class="cat-tile" href="{c.url('projects', query='?type=' + k['key'], frag='#projects')}">
  {icon(k["icon"])}<strong>{esc(k["label"][c.lang])}</strong><span>{esc(k["desc"][c.lang])}</span>
  <span class="count">{counts[k["key"]]} {c.t("Projekte", "projects") if counts[k["key"]] != 1 else c.t("Projekt", "project")}</span>
</a>""" for k in D.CATEGORIES)

    cities = sorted({p["city"] for p in D.PROJECTS})
    years = sorted({p["end"] for p in D.PROJECTS}, reverse=True)
    opt = lambda v, label: f'<option value="{esc(v)}">{esc(label)}</option>'  # noqa: E731
    sel_type = opt("", c.t("Alle Typen", "All types")) + "".join(opt(k["key"], k["label"][c.lang]) for k in D.CATEGORIES)
    sel_city = opt("", c.t("Alle Orte", "All locations")) + "".join(opt(x, x) for x in cities)
    sel_size = opt("", c.t("Alle Größen", "All sizes")) + "".join(opt(k, v[c.lang]) for k, v in D.SIZES.items())
    sel_year = opt("", c.t("Alle Jahre", "All years")) + "".join(opt(str(y), str(y)) for y in years)

    cards = "".join(project_card(c, p) for p in D.PROJECTS)
    body = page_header(
        c, c.t("Öffentliche Projekte", "Public projects"),
        c.t("Referenzen ausschließlich für öffentliche Auftraggeber: Bildung, Gesundheit, Verwaltung und Kultur in Stuttgart und Baden-Württemberg.",
            "References exclusively for public clients: education, healthcare, administration and culture in Stuttgart and Baden-Württemberg."),
        crumbs=[(c.t("Öffentliche Projekte", "Public projects"), None)],
    ) + f"""
<section class="section" aria-labelledby="categories-title">
  <div class="container">
    {section_head(c.t("Projektbereiche", "Project categories"), level=2, hid="categories-title")}
    <div class="grid grid--4">{tiles}</div>
  </div>
</section>

<section class="section section--grey" aria-labelledby="projects">
  <div class="container">
    {section_head(c.t("Projektübersicht", "Project overview"),
                  c.t("Filtern Sie nach Objekttyp, Ort, Größenordnung und Fertigstellungsjahr. Mit „Musterdaten“ gekennzeichnete Projekte sind Platzhalter.",
                      "Filter by building type, location, size and year of completion. Projects marked “Sample data” are placeholders."),
                  hid="projects")}
    <form class="filter" id="project-filter" hidden aria-label="{c.t('Projekte filtern', 'Filter projects')}">
      <div class="field"><label for="f-type">{c.t("Objekttyp", "Building type")}</label><select id="f-type" name="f-type">{sel_type}</select></div>
      <div class="field"><label for="f-city">{c.t("Ort", "Location")}</label><select id="f-city" name="f-city">{sel_city}</select></div>
      <div class="field"><label for="f-size">{c.t("Größenordnung", "Project size")}</label><select id="f-size" name="f-size">{sel_size}</select></div>
      <div class="field"><label for="f-year">{c.t("Fertigstellung", "Completed")}</label><select id="f-year" name="f-year">{sel_year}</select></div>
      <button class="btn btn--outline" type="reset">{c.t("Zurücksetzen", "Reset")}</button>
    </form>
    <p class="filter-status" id="filter-status" role="status" hidden
       data-one="{c.t('{n} von {total} Projekten angezeigt', '{n} of {total} projects shown')}"
       data-many="{c.t('{n} von {total} Projekten angezeigt', '{n} of {total} projects shown')}"></p>
    <div class="grid grid--3" id="project-list">{cards}</div>
    <div class="empty-state" id="filter-empty" hidden>
      <p><strong>{c.t("Keine Projekte für diese Auswahl.", "No projects match this selection.")}</strong></p>
      <p class="mb-0">{c.t("Bitte ändern Sie die Filter oder fordern Sie das vollständige Projektarchiv an.", "Please change the filters or download the complete project archive.")}</p>
    </div>
  </div>
</section>
{cta_band(c)}"""
    render(c, c.t("Öffentliche Projekte", "Public projects"),
           c.t("Referenzprojekte für Kommunen und öffentliche Auftraggeber in Baden-Württemberg: Schulen, Kliniken, Verwaltungsgebäude und Kultur.",
               "Reference projects for municipalities and public clients in Baden-Württemberg: schools, hospitals, administrative buildings and culture."),
           body, scripts=["assets/js/projects-filter.js"])


def page_project(lang, p):
    c = Ctx(lang, "p:" + p["slug"])
    title = p["title"][c.lang]
    paragraphs = p.get("text", {}).get(c.lang) or [p["summary"][c.lang]]
    text = "".join(f"<p>{esc(x)}</p>" for x in paragraphs)
    body = page_header(
        c, esc(title), esc(p["summary"][c.lang]),
        crumbs=[(c.t("Öffentliche Projekte", "Public projects"), c.url("projects")), (esc(title), None)],
    ) + f"""
<section class="section" aria-label="{c.t('Fotodokumentation', 'Photo documentation')}">
  <div class="container">
    {ba_pair(c, p, eager=True)}
    <p class="text-muted mt-6" style="font-size:var(--fs-small)">{c.t("Fotodokumentation zum Vergleich von Ausgangs- und Endzustand.", "Photo documentation comparing the initial and final condition.")}{c.t(" Platzhalterbilder.", " Placeholder images.") if p["sample"] and not p.get("photos") else ""}</p>
  </div>
</section>
<section class="section section--grey">
  <div class="container">
    <div class="grid grid--split">
      <div>
        <h2>{c.t("Technische Beschreibung", "Technical description")}</h2>
        {text}
        <h3>{c.t("Leistungsumfang", "Scope of works")}</h3>
        {check_list([esc(s) for s in p["scope"][c.lang]])}
        <h3 class="mt-6">{c.t("Normen und Nachweise", "Standards and proof")}</h3>
        {cert_tags(p)}
      </div>
      <div>
        <h2>{c.t("Projektdaten", "Project data")}</h2>
        <div class="card">{project_table(c, p)}</div>
      </div>
    </div>
    <div class="btn-row mt-7">
      <a class="btn btn--outline" href="{c.url('projects', frag='#projects')}">{icon("arrow-left")}{c.t("Alle Projekte", "All projects")}</a>
      <a class="btn btn--primary" href="{c.doc('archive')}" download>{icon("download")}{c.t("Projektarchiv herunterladen (PDF)", "Download project archive (PDF)")}</a>
    </div>
  </div>
</section>"""
    render(c, title,
           c.t(f"{title}: {p['summary']['de']} Auftraggeber: {p['client']['de']}.",
               f"{title}: {p['summary']['en']} Client: {p['client']['en']}."),
           body, section="projects", scripts=["assets/js/lightbox.js"])


def page_standards(lang):
    c = Ctx(lang, "standards")
    blocks = [
        ("ISO 9001:2015", c.t("Qualitätsmanagementsystem", "Quality management system"), "iso",
         c.t("Zertifiziertes Qualitätsmanagement", "Certified quality management"),
         c.t("Unser Qualitätsmanagementsystem ist nach ISO 9001:2015 zertifiziert und wird jährlich durch eine unabhängige Zertifizierungsstelle überprüft.",
             "Our quality management system is certified to ISO 9001:2015 and audited annually by an independent certification body."),
         [c.t("Dokumentierte Prozesse von der Kalkulation bis zur Abnahme", "Documented processes from estimating to acceptance"),
          c.t("Regelmäßige interne Audits und Managementbewertung", "Regular internal audits and management reviews"),
          c.t("Lückenlose Rückverfolgbarkeit von Materialien und Prüfungen", "Full traceability of materials and inspections")], "certificates"),
        ("VOB/B · VOB/C · DIN", c.t("Vergabe- und Vertragsordnung für Bauleistungen", "German construction contract procedures"), "vob",
         c.t("VOB/DIN-Konformität", "VOB/DIN compliance"),
         c.t("Wir führen alle Leistungen nach VOB/B (Vertragsbedingungen) und VOB/C (Allgemeine Technische Vertragsbedingungen, ATV) sowie den einschlägigen DIN-Normen aus.",
             "We carry out all works according to VOB/B (contract conditions) and VOB/C (general technical specifications, ATV) and the relevant DIN standards."),
         [c.t("Transparente Abrechnung nach Aufmaß", "Transparent invoicing based on measured quantities"),
          c.t("Schriftliche Bedenkenanzeigen und Behinderungsanzeigen nach § 4 und § 6 VOB/B", "Written notices of concerns and hindrances under § 4 and § 6 VOB/B"),
          c.t("Förmliche Abnahme nach § 12 VOB/B", "Formal acceptance under § 12 VOB/B")], "methodology"),
        ("GEG", c.t("Gebäudeenergiegesetz", "Buildings Energy Act"), "geg",
         c.t("Energetische Anforderungen", "Energy requirements"),
         c.t("Energetische Sanierungen und Neubauten führen wir nach den Anforderungen des Gebäudeenergiegesetzes aus und dokumentieren die Nachweise für den Auftraggeber.",
             "We carry out energy refurbishments and new builds according to the Buildings Energy Act and document the proof for the client."),
         [c.t("Ausführung nach Energiebedarfsausweis und Fachplanung", "Execution according to the energy performance calculation and specialist design"),
          c.t("Luftdichtheitsprüfung auf Anforderung", "Airtightness testing on request"),
          c.t("Unternehmererklärungen nach GEG", "Contractor declarations under the GEG")], None),
        ("DGUV Regel 100-001", c.t("Grundsätze der Prävention", "Principles of prevention"), "dguv",
         c.t("Arbeitssicherheit auf der Baustelle", "Occupational safety on site"),
         c.t("Arbeitsschutz organisieren wir nach DGUV Regel 100-001, dem Arbeitsschutzgesetz (ArbSchG), der Arbeitsstättenverordnung (ArbStättV) und der Baustellenverordnung.",
             "We organise occupational safety according to DGUV Rule 100-001, the Occupational Safety and Health Act (ArbSchG), the Workplace Ordinance (ArbStättV) and the Construction Site Ordinance."),
         [c.t("Gefährdungsbeurteilung und Notfallplan für jede Baustelle", "Risk assessment and emergency plan for every site"),
          c.t("Jährliche dokumentierte Unterweisungen", "Annual documented safety training"),
          c.t("Unfall- und Ereignisbuch, einsehbar für den Auftraggeber", "Accident and incident log open to the client")], None),
        ("§ 634a BGB", c.t("Verjährung der Mängelansprüche", "Limitation of claims for defects"), "bgb",
         c.t("5 Jahre Gewährleistung", "5-year warranty"),
         c.t("Für Bauwerke haften wir fünf Jahre ab Abnahme für Mängel. Bei VOB/B-Verträgen vereinbaren wir auf Wunsch ebenfalls fünf Jahre.",
             "For buildings we are liable for defects for five years from acceptance. For VOB/B contracts we also agree five years on request."),
         [c.t("Mängelbeseitigung durch eigenes Personal", "Defects remedied by our own staff"),
          c.t("Gewährleistungsbürgschaft auf Anforderung", "Warranty bond on request"),
          c.t("Begehung vor Ablauf der Gewährleistungsfrist", "Inspection before the warranty period expires")], "warranty"),
        ("Handwerkskammer", c.t("Handwerkskammer Region Stuttgart", "Stuttgart Region Chamber of Crafts"), "hwk",
         c.t("Eintragung in die Handwerksrolle", "Entry in the trade register"),
         c.t("Die SDTT GmbH ist bei der Handwerkskammer Region Stuttgart in die Handwerksrolle eingetragen. Die Eintragungsnummer finden Sie im Impressum.",
             "SDTT GmbH is entered in the trade register of the Stuttgart Region Chamber of Crafts. The registration number is listed in the imprint."),
         [c.t("Meisterbetrieb in den eingetragenen Gewerken", "Master craftsman business in the registered trades"),
          c.t("Ausbildungsbetrieb", "Training company")], None),
    ]
    html_blocks = ""
    for code, name, bid, title, text, bullets, doc in blocks:
        dl = ""
        if doc:
            d = next(x for x in D.DOCS if x["key"] == doc)
            dl = f'<p class="mt-6 mb-0"><a class="link-arrow" href="{c.doc(doc)}" download>{icon("download")}{esc(d["title"][c.lang])} (PDF)</a></p>'
        html_blocks += f"""<div class="std-block" id="{bid}">
  <div><p class="std-code" lang="de">{code}</p><p class="std-name">{name}</p></div>
  <div>
    <h2>{title}</h2>
    <p>{text}</p>
    <h3 class="visually-hidden">{c.t("Was das für Sie bedeutet", "What this means for you")}</h3>
    {check_list(bullets)}
    {dl}
  </div>
</div>"""
    body = page_header(
        c, c.t("Normen &amp; Zertifikate", "Standards &amp; certificates"),
        c.t("Die Standards, nach denen wir für öffentliche Auftraggeber bauen – mit Nachweisen zum Download.",
            "The standards we build to for public clients – with proof available for download."),
        crumbs=[(c.t("Normen &amp; Zertifikate", "Standards &amp; certificates"), None)],
    ) + f"""
<section class="section">
  <div class="container"><!-- PLATZHALTER: Zertifikatsnummern und Prüfstellen ergänzen -->{html_blocks}</div>
</section>
<section class="section section--grey" aria-labelledby="commitments-title">
  <div class="container">
    {section_head(c.t("Unsere Zusagen in jedem Vertrag", "Our commitments in every contract"), hid="commitments-title")}
    {requirements(c)}
  </div>
</section>
{cta_band(c)}"""
    render(c, c.t("Normen & Zertifikate", "Standards & certificates"),
           c.t("ISO 9001:2015, VOB/B und DIN, GEG, DGUV Regel 100-001 und 5 Jahre Gewährleistung nach § 634a BGB – Nachweise für öffentliche Auftraggeber.",
               "ISO 9001:2015, VOB/B and DIN, GEG, DGUV Rule 100-001 and a 5-year warranty under § 634a BGB – proof for public clients."),
           body)


def page_company(lang):
    c = Ctx(lang, "company")
    steps = [
        (c.t("Projektstart und Bauablaufplanung", "Project start and scheduling"),
         c.t("Abstimmung mit Auftraggeber und Fachplanern, Terminplan mit Pufferzeiten, Baustelleneinrichtung.",
             "Coordination with the client and specialist designers, schedule with buffers, site set-up.")),
        (c.t("Kostenaufstellung", "Cost breakdown"),
         c.t("Detaillierte Kostenaufstellung 30 Tage vor Baubeginn, Freigabe durch den Auftraggeber.",
             "Detailed cost breakdown 30 days before construction starts, approved by the client.")),
        (c.t("Ausführung mit Wochenberichten", "Execution with weekly reports"),
         c.t("Baufortschritts- und Soll-Ist-Kostenberichte jede Woche, Nachträge nur nach schriftlicher Beauftragung.",
             "Progress and budget-versus-actual reports every week, change orders only after written instruction.")),
        (c.t("Qualitätssicherung", "Quality assurance"),
         c.t("Eigene Prüfungen nach ISO 9001 und Begleitung durch unabhängige Prüfer (TÜV oder DEKRA).",
             "In-house inspections to ISO 9001 and support from independent inspectors (TÜV or DEKRA).")),
        (c.t("Abnahme und Dokumentation", "Acceptance and documentation"),
         c.t("Förmliche Abnahme, Übergabe von Bestandsplänen, Materialnachweisen und Prüfprotokollen.",
             "Formal acceptance, handover of as-built drawings, material certificates and test reports.")),
        (c.t("Gewährleistung", "Warranty"),
         c.t("Fünf Jahre Mängelhaftung, Mängelbeseitigung durch eigenes Personal.",
             "Five years' liability for defects, remedied by our own staff.")),
    ]
    steps_html = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in steps)
    body = page_header(
        c, c.t("Unternehmen", "Company"),
        c.t("Generalunternehmer für öffentliche Bauprojekte mit Sitz in Stuttgart – eigenes Personal, geprüfte Prozesse, feste Ansprechpartner.",
            "General contractor for public construction projects based in Stuttgart – own staff, audited processes, dedicated contacts."),
        crumbs=[(c.t("Unternehmen", "Company"), None)],
    ) + f"""
<section class="section" aria-labelledby="history-title">
  <div class="container">
    <div class="grid grid--split">
      <div>
        <!-- PLATZHALTER: Firmengeschichte mit realen Daten ergänzen -->
        <h2 id="history-title">{c.t("Geschichte", "History")}</h2>
        <p>{c.t("Seit über 20 Jahren realisiert SDTT Bauprojekte für Kommunen, Landkreise und öffentliche Einrichtungen in der Region Stuttgart und in Baden-Württemberg.",
                "For more than 20 years SDTT has delivered construction projects for municipalities, districts and public institutions in the Stuttgart region and Baden-Württemberg.")}</p>
        <p>{c.t("Aus einem Handwerksbetrieb ist ein Generalunternehmer mit eigenem Fachpersonal entstanden. Unser Projektarchiv umfasst über 120 abgeschlossene öffentliche Projekte – von der Kita-Sanierung bis zur Modernisierung eines Rathauses.",
                "What began as a craft business has grown into a general contractor with its own specialist staff. Our project archive covers more than 120 completed public projects – from day-care centre refurbishments to town hall modernisations.")}</p>
      </div>
      <div>
        <h2>{c.t("Team", "Team")}</h2>
        <p>{c.t("Über 90 fest angestellte Mitarbeitende: Bauingenieure, Bauleiter, Poliere, Fachhandwerker und Fachkräfte für Qualitätssicherung und Arbeitssicherheit.",
                "More than 90 permanent employees: civil engineers, site managers, foremen, skilled tradespeople and specialists in quality assurance and site safety.")}</p>
        {check_list([c.t("Eigene Bauleitung und Poliere in jedem Projekt", "Own site management and foremen on every project"),
                      c.t("Feste Teams über die gesamte Projektdauer", "Stable teams for the full project duration"),
                      c.t("Lebensläufe des Schlüsselpersonals als PDF", "CVs of key personnel as PDF")])}
        <p class="mt-6 mb-0"><a class="link-arrow" href="{c.doc('cvs')}" download>{icon("download")}{c.t("Lebensläufe herunterladen (PDF)", "Download CVs (PDF)")}</a></p>
      </div>
    </div>
    <div class="mt-7">{figures_block(c)}</div>
  </div>
</section>

<section class="section section--grey" aria-labelledby="resources-title">
  <div class="container">
    {section_head(c.t("Ressourcen und Kapazitäten", "Resources and capacity"),
                  c.t("Gesicherte Kapazität auch für parallele Projekte unterschiedlicher Größenordnung.", "Guaranteed capacity, including for parallel projects of different sizes."),
                  hid="resources-title")}
    <div class="grid grid--3">
      <article class="card"><h3 class="card-title">{c.t("Personal", "Staff")}</h3>{check_list([c.t("Großer Stamm fest angestellter Fachkräfte", "Large core of permanent specialists"), c.t("Netzwerk qualifizierter Nachunternehmer", "Network of qualified subcontractors"), c.t("Pufferressourcen für Planänderungen", "Buffer resources for design changes")])}</article>
      <article class="card"><h3 class="card-title">{c.t("Material und Logistik", "Materials and logistics")}</h3>{check_list([c.t("Eigenes Materiallager in Stuttgart", "Own material store in Stuttgart"), c.t("Kurzfristige Einsätze und Notfallreparaturen", "Short-notice assignments and emergency repairs"), c.t("Eigene Baustelleneinrichtung", "Own site equipment")])}</article>
      <article class="card"><h3 class="card-title">{c.t("Projektgrößen", "Project sizes")}</h3>{check_list([c.t("Projekte von 0,5 bis 5 Mio. € netto", "Projects from €0.5 m to €5 m net"), c.t("Größere Vorhaben in Arbeitsgemeinschaft", "Larger projects as a joint venture"), c.t("Mehrere Baustellen parallel", "Several sites in parallel")])}</article>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="method-title">
  <div class="container">
    {section_head(c.t("Methodik für Großprojekte", "Methodology for major projects"),
                  c.t("Ein festgelegter Ablauf mit klaren Berichtspflichten – vom Projektstart bis zur Gewährleistung.",
                      "A defined process with clear reporting duties – from project start to the warranty period."),
                  hid="method-title")}
    <ol class="steps">{steps_html}</ol>
    <div class="btn-row mt-7"><a class="btn btn--primary" href="{c.doc('methodology')}" download>{icon("download")}{c.t("Projektmanagement-Methodik herunterladen (PDF)", "Download project management methodology (PDF)")}</a></div>
  </div>
</section>

<section class="section section--grey" aria-labelledby="management-title">
  <div class="container">
    {section_head(c.t("Geschäftsleitung", "Management"), hid="management-title")}
    <!-- PLATZHALTER: Geschäftsführung -->
    <div class="grid grid--2">
      <article class="contact-card">
        <h3 class="contact-role">{c.t("Geschäftsführung", "Managing director")}</h3>
        <p class="contact-name mt-6"><span class="placeholder">{c.t("[PLATZHALTER Name]", "[PLACEHOLDER name]")}</span></p>
        <ul class="contact-lines">
          <li>{icon("mail")}<span>{mailto(D.COMPANY["email"])}</span></li>
          <li>{icon("phone")}<span>{tel(D.COMPANY["phone"])}</span></li>
        </ul>
      </article>
      <article class="contact-card">
        <h3 class="contact-role">{c.t("Öffentliche Ausschreibungen", "Public procurement")}</h3>
        <p class="contact-name mt-6">{esc(D.PEOPLE[0]["name"])}</p>
        <ul class="contact-lines">
          <li>{icon("mail")}<span>{mailto(D.PEOPLE[0]["email"])}</span></li>
          <li>{icon("phone")}<span>{tel(D.PEOPLE[0]["phone"])}</span></li>
        </ul>
      </article>
    </div>
  </div>
</section>"""
    render(c, c.t("Unternehmen", "Company"),
           c.t("SDTT GmbH: über 20 Jahre Erfahrung mit öffentlichen Auftraggebern, über 90 fest angestellte Mitarbeitende, Methodik für Großprojekte.",
               "SDTT GmbH: more than 20 years with public clients, over 90 permanent employees, a proven methodology for major projects."),
           body)


def page_tenders(lang):
    c = Ctx(lang, "tenders")
    titles = [
        c.t("Kontakt und Bekanntmachung", "Contact and notice"),
        c.t("Eignungsnachweise", "Proof of eligibility"),
        c.t("Angebot", "Bid"),
        c.t("Aufklärung und Zuschlag", "Clarification and award"),
        c.t("Ausführung", "Execution"),
        c.t("Abnahme und Gewährleistung", "Acceptance and warranty"),
    ]
    texts = [
        c.t(f"Senden Sie uns die Bekanntmachung oder die Vergabeunterlagen an {D.PEOPLE[0]['email']}. Wir bestätigen den Eingang innerhalb eines Werktags.",
            f"Send us the contract notice or tender documents at {D.PEOPLE[0]['email']}. We confirm receipt within one working day."),
        c.t("Zertifikate, Referenzen, Versicherungsnachweise und Lebensläufe stehen unten zum Download bereit. Projektspezifische Nachweise folgen in der Regel innerhalb von zwei Werktagen.",
            "Certificates, references, proof of insurance and CVs are available for download below. Project-specific proof usually follows within two working days."),
        c.t("Fristgerechte Abgabe über die von Ihnen vorgegebene Vergabeplattform, vollständig und formgerecht.",
            "Submission on time via the e-procurement platform you specify, complete and in the required form."),
        c.t("Wir beantworten Aufklärungsfragen kurzfristig und benennen das Projektteam verbindlich.",
            "We answer clarification requests at short notice and commit to the named project team."),
        c.t("Ausführung nach VOB/B mit wöchentlichen Fortschritts- und Kostenberichten.",
            "Execution according to VOB/B with weekly progress and cost reports."),
        c.t("Förmliche Abnahme, vollständige Dokumentation und fünf Jahre Mängelhaftung.",
            "Formal acceptance, complete documentation and five years' liability for defects."),
    ]
    steps_html = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in zip(titles, texts))
    body = page_header(
        c, c.t("Ausschreibungen &amp; Vergabe", "Tenders &amp; procurement"),
        c.t("Alles, was Vergabestellen für die Eignungsprüfung brauchen: Ablauf, Unterlagen, Ansprechpartner und Antworten auf häufige Fragen.",
            "Everything contracting authorities need for the eligibility assessment: process, documents, contacts and answers to common questions."),
        crumbs=[(c.t("Ausschreibungen &amp; Vergabe", "Tenders &amp; procurement"), None)],
    ) + f"""
<section class="section" aria-labelledby="process">
  <div class="container">
    {section_head(c.t("So arbeiten wir mit Kommunen zusammen", "How we work with municipalities"), hid="process")}
    <ol class="steps">{steps_html}</ol>
  </div>
</section>

<section class="section section--grey" aria-labelledby="downloads">
  <div class="container">
    {section_head(c.t("Unterlagen zum Download", "Documents for download"),
                  c.t("Sieben Dokumente für Ihre Vergabeakte – ohne Registrierung.", "Seven documents for your tender file – no registration required."),
                  hid="downloads")}
    {doc_table(c)}
  </div>
</section>

<section class="section" aria-labelledby="contacts">
  <div class="container">
    {section_head(c.t("Ansprechpartner für Ausschreibungen", "Contacts for tenders"), hid="contacts")}
    <div class="grid grid--3 grid--contacts">{"".join(contact_card(c, p) for p in D.PEOPLE)}</div>
    {emergency_block(c)}
  </div>
</section>

<section class="section section--grey" aria-labelledby="faq">
  <div class="container container--narrow">
    {section_head(c.t("Häufige Fragen", "Frequently asked questions"), hid="faq")}
    {faq(c)}
  </div>
</section>"""
    render(c, c.t("Ausschreibungen & Vergabe", "Tenders & procurement"),
           c.t("Unterlagen für Vergabestellen ohne Registrierung: Projektarchiv, Zertifikate, Referenzschreiben, Lebensläufe, Methodik, Gewährleistung, Versicherung.",
               "Documents for contracting authorities without registration: project archive, certificates, reference letters, CVs, methodology, warranty, insurance."),
           body)


def page_contact(lang):
    c = Ctx(lang, "contact")
    co = D.COMPANY
    body = page_header(
        c, c.t("Kontakt", "Contact"),
        c.t("Direkte Ansprechpartner für Vergabe, Technik und Qualität – und ein Notfallkontakt rund um die Uhr.",
            "Direct contacts for procurement, technical matters and quality – plus an emergency line around the clock."),
        crumbs=[(c.t("Kontakt", "Contact"), None)],
    ) + f"""
<section class="section" aria-labelledby="departments-title">
  <div class="container">
    {section_head(c.t("Abteilungen", "Departments"), hid="departments-title")}
    <div class="grid grid--3 grid--contacts">{"".join(contact_card(c, p) for p in D.PEOPLE)}</div>
    {emergency_block(c)}
  </div>
</section>
<section class="section section--grey" aria-labelledby="office-title">
  <div class="container">
    <div class="grid grid--split">
      <div>
        <!-- PLATZHALTER: Anschrift und Zentrale -->
        <h2 id="office-title">{c.t("Zentrale", "Head office")}</h2>
        <ul class="contact-lines">
          <li>{icon("pin")}<span>SDTT GmbH<br>{co["street"]}<br>{co["zip_city"]}<br>{co["country"][c.lang]}</span></li>
          <li>{icon("phone")}<span>{tel(co["phone"])}</span></li>
          <li>{icon("mail")}<span>{mailto(co["email"])}</span></li>
          <li>{icon("chat")}<span>WhatsApp: <a href="https://wa.me/{co["whatsapp"][1]}" rel="noopener">{esc(co["whatsapp"][0])}</a></span></li>
          <li>{icon("clock")}<span>{co["hours"][c.lang]}</span></li>
        </ul>
      </div>
      <div>
        <h2>{c.t("Anfragen von Vergabestellen", "Enquiries from contracting authorities")}</h2>
        <p>{c.t("Bitte senden Sie Bekanntmachungen und Vergabeunterlagen direkt an", "Please send contract notices and tender documents directly to")} {mailto(D.PEOPLE[0]["email"])}.
           {c.t("Eingangsbestätigung innerhalb eines Werktags.", "We confirm receipt within one working day.")}</p>
        <p>{c.t("Unterlagen für die Eignungsprüfung finden Sie ohne Registrierung unter", "Documents for the eligibility assessment are available without registration under")}
           <a href="{c.url('tenders', frag='#downloads')}">{c.t("Ausschreibungen &amp; Vergabe", "Tenders &amp; procurement")}</a>.</p>
        <p class="text-muted" style="font-size:var(--fs-small)">{c.t("Hinweise zur Verarbeitung Ihrer Daten finden Sie in der", "Information on how we process your data is available in our")}
           <a href="{c.url('privacy')}">{c.t("Datenschutzerklärung", "privacy policy")}</a>.</p>
      </div>
    </div>
  </div>
</section>"""
    render(c, c.t("Kontakt", "Contact"),
           c.t("Kontakt zu SDTT: Abteilung öffentliche Ausschreibungen, technische Leitung, Qualitätsmanagement und 24/7-Notfallkontakt.",
               "Contact SDTT: public procurement, technical department, quality management and 24/7 emergency line."),
           body)


def ph(c, de, en=None):
    return f'<span class="placeholder">[{c.t("PLATZHALTER", "PLACEHOLDER")}: {c.t(de, en or de)}]</span>'


def legal_page(c, title, desc, inner):
    notice = c.t("Entwurf mit Platzhaltern – vor Veröffentlichung rechtlich prüfen lassen.",
                 "Draft with placeholders – to be reviewed by a lawyer before publication.")
    lang_note = "" if c.lang == "de" else '<p class="text-muted">This English version is provided for information only. The German version is legally binding.</p>'
    body = page_header(c, title, crumbs=[(title, None)]) + f"""
<section class="section">
  <div class="container"><div class="prose">
    <div class="notice">{notice}</div>
    {lang_note}
    {inner}
  </div></div>
</section>"""
    render(c, title, desc, body)


def page_imprint(lang):
    c = Ctx(lang, "imprint")
    co = D.COMPANY
    inner = f"""
<h2>{c.t("Angaben gemäß § 5 DDG", "Information pursuant to § 5 DDG (German Digital Services Act)")}</h2>
<p>SDTT GmbH<br>{co["street"]}<br>{co["zip_city"]}<br>{co["country"][c.lang]}</p>
<h2>{c.t("Vertreten durch", "Represented by")}</h2>
<p>{c.t("Geschäftsführer", "Managing director")}: {ph(c, "Name", "name")}</p>
<h2>{c.t("Kontakt", "Contact")}</h2>
<p>{c.t("Telefon", "Phone")}: {tel(co["phone"])}<br>{c.t("E-Mail", "Email")}: {mailto(co["email"])}</p>
<h2>{c.t("Registereintrag", "Register entry")}</h2>
<p>{c.t("Registergericht", "Register court")}: {c.t("Amtsgericht Stuttgart", "Local Court (Amtsgericht) Stuttgart")}<br>{c.t("Registernummer", "Register number")}: HRB {ph(c, "Nummer", "number")}</p>
<h2>{c.t("Umsatzsteuer-ID", "VAT ID")}</h2>
<p>{c.t("Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG", "VAT identification number according to § 27a UStG")}: DE {ph(c, "Nummer", "number")}</p>
<h2>{c.t("Handwerkskammer und Berufsrecht", "Chamber of Crafts and professional regulations")}</h2>
<p>{c.t("Zuständige Kammer", "Competent chamber")}: Handwerkskammer Region Stuttgart, Heilbronner Straße 43, 70191 Stuttgart<br>
{c.t("Eintragung in die Handwerksrolle", "Entry in the trade register")}: {c.t("Nr.", "No.")} {ph(c, "Nummer", "number")}<br>
{c.t("Berufsbezeichnung", "Professional title")}: {ph(c, "z. B. Maurer- und Betonbauermeister", "e.g. master bricklayer and concrete builder")} ({c.t("verliehen in Deutschland", "awarded in Germany")})<br>
{c.t("Berufsrechtliche Regelung", "Professional regulation")}: {c.t("Handwerksordnung (HwO)", "Crafts Code (Handwerksordnung, HwO)")}</p>
<h2>{c.t("Berufshaftpflichtversicherung", "Professional liability insurance")}</h2>
<p>{c.t("Versicherer", "Insurer")}: {ph(c, "Name und Anschrift", "name and address")}<br>{c.t("Geltungsbereich", "Territorial scope")}: {c.t("Deutschland", "Germany")}</p>
<h2>{c.t("Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV", "Responsible for content pursuant to § 18(2) MStV")}</h2>
<p>{ph(c, "Name, Anschrift wie oben", "name, address as above")}</p>
<h2>{c.t("Verbraucherstreitbeilegung", "Consumer dispute resolution")}</h2>
<p>{c.t("Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.",
        "We are neither willing nor obliged to take part in dispute resolution proceedings before a consumer arbitration board.")}</p>"""
    legal_page(c, c.t("Impressum", "Imprint"),
               c.t("Impressum der SDTT GmbH, Stuttgart.", "Imprint of SDTT GmbH, Stuttgart."), inner)


def page_privacy(lang):
    c = Ctx(lang, "privacy")
    co = D.COMPANY
    inner = f"""
<h2>{c.t("1. Verantwortlicher", "1. Controller")}</h2>
<p>SDTT GmbH, {co["street"]}, {co["zip_city"]}<br>{c.t("E-Mail", "Email")}: {mailto(co["email"])} · {c.t("Telefon", "Phone")}: {tel(co["phone"])}</p>
<p>{c.t("Datenschutzbeauftragte/r", "Data protection officer")}: {ph(c, "Name und Kontakt, falls bestellt", "name and contact, if appointed")}</p>
<h2>{c.t("2. Bereitstellung der Website und Server-Logfiles", "2. Hosting and server log files")}</h2>
<p>{c.t("Beim Aufruf der Website verarbeitet unser Hosting-Anbieter technisch notwendige Daten (IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browsertyp) zur Auslieferung und Absicherung der Website. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Die Logfiles werden nach",
        "When you visit the website, our hosting provider processes technically necessary data (IP address, date and time, requested page, browser type) to deliver and secure the website. The legal basis is Art. 6(1)(f) GDPR. Log files are deleted after")}
   {ph(c, "Anzahl", "number")} {c.t("Tagen gelöscht.", "days.")}</p>
<p>{c.t("Hosting-Anbieter", "Hosting provider")}: {ph(c, "Name und Anschrift", "name and address")}. {c.t("Mit dem Anbieter besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO.", "A data processing agreement under Art. 28 GDPR is in place with the provider.")}</p>
<h2>{c.t("3. Keine Cookies, kein Tracking", "3. No cookies, no tracking")}</h2>
<p>{c.t("Diese Website setzt keine Cookies und verwendet keine Analyse- oder Tracking-Dienste. Schriftarten werden lokal von unserem Server geladen; es findet keine Verbindung zu Servern Dritter statt.",
        "This website does not set cookies and does not use analytics or tracking services. Fonts are loaded locally from our server; no connection to third-party servers is made.")}</p>
<h2>{c.t("4. Kontakt per E-Mail, Telefon oder WhatsApp", "4. Contact by email, phone or WhatsApp")}</h2>
<p>{c.t("Wenn Sie uns kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung der Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) bzw. Art. 6 Abs. 1 lit. f DSGVO. Bei Nutzung von WhatsApp gelten zusätzlich die Datenschutzbestimmungen der WhatsApp Ireland Ltd.; dabei können Daten in Drittländer übermittelt werden.",
        "If you contact us, we process your details to handle your enquiry. The legal basis is Art. 6(1)(b) GDPR (pre-contractual measures) or Art. 6(1)(f) GDPR. If you use WhatsApp, the privacy policy of WhatsApp Ireland Ltd. also applies, and data may be transferred to third countries.")}</p>
<h2>{c.t("5. Speicherdauer", "5. Storage period")}</h2>
<p>{c.t("Wir löschen personenbezogene Daten, sobald der Zweck entfällt und keine gesetzlichen Aufbewahrungspflichten (z. B. nach HGB oder AO) entgegenstehen.",
        "We delete personal data as soon as the purpose no longer applies, unless statutory retention obligations (e.g. under the German Commercial Code or Fiscal Code) require otherwise.")}</p>
<h2>{c.t("6. Ihre Rechte", "6. Your rights")}</h2>
<p>{c.t("Sie haben das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21 DSGVO).",
        "You have the right of access (Art. 15), rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), data portability (Art. 20) and objection (Art. 21 GDPR).")}</p>
<h2>{c.t("7. Beschwerderecht", "7. Right to lodge a complaint")}</h2>
<p>{c.t("Sie können sich bei einer Datenschutz-Aufsichtsbehörde beschweren. Zuständig für uns ist der Landesbeauftragte für den Datenschutz und die Informationsfreiheit Baden-Württemberg.",
        "You can lodge a complaint with a data protection supervisory authority. The authority responsible for us is the State Commissioner for Data Protection and Freedom of Information of Baden-Württemberg.")}</p>
<p class="text-muted">{c.t("Stand", "Last updated")}: {ph(c, "Datum", "date")}</p>"""
    legal_page(c, c.t("Datenschutzerklärung", "Privacy policy"),
               c.t("Datenschutzerklärung der SDTT GmbH nach DSGVO.", "Privacy policy of SDTT GmbH under the GDPR."), inner)


def page_terms(lang):
    c = Ctx(lang, "terms")
    sections = [
        (c.t("§ 1 Geltungsbereich", "§ 1 Scope"),
         c.t("Diese Bedingungen gelten für Verträge der SDTT GmbH mit öffentlichen Auftraggebern, insbesondere Kommunen, Landkreisen, Landes- und Bundesbehörden sowie Unternehmen der öffentlichen Hand.",
             "These terms apply to contracts between SDTT GmbH and public clients, in particular municipalities, districts, state and federal authorities and publicly owned companies.")),
        (c.t("§ 2 Vertragsgrundlagen und Rangfolge", "§ 2 Contract basis and order of precedence"),
         c.t("Es gelten in folgender Reihenfolge: die Vergabeunterlagen und besonderen Vertragsbedingungen des Auftraggebers, die VOB/B, die VOB/C sowie ergänzend diese Bedingungen. Bei Widersprüchen gehen die Bedingungen des Auftraggebers vor.",
             "The following apply in this order: the client's tender documents and special contract conditions, VOB/B, VOB/C and, additionally, these terms. In case of conflict, the client's conditions prevail.")),
        (c.t("§ 3 Angebote", "§ 3 Bids"),
         c.t("Angebote sind für die in den Vergabeunterlagen genannte Bindefrist verbindlich.",
             "Bids are binding for the validity period stated in the tender documents.")),
        (c.t("§ 4 Ausführungsfristen", "§ 4 Completion dates"),
         c.t("Ausführungsfristen richten sich nach § 5 VOB/B und dem vereinbarten Bauzeitenplan. Vertragsstrafen gelten nach Maßgabe der Vergabeunterlagen (§ 11 VOB/B).",
             "Completion dates follow § 5 VOB/B and the agreed construction schedule. Contractual penalties apply as set out in the tender documents (§ 11 VOB/B).")),
        (c.t("§ 5 Nachträge", "§ 5 Change orders"),
         c.t("Zusätzliche oder geänderte Leistungen werden nur nach schriftlicher Beauftragung durch den Auftraggeber ausgeführt (§ 2 Abs. 5 und 6 VOB/B).",
             "Additional or changed works are carried out only after written instruction by the client (§ 2(5) and (6) VOB/B).")),
        (c.t("§ 6 Abnahme", "§ 6 Acceptance"),
         c.t("Die Abnahme erfolgt förmlich nach § 12 VOB/B.", "Acceptance takes place formally under § 12 VOB/B.")),
        (c.t("§ 7 Mängelansprüche", "§ 7 Claims for defects"),
         c.t("Die Verjährungsfrist für Mängelansprüche bei Bauwerken beträgt fünf Jahre ab Abnahme (§ 634a BGB bzw. vertraglich vereinbart nach § 13 Abs. 4 VOB/B).",
             "The limitation period for claims for defects in buildings is five years from acceptance (§ 634a BGB or as agreed under § 13(4) VOB/B).")),
        (c.t("§ 8 Zahlung und Sicherheiten", "§ 8 Payment and security"),
         c.t("Zahlungen erfolgen nach § 16 VOB/B. Sicherheitsleistungen werden nach § 17 VOB/B durch Bürgschaft gestellt.",
             "Payments are made according to § 16 VOB/B. Security is provided by guarantee according to § 17 VOB/B.")),
        (c.t("§ 9 Gerichtsstand", "§ 9 Place of jurisdiction"),
         c.t("Gerichtsstand ist, soweit zulässig, Stuttgart. Es gilt deutsches Recht.",
             "To the extent permitted, the place of jurisdiction is Stuttgart. German law applies.")),
    ]
    inner = "".join(f"<h2>{a}</h2><p>{b}</p>" for a, b in sections)
    inner += f'<p class="text-muted">{c.t("Stand", "Last updated")}: {ph(c, "Datum", "date")}</p>'
    legal_page(c, c.t("Allgemeine Geschäftsbedingungen", "General terms and conditions"),
               c.t("Allgemeine Geschäftsbedingungen der SDTT GmbH für öffentliche Auftraggeber.",
                   "General terms and conditions of SDTT GmbH for public clients."), inner)


def page_404():
    html = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Seite nicht gefunden – Page not found | SDTT</title>
<link rel="icon" href="/assets/img/logo/SDTT_Bildzeichen_Marineblau.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/tokens.css">
<link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
<main id="main" class="section">
  <div class="container container--narrow">
    <p class="eyebrow">404</p>
    <h1>Seite nicht gefunden</h1>
    <p>Die angeforderte Seite existiert nicht oder wurde verschoben.</p>
    <p><a class="btn btn--primary" href="/">Zur Startseite</a></p>
    <hr style="border:0;border-top:1px solid var(--color-border);margin:var(--space-7) 0">
    <h2 lang="en">Page not found</h2>
    <p lang="en">The page you requested does not exist or has been moved.</p>
    <p lang="en"><a class="btn btn--outline" href="/en/">Go to home page</a></p>
  </div>
</main>
</body>
</html>
"""
    write("404.html", html)


# ---------------------------------------------------------------- images
def building_svg(floors, seed, after, w=600, h=400):
    rnd = random.Random(seed)
    sky = "#e6edf4" if after else "#d6d5d1"
    ground = "#c3c9bd" if after else "#a8a49b"
    facade = "#f6f5f1" if after else "#b8b1a5"
    glass = "#3b6894" if after else "#7b8086"
    frame = "#1a3d66" if after else "#5f5a52"
    ground_y = h - 56
    fh = min(72, (ground_y - 50) // (floors + 0.6))
    bw = rnd.choice([w * 0.62, w * 0.7, w * 0.78])
    bx = (w - bw) / 2
    bh = fh * floors + 26
    by = ground_y - bh
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
           f'<rect width="{w}" height="{h}" fill="{sky}"/>',
           f'<rect y="{ground_y}" width="{w}" height="{h - ground_y}" fill="{ground}"/>',
           f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{facade}"/>',
           f'<rect x="{bx - 6:.0f}" y="{by - 10:.0f}" width="{bw + 12:.0f}" height="12" fill="{frame}"/>']
    cols = max(4, int(bw // 62))
    cw = bw / cols
    win_w = cw * 0.52
    win_h = fh * 0.56
    for f in range(floors):
        y = by + 18 + f * fh
        for i in range(cols):
            x = bx + i * cw + (cw - win_w) / 2
            if f == floors - 1 and i == cols // 2:
                continue  # entrance below
            if not after and rnd.random() < 0.18:
                out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{win_w:.0f}" height="{win_h:.0f}" fill="#9b958a"/>')
                continue
            out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{win_w:.0f}" height="{win_h:.0f}" fill="{glass}"/>')
            out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{win_w:.0f}" height="{win_h:.0f}" fill="none" stroke="{frame}" stroke-width="3"/>')
            if after:
                out.append(f'<line x1="{x + win_w / 2:.0f}" y1="{y:.0f}" x2="{x + win_w / 2:.0f}" y2="{y + win_h:.0f}" stroke="{frame}" stroke-width="2"/>')
    dx = bx + (cols // 2) * cw + (cw - win_w) / 2
    dh = fh * 0.78
    out.append(f'<rect x="{dx:.0f}" y="{ground_y - dh:.0f}" width="{win_w:.0f}" height="{dh:.0f}" fill="{frame}"/>')
    if after:
        out.append(f'<rect x="{bx:.0f}" y="{ground_y - 8:.0f}" width="{bw:.0f}" height="8" fill="#1a3d66"/>')
        for tx in (bx - 40, bx + bw + 40):
            if 20 < tx < w - 20:
                out.append(f'<rect x="{tx - 3:.0f}" y="{ground_y - 30:.0f}" width="6" height="30" fill="#5c4a36"/>')
                out.append(f'<circle cx="{tx:.0f}" cy="{ground_y - 44:.0f}" r="22" fill="#4a7c59"/>')
    else:
        for _ in range(5):
            sx = bx + rnd.random() * bw
            out.append(f'<rect x="{sx:.0f}" y="{by:.0f}" width="{4 + rnd.random() * 10:.0f}" height="{bh * (0.3 + rnd.random() * 0.5):.0f}" fill="#000" opacity="0.07"/>')
        cx = bx + bw * (0.2 + rnd.random() * 0.6)
        out.append(f'<polyline points="{cx:.0f},{by + 30:.0f} {cx + 12:.0f},{by + 60:.0f} {cx + 4:.0f},{by + 92:.0f} {cx + 18:.0f},{by + 130:.0f}" fill="none" stroke="#5f5a52" stroke-width="2"/>')
    out.append("</svg>")
    return "\n".join(out)


def build_images():
    for p in D.PROJECTS:
        if p.get("photos"):
            continue  # real photos are supplied as files
        before, after = img_paths(p)
        write(before, building_svg(p["floors"], p["seed"], False))
        write(after, building_svg(p["floors"], p["seed"], True))


# ---------------------------------------------------------------- PDFs
def make_pdf(lines):
    """Minimal one-page PDF (Helvetica, WinAnsi). lines: list of (size, text)."""
    def pdf_str(s):
        b = s.encode("cp1252", errors="replace")
        return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")

    y = 780
    content = b"BT\n"
    for size, text in lines:
        content += f"/F1 {size} Tf 1 0 0 1 56 {y} Tm\n".encode() + b"(" + pdf_str(text) + b") Tj\n"
        y -= int(size * 1.6)
    content += b"ET\n"
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"endstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


def build_pdfs():
    co = D.COMPANY
    for lang in LANGS:
        de = lang == "de"
        for d in D.DOCS:
            lines = [
                (20, d["title"][lang]),
                (11, d["note"][lang]),
                (10, ""),
                (11, f"SDTT GmbH · {co['street']} · {co['zip_city']}"),
                (10, ""),
                (12, "PLATZHALTERDOKUMENT" if de else "PLACEHOLDER DOCUMENT"),
                (11, "Wird vor Veröffentlichung durch das Originaldokument ersetzt." if de
                     else "To be replaced with the original document before publication."),
                (10, ""),
            ]
            if d["key"] == "archive":
                lines.append((12, "Projektübersicht (Auszug)" if de else "Project overview (extract)"))
                for p in D.PROJECTS:
                    lines.append((9, f"{period(p)}  {p['title'][lang]}  –  {p['budget'][lang]}"))
            write(f"downloads/{lang}/{d['file'][lang]}", make_pdf(lines), binary=True)
    for p in D.PROJECTS:
        lines = [
            (18, "Referenzschreiben"),
            (12, p["title"]["de"]),
            (10, ""),
            (11, f"Auftraggeber: {p['client']['de']}"),
            (11, f"Zeitraum: {period(p)}  ·  Auftragsvolumen: {p['budget']['de']}"),
            (10, ""),
            (12, "PLATZHALTERDOKUMENT"),
            (11, "Wird durch das unterzeichnete Referenzschreiben des Auftraggebers ersetzt."),
        ]
        write(ref_letter_path(p), make_pdf(lines), binary=True)


# ---------------------------------------------------------------- sitemap / robots
def build_sitemap():
    urls = []
    for pid, paths in ROUTES.items():
        for lang in LANGS:
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(paths[l])}"/>' for l in LANGS)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{abs_url(paths["de"])}"/>'
            urls.append(f"  <url>\n    <loc>{abs_url(paths[lang])}</loc>{alts}\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    if D.INDEXABLE:
        robots = f"User-agent: *\nAllow: /\n\nSitemap: {D.SITE_URL}/sitemap.xml\n"
    else:
        robots = "# Placeholder content – indexing disabled until go-live (site_data.INDEXABLE).\nUser-agent: *\nDisallow: /\n"
    write("robots.txt", robots)


# ---------------------------------------------------------------- main
def main():
    for lang in LANGS:
        page_home(lang)
        page_projects(lang)
        for p in D.PROJECTS:
            page_project(lang, p)
        page_standards(lang)
        page_company(lang)
        page_tenders(lang)
        page_contact(lang)
        page_imprint(lang)
        page_privacy(lang)
        page_terms(lang)
    page_404()
    build_images()
    build_pdfs()
    build_sitemap()
    print(f"Built {len(written)} files.")


if __name__ == "__main__":
    main()
