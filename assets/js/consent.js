/* SDTT — consent manager (cookies and similar storage), built for German law (§ 25 TDDDG, Art. 6/7 DSGVO).
   - No third-party service: everything runs from this file, nothing is loaded from outside.
   - "Reject" and "Accept" look the same and are equally easy to reach (no nudging).
   - Only technically necessary storage is used without consent. Optional categories stay OFF until chosen.
   - The choice is saved in this browser (localStorage "sdtt-consent") for 6 months and can be changed at any
     time through the footer link "Cookie-Einstellungen" (or any element with data-consent-open).
   - Scripts of optional services must be added as  <script type="text/plain" data-consent="statistics" src="…">
     (or "media"). They run only after the matching category was accepted.
   Currently this website uses NO optional services: the optional categories are prepared, not active. */
(function () {
  "use strict";

  var KEY = "sdtt-consent", VERSION = 1, MAX_AGE = 1000 * 60 * 60 * 24 * 182;
  var en = document.documentElement.lang === "en";
  var T = en ? {
    title: "Privacy settings",
    text: "We only use technically necessary storage on this website. Optional categories are switched off unless you allow them. You can change your choice at any time.",
    more: "Privacy policy", reject: "Reject all", settings: "Settings", accept: "Accept all", save: "Save selection", close: "Close",
    necTitle: "Necessary", necText: "Stores your privacy choice in this browser. Required for the website to work; cannot be switched off.", always: "Always on",
    statTitle: "Statistics", statText: "Anonymous usage statistics. Currently not used on this website.",
    mediaTitle: "External content", mediaText: "Content from other providers, such as maps or videos. Currently not used on this website."
  } : {
    title: "Datenschutz-Einstellungen",
    text: "Wir verwenden auf dieser Website nur technisch notwendige Speicherungen. Optionale Kategorien bleiben ausgeschaltet, solange Sie sie nicht erlauben. Sie können Ihre Auswahl jederzeit ändern.",
    more: "Datenschutzerklärung", reject: "Alle ablehnen", settings: "Einstellungen", accept: "Alle akzeptieren", save: "Auswahl speichern", close: "Schließen",
    necTitle: "Notwendig", necText: "Speichert Ihre Datenschutz-Auswahl in diesem Browser. Für den Betrieb der Website erforderlich; kann nicht abgeschaltet werden.", always: "Immer aktiv",
    statTitle: "Statistik", statText: "Anonyme Nutzungsstatistik. Wird auf dieser Website derzeit nicht eingesetzt.",
    mediaTitle: "Externe Inhalte", mediaText: "Inhalte anderer Anbieter, z. B. Karten oder Videos. Werden auf dieser Website derzeit nicht eingesetzt."
  };
  var privacyHref = (function () {
    var a = document.querySelector('.site-footer a[href*="datenschutz"], .site-footer a[href*="privacy"]');
    return a ? a.getAttribute("href") : "#";
  })();

  function read() {
    try {
      var d = JSON.parse(localStorage.getItem(KEY) || "null");
      if (!d || d.v !== VERSION || !d.t || Date.now() - d.t > MAX_AGE) return null;
      return d;
    } catch (e) { return null; }
  }
  var state = read();

  function allowed(cat) { return !!(state && state.c && state.c[cat]); }
  function activate() {
    Array.prototype.forEach.call(document.querySelectorAll('script[type="text/plain"][data-consent]'), function (s) {
      if (s.__done || !allowed(s.getAttribute("data-consent"))) return;
      s.__done = true;
      var n = document.createElement("script");
      Array.prototype.forEach.call(s.attributes, function (a) { if (a.name !== "type") n.setAttribute(a.name, a.value); });
      n.text = s.text;
      s.parentNode.replaceChild(n, s);
    });
  }
  function write(c) {
    var d = { v: VERSION, t: Date.now(), c: c };
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { /* private mode: the choice lasts for this page only */ }
    state = d;
    activate();
    document.dispatchEvent(new CustomEvent("sdtt:consent", { detail: c }));
  }
  window.SDTTConsent = { has: allowed, open: function () { openSettings(); } };

  function el(tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; return e; }

  /* ---- banner ---- */
  var banner;
  function showBanner() {
    if (banner) return;
    banner = el("section", "cm");
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", T.title);
    banner.innerHTML =
      '<div class="cm-text"><h2 class="cm-title">' + T.title + '</h2><p>' + T.text +
      ' <a href="' + privacyHref + '">' + T.more + '</a></p></div>' +
      '<div class="cm-actions">' +
      '<button type="button" class="btn btn--outline cm-btn" data-a="reject">' + T.reject + '</button>' +
      '<button type="button" class="btn btn--outline cm-btn" data-a="settings">' + T.settings + '</button>' +
      '<button type="button" class="btn btn--outline cm-btn" data-a="accept">' + T.accept + '</button></div>';
    document.body.appendChild(banner);
    banner.addEventListener("click", function (e) {
      var a = e.target.closest("button[data-a]"); if (!a) return;
      var k = a.getAttribute("data-a");
      if (k === "reject") { write({ statistics: false, media: false }); hideBanner(); }
      if (k === "accept") { write({ statistics: true, media: true }); hideBanner(); }
      if (k === "settings") openSettings();
    });
  }
  function hideBanner() { if (banner) { banner.parentNode.removeChild(banner); banner = null; } }

  /* ---- settings dialog ---- */
  var dlg;
  function row(id, title, text, on, locked) {
    return '<div class="cm-row"><div><h3 class="cm-h3">' + title + '</h3><p>' + text + '</p></div>' +
      (locked ? '<span class="cm-always">' + T.always + '</span>' :
        '<label class="cm-switch"><input type="checkbox" id="cm-' + id + '"' + (on ? " checked" : "") + '><span class="cm-slider"></span><span class="visually-hidden">' + title + '</span></label>') + '</div>';
  }
  function openSettings() {
    if (typeof HTMLDialogElement === "undefined") return;
    if (dlg && dlg.parentNode) dlg.parentNode.removeChild(dlg);
    var s = (state && state.c) || {};
    dlg = el("dialog", "cm-dialog");
    dlg.setAttribute("data-lenis-prevent", "");
    dlg.setAttribute("aria-label", T.title);
    dlg.innerHTML = '<div class="cm-panel"><button type="button" class="cm-x" aria-label="' + T.close + '">&times;</button>' +
      '<h2 class="cm-title">' + T.title + '</h2><p>' + T.text + ' <a href="' + privacyHref + '">' + T.more + '</a></p>' +
      row("nec", T.necTitle, T.necText, true, true) +
      row("statistics", T.statTitle, T.statText, !!s.statistics) +
      row("media", T.mediaTitle, T.mediaText, !!s.media) +
      '<div class="cm-actions cm-actions--end">' +
      '<button type="button" class="btn btn--outline cm-btn" data-a="reject">' + T.reject + '</button>' +
      '<button type="button" class="btn btn--outline cm-btn" data-a="save">' + T.save + '</button>' +
      '<button type="button" class="btn btn--outline cm-btn" data-a="accept">' + T.accept + '</button></div></div>';
    document.body.appendChild(dlg);
    var me = dlg;
    me.addEventListener("click", function (e) {
      if (e.target === me || e.target.closest(".cm-x")) { me.close(); return; }
      var a = e.target.closest("button[data-a]"); if (!a) return;
      var k = a.getAttribute("data-a"), c;
      if (k === "reject") c = { statistics: false, media: false };
      else if (k === "accept") c = { statistics: true, media: true };
      else c = { statistics: me.querySelector("#cm-statistics").checked, media: me.querySelector("#cm-media").checked };
      write(c); hideBanner(); me.close();
    });
    me.addEventListener("close", function () { if (me.parentNode) me.parentNode.removeChild(me); if (dlg === me) dlg = null; });
    me.showModal();
  }

  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-consent-open]")) { e.preventDefault(); openSettings(); }
  });

  if (state) activate(); else showBanner();
})();
