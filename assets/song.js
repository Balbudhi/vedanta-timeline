/* =============================================================
   Koi Hor Nahi Hai Mera — song data + render
   -------------------------------------------------------------
   LINES: every distinct line of the song, keyed by id.
   Edit the `english` field freely — the refrain (and any
   line repeated by reference) updates everywhere at once.
   `words` is the word-by-word breakdown shown on click; the
   `roman` field of each word must match a substring of the
   line's roman text (case-insensitive) so the hover-highlight
   can find it.
   ============================================================= */

const LINES = {
  invocation: {
    roman: "Maa meri sachiyaan jota wali maata, teri sada hi jai",
    english: "My Mother, O Mother of the true sacred flames — may victory always be Yours.",
    words: [
      { roman: "Maa",        gloss: "Mother" },
      { roman: "meri",       gloss: "my" },
      { roman: "sachiyaan",  gloss: "true / genuine (fem. pl., modifying ‘flames’)" },
      { roman: "jota",       gloss: "flames; the divine jyoti" },
      { roman: "wali",       gloss: "possessor of, associated with" },
      { roman: "maata",      gloss: "Mother Goddess" },
      { roman: "teri",       gloss: "Your" },
      { roman: "sada hi",    gloss: "always" },
      { roman: "jai",        gloss: "victory, glory, praise" }
    ],
    note: "Addressed to the Goddess as bearer of the sacred flame (jyotī̃-wālī mātā) — Vaishno Devi / Jwala Ji / Shakta register."
  },

  refrain: {
    roman: "Main ladd phadya ae tera, koi hor nahi ae mera",
    english: "I have held onto Your hem; I have no one else but You.",
    words: [
      { roman: "Main",     gloss: "I" },
      { roman: "ladd",     gloss: "hem / edge of the garment (the pallu)" },
      { roman: "phadya",   gloss: "have grasped, have caught hold of" },
      { roman: "ae",       gloss: "is (auxiliary: ‘have’)" },
      { roman: "tera",     gloss: "Yours" },
      { roman: "koi hor",  gloss: "anyone else" },
      { roman: "nahi ae",  gloss: "there is not" },
      { roman: "mera",     gloss: "mine, belonging to me" }
    ],
    note: "Not abstract faith — a child physically clutching the Mother's garment-edge."
  },

  v1a: {
    roman: "Asi saah chhad jaavange",
    english: "We will eventually let go of our breath.",
    words: [
      { roman: "Asi",        gloss: "we" },
      { roman: "saah",       gloss: "breath" },
      { roman: "chhad",      gloss: "leaving, releasing" },
      { roman: "jaavange",   gloss: "will go (future, 1pl.)" }
    ],
    note: "i.e. ‘we will die.’"
  },

  v1b: {
    roman: "Pher baajaa maaroge, asi mud nahiyo aavange",
    english: "Then You will call out to us, but we will not return.",
    words: [
      { roman: "Pher",       gloss: "then, afterwards" },
      { roman: "baajaa",     gloss: "calls, cries (vocative summons)" },
      { roman: "maaroge",    gloss: "will strike / call out" },
      { roman: "asi",        gloss: "we" },
      { roman: "mud",        gloss: "back, again" },
      { roman: "nahiyo",     gloss: "not (emphatic negation)" },
      { roman: "aavange",    gloss: "will come" }
    ],
    note: "‘bāj māranā’ = to call out / summon. Devotional paradox: ‘call me now, before death.’"
  },

  v2a: {
    roman: "Is zindagi ton ki laina, maa",
    english: "What is there to gain from this life anyway, Mother?",
    words: [
      { roman: "Is",         gloss: "this" },
      { roman: "zindagi",    gloss: "life" },
      { roman: "ton",        gloss: "from" },
      { roman: "ki",         gloss: "what" },
      { roman: "laina",      gloss: "is there to take (gerundive)" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v2b: {
    roman: "Darshan na hoya, pher jee ke ki laina",
    english: "If I do not get to see You, what is the point of living?",
    words: [
      { roman: "Darshan",    gloss: "sacred sight; reciprocal seeing of the deity" },
      { roman: "na hoya",    gloss: "did not happen / has not occurred" },
      { roman: "pher",       gloss: "then" },
      { roman: "jee ke",     gloss: "by living" },
      { roman: "ki laina",   gloss: "what is there to gain" }
    ],
    note: "Darśan is not mere seeing — it is mutual presence: the devotee sees the deity and is seen."
  },

  v3a: {
    roman: "Asi dar tere aavange",
    english: "We will come to Your door just like this.",
    words: [
      { roman: "Asi",        gloss: "we" },
      { roman: "dar",        gloss: "door, threshold, court (shrine)" },
      { roman: "tere",       gloss: "Your" },
      { roman: "aavange",    gloss: "will come" }
    ]
  },

  v3b: {
    roman: "Saun apni paavegi, tainu chhad ke na jaavange",
    english: "Even if You make us swear on our own lives, we will not leave You.",
    words: [
      { roman: "Saun",       gloss: "oath" },
      { roman: "apni",       gloss: "(Your) own" },
      { roman: "paavegi",    gloss: "will place (the oath on us)" },
      { roman: "tainu",      gloss: "You (accusative)" },
      { roman: "chhad ke",   gloss: "leaving, having left" },
      { roman: "na jaavange",gloss: "will not go" }
    ]
  },

  v4a: {
    roman: "Eh zindagi teri ae, maa",
    english: "This life is already Yours, Mother.",
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
    english: "Who knows when the final call will come? This body is just a pile of dust.",
    words: [
      { roman: "Kado",       gloss: "when (who knows when)" },
      { roman: "pheraa",     gloss: "turn, cycle, summons" },
      { roman: "aa jaave",   gloss: "may come" },
      { roman: "is",         gloss: "this" },
      { roman: "mitti",      gloss: "earth, dust, clay" },
      { roman: "di",         gloss: "of" },
      { roman: "dheri",      gloss: "heap, pile" },
      { roman: "ae",         gloss: "is" }
    ],
    note: "‘miṭṭī dī ḍherī’ — a heap of dust. Stark mortality imagery."
  },

  v5a: {
    roman: "Tere charna ch reh laange",
    english: "We will just stay at Your feet.",
    words: [
      { roman: "Tere",       gloss: "Your" },
      { roman: "charna",     gloss: "feet (sacred, oblique plural)" },
      { roman: "ch",         gloss: "in / at (postposition)" },
      { roman: "reh laange", gloss: "we will remain (compound verb)" }
    ]
  },

  v5b: {
    roman: "Tu saanu maaf kar deyi, asi hass ke seh laange",
    english: "Forgive us, and we will endure everything with a smile.",
    words: [
      { roman: "Tu",         gloss: "You" },
      { roman: "saanu",      gloss: "us (dative)" },
      { roman: "maaf kar deyi", gloss: "forgive (imperative, respectful)" },
      { roman: "asi",        gloss: "we" },
      { roman: "hass ke",    gloss: "smiling, having laughed" },
      { roman: "seh laange", gloss: "will endure (compound verb)" }
    ]
  },

  v6a: {
    roman: "Tera ho ke main aavanga, maa",
    english: "I will come back belonging only to You, Mother.",
    words: [
      { roman: "Tera",       gloss: "Yours" },
      { roman: "ho ke",      gloss: "having become" },
      { roman: "main",       gloss: "I" },
      { roman: "aavanga",    gloss: "will come (1sg.)" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v6b: {
    roman: "Tu vi pher rovengi, je chhad tainu jaavanga",
    english: "Even You will cry then, if I ever leave You.",
    words: [
      { roman: "Tu vi",      gloss: "You too" },
      { roman: "pher",       gloss: "then" },
      { roman: "rovengi",    gloss: "will weep (2sg. fem.)" },
      { roman: "je",         gloss: "if" },
      { roman: "chhad",      gloss: "leaving" },
      { roman: "tainu",      gloss: "You (acc.)" },
      { roman: "jaavanga",   gloss: "I go (1sg. fut.)" }
    ],
    note: "Bhakti intimacy: the devotee imagines mutual emotional dependence with the deity."
  },

  v7a: {
    roman: "Tere reham bathere ne, maa",
    english: "Your mercies are countless, Mother.",
    words: [
      { roman: "Tere",       gloss: "Your" },
      { roman: "reham",      gloss: "mercies, graces" },
      { roman: "bathere",    gloss: "countless, abundant" },
      { roman: "ne",         gloss: "are (plural copula)" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v7b: {
    roman: "Khushiya dikha de vi maa, nahi te hanju bathere ne",
    english: "Show us happiness, Mother, otherwise there are so many tears.",
    words: [
      { roman: "Khushiya",   gloss: "joys, happiness" },
      { roman: "dikha de",   gloss: "show (imperative)" },
      { roman: "vi",         gloss: "at least, also" },
      { roman: "maa",        gloss: "Mother" },
      { roman: "nahi te",    gloss: "otherwise" },
      { roman: "hanju",      gloss: "tears" },
      { roman: "bathere ne", gloss: "are plentiful" }
    ]
  },

  v8a: {
    roman: "Asi pher vi nahi bolange, maa",
    english: "Even then, we will not say a word of complaint, Mother.",
    words: [
      { roman: "Asi",        gloss: "we" },
      { roman: "pher vi",    gloss: "even then, still" },
      { roman: "nahi bolange",gloss: "will not speak / complain" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  v8b: {
    roman: "Ikk vaari dass te jaa, dukh kihde agge pholange",
    english: "Just tell us once, who else is there to share our sorrows with?",
    words: [
      { roman: "Ikk vaari",  gloss: "just once" },
      { roman: "dass",       gloss: "tell" },
      { roman: "te jaa",     gloss: "and go (idiomatic: ‘do tell’)" },
      { roman: "dukh",       gloss: "sorrows, pains" },
      { roman: "kihde agge", gloss: "before whom" },
      { roman: "pholange",   gloss: "will unfurl, open out" }
    ],
    note: "‘pholṇā’ = to spread/unfold something out — here, to open one's heart."
  },

  outro1: {
    roman: "Eh likh ke main jaavanga, maa",
    english: "I will leave this world writing these very words, Mother:",
    words: [
      { roman: "Eh",         gloss: "this" },
      { roman: "likh ke",    gloss: "having written" },
      { roman: "main",       gloss: "I" },
      { roman: "jaavanga",   gloss: "will go, will depart" },
      { roman: "maa",        gloss: "Mother" }
    ]
  },

  outro2: {
    roman: "Agle janam vi maa, tera putt kahavanga",
    english: "Even in my next life, Mother, I will be called Your son.",
    words: [
      { roman: "Agle janam", gloss: "in the next birth" },
      { roman: "vi",         gloss: "also, even" },
      { roman: "maa",        gloss: "Mother" },
      { roman: "tera",       gloss: "Your" },
      { roman: "putt",       gloss: "son (emotionally charged in Punjabi)" },
      { roman: "kahavanga",  gloss: "will be called" }
    ]
  },

  closing: {
    roman: "Koi hor nahi ae mera",
    english: "I have no one else but You.",
    words: [
      { roman: "Koi hor",    gloss: "anyone else" },
      { roman: "nahi ae",    gloss: "is not" },
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

/* Tokenize the roman line into <span class="w">…</span> spans,
   matching each word entry to its position in the line so hover
   can link the span to its breakdown row. Multi-word tokens
   ("koi hor", "reh laange") are matched as a single span. */
function renderRomanWithSpans(roman, words) {
  if (!words || !words.length) return escapeHtml(roman);

  let html = "";
  let cursor = 0;
  const lower = roman.toLowerCase();

  for (let i = 0; i < words.length; i++) {
    const token = words[i].roman;
    const idx = lower.indexOf(token.toLowerCase(), cursor);
    if (idx === -1) {
      // Couldn't locate this word — append the rest as plain text and bail.
      html += escapeHtml(roman.slice(cursor));
      cursor = roman.length;
      break;
    }
    if (idx > cursor) html += escapeHtml(roman.slice(cursor, idx));
    const surface = roman.slice(idx, idx + token.length);
    html += `<span class="w" data-word-i="${i}" tabindex="0">${escapeHtml(surface)}</span>`;
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

  const noteHtml = line.note
    ? `<div class="line-note">${escapeHtml(line.note)}</div>`
    : "";

  const breakdownRows = (line.words || []).map((w, i) => `
    <tr data-word-i="${i}">
      <td class="bd-roman">${escapeHtml(w.roman)}</td>
      <td class="bd-gloss">${escapeHtml(w.gloss)}</td>
    </tr>`).join("");

  return `
    ${sectionHead}
    <article class="line" id="${instanceId}">
      <div class="line-body">
        <div class="line-roman">${renderRomanWithSpans(line.roman, line.words)}${repBadge}</div>
        <div class="line-english">${escapeHtml(line.english)}</div>
        ${noteHtml}
      </div>
      <button class="line-toggle" type="button" aria-expanded="false" aria-controls="${instanceId}-bd">
        <span class="line-toggle-caret" aria-hidden="true"></span>
        <span class="line-toggle-label">Word by word</span>
      </button>
      <div class="line-breakdown" id="${instanceId}-bd" hidden>
        <table>
          <tbody>${breakdownRows}</tbody>
        </table>
      </div>
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
    const instanceId = `ln-${idx}-${entry.ref}`;
    html += renderLine(line, entry.repeats, entry.sectionLabel, instanceId);
  });
  root.innerHTML = html;

  wireInteractions(root);
}

/* Word-tooltip element (single, reused). */
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

function showTooltip(span, gloss) {
  const tip = ensureTooltip();
  tip.textContent = gloss;
  tip.hidden = false;
  const r = span.getBoundingClientRect();
  // Position above the word, centered.
  tip.style.left = "0px";
  tip.style.top = "0px";
  const tr = tip.getBoundingClientRect();
  let left = r.left + r.width / 2 - tr.width / 2 + window.scrollX;
  let top  = r.top - tr.height - 8 + window.scrollY;
  // Keep within viewport horizontally.
  const margin = 8;
  if (left < margin + window.scrollX) left = margin + window.scrollX;
  const maxLeft = window.scrollX + document.documentElement.clientWidth - tr.width - margin;
  if (left > maxLeft) left = maxLeft;
  // Flip below if no room above.
  if (top < window.scrollY + margin) top = r.bottom + 8 + window.scrollY;
  tip.style.left = left + "px";
  tip.style.top  = top + "px";
}

function hideTooltip() {
  if (tooltipEl) tooltipEl.hidden = true;
}

function wireInteractions(root) {
  // Toggle breakdown panel.
  root.addEventListener("click", e => {
    const toggle = e.target.closest(".line-toggle");
    if (toggle) {
      const article = toggle.closest(".line");
      const bd = article.querySelector(".line-breakdown");
      const open = !bd.hidden;
      bd.hidden = open;
      toggle.setAttribute("aria-expanded", String(!open));
      article.classList.toggle("is-open", !open);
      return;
    }
    // Click on a word: also opens the breakdown (preview → reveal).
    const word = e.target.closest(".w");
    if (word) {
      const article = word.closest(".line");
      const bd = article.querySelector(".line-breakdown");
      const t  = article.querySelector(".line-toggle");
      if (bd && bd.hidden) {
        bd.hidden = false;
        t.setAttribute("aria-expanded", "true");
        article.classList.add("is-open");
      }
      const i = word.dataset.wordI;
      const row = bd.querySelector(`tr[data-word-i="${i}"]`);
      if (row) {
        row.classList.add("flash");
        row.scrollIntoView({ block: "nearest", behavior: "smooth" });
        setTimeout(() => row.classList.remove("flash"), 900);
      }
    }
  });

  // Hover: show tooltip + sync-highlight the matching breakdown row.
  root.addEventListener("mouseover", e => {
    const word = e.target.closest(".w");
    if (!word) return;
    const article = word.closest(".line");
    const i = word.dataset.wordI;
    const id = article.id;
    // Find the line's data via the rendered table — gloss is the second cell.
    const row = article.querySelector(`.line-breakdown tr[data-word-i="${i}"]`);
    if (!row) return;
    const gloss = row.querySelector(".bd-gloss").textContent;
    showTooltip(word, gloss);
    word.classList.add("is-hi");
    row.classList.add("is-hi");
  });
  root.addEventListener("mouseout", e => {
    const word = e.target.closest(".w");
    if (!word) return;
    hideTooltip();
    word.classList.remove("is-hi");
    const article = word.closest(".line");
    const i = word.dataset.wordI;
    const row = article.querySelector(`.line-breakdown tr[data-word-i="${i}"]`);
    if (row) row.classList.remove("is-hi");
  });

  // Keyboard focus: same as hover.
  root.addEventListener("focusin", e => {
    const word = e.target.closest(".w");
    if (!word) return;
    const article = word.closest(".line");
    const i = word.dataset.wordI;
    const row = article.querySelector(`.line-breakdown tr[data-word-i="${i}"]`);
    if (!row) return;
    showTooltip(word, row.querySelector(".bd-gloss").textContent);
    word.classList.add("is-hi");
    row.classList.add("is-hi");
  });
  root.addEventListener("focusout", e => {
    const word = e.target.closest(".w");
    if (!word) return;
    hideTooltip();
    word.classList.remove("is-hi");
    const article = word.closest(".line");
    const i = word.dataset.wordI;
    const row = article.querySelector(`.line-breakdown tr[data-word-i="${i}"]`);
    if (row) row.classList.remove("is-hi");
  });

  // Hide tooltip on scroll.
  window.addEventListener("scroll", hideTooltip, { passive: true });
}

document.addEventListener("DOMContentLoaded", render);
