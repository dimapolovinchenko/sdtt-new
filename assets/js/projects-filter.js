/* SDTT — project filter (type, city, size, completion year).
   Cards are rendered in HTML; this script only shows/hides them.
   Without JS all projects stay visible. */
(function () {
  "use strict";

  var form = document.getElementById("project-filter");
  var list = document.getElementById("project-list");
  if (!form || !list) return;

  var keys = ["type", "city", "size", "year"];
  var cards = list.querySelectorAll(".project-card");
  var status = document.getElementById("filter-status");
  var empty = document.getElementById("filter-empty");

  form.hidden = false;
  if (status) status.hidden = false;

  function current() {
    var v = {};
    for (var i = 0; i < keys.length; i++) {
      var el = form.elements["f-" + keys[i]];
      v[keys[i]] = el ? el.value : "";
    }
    return v;
  }

  function apply(updateUrl) {
    var v = current();
    var shown = 0;
    for (var i = 0; i < cards.length; i++) {
      var c = cards[i];
      var match = true;
      for (var k = 0; k < keys.length; k++) {
        if (v[keys[k]] && c.getAttribute("data-" + keys[k]) !== v[keys[k]]) { match = false; break; }
      }
      c.hidden = !match;
      if (match) shown++;
    }
    if (status) {
      var tpl = shown === 1 ? status.getAttribute("data-one") : status.getAttribute("data-many");
      status.textContent = tpl.replace("{n}", shown).replace("{total}", cards.length);
    }
    if (empty) empty.hidden = shown !== 0;

    if (updateUrl && window.history && history.replaceState) {
      var params = [];
      for (var j = 0; j < keys.length; j++) {
        if (v[keys[j]]) params.push(keys[j] + "=" + encodeURIComponent(v[keys[j]]));
      }
      history.replaceState(null, "", location.pathname + (params.length ? "?" + params.join("&") : "") + location.hash);
    }
  }

  // Preselect from URL, e.g. ?type=education (used by the header dropdown).
  var query = location.search.replace(/^\?/, "").split("&");
  for (var q = 0; q < query.length; q++) {
    var pair = query[q].split("=");
    var field = form.elements["f-" + pair[0]];
    if (field && pair[1]) {
      var val = decodeURIComponent(pair[1]);
      for (var o = 0; o < field.options.length; o++) {
        if (field.options[o].value === val) { field.value = val; break; }
      }
    }
  }

  form.addEventListener("change", function () { apply(true); });
  form.addEventListener("submit", function (e) { e.preventDefault(); apply(true); });
  form.addEventListener("reset", function () { setTimeout(function () { apply(true); }, 0); });

  apply(false);
})();
