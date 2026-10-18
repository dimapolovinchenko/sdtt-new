/* SDTT — opens project photos full screen. Click or Enter on a picture, Esc / click outside / × to close.
   Without JavaScript the link simply opens the picture itself. */
(function () {
  "use strict";
  var links = document.querySelectorAll("a[data-lightbox]");
  if (!links.length || typeof HTMLDialogElement === "undefined") return;

  var dlg = document.createElement("dialog");
  dlg.className = "lb";
  dlg.setAttribute("aria-label", document.documentElement.lang === "en" ? "Enlarged picture" : "Vergrößertes Bild");
  dlg.innerHTML = '<div class="lb-inner"><img alt=""></div><button type="button" class="lb-close" aria-label="' +
    (document.documentElement.lang === "en" ? "Close" : "Schließen") + '">&times;</button>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector("img");

  Array.prototype.forEach.call(links, function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var thumb = a.querySelector("img");
      img.src = a.getAttribute("href");
      img.alt = thumb ? thumb.alt : "";
      dlg.showModal();
    });
  });
  dlg.addEventListener("click", function (e) { if (e.target !== img) dlg.close(); });
  dlg.addEventListener("close", function () { img.removeAttribute("src"); });
})();
