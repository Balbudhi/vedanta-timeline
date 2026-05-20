/* =============================================================
   Koi Hor Nahi Hai Mera — song data + render
   -------------------------------------------------------------
   LINES: every distinct line of the song, keyed by id. Edit the
   `english` string to revise a translation; refs in SEQUENCE
   propagate (the refrain is stored once and re-used).

   English markup format:
     {N:phrase}  or  {N,M:phrase}
   Each {N:…} marks `phrase` as the English rendering of the
   word at index N in `words` (0-indexed). Hovering that word
   highlights the matching English span (and shows the gloss
   in a tooltip). Multiple word indices may share a phrase.
   ============================================================= */

const LINES = {
  invocation: {
    roman: "Maa meri sachiyaan jota wali maata, teri sada hi jai",
    english: "{1:My} {0:Mother}, {5:O Mother} {4:of} the {2:true, eternal} {3:sacred flames} — may {8:victory} {7:always} be {6:Yours}.",
    words: [
      { roman: "Maa",        gloss: "Mother" },
      { roman: "meri",       gloss: "my" },
      { roman: "sachiyaan",  gloss: "true, genuine, eternal" },
      { roman: "jota",       gloss: "sacred flames; the divine jyoti" },
      { roman: "wali",       gloss: "bearer of, associated with" },
      { roman: "maata",      gloss: "Mother Goddess" },
      { roman: "teri",       gloss: "Your" },
      { roman: "sada hi",    gloss: "always, forever" },
      { roman: "jai",        gloss: "victory, glory, praise" }
    ]
  },

  refrain: {
    roman: "Main ladd phadya ae tera, koi hor nahi ae mera",
    english: "{0:I} {3:have} {2:held onto} {4:Your} {1:hem}; {6:I have no} {5:one else} {7:but You}.",
    words: [
      { roman: "Main",     gloss: "I" },
      { roman: "ladd",     gloss: "the hem, the edge of Your garment" },
      { roman: "phadya",   gloss: "have grasped, have held" },
      { roman: "ae",       gloss: "is — used here as the auxiliary ‘have’" },
      { roman: "tera",     gloss: "Yours" },
      { roman: "koi hor",  gloss: "anyone else" },
      { roman: "nahi ae",  gloss: "there is not" },
      { roman: "mera",     gloss: "mine" }
    ]
  },

  v1a: {
    roman: "Asi saah chhad jaavange",
    english: "{0:We} {3:will} eventually {2:let go} of our {1:breath}.",
    words: [
      { roman: "Asi",        gloss: "we" },
      { roman: "saah",       gloss: "breath" },
      { roman: "chhad",      gloss: "releasing, letting go" },
      { roman: "jaavange",   gloss: "we will go" }
    ]
  },

  v1b: {
    roman: "Pher baajaa maaroge, asi mud nahiyo aavange",
    english: "{0:Then} {2:You will} {1:call out} to us, but {3:we} {6:will} {5:not} {4:return}.",
    words: [
      { roman: "Pher",       gloss: "then, afterwards" },
      { roman: "baajaa",     gloss: "cries, calls (out to)" },
      { roman: "maaroge",    gloss: "You will strike, You will call out" },
      { roman: "asi",        gloss: "we" },
      { roman: "mud",        gloss: "back, again" },
      { roman: "nahiyo",     gloss: "not (emphatic)" },
      { roman: "aavange",    gloss: "we will come" }
    ]
  },

  v2a: {
    roman: "Is zindagi ton ki laina, maa",
    english: "{3:What} {4:is there to gain} {2:from} {0:this} {1:life} anyway, {5:Mother}?",
    words: [
      { roman: "Is",         gloss: "this" },
      { roman: "zindagi",    gloss: "life" },
      { roman: "ton",        gloss: "from" },
      { roman: "ki",         gloss: "what" },
      { roman: "laina",      gloss: "is there to take, is there to gain" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v2b: {
    roman: "Darshan na hoya, pher jee ke ki laina",
    english: "If I {1:do not get} to {0:see You}, {4:what is the point} {3:of living}?",
    words: [
      { roman: "Darshan",    gloss: "sacred sight — the reciprocal seeing of the deity" },
      { roman: "na hoya",    gloss: "has not occurred, did not happen" },
      { roman: "pher",       gloss: "then" },
      { roman: "jee ke",     gloss: "by living" },
      { roman: "ki laina",   gloss: "what is there to gain" }
    ]
  },

  v3a: {
    roman: "Asi dar tere aavange",
    english: "{0:We} {3:will come} to {2:Your} {1:door} just like this.",
    words: [
      { roman: "Asi",        gloss: "we" },
      { roman: "dar",        gloss: "door, threshold of Your shrine" },
      { roman: "tere",       gloss: "Your" },
      { roman: "aavange",    gloss: "we will come" }
    ]
  },

  v3b: {
    roman: "Saun apni paavegi, tainu chhad ke na jaavange",
    english: "Even if {2:You make us} {0:swear} on {1:our own} lives, we {5:will not} {4:leave} {3:You}.",
    words: [
      { roman: "Saun",       gloss: "oath" },
      { roman: "apni",       gloss: "Your own" },
      { roman: "paavegi",    gloss: "You will place the oath upon us" },
      { roman: "tainu",      gloss: "You" },
      { roman: "chhad ke",   gloss: "leaving, having left" },
      { roman: "na jaavange",gloss: "we will not go" }
    ]
  },

  v4a: {
    roman: "Eh zindagi teri ae, maa",
    english: "{0:This} {1:life} {3:is} already {2:Yours}, {4:Mother}.",
    words: [
      { roman: "Eh",         gloss: "this" },
      { roman: "zindagi",    gloss: "life" },
      { roman: "teri",       gloss: "Yours" },
      { roman: "ae",         gloss: "is" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v4b: {
    roman: "Kado pheraa aa jaave, is mitti di dheri ae",
    english: "{0:Who knows when} {1:the final call} {2:will come}? {3:This} body {7:is} just a {6:pile} {5:of} {4:dust}.",
    words: [
      { roman: "Kado",       gloss: "whenever, who knows when" },
      { roman: "pheraa",     gloss: "the turn, the cycle, the final summons" },
      { roman: "aa jaave",   gloss: "may come" },
      { roman: "is",         gloss: "this" },
      { roman: "mitti",      gloss: "earth, dust, clay" },
      { roman: "di",         gloss: "of" },
      { roman: "dheri",      gloss: "heap, pile" },
      { roman: "ae",         gloss: "is" }
    ]
  },

  v5a: {
    roman: "Tere charna ch reh laange",
    english: "{3:We will just stay} {2:at} {0:Your} {1:feet}.",
    words: [
      { roman: "Tere",       gloss: "Your" },
      { roman: "charna",     gloss: "Your sacred feet" },
      { roman: "ch",         gloss: "at, in" },
      { roman: "reh laange", gloss: "we will stay, we will remain" }
    ]
  },

  v5b: {
    roman: "Tu saanu maaf kar deyi, asi hass ke seh laange",
    english: "{2:Forgive} {1:us}, and {3:we} {5:will endure} everything {4:with a smile}.",
    words: [
      { roman: "Tu",         gloss: "You" },
      { roman: "saanu",      gloss: "us" },
      { roman: "maaf kar deyi", gloss: "forgive — a gentle, respectful command" },
      { roman: "asi",        gloss: "we" },
      { roman: "hass ke",    gloss: "smiling, with a smile" },
      { roman: "seh laange", gloss: "we will endure, we will bear it" }
    ]
  },

  v6a: {
    roman: "Tera ho ke main aavanga, maa",
    english: "{2:I} {3:will come back} {1:belonging} only {0:to You}, {4:Mother}.",
    words: [
      { roman: "Tera",       gloss: "Yours" },
      { roman: "ho ke",      gloss: "having become" },
      { roman: "main",       gloss: "I" },
      { roman: "aavanga",    gloss: "I will come" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v6b: {
    roman: "Tu vi pher rovengi, je chhad tainu jaavanga",
    english: "{0:Even You} {2:will cry} {1:then}, {3:if} {6:I} ever {4:leave} {5:You}.",
    words: [
      { roman: "Tu vi",      gloss: "You too" },
      { roman: "pher",       gloss: "then" },
      { roman: "rovengi",    gloss: "You will weep" },
      { roman: "je",         gloss: "if" },
      { roman: "chhad",      gloss: "leaving" },
      { roman: "tainu",      gloss: "You" },
      { roman: "jaavanga",   gloss: "I will go" }
    ]
  },

  v7a: {
    roman: "Tere reham bathere ne, maa",
    english: "{0:Your} {1:mercies} {3:are} {2:countless}, {4:Mother}.",
    words: [
      { roman: "Tere",       gloss: "Your" },
      { roman: "reham",      gloss: "mercies, graces" },
      { roman: "bathere",    gloss: "countless, abundant" },
      { roman: "ne",         gloss: "are" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v7b: {
    roman: "Khushiya dikha de vi maa, nahi te hanju bathere ne",
    english: "{1:Show} us {0:happiness}, {3:Mother}, {4:otherwise} there {6:are so many} {5:tears}.",
    words: [
      { roman: "Khushiya",   gloss: "joys, happiness" },
      { roman: "dikha de",   gloss: "show us" },
      { roman: "vi",         gloss: "at least, also" },
      { roman: "maa",        gloss: "Mother" },
      { roman: "nahi te",    gloss: "otherwise" },
      { roman: "hanju",      gloss: "tears" },
      { roman: "bathere ne", gloss: "are plentiful, are many" }
    ]
  },

  v8a: {
    roman: "Asi pher vi nahi bolange, maa",
    english: "{1:Even then}, {0:we} {2:will not say a word of complaint}, {3:Mother}.",
    words: [
      { roman: "Asi",        gloss: "we" },
      { roman: "pher vi",    gloss: "even then, still" },
      { roman: "nahi bolange",gloss: "will not speak, will not complain" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v8b: {
    roman: "Ikk vaari dass te jaa, dukh kihde agge pholange",
    english: "{2:Just} {1:tell} us {0:once}, {4:who else} {5:is there to share} {3:our sorrows} with?",
    words: [
      { roman: "Ikk vaari",  gloss: "just once" },
      { roman: "dass",       gloss: "tell" },
      { roman: "te jaa",     gloss: "go on, do tell" },
      { roman: "dukh",       gloss: "sorrows, pains" },
      { roman: "kihde agge", gloss: "before whom" },
      { roman: "pholange",   gloss: "will spread open, will unfurl — as in opening one’s heart" }
    ]
  },

  outro1: {
    roman: "Eh likh ke main jaavanga, maa",
    english: "{2:I} {3:will leave this world} {1:writing} {0:these very words}, {4:Mother}:",
    words: [
      { roman: "Eh",         gloss: "this, these very words" },
      { roman: "likh ke",    gloss: "having written" },
      { roman: "main",       gloss: "I" },
      { roman: "jaavanga",   gloss: "I will go, I will depart" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  outro2: {
    roman: "Agle janam vi maa, tera putt kahavanga",
    english: "{1:Even} in my {0:next life}, {2:Mother}, {5:I will be called} {3:Your} {4:son}.",
    words: [
      { roman: "Agle janam", gloss: "in the next birth" },
      { roman: "vi",         gloss: "also, even" },
      { roman: "maa",        gloss: "Mother" },
      { roman: "tera",       gloss: "Your" },
      { roman: "putt",       gloss: "son — a deeply tender word in Punjabi" },
      { roman: "kahavanga",  gloss: "I will be called" }
    ]
  },

  closing: {
    roman: "Koi hor nahi ae mera",
    english: "{1:I have no} {0:one else} {2:but You}.",
    words: [
      { roman: "Koi hor",    gloss: "anyone else" },
      { roman: "nahi ae",    gloss: "there is not" },
      { roman: "mera",       gloss: "mine" }
    ]
  }
};

/* SEQUENCE — the song's structure, in order.
   Each entry references a line id and an optional repetition count.
   `sectionLabel` adds a small heading above the next line. */
const SEQUENCE = [
  { ref: "invocation", sectionLabel: "Invocation" },

  { ref: "refrain", repeats: 4, sectionLabel: "Refrain" },

  { ref: "v1a", repeats: 4, sectionLabel: "I" },
  { ref: "v1b", repeats: 4 },

  { ref: "refrain", repeats: 2 },

  { ref: "v2a", repeats: 4, sectionLabel: "II" },
  { ref: "v2b", repeats: 4 },

  { ref: "refrain", repeats: 4 },

  { ref: "v3a", repeats: 4, sectionLabel: "III" },
  { ref: "v3b", repeats: 2 },

  { ref: "refrain", repeats: 4 },

  { ref: "v4a", repeats: 4, sectionLabel: "IV" },
  { ref: "v4b", repeats: 2 },

  { ref: "refrain", repeats: 4 },

  { ref: "v5a", repeats: 4, sectionLabel: "V" },
  { ref: "v5b", repeats: 4 },

  { ref: "refrain", repeats: 2 },

  { ref: "v6a", repeats: 4, sectionLabel: "VI" },
  { ref: "v6b", repeats: 2 },

  { ref: "refrain", repeats: 2 },

  { ref: "v7a", repeats: 4, sectionLabel: "VII" },
  { ref: "v7b", repeats: 2 },

  { ref: "refrain", repeats: 4 },

  { ref: "v8a", repeats: 4, sectionLabel: "VIII" },
  { ref: "v8b", repeats: 4 },

  { ref: "outro1", repeats: 4, sectionLabel: "Coda" },
  { ref: "outro2", repeats: 4 },

  { ref: "refrain", repeats: 6 },

  { ref: "closing" }
];

/* =============================================================
   RENDER
   ============================================================= */

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

function renderEnglishWithSpans(english) {
  const re = /\{([\d,\s]+):([^}]*)\}/g;
  let out = "";
  let last = 0;
  let m;
  while ((m = re.exec(english)) !== null) {
    if (m.index > last) out += escapeHtml(english.slice(last, m.index));
    const indices = m[1].split(",").map(s => s.trim()).filter(Boolean).join(" ");
    out += `<span class="we" data-word-i="${indices}">${escapeHtml(m[2])}</span>`;
    last = m.index + m[0].length;
  }
  if (last < english.length) out += escapeHtml(english.slice(last));
  return out;
}

function renderRomanWithSpans(roman, words) {
  if (!words || !words.length) return escapeHtml(roman);
  let html = "";
  let cursor = 0;
  const lower = roman.toLowerCase();
  for (let i = 0; i < words.length; i++) {
    const token = words[i].roman;
    const idx = lower.indexOf(token.toLowerCase(), cursor);
    if (idx === -1) {
      html += escapeHtml(roman.slice(cursor));
      cursor = roman.length;
      break;
    }
    if (idx > cursor) html += escapeHtml(roman.slice(cursor, idx));
    const surface = roman.slice(idx, idx + token.length);
    html += `<span class="w" data-word-i="${i}" data-gloss="${escapeHtml(words[i].gloss)}" tabindex="0">${escapeHtml(surface)}</span>`;
    cursor = idx + token.length;
  }
  if (cursor < roman.length) html += escapeHtml(roman.slice(cursor));
  return html;
}

function renderLine(line, repeats, sectionLabel, instanceId) {
  const repBadge = repeats && repeats > 1
    ? `<span class="rep" aria-label="repeated ${repeats} times">×${repeats}</span>`
    : "";
  const sectionHead = sectionLabel
    ? `<div class="section-label">${escapeHtml(sectionLabel)}</div>`
    : "";
  return `
    ${sectionHead}
    <article class="line" id="${instanceId}">
      <div class="line-roman">${renderRomanWithSpans(line.roman, line.words)}${repBadge}</div>
      <div class="line-english">${renderEnglishWithSpans(line.english)}</div>
    </article>
  `;
}

function render() {
  const root = document.getElementById("songRoot");
  if (!root) return;
  let html = "";
  SEQUENCE.forEach((entry, idx) => {
    const line = LINES[entry.ref];
    if (!line) return;
    html += renderLine(line, entry.repeats, entry.sectionLabel, `ln-${idx}-${entry.ref}`);
  });
  root.innerHTML = html;
  wireInteractions(root);
}

/* ----- Tooltip (single, reused) ----- */
let tooltipEl = null;
function ensureTooltip() {
  if (tooltipEl) return tooltipEl;
  tooltipEl = document.createElement("div");
  tooltipEl.className = "word-tooltip";
  tooltipEl.setAttribute("role", "tooltip");
  tooltipEl.hidden = true;
  document.body.appendChild(tooltipEl);
  return tooltipEl;
}
function showTooltip(span, text) {
  const tip = ensureTooltip();
  tip.textContent = text;
  tip.hidden = false;
  const r = span.getBoundingClientRect();
  tip.style.left = "0px";
  tip.style.top  = "0px";
  const tr = tip.getBoundingClientRect();
  const margin = 8;
  let left = r.left + r.width / 2 - tr.width / 2 + window.scrollX;
  let top  = r.top - tr.height - 8 + window.scrollY;
  const minLeft = window.scrollX + margin;
  const maxLeft = window.scrollX + document.documentElement.clientWidth - tr.width - margin;
  if (left < minLeft) left = minLeft;
  if (left > maxLeft) left = maxLeft;
  if (top < window.scrollY + margin) top = r.bottom + 8 + window.scrollY;
  tip.style.left = left + "px";
  tip.style.top  = top + "px";
}
function hideTooltip() { if (tooltipEl) tooltipEl.hidden = true; }

function activate(span) {
  const article = span.closest(".line");
  if (!article) return;
  const i = span.dataset.wordI;
  span.classList.add("is-hi");
  article.querySelectorAll(".we").forEach(el => {
    const idx = el.dataset.wordI.split(/\s+/);
    if (idx.includes(i)) el.classList.add("is-hi");
  });
  showTooltip(span, span.dataset.gloss || "");
}
function deactivate(span) {
  const article = span.closest(".line");
  if (!article) return;
  const i = span.dataset.wordI;
  span.classList.remove("is-hi");
  article.querySelectorAll(".we").forEach(el => {
    const idx = el.dataset.wordI.split(/\s+/);
    if (idx.includes(i)) el.classList.remove("is-hi");
  });
  hideTooltip();
}
function deactivateAll(root) {
  if (tooltipEl) tooltipEl.hidden = true;
  root.querySelectorAll(".w.is-hi, .we.is-hi").forEach(el => el.classList.remove("is-hi"));
}

function wireInteractions(root) {
  let stickyWord = null;
  let hoverWord  = null;

  root.addEventListener("mouseover", e => {
    const w = e.target.closest(".w");
    if (!w || w === hoverWord) return;
    if (hoverWord && hoverWord !== stickyWord) deactivate(hoverWord);
    hoverWord = w;
    activate(w);
  });
  root.addEventListener("mouseout", e => {
    const w = e.target.closest(".w");
    if (!w) return;
    const to = e.relatedTarget;
    if (to && w.contains(to)) return;
    if (w !== stickyWord) deactivate(w);
    if (hoverWord === w) hoverWord = null;
  });

  root.addEventListener("click", e => {
    const w = e.target.closest(".w");
    if (!w) return;
    e.stopPropagation();
    if (stickyWord === w) {
      stickyWord = null;
      deactivate(w);
      return;
    }
    if (stickyWord) deactivate(stickyWord);
    stickyWord = w;
    activate(w);
  });
  document.addEventListener("click", () => {
    if (stickyWord) { deactivate(stickyWord); stickyWord = null; }
  });

  root.addEventListener("focusin", e => {
    const w = e.target.closest(".w");
    if (!w) return;
    activate(w);
  });
  root.addEventListener("focusout", e => {
    const w = e.target.closest(".w");
    if (!w || w === stickyWord) return;
    deactivate(w);
  });

  window.addEventListener("scroll", () => {
    if (tooltipEl) tooltipEl.hidden = true;
  }, { passive: true });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      if (stickyWord) { deactivate(stickyWord); stickyWord = null; }
      else deactivateAll(root);
    }
  });
}

document.addEventListener("DOMContentLoaded", render);
