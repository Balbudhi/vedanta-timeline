/* Bhagavad-Gītā, the whole text in one article: a chapter chooser that loads each chapter's
   verses.js (and audio.js) only when it is opened, and hands it to the shared GitaReader
   (assets/gita.js, unchanged). GENERATED into gita/bhagavad-gita/ by scripts/gita/build_whole_gita.py
   from scripts/gita/article/reader.js; the chapter list is chapters.js. */
(function () {
  "use strict";
  const KEY = "gita-whole-chapter";
  const loads = new Map();

  function loadScript(src) {
    if (loads.has(src)) return loads.get(src);
    const p = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src; s.async = false;
      s.onload = () => resolve();
      s.onerror = () => { s.remove(); loads.delete(src); reject(new Error("failed to load " + src)); };
      document.head.appendChild(s);
    });
    loads.set(src, p);
    return p;
  }

  function remembered(chapters) {
    let n = null;
    try { n = parseInt(localStorage.getItem(KEY) || "", 10); } catch (_) {}
    const ok = chapters.filter(c => c.available);
    return (ok.find(c => c.n === n) || ok[0] || null);
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

  // opts: {base: path prefix of the site root ("" in the app, "../../" standalone), glossaryBase,
  //        onGlossary, onThinker, linkifyGlossary, glossaryResolve, voicebarSlot}
  function mount(root, opts) {
    opts = opts || {};
    const chapters = (window.GITA_WHOLE_CHAPTERS || []).slice().sort((a, b) => a.n - b.n);
    const base = opts.base || "";
    root.innerHTML = `
      <div class="gita-whole">
        <div class="gita-whole-bar" role="group" aria-label="Chapter">
          <button type="button" class="gita-whole-prev" aria-label="Previous chapter">‹</button>
          <label class="gita-whole-label">Chapter
            <select class="gita-whole-select">${chapters.map(c =>
              `<option value="${c.n}"${c.available ? "" : " disabled"}>${c.n}${c.available ? "" : " (in preparation)"}</option>`).join("")}</select>
          </label>
          <button type="button" class="gita-whole-next" aria-label="Next chapter">›</button>
          <span class="gita-whole-count" aria-live="polite"></span>
        </div>
        <div class="gita-whole-chapter"></div>
      </div>`;
    const sel = root.querySelector(".gita-whole-select");
    const host = root.querySelector(".gita-whole-chapter");
    const count = root.querySelector(".gita-whole-count");
    let token = 0;

    async function open(ch) {
      if (!ch || !ch.available) return;
      const mine = ++token;
      sel.value = String(ch.n);
      try { localStorage.setItem(KEY, String(ch.n)); } catch (_) {}
      host.innerHTML = '<p class="gita-whole-loading">Loading chapter ' + ch.n + "…</p>";
      const dir = base + "gita/ch" + ch.n + "/";
      try {
        for (const f of ch.files) await loadScript(dir + f + (ch.v ? "?v=" + ch.v : ""));
      } catch (e) {
        if (mine === token && root.isConnected) host.innerHTML = '<p role="status">Chapter ' + ch.n + " could not be loaded. Check your connection and choose it again.</p>";
        return;
      }
      if (mine !== token || !root.isConnected || !window.GitaReader) return;   // a newer choice, or the article was closed
      const verses = window["CH" + ch.n + "_VERSES"] || [];
      count.textContent = verses.length + " verses";
      window.GitaReader.render(host, {
        glossaryBase: opts.glossaryBase, audioBase: dir, voicebarSlot: opts.voicebarSlot,
        onGlossary: opts.onGlossary, onThinker: opts.onThinker,
        linkifyGlossary: opts.linkifyGlossary, glossaryResolve: opts.glossaryResolve,
        data: { verses, commentary: null, aurobindo: null, parallels: null, audio: window["CH" + ch.n + "_AUDIO"] || null },
      });
    }

    function step(d) {
      const ok = chapters.filter(c => c.available);
      const i = ok.findIndex(c => String(c.n) === sel.value);
      const next = ok[i + d];
      if (next) open(next);
    }
    sel.addEventListener("change", () => open(chapters.find(c => String(c.n) === sel.value)));
    root.querySelector(".gita-whole-prev").addEventListener("click", () => step(-1));
    root.querySelector(".gita-whole-next").addEventListener("click", () => step(1));
    return open(remembered(chapters));
  }

  window.GitaWhole = { mount };

  // Standalone page (gita/bhagavad-gita/index.html): mounts into #gitaWholeRoot.
  document.addEventListener("DOMContentLoaded", () => {
    const root = document.getElementById("gitaWholeRoot");
    if (root) mount(root, { base: "../../", glossaryBase: "../../data/glossary/", voicebarSlot: document.getElementById("voicebarSlot") });
  });
})();
