/* SDTT — before/after comparison slider.
   The range input covers the picture (drag anywhere, or use the arrow keys); its value moves
   the dividing line. Without JavaScript the picture stays at 50 / 50. */
(function () {
  "use strict";

  var sliders = document.querySelectorAll(".ba-slider");
  Array.prototype.forEach.call(sliders, function (slider) {
    var range = slider.querySelector(".ba-range");
    if (!range) return;

    function update() { slider.style.setProperty("--pos", range.value + "%"); }
    range.addEventListener("input", update);
    update();
  });
})();
