# sdtt.de

Bilingual (German default, English under `/en/`) static website for SDTT GmbH,
general contractor for public and municipal construction projects.

## How it works

The site is plain HTML/CSS/JS. The HTML pages are **generated** — do not edit
the `.html` files by hand, they are overwritten on every build.

| What to change | Where |
| --- | --- |
| Projects, contacts, documents, key figures | `tools/site_data.py` |
| Page texts (DE and EN side by side), layout | `tools/build.py` |
| Colours, fonts, spacing | `assets/css/tokens.css` |
| Components and layout styles | `assets/css/main.css` |
| Navigation / filter behaviour | `assets/js/main.js`, `assets/js/projects-filter.js` |

Build (Python 3, standard library only):

```bash
python tools/build.py
```

Preview locally:

```bash
python -m http.server 8080
```

Then open http://localhost:8080 (German) or http://localhost:8080/en/ (English).

## Before go-live

- Replace all data marked `PLATZHALTER` / `[PLACEHOLDER]` (names, phone numbers,
  projects, figures, imprint and privacy details).
- Replace the generated placeholder PDFs in `downloads/` and images in
  `assets/img/` with the real files (keep the file names or update `site_data.py`).
- Have the Impressum, Datenschutzerklärung and AGB reviewed by a lawyer.
- Set `INDEXABLE = True` in `tools/site_data.py` and rebuild. Until then every
  page has `noindex` and `robots.txt` blocks crawlers.
- Configure the host to serve `404.html` for missing pages.

## Rules

- Only German and English on the site.
- No cookies, no trackers, no third-party requests (fonts are self-hosted:
  Public Sans and IBM Plex Mono, SIL Open Font License).
