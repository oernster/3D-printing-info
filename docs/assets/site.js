/* 3D-printing-info site behaviour: theme, navigation, search, image viewer,
   copy buttons, list filters, table of contents and the config viewer. */
(function () {
  "use strict";

  var doc = document.documentElement;
  var root = doc.getAttribute("data-root") || "";
  var themeKey = doc.getAttribute("data-theme-key");

  var SEARCH_LIMIT = 40;
  var SEARCH_MIN_CHARS = 2;
  var WEIGHT = { titleStart: 14, title: 10, summary: 4, section: 3, body: 1 };
  var COPY_RESET_MS = 1600;
  var REVOKE_MS = 1000;
  var TOC_ROOT_MARGIN = "0px 0px -70% 0px";

  function $(selector, scope) { return (scope || document).querySelector(selector); }
  function $all(selector, scope) { return Array.prototype.slice.call((scope || document).querySelectorAll(selector)); }
  var ENTITIES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  function escapeHtml(text) { return String(text).replace(/[&<>"']/g, function (c) { return ENTITIES[c]; }); }
  function plainClick(ev) { return ev.button === 0 && !ev.ctrlKey && !ev.metaKey && !ev.shiftKey && !ev.altKey; }

  /* Theme ------------------------------------------------------------- */

  function initTheme() {
    $all("[data-theme-toggle]").forEach(function (button) {
      button.addEventListener("click", function () {
        var next = doc.getAttribute("data-theme") === "dark" ? "light" : "dark";
        doc.setAttribute("data-theme", next);
        try { localStorage.setItem(themeKey, next); } catch (e) { /* storage unavailable */ }
      });
    });
    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (ev) {
        var stored = null;
        try { stored = localStorage.getItem(themeKey); } catch (e) { /* storage unavailable */ }
        if (!stored) doc.setAttribute("data-theme", ev.matches ? "dark" : "light");
      });
    }
  }

  /* Navigation -------------------------------------------------------- */

  function initNav() {
    var button = $("[data-nav-toggle]");
    var nav = $("#main-nav");
    if (!button || !nav) return;
    button.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
        button.focus();
      }
    });
  }

  /* Copy -------------------------------------------------------------- */

  function copyText(text, button) {
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(text).then(function () {
      var label = button.getAttribute("data-label") || button.textContent;
      button.setAttribute("data-label", label);
      button.textContent = "Copied";
      setTimeout(function () { button.textContent = label; }, COPY_RESET_MS);
    }, function () { /* clipboard refused */ });
  }

  function initCopy() {
    $all(".prose pre").forEach(function (pre) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "copy-btn";
      button.textContent = "Copy";
      button.addEventListener("click", function () {
        var code = pre.querySelector("code") || pre;
        copyText(code.textContent, button);
      });
      pre.appendChild(button);
    });
  }

  /* Search ------------------------------------------------------------ */

  function initSearch() {
    var modal = $("[data-search]");
    if (!modal) return;
    var input = $("[data-search-input]", modal);
    var list = $("[data-search-results]", modal);
    var hint = $("[data-search-hint]", modal);
    var index = null;
    var loading = null;
    var active = -1;
    var lastFocus = null;

    function load() {
      if (!loading) {
        loading = fetch(root + "search.json")
          .then(function (response) { return response.json(); })
          .then(function (data) { index = data; })
          .catch(function () { index = []; hint.textContent = "Search could not load. Try again when online."; });
      }
      return loading;
    }

    function score(entry, terms) {
      var title = entry.t.toLowerCase();
      var summary = (entry.d || "").toLowerCase();
      var section = (entry.s || "").toLowerCase();
      var body = (entry.x || "").toLowerCase();
      var total = 0;
      for (var i = 0; i < terms.length; i++) {
        var term = terms[i];
        var hit = false;
        if (title.indexOf(term) === 0) { total += WEIGHT.titleStart; hit = true; }
        else if (title.indexOf(term) > -1) { total += WEIGHT.title; hit = true; }
        if (summary.indexOf(term) > -1) { total += WEIGHT.summary; hit = true; }
        if (section.indexOf(term) > -1) { total += WEIGHT.section; hit = true; }
        if (body.indexOf(term) > -1) { total += WEIGHT.body; hit = true; }
        if (!hit) return 0;
      }
      return total;
    }

    function href(url) { return /^[a-z][a-z0-9+.-]*:/i.test(url) ? url : (root + url) || "./"; }

    function setActive(position) {
      var items = $all("li", list);
      if (!items.length) return;
      active = (position + items.length) % items.length;
      items.forEach(function (item, i) { item.classList.toggle("is-active", i === active); });
      items[active].scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", items[active].id);
    }

    function render() {
      var query = input.value.trim().toLowerCase();
      list.innerHTML = "";
      active = -1;
      input.removeAttribute("aria-activedescendant");
      if (!index || query.length < SEARCH_MIN_CHARS) {
        hint.hidden = false;
        hint.textContent = hint.getAttribute("data-default");
        return;
      }
      var terms = query.split(/\s+/).filter(Boolean);
      var hits = index
        .map(function (entry) { return [score(entry, terms), entry]; })
        .filter(function (pair) { return pair[0] > 0; })
        .sort(function (a, b) { return b[0] - a[0]; })
        .slice(0, SEARCH_LIMIT);
      if (!hits.length) {
        hint.hidden = false;
        hint.textContent = "Nothing matches that. Try a different word.";
        return;
      }
      hint.hidden = true;
      list.innerHTML = hits.map(function (pair, i) {
        var entry = pair[1];
        var desc = entry.d ? '<span class="sr-desc">' + escapeHtml(entry.d) + "</span>" : "";
        return '<li role="option" id="sr-' + i + '"><a href="' + escapeHtml(href(entry.u)) + '">' +
          '<span class="sr-title">' + escapeHtml(entry.t) + '</span>' +
          '<span class="sr-section">' + escapeHtml(entry.s) + "</span>" + desc + "</a></li>";
      }).join("");
    }

    function open() {
      lastFocus = document.activeElement;
      modal.hidden = false;
      document.body.classList.add("modal-open");
      input.focus();
      input.select();
      load().then(render);
    }

    function close() {
      modal.hidden = true;
      document.body.classList.remove("modal-open");
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    input.addEventListener("input", render);
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowDown") { ev.preventDefault(); setActive(active + 1); }
      else if (ev.key === "ArrowUp") { ev.preventDefault(); setActive(active - 1); }
      else if (ev.key === "Enter") {
        var items = $all("li a", list);
        var target = items[active >= 0 ? active : 0];
        if (target) { ev.preventDefault(); window.location.href = target.href; }
      }
    });
    modal.addEventListener("keydown", function (ev) { if (ev.key === "Escape") close(); });
    $all("[data-search-close]", modal).forEach(function (el) { el.addEventListener("click", close); });
    $all("[data-search-open]").forEach(function (el) { el.addEventListener("click", open); });
    document.addEventListener("keydown", function (ev) {
      if (!modal.hidden) return;
      var tag = document.activeElement ? document.activeElement.tagName : "";
      var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(tag);
      var shortcut = (ev.key === "k" || ev.key === "K") && (ev.ctrlKey || ev.metaKey);
      if (shortcut || (ev.key === "/" && !typing)) { ev.preventDefault(); open(); }
    });
  }

  /* Image viewer ------------------------------------------------------ */

  function initLightbox() {
    var box = $("[data-lightbox]");
    var links = $all("a.zoom");
    if (!box || !links.length) return;
    var img = $("[data-lb-img]", box);
    var caption = $("[data-lb-caption]", box);
    var full = $("[data-lb-full]", box);
    var closeButton = $("[data-lb-close]", box);
    var at = 0;
    var lastFocus = null;
    if (links.length < 2) box.classList.add("is-single");

    function show(position) {
      at = (position + links.length) % links.length;
      var link = links[at];
      var text = link.getAttribute("data-caption") || "";
      img.classList.add("is-loading");
      img.src = link.getAttribute("data-thumb") || link.href;
      img.alt = text;
      caption.textContent = text;
      full.href = link.href;
      var hires = new Image();
      hires.onload = function () {
        if (links[at] !== link) return;
        img.src = link.href;
        img.classList.remove("is-loading");
      };
      hires.src = link.href;
    }

    function open(position) {
      lastFocus = document.activeElement;
      box.hidden = false;
      document.body.classList.add("modal-open");
      show(position);
      closeButton.focus();
    }

    function close() {
      box.hidden = true;
      img.removeAttribute("src");
      document.body.classList.remove("modal-open");
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    links.forEach(function (link, i) {
      link.addEventListener("click", function (ev) {
        if (!plainClick(ev)) return;
        ev.preventDefault();
        open(i);
      });
    });
    closeButton.addEventListener("click", close);
    $("[data-lb-prev]", box).addEventListener("click", function () { show(at - 1); });
    $("[data-lb-next]", box).addEventListener("click", function () { show(at + 1); });
    box.addEventListener("click", function (ev) { if (ev.target === box) close(); });
    document.addEventListener("keydown", function (ev) {
      if (box.hidden) return;
      if (ev.key === "Escape") close();
      else if (ev.key === "ArrowLeft") show(at - 1);
      else if (ev.key === "ArrowRight") show(at + 1);
    });
  }

  /* List filters ------------------------------------------------------ */

  function initFilters() {
    $all("[data-filter]").forEach(function (input) {
      var key = input.getAttribute("data-filter");
      var scope = $('[data-filter-scope="' + key + '"]');
      var count = $('[data-filter-count="' + key + '"]');
      if (!scope) return;
      var items = $all("[data-filter-item]", scope);
      var groups = $all("[data-filter-group]", scope).reverse();
      var texts = items.map(function (el) { return el.textContent.toLowerCase(); });

      function apply() {
        var terms = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
        var shown = 0;
        items.forEach(function (el, i) {
          var match = terms.every(function (term) { return texts[i].indexOf(term) > -1; });
          el.hidden = !match;
          if (match) shown += 1;
        });
        groups.forEach(function (group) {
          var visible = $all("[data-filter-item]", group).some(function (el) { return !el.hidden; });
          group.hidden = !visible;
          if (group.tagName === "DETAILS") {
            group.open = terms.length ? visible : group.hasAttribute("data-default-open");
          }
        });
        if (count) count.textContent = terms.length ? shown + " of " + items.length : items.length + " in total";
      }

      input.addEventListener("input", apply);
      apply();
    });
  }

  /* Table of contents ------------------------------------------------- */

  function initToc() {
    var links = $all(".toc a");
    if (!links.length || !("IntersectionObserver" in window)) return;
    var byId = {};
    links.forEach(function (link) { byId[decodeURIComponent(link.hash.slice(1))] = link; });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) { link.classList.remove("is-active"); });
        var link = byId[entry.target.id];
        if (link) link.classList.add("is-active");
      });
    }, { rootMargin: TOC_ROOT_MARGIN });
    Object.keys(byId).forEach(function (id) {
      var heading = document.getElementById(id);
      if (heading) observer.observe(heading);
    });
  }

  /* Config viewer ----------------------------------------------------- */

  var CONFIG_TOKENS = /(\{%.*?%\}|\{\{.*?\}\}|\{[^{}]*\})|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b[GM]\d+(?:\.\d+)?\b)|(\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b)|(-?\b\d+(?:\.\d+)?\b)/g;
  var CONFIG_CLASSES = ["jinja", "string", "gcode", "macro", "number"];
  var PYTHON_TOKENS = /(#.*$)|((?:[rbfRBF]{1,2})?(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'))|(\b(?:import|from|as|def|class|return|if|elif|else|for|while|try|except|finally|with|not|and|or|in|is|None|True|False|raise|pass|lambda|yield)\b)|(\b\d+(?:\.\d+)?\b)/g;
  var PYTHON_CLASSES = ["comment", "string", "keyword", "number"];

  function span(kind, text) { return '<span class="t-' + kind + '">' + escapeHtml(text) + "</span>"; }

  function tokenize(text, pattern, classes) {
    var out = "";
    var last = 0;
    var match;
    pattern.lastIndex = 0;
    while ((match = pattern.exec(text)) !== null) {
      if (match[0] === "") { pattern.lastIndex += 1; continue; }
      out += escapeHtml(text.slice(last, match.index));
      for (var group = 1; group < match.length; group++) {
        if (match[group] !== undefined) { out += span(classes[group - 1], match[0]); break; }
      }
      last = match.index + match[0].length;
    }
    return out + escapeHtml(text.slice(last));
  }

  function highlightConfig(line) {
    if (/^\s*[#;]/.test(line)) return span("comment", line);
    var body = line;
    var comment = "";
    var split = line.match(/^(.*?\S)(\s+[#;].*)$/);
    if (split) { body = split[1]; comment = split[2]; }
    var tail = comment ? span("comment", comment) : "";
    var section = body.match(/^(\s*)(\[[^\]]+\])(\s*)$/);
    if (section) return escapeHtml(section[1]) + span("section", section[2]) + escapeHtml(section[3]) + tail;
    var pair = body.match(/^(\s*)([A-Za-z0-9_.\-]+)(\s*[:=])(.*)$/);
    if (pair) return escapeHtml(pair[1]) + span("key", pair[2]) + escapeHtml(pair[3]) + tokenize(pair[4], CONFIG_TOKENS, CONFIG_CLASSES) + tail;
    return tokenize(body, CONFIG_TOKENS, CONFIG_CLASSES) + tail;
  }

  function highlight(line, isPython) {
    return isPython ? tokenize(line, PYTHON_TOKENS, PYTHON_CLASSES) : highlightConfig(line);
  }

  function initViewer() {
    var viewer = $("[data-viewer]");
    var indexEl = $("#config-index");
    if (!viewer || !indexEl) return;
    var files = JSON.parse(indexEl.textContent);
    var byPath = {};
    files.forEach(function (file) { byPath[file.path] = file; });
    var rawBase = viewer.getAttribute("data-raw-base");
    var blobBase = viewer.getAttribute("data-blob-base");
    var title = $("[data-viewer-title]");
    var pathEl = $("[data-viewer-path]");
    var groupEl = $("[data-viewer-group]");
    var context = $("[data-viewer-context]");
    var code = $("[data-viewer-code]");
    var github = $("[data-viewer-github]");
    var copyButton = $("[data-viewer-copy]");
    var downloadButton = $("[data-viewer-download]");
    var wrapButton = $("[data-viewer-wrap]");
    var titleSuffix = document.title;
    var current = null;
    var text = "";

    function encodePath(path) { return path.split("/").map(encodeURIComponent).join("/"); }

    function select(path, push) {
      var file = byPath[path];
      if (!file) return;
      current = file;
      text = "";
      title.textContent = file.label;
      pathEl.textContent = file.path;
      groupEl.textContent = file.group;
      context.innerHTML = 'Part of <a href="' + escapeHtml(root + file.page) + '">' + escapeHtml(file.group) + "</a>";
      github.href = blobBase + encodePath(file.path);
      document.title = file.label + " | " + titleSuffix;
      $all("[data-viewer-link]").forEach(function (link) {
        link.classList.toggle("is-active", link.getAttribute("data-path") === path);
      });
      code.innerHTML = '<p class="viewer-empty">Loading ' + escapeHtml(file.path) + "</p>";
      if (push) history.pushState({ path: path }, "", "?f=" + encodeURIComponent(path));
      fetch(rawBase + encodePath(file.path))
        .then(function (response) {
          if (!response.ok) throw new Error("HTTP " + response.status);
          return response.text();
        })
        .then(function (body) {
          if (current !== file) return;
          text = body;
          var isPython = /\.py$/.test(file.path);
          var lines = body.replace(/\r\n/g, "\n").replace(/\n$/, "").split("\n");
          code.innerHTML = '<pre class="code-view"><code>' + lines.map(function (line) {
            return '<span class="line">' + highlight(line, isPython) + "</span>";
          }).join("") + "</code></pre>";
        })
        .catch(function () {
          if (current !== file) return;
          code.innerHTML = '<p class="viewer-empty">This file could not be loaded. <a href="' +
            escapeHtml(github.href) + '">Open it on GitHub</a>.</p>';
        });
    }

    copyButton.addEventListener("click", function () { if (text) copyText(text, copyButton); });
    downloadButton.addEventListener("click", function () {
      if (!text || !current) return;
      var url = URL.createObjectURL(new Blob([text], { type: "text/plain" }));
      var anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = current.path.split("/").pop();
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, REVOKE_MS);
    });
    wrapButton.addEventListener("click", function () {
      var on = code.classList.toggle("is-wrapped");
      wrapButton.setAttribute("aria-pressed", String(on));
    });
    $all("[data-viewer-link]").forEach(function (link) {
      link.addEventListener("click", function (ev) {
        if (!plainClick(ev)) return;
        ev.preventDefault();
        select(link.getAttribute("data-path"), true);
        if (window.matchMedia("(max-width: 900px)").matches) code.scrollIntoView({ block: "start" });
      });
    });
    window.addEventListener("popstate", function () {
      var path = new URLSearchParams(window.location.search).get("f");
      if (path) select(path, false);
    });
    var initial = new URLSearchParams(window.location.search).get("f");
    if (initial) select(initial, false);
  }

  function start() {
    initTheme();
    initNav();
    initCopy();
    initSearch();
    initLightbox();
    initFilters();
    initToc();
    initViewer();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
