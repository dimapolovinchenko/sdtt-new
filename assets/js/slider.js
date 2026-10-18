/* SDTT — competence slider: one picture at a time, arrows, counter, swipe and keyboard.
   Without JavaScript all slides are shown one below the other. */
(function () {
  "use strict";

  var sliders = document.querySelectorAll(".cs");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  Array.prototype.forEach.call(sliders, function (root) {
    var viewport = root.querySelector(".cs-viewport");
    var track = root.querySelector(".cs-track");
    var slides = root.querySelectorAll(".cs-slide");
    var prev = root.querySelector(".cs-prev");
    var next = root.querySelector(".cs-next");
    var num = root.querySelector(".cs-num");
    var caption = root.querySelector(".cs-caption");
    if (!viewport || !track || slides.length < 2) return;

    var index = 0;
    var count = slides.length;
    if (reduce) track.style.transition = "none";

    function pad(n) { return n < 10 ? "0" + n : String(n); }

    function show(i) {
      index = (i + count) % count;                       // loops around at both ends
      track.style.transform = "translate3d(" + (-index * 100) + "%,0,0)";
      Array.prototype.forEach.call(slides, function (s, k) {
        if (k === index) s.removeAttribute("aria-hidden"); else s.setAttribute("aria-hidden", "true");
      });
      if (num) num.textContent = pad(index + 1);
      if (caption) caption.textContent = slides[index].getAttribute("data-caption") || "";
    }

    prev.addEventListener("click", function () { show(index - 1); });
    next.addEventListener("click", function () { show(index + 1); });

    viewport.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); show(index - 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); show(index + 1); }
    });

    // Swipe (touch and pen). Vertical scrolling stays untouched.
    var startX = null;
    viewport.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "mouse") return;
      startX = e.clientX;
    });
    viewport.addEventListener("pointerup", function (e) {
      if (startX === null) return;
      var dx = e.clientX - startX;
      startX = null;
      if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1));
    });
    viewport.addEventListener("pointercancel", function () { startX = null; });

    root.classList.add("is-ready");
    show(0);
  });
})();
