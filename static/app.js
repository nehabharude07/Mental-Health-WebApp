/* Mental Health Screening System - frontend helpers */
(function () {
  "use strict";

  /* ---------- tabs ---------- */
  var tabs = document.querySelectorAll(".tab");
  Array.prototype.forEach.call(tabs, function (tab) {
    tab.addEventListener("click", function () {
      Array.prototype.forEach.call(tabs, function (t) { t.classList.remove("on"); });
      Array.prototype.forEach.call(document.querySelectorAll(".pane"), function (p) {
        p.classList.add("hidden");
      });
      tab.classList.add("on");
      var pane = document.getElementById(tab.dataset.target);
      if (pane) pane.classList.remove("hidden");
    });
  });

  /* ---------- questionnaire progress ---------- */
  var form = document.getElementById("screening-form");
  if (form) {
    var progress = document.getElementById("progress");
    var names = {};
    Array.prototype.forEach.call(
      form.querySelectorAll('input[type="radio"]'),
      function (i) { names[i.name] = true; }
    );
    var keys = Object.keys(names);

    function answered() {
      return keys.filter(function (n) {
        return form.querySelector('input[name="' + n + '"]:checked');
      }).length;
    }

    function update() {
      if (!progress) return;
      var n = answered();
      progress.textContent = n + " / " + keys.length;
      progress.classList.toggle("ready", n === keys.length);
    }

    form.addEventListener("change", update);
    form.addEventListener("reset", function () { setTimeout(update, 0); });

    // submit par pehla unanswered question highlight karo
    form.addEventListener("submit", function (e) {
      var missing = null;
      keys.some(function (n) {
        if (!form.querySelector('input[name="' + n + '"]:checked')) { missing = n; return true; }
        return false;
      });
      if (missing) {
        e.preventDefault();
        var row = form.querySelector('input[name="' + missing + '"]').closest("li.q");
        row.scrollIntoView({ behavior: "smooth", block: "center" });
        row.style.background = "rgba(248,113,113,.12)";
        setTimeout(function () { row.style.background = ""; }, 1800);
      }
    });
    update();
  }

  /* ---------- free-text word counter ---------- */
  var textarea = document.getElementById("description");
  var counter = document.getElementById("wordcount");
  if (textarea && counter) {
    var min = parseInt(counter.dataset.min || "15", 10);
    function countWords() {
      var n = textarea.value.trim() ? textarea.value.trim().split(/\s+/).length : 0;
      counter.textContent = n + " / " + min + " words";
      counter.classList.toggle("ready", n >= min);
    }
    textarea.addEventListener("input", countWords);
    countWords();
  }

  /* ---------- scroll to result ---------- */
  var result = document.querySelector(".result-card");
  if (result) result.scrollIntoView({ behavior: "smooth", block: "start" });
})();
