/* SDTT — navigation (mobile menu, dropdowns). No dependencies. */
(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  if (!header) return;

  var navToggle = header.querySelector(".nav-toggle");
  var subToggles = header.querySelectorAll(".sub-toggle");

  function setNav(open) {
    header.classList.toggle("nav-open", open);
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function setSub(btn, open) {
    var menu = document.getElementById(btn.getAttribute("aria-controls"));
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    if (menu) menu.classList.toggle("is-open", open);
  }

  function closeAllSubs(except) {
    for (var i = 0; i < subToggles.length; i++) {
      if (subToggles[i] !== except) setSub(subToggles[i], false);
    }
  }

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      setNav(navToggle.getAttribute("aria-expanded") !== "true");
    });
  }

  for (var i = 0; i < subToggles.length; i++) {
    subToggles[i].addEventListener("click", function (e) {
      var btn = e.currentTarget;
      var open = btn.getAttribute("aria-expanded") !== "true";
      closeAllSubs(btn);
      setSub(btn, open);
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    for (var i = 0; i < subToggles.length; i++) {
      if (subToggles[i].getAttribute("aria-expanded") === "true") {
        setSub(subToggles[i], false);
        subToggles[i].focus();
        return;
      }
    }
    if (header.classList.contains("nav-open")) {
      setNav(false);
      navToggle.focus();
    }
  });

  document.addEventListener("click", function (e) {
    if (!header.contains(e.target)) closeAllSubs(null);
  });

  // Close an open dropdown when keyboard focus leaves its menu item.
  var items = header.querySelectorAll(".nav-item--has-sub");
  for (var j = 0; j < items.length; j++) {
    items[j].addEventListener("focusout", function (e) {
      var item = e.currentTarget;
      if (e.relatedTarget && !item.contains(e.relatedTarget)) {
        var btn = item.querySelector(".sub-toggle");
        if (btn) setSub(btn, false);
      }
    });
  }
})();
