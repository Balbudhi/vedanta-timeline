// Bounded DOM fixture for article ownership tests, not a browser parser/layout engine.
const assert = require("node:assert/strict");
class Element {
  constructor(tag = "div", attrs = {}, text = null) {
    this.tagName = tag.toUpperCase(); this.attrs = attrs; this.children = [];
    this.parentNode = null; this.text = text; this.scrollTop = 0; this.hidden = false;
    this.style = { setProperty() {} }; this.writes = 0; this.listeners = new Map();
    this.paused = true; this.ended = false; this.currentTime = 0; this.duration = 100;
    this.classList = {
      contains: c => (this.attrs.class || "").split(/\s+/).includes(c),
      add: c => { if (!this.classList.contains(c)) this.attrs.class = ((this.attrs.class || "") + " " + c).trim(); },
      remove: c => { this.attrs.class = (this.attrs.class || "").split(/\s+/).filter(x => x !== c).join(" "); },
      toggle: (c, on) => { if (on ?? !this.classList.contains(c)) this.classList.add(c); else this.classList.remove(c); },
    };
  }
  get dataset() {
    return new Proxy({}, {
      get: (_, key) => this.attrs["data-" + String(key).replace(/[A-Z]/g, c => "-" + c.toLowerCase())],
      set: (_, key, value) => { this.attrs["data-" + String(key).replace(/[A-Z]/g, c => "-" + c.toLowerCase())] = String(value); return true; },
    });
  }
  get innerHTML() { return this.children.map(x => x.outerHTML).join(""); }
  set innerHTML(html) { this.writes++; this.replaceChildren(...parse(String(html))); }
  get outerHTML() {
    if (this.text !== null) return this.text;
    const tag = this.tagName.toLowerCase();
    const start = `<${tag}${Object.entries(this.attrs).map(([k,v]) => ` ${k}="${v}"`).join("")}>`;
    return /^(?:br|hr|img|input|meta|link)$/.test(tag) ? start : `${start}${this.innerHTML}</${tag}>`;
  }

  get textContent() { return this.text !== null ? this.text.replace(/<[^>]*>/g, "") : this.children.map(x => x.textContent).join(""); }
  set textContent(s) { this.replaceChildren(new Element("#text", {}, String(s))); }
  appendChild(el) { if (el.parentNode) el.remove(); el.parentNode = this; this.children.push(el); return el; }
  append(...els) { for (const el of els) this.appendChild(el); }
  replaceChildren(...els) { for (const el of this.children) el.parentNode = null; this.children = []; this.append(...els); }
  remove() { this.removed = true; if (this.parentNode) { const p = this.parentNode; p.children.splice(p.children.indexOf(this),1); this.parentNode = null; } }
  replaceWith(el) { const p = this.parentNode; assert.ok(p, "replacement target attached"); const i = p.children.indexOf(this); this.parentNode = null; el.parentNode = p; p.children[i] = el; }
  insertAdjacentHTML(where, html) { assert.equal(where, "beforeend", "fixture supports append insertion only"); this.append(...parse(html)); }
  setAttribute(k,v) { this.attrs[k] = String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  closest(selector) { return this.matches(selector) ? this : this.parentNode?.closest(selector) || null; }
  getAttribute(k) { return this.attrs[k] ?? null; }
  get lastChild() { return this.children.at(-1) || null; }
  get nodeValue() { return this.text; }
  set nodeValue(value) { this.text = String(value); }
  get firstElementChild() { return this.children.find(x => x.text === null) || null; }
  contains(el) { return this === el || this.children.some(x => x.contains(el)); }
  get isConnected() { return this.parentNode ? this.parentNode.isConnected : this.tagName === "BODY"; }
  matches(selector) {
    if (this.text !== null) return false;
    if (selector.startsWith(".")) return this.classList.contains(selector.slice(1));
    if (selector.startsWith("#")) return this.attrs.id === selector.slice(1);
    const m = selector.match(/^([\w-]+)?\[([\w-]+)(?:=["']?([^"'\]]+)["']?)?\]$/);
    if (m) return (!m[1] || this.tagName.toLowerCase() === m[1]) && this.attrs[m[2]] != null && (m[3] == null || this.attrs[m[2]] === m[3]);
    return this.tagName.toLowerCase() === selector;
  }
  querySelectorAll(selector) { const all = []; for (const child of this.children) { if (child.matches(selector)) all.push(child); all.push(...child.querySelectorAll(selector)); } return all; }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  addEventListener(name, fn) { if(!this.listeners.has(name))this.listeners.set(name,[]);this.listeners.get(name).push(fn); }
  removeEventListener(name, fn) { this.listeners.set(name,(this.listeners.get(name)||[]).filter(x=>x!==fn)); }
  emit(name, event={}) { for(const fn of this.listeners.get(name)||[])fn(event); }
  pause() { this.paused=true; }
  play() { this.paused=false; return Promise.resolve(); }
}
function parse(html) {
  const root = new Element(), stack = [root];
  for (const token of html.match(/<!--[\s\S]*?-->|<[^>]+>|[^<]+/g) || []) {
    if (token.startsWith("<!--")) continue;
    if (token.startsWith("</")) { if (stack.length > 1) stack.pop(); continue; }
    if (token.startsWith("<")) {
      const tag = token.match(/^<([\w-]+)/)?.[1]; if (!tag) continue;
      const attrs = {};
      const attributes = token.slice(tag.length + 1, -1);
      for (const m of attributes.matchAll(/([\w-]+)(?:\s*=\s*"([^"]*)")?/g)) attrs[m[1]] = m[2] ?? "";
      const el = new Element(tag,attrs); stack.at(-1).appendChild(el);
      if (!/^(?:br|hr|img|input|meta|link)$/i.test(tag) && !token.endsWith("/>")) stack.push(el);
    } else stack.at(-1).appendChild(new Element("#text", {}, token));
  }
  return [...root.children];
}

module.exports = { Element };
