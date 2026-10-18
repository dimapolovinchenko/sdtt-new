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

Preview locally (this server supports HTTP range requests, which the scroll-controlled
hero video needs; `python -m http.server` does not):

```bash
python tools/serve.py 8080
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

## Brand

Fonts and logo follow the SDTT brand handbook (v1.6):

- Hanken Grotesk (headings, large numbers), Public Sans (text), IBM Plex Mono (data, labels).
  Self-hosted in `assets/fonts/`, licence texts (SIL OFL 1.1) in `assets/fonts/licenses/`.
- Logo files from the official logo package are used unchanged (`assets/img/logo/`).
  Main version with tagline from 640 px width, small version below; the symbol is the favicon.
- Hero: a video that follows the scroll position (`assets/js/hero-scrub.js`). The page opens on the
  last frame (`assets/video/hero-poster.jpg`); scrolling down plays the clip backwards. On screens
  from 1280×720 up the hero stays pinned while it plays. With "reduce motion" the still image stays.
  Files: `hero-scrub.mp4` (1280×720) and `hero-scrub-sm.mp4` (854×480, phones), both encoded with a
  keyframe on every frame (`ffmpeg -g 1`) so scrubbing is smooth. The left half of the picture is
  sky and carries the text. To swap the video: re-encode the new clip the same way and replace the files.
  The first generated photo is kept in `source-images/` (not published).

## Animation

`assets/js/reveal.js` (plain JavaScript, no libraries) plus the "Reveal animations" block in
`assets/css/main.css`. Headings reveal by letters/words from a mask; cards, texts and buttons
slide in as whole blocks; photos open like a shutter; key figures count up. Every effect is
at most 1.2 s. Nothing is hidden without JavaScript or when the system asks to reduce motion.
Legal pages (`.prose`) are not animated.

## Smooth scrolling

[Lenis](https://github.com/darkroomengineering/lenis) (MIT licence, version 1.3.27, self-hosted in
`assets/js/lenis.min.js`, licence in `assets/js/lenis-LICENSE.txt`), started by `assets/js/smooth-scroll.js`.
Tune the glide with `lerp` there (lower = longer). It is off with "reduce motion"; touch scrolling stays native.

## Rules

- Only German and English on the site.
- No cookies, no trackers, no third-party requests (all fonts are self-hosted).
