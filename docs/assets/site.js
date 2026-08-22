(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    links.addEventListener("click", function (event) {
      if (event.target.tagName === "A") {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (node) {
    node.textContent = String(new Date().getFullYear());
  });

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealNodes = document.querySelectorAll(".reveal");
  if (reduced || !("IntersectionObserver" in window)) {
    revealNodes.forEach(function (node) { node.classList.add("visible"); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealNodes.forEach(function (node) { observer.observe(node); });
  }

  var grid = document.querySelector("[data-capability-grid]");
  if (!grid || !Array.isArray(window.MAW_CAPABILITIES)) {
    return;
  }

  var query = document.querySelector("[data-capability-search]");
  var count = document.querySelector("[data-capability-count]");
  var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var requestedFilter = new URLSearchParams(window.location.search).get("filter");
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
      '<div class="meta">',
      '<span class="badge">' + escapeHtml(item.origin === "adapted" ? "Pedro v2.1.0 lineage" : "MAW Codex original") + '</span>',
      '<span class="badge">' + escapeHtml(item.family) + '</span>',
      '<span class="badge">' + escapeHtml(item.mode) + '</span>',
      '</div>',
      '<h2><code>$' + escapeHtml(item.name) + '</code></h2>',
      '<p>' + escapeHtml(item.summary) + '</p>',
      '<p class="translation"><strong>Codex translation:</strong> ' + escapeHtml(item.translation) + '</p>',
      '</article>'
    ].join("");
  }

  function render() {
    var needle = query ? query.value.trim().toLowerCase() : "";
    var visible = window.MAW_CAPABILITIES.filter(function (item) {
      var filterMatch = active === "all" || item.origin === active || item.family === active;
      var haystack = [item.name, item.family, item.mode, item.summary, item.translation].join(" ").toLowerCase();
      return filterMatch && (!needle || haystack.indexOf(needle) !== -1);
    });

    grid.innerHTML = visible.map(card).join("");
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
    query.addEventListener("input", render);
  }

  render();
}());
