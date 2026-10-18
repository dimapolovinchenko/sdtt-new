/* SDTT — hero video that follows the scroll position (no autoplay).
   The page opens on the LAST frame of the video (the poster image). Scrolling down
   plays the video backwards, so the camera glides down the facade with the scroll.
   The hero is exactly one window high. The clip plays while the hero scrolls out of view,
   and the text dissolves to the left on the way.
   With "reduce motion" or without JavaScript the poster stays as a still image. */
(function () {
  "use strict";

  var root = document.documentElement;
  var track = document.querySelector(".hero-track");
  var hero = track && track.querySelector(".hero");
  var video = track && track.querySelector(".hero-video");
  if (!video) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var pinMq = window.matchMedia("(min-width: 0px)"); // hero = window height at every screen size
  var smallMq = window.matchMedia("(max-width: 40em)");

  var copy = track.querySelector(".hero-copy");
  // The scroll distance equals the 6 s clip. The text starts to dissolve at 1 s and is gone at 4 s.
  var FADE_START_S = 1, FADE_END_S = 4;
  var duration = 0;
  var target = 0;   // 0 = last frame, 1 = first frame
  var current = 0;
  var raf = 0;
  var ready = false;
  var headerH = 0;

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

  function measure() {
    var header = document.querySelector(".site-header");
    headerH = header ? header.offsetHeight : 0;
    root.classList.toggle("hero-pin", pinMq.matches);
    if (!pinMq.matches) applyText(0);
    fitCopy();
  }

  /* The hero is exactly as tall as the window (below the menu bar). On a low window the text block is
     scaled down a little so that it fits; if it would have to become too small, the hero grows instead. */
  function fitCopy() {
    if (!copy) return;
    copy.style.zoom = "";
    hero.style.height = "";
    if (!pinMq.matches) return;
    var inner = copy.closest(".hero-inner");
    var pad = inner ? parseFloat(getComputedStyle(inner).paddingTop) + parseFloat(getComputedStyle(inner).paddingBottom) : 64;
    var avail = hero.clientHeight - pad;
    var need = copy.offsetHeight;
    if (!(need > avail) || need <= 0) return;
    var z = avail / need;
    if (z >= 0.72) {
      copy.style.zoom = z.toFixed(3);
    } else {
      copy.style.zoom = "0.72";
      hero.style.height = Math.ceil(need * 0.72 + pad) + "px";
    }
  }

  /* While the hero is pinned, the text dissolves (opacity 100 → 0) and drifts to the left. */
  function applyText(p) {
    if (!copy) return;
    if (!pinMq.matches || p <= 0.0001) {
      copy.style.opacity = "";
      copy.style.transform = "";
      copy.style.visibility = "";
      return;
    }
    var len = duration || 6;
    var from = FADE_START_S / len, to = FADE_END_S / len;
    var k = Math.max(0, Math.min((p - from) / (to - from), 1));
    var e = 1 - Math.pow(1 - k, 2);                 // drift eases out
    copy.style.opacity = String(1 - k);             // linear dissolve 100 → 0 %
    copy.style.transform = "translate3d(" + (-e * 9).toFixed(2) + "vw,0,0)";
    copy.style.visibility = k >= 1 ? "hidden" : "";  // no invisible links to click
  }

  function progress() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (pinMq.matches) {
      // The hero is exactly one window high; the clip plays while it scrolls out of view.
      return clamp(y / hero.offsetHeight);
    }
    return clamp(y / (hero.offsetTop + hero.offsetHeight));
  }

  function seek() {
    raf = 0;
    current += (target - current) * 0.18;
    if (Math.abs(target - current) < 0.0004) current = target;
    applyText(current);
    if (ready) {
      var t = Math.max(0, Math.min(duration - 0.05, (1 - current) * duration));
      if (Math.abs(video.currentTime - t) > 0.02) {
        if (video.fastSeek) video.fastSeek(t); else video.currentTime = t;
      }
    }
    if (current !== target) raf = requestAnimationFrame(seek);
  }

  function onScroll() {
    target = progress();
    if (!raf) raf = requestAnimationFrame(seek);
  }

  function init() {
    duration = video.duration || 6;
    ready = true;
    // Show the last frame first (it is identical to the poster, so nothing jumps).
    video.currentTime = Math.max(0, duration - 0.05);
    video.addEventListener("seeked", function once() {
      video.removeEventListener("seeked", once);
      video.classList.add("is-ready");
      onScroll();
    });
  }

  measure();
  video.src = (smallMq.matches ? video.getAttribute("data-src-small") : video.getAttribute("data-src"));
  video.preload = "auto";
  video.muted = true;
  if (video.readyState >= 1) init(); else video.addEventListener("loadedmetadata", init);

  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitCopy);
  window.addEventListener("load", fitCopy);
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () { measure(); onScroll(); });
  if (pinMq.addEventListener) pinMq.addEventListener("change", function () { measure(); onScroll(); });
})();
