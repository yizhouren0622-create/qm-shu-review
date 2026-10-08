(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function markActiveNav() {
    var path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    if (!path || path === "") path = "index.html";
    var links = document.querySelectorAll(".site-links a[data-page]");
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute("data-page") === path) {
        links[i].className += (links[i].className ? " " : "") + "is-active";
      }
    }
  }

  function setupMenu() {
    var top = document.querySelector(".site-top");
    var btn = document.querySelector(".site-menu-btn");
    if (!top || !btn) return;
    btn.addEventListener("click", function () {
      var open = top.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    var links = top.querySelectorAll(".site-links a");
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener("click", function () {
        top.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
      });
    }
  }

  function renderMath() {
    if (!window.renderMathInElement) {
      setTimeout(renderMath, 50);
      return;
    }
    try {
      renderMathInElement(document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false }
        ],
        throwOnError: false,
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
      });
    } catch (e) {
      /* keep page readable even if KaTeX fails */
    }
  }

  ready(function () {
    markActiveNav();
    setupMenu();
    renderMath();
  });
})();
