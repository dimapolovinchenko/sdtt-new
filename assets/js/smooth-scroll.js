/* SDTT — smooth scrolling (Lenis, MIT licence, self-hosted: assets/js/lenis.min.js).
   Mouse wheel and trackpad scrolling glide instead of jumping. Touch scrolling, the keyboard
   and "#" links keep working. Off when the system asks to reduce motion. */
(function () {
  "use strict";

  if (typeof Lenis === "undefined") return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var lenis = new Lenis({
    lerp: 0.09,          // lower = longer glide
    smoothWheel: true,
    wheelMultiplier: 1,
    anchors: { offset: -72 } // "#" links stop below the sticky header
  });

  function frame(time) {
    lenis.raf(time);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  window.sdttLenis = lenis;
})();
