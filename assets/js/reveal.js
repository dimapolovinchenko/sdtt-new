/* SDTT — reveal animations (no libraries).
   - Headings: letters (hero H1) or words slide up from behind a mask.
   - Cards, paragraphs, buttons, contacts: the whole block slides up and fades in.
   - Photos: opened like a shutter. Key figures: count up.
   Single effects take 1 to 2 s; the home hero follows the order and timing of the reference
   site (about 3.8 s in total). Without JavaScript, or with "reduce motion"
   set in the system, nothing is hidden and nothing animates. */
(function () {
  "use strict";

  var root = document.documentElement;
  if (!root.classList.contains("js")) return;
  window.__rv = true; // tells the fail-safe in <head> that this script is running

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;

  function all(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }
  function inLegal(el) { return !!el.closest(".prose"); }
  function seen(el) { if (!el || el.__rv) return true; el.__rv = true; return false; }

  var observed = [];

  // Hero picture starts fully transparent (see CSS); it fades in from start().
  (function () {
    var m = document.querySelector(".hero-media");
    if (m) { m.classList.add("rv-fade"); m.style.setProperty("--dur", "2s"); }
  })();

  /* Whole-block reveal: fade + slide up. `hero` blocks run on load with fixed delays. */
  function block(el, delay, opts) {
    if (seen(el)) return;
    opts = opts || {};
    el.classList.add("rv", "rv-b");
    if (opts.hero) el.classList.add("rv-h");
    if (delay) el.style.setProperty("--d", delay + "s");
    if (opts.dur) el.style.setProperty("--dur", opts.dur + "s");
    if (opts.x) el.style.setProperty("--rx", opts.x);   // start offset sideways (e.g. "-3rem" = from the left)
    if (opts.y) el.style.setProperty("--ry", opts.y);   // start offset downwards
    observed.push(el);
  }

  /* Words fade in while rising and tilting forward (like the subtitle on the reference site). */
  function fadeWords(el, base, spread, wdur, hero) {
    if (seen(el)) return;
    if (el.children.length) { block(el, base, { hero: hero }); return; }
    var text = el.textContent.replace(/\s+/g, " ").trim();
    if (!text) return;
    el.setAttribute("aria-label", text);
    el.classList.add("rv", "rv-t", "rv-fw");
    if (hero) el.classList.add("rv-h");
    if (wdur) el.style.setProperty("--wdur", wdur + "s");
    var n = text.split(" ").length;
    var step = n > 1 ? Math.min(0.04, spread / (n - 1)) : 0;
    var frag = document.createDocumentFragment();
    text.split(" ").forEach(function (w, i) {
      if (i) frag.appendChild(document.createTextNode(" "));
      var s = document.createElement("span");
      s.className = "rv-f";
      s.setAttribute("aria-hidden", "true");
      s.style.setProperty("--d", (base + i * step).toFixed(3) + "s");
      s.textContent = w;
      frag.appendChild(s);
    });
    el.textContent = "";
    el.appendChild(frag);
    observed.push(el);
  }

  /* Photo reveal: shutter opens from the bottom, picture settles from a slight zoom. */
  function photo(el) {
    if (seen(el)) return;
    el.classList.add("rv", "rv-p");
    observed.push(el);
  }

  function mask(parent, text, d) {
    var m = document.createElement("span");
    m.className = "rv-m";
    m.setAttribute("aria-hidden", "true");
    var i = document.createElement("span");
    i.className = "rv-i";
    i.style.setProperty("--d", d.toFixed(3) + "s");
    i.textContent = text;
    m.appendChild(i);
    parent.appendChild(m);
  }

  /* Heading reveal by letters or words. Keeps the accessible name via aria-label. */
  function split(el, mode, base, spread, hero, idur) {
    if (seen(el)) return;
    if (el.children.length) { block(el, base, { hero: hero }); return; } // keep inner markup intact
    var text = el.textContent.replace(/\s+/g, " ").trim();
    if (!text) return;
    el.setAttribute("aria-label", text);
    el.classList.add("rv", "rv-t");
    if (hero) el.classList.add("rv-h");
    if (idur) el.style.setProperty("--idur", idur + "s");

    var words = text.split(" ");
    var n = mode === "chars" ? text.replace(/ /g, "").length : words.length;
    var step = n > 1 ? Math.min(mode === "chars" ? 0.05 : 0.09, spread / (n - 1)) : 0;
    var k = 0;
    var frag = document.createDocumentFragment();

    words.forEach(function (w, wi) {
      if (wi) frag.appendChild(document.createTextNode(" "));
      if (mode === "chars") {
        var holder = document.createElement("span");
        holder.className = "rv-w";
        holder.setAttribute("aria-hidden", "true");
        Array.from(w).forEach(function (ch) { mask(holder, ch, base + k * step); k++; });
        frag.appendChild(holder);
      } else {
        mask(frag, w, base + k * step);
        k++;
      }
    });
    el.textContent = "";
    el.appendChild(frag);
    observed.push(el);
  }

  /* Key figures: "120+" counts from 0. The real value stays readable for screen readers. */
  function prepCount(el) {
    if (seen(el)) return;
    var text = el.textContent.trim();
    var m = /^(\d+)(.*)$/.exec(text);
    if (!m) return;
    el.setAttribute("data-count", m[1]);
    el.setAttribute("data-suffix", m[2]);
    el.innerHTML = '<span aria-hidden="true">0' + m[2] + '</span><span class="visually-hidden">' + text + "</span>";
    observed.push(el);
  }

  function runCount(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var suffix = el.getAttribute("data-suffix") || "";
    var out = el.firstChild;
    var t0 = null;
    var dur = 1800;
    function tick(t) {
      if (t0 === null) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var e = 1 - Math.pow(1 - p, 3);
      out.textContent = Math.round(target * e) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- What gets animated ---------- */

  var hero = document.querySelector(".hero");

  // Menu bar content drops in from the top.
  // (Not observed: it starts above its final place, so it is shown directly in start().)
  var headerInner = document.querySelector(".site-header .header-inner");
  if (headerInner) {
    headerInner.classList.add("rv", "rv-hd", "rv-h");
    headerInner.style.setProperty("--d", (hero ? 0.5 : 0.2) + "s");
    headerInner.style.setProperty("--dur", (hero ? 1.5 : 1) + "s");
  }

  // Home hero on load. Timeline (seconds after the page is ready):
  //   0.0 – 2.0   background picture / video fades in (opacity 0 → 100 %)
  //   0.5 – 2.0   menu fades in while dropping from the top
  //   1.0 – 2.5   text block: label from the left, headline letters rise from a mask,
  //               intro words fade in, list, norms line and buttons rise from below
  var media = hero && hero.querySelector(".hero-media");
  if (hero) {
    block(hero.querySelector(".eyebrow"), 1.0, { hero: true, dur: 0.75, x: "-3rem", y: "0rem" });
    split(hero.querySelector("h1"), "chars", 1.0, 0.4, true, 1.05);          // last letter ends at 2.45
    fadeWords(hero.querySelector(".lead"), 1.5, 0.3, 0.7, true);             // last word ends at 2.5
    block(hero.querySelector(".hero-sub"), 1.85, { hero: true, dur: 0.65, y: "2.5rem" });
    block(hero.querySelector(".btn-row"), 1.9, { hero: true, dur: 0.6, y: "1.5rem" });
  }

  // Page header on sub pages.
  var ph = document.querySelector(".page-header");
  if (ph) {
    block(ph.querySelector(".breadcrumbs"), 0, { hero: true, dur: 1.0 });
    block(ph.querySelector(".eyebrow"), 0, { hero: true, dur: 1.0 });
    split(ph.querySelector("h1"), "words", 0.1, 0.5, true);
    block(ph.querySelector(".lead"), 0.5, { hero: true, dur: 1.2 });
    block(ph.querySelector(".notice"), 0.6, { hero: true, dur: 1.1 });
  }

  // Section headings: words rise out of a mask.
  all("main h2").forEach(function (h) { if (!inLegal(h)) split(h, "words", 0, 0.5, false); });

  // Short text, cards, contacts, tables, buttons: the whole block moves.
  [
    ".section-head .eyebrow", ".section-head p",
    ".cs-intro", ".cs-main", ".card", ".req", ".contact-card", ".project-card", ".featured-project", ".cat-tile",
    ".figure", ".hl-item", ".steps li", ".std-block", ".emergency", ".doc-table", ".doc-note", ".faq",
    ".filter", ".filter-status", ".empty-state", ".btn-row", ".cta-band > div",
    ".grid--split > div > *", ".footer-grid > div"
  ].forEach(function (sel) {
    all(sel).forEach(function (el) {
      if (!inLegal(el) && !el.closest(".hero") && !el.closest(".page-header")) block(el, 0);
    });
  });

  // Photos.
  all(".ba-pair figure, .project-card-media, .fp-media").forEach(photo);

  // Numbers.
  all(".figure-value").forEach(prepCount);

  /* ---------- Trigger ---------- */

  function reveal(el) {
    el.classList.add("is-in");
    if (el.hasAttribute("data-count")) runCount(el);
  }

  // A photo that is clipped away at the start has nothing to intersect with, so the observer
  // watches its parent instead and reveals the photo when the parent comes into view.
  var hostOf = new Map();
  function observeTarget(el) { return el.classList.contains("rv-p") && el.parentElement ? el.parentElement : el; }

  var io = new IntersectionObserver(function (entries) {
    function targets(e) { return [e.target].concat(hostOf.get(e.target) || []); }
    // Elements the visitor already scrolled past (fast scroll, anchor jump, reload) are shown at once.
    entries.forEach(function (e) {
      if (!e.isIntersecting && e.boundingClientRect.bottom < 0) { targets(e).forEach(reveal); io.unobserve(e.target); }
    });
    var vis = entries.filter(function (e) { return e.isIntersecting; }).sort(function (a, b) {
      var ra = a.boundingClientRect, rb = b.boundingClientRect;
      return (Math.round(ra.top / 40) - Math.round(rb.top / 40)) || (ra.left - rb.left);
    });
    // Elements that appear together are staggered a little (max 0.5 s).
    vis.forEach(function (e, i) {
      targets(e).forEach(function (el) {
        if (!el.classList.contains("rv-h")) el.style.setProperty("--sd", Math.min(i, 4) * 0.12 + "s");
        reveal(el);
      });
      io.unobserve(e.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });

  function start() {
    if (headerInner) headerInner.classList.add("is-in");
    observed.forEach(function (el) {
      var t = observeTarget(el);
      if (t !== el) { if (!hostOf.has(t)) hostOf.set(t, []); hostOf.get(t).push(el); }
      io.observe(t);
    });

    // Hero picture: fades in once the still image is loaded.
    if (media) {
      var poster = media.querySelector("img");
      var shown = false;
      var show = function () {
        if (shown) return;
        shown = true;
        media.classList.add("is-in");
      };
      if (poster && poster.complete && poster.naturalWidth) show();
      else if (poster) { poster.addEventListener("load", show); poster.addEventListener("error", show); setTimeout(show, 1500); }
      else show();
    }
  }

  // Wait for the fonts (max 0.6 s) so letters do not jump while they animate.
  if (document.fonts && document.fonts.ready) {
    var fired = false;
    var go = function () { if (!fired) { fired = true; start(); } };
    document.fonts.ready.then(go);
    setTimeout(go, 600);
  } else {
    start();
  }
})();
