(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");

  if (toggle && links) {
    toggle.closest(".nav").classList.add("has-menu");
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    toggle.closest(".nav").addEventListener("keydown", function (event) {
      if (event.key === "Escape" && links.classList.contains("open")) {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
    links.addEventListener("click", function (event) {
      if (event.target.tagName === "A") {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  var grid = document.querySelector("[data-capability-grid]");
  if (!grid || !Array.isArray(window.MAW_CAPABILITIES)) {
    return;
  }

  var query = document.querySelector("[data-capability-search]");
  var count = document.querySelector("[data-capability-count]");
  var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var params = new URLSearchParams(window.location.search);
  var requestedFilter = params.get("filter");
  var availableFilters = buttons.map(function (button) {
    return button.getAttribute("data-filter");
  });
  var active = availableFilters.indexOf(requestedFilter) !== -1 ? requestedFilter : "all";
  buttons.forEach(function (button) {
    button.setAttribute("aria-pressed", String(button.getAttribute("data-filter") === active));
  });

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function card(item) {
    return [
      '<article class="capability" data-origin="' + escapeHtml(item.origin) + '">',
      '<h3><code>$mawcodex:' + escapeHtml(item.name) + '</code></h3>',
      '<p class="meta">' + escapeHtml([item.family, item.mode].join(" / ")) + '</p>',
      '<p>' + escapeHtml(item.summary) + '</p>',
      '<p class="translation">' + escapeHtml(item.translation) + '</p>',
      '</article>'
    ].join("");
  }

  function render() {
    var needle = query ? query.value.trim().toLowerCase() : "";
    var visible = window.MAW_CAPABILITIES.filter(function (item) {
      var filterMatch = active === "all" || item.origin === active || item.family === active;
      var haystack = ["$mawcodex:" + item.name, item.family, item.mode, item.summary, item.translation].join(" ").toLowerCase();
      return filterMatch && (!needle || haystack.indexOf(needle) !== -1);
    });

    grid.innerHTML = visible.length ? visible.map(card).join("") : "<p>No skills match this search.</p>";
    if (count) {
      count.textContent = visible.length + " of " + window.MAW_CAPABILITIES.length + " skills";
    }
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      active = button.getAttribute("data-filter");
      buttons.forEach(function (candidate) {
        candidate.setAttribute("aria-pressed", String(candidate === button));
      });
      render();
    });
  });

  if (query) {
    query.value = params.get("q") || "";
    query.addEventListener("input", render);
  }

  render();
}());
