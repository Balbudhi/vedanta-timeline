#!/usr/bin/env node
"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "..");
const app = fs.readFileSync(path.join(ROOT, "assets/app.js"), "utf8");
const css = fs.readFileSync(path.join(ROOT, "assets/style.css"), "utf8");

function token(name) {
  const match = css.match(new RegExp(`--z-${name}:\\s*(\\d+)`));
  assert.ok(match, `missing --z-${name}`);
  return Number(match[1]);
}

const reader = token("reader-overlay");
const scrim = token("popover-scrim");
const popover = token("popover");
const filter = token("filter-drawer");
const topbar = token("topbar");
const modal = token("modal");
assert.ok(reader < scrim, "popover scrim is above the mobile reader");
assert.ok(scrim < popover, "popover is above its scrim");
assert.ok(reader < filter && filter < topbar, "filter is above the reader and below the topbar");
assert.ok(topbar < modal, "true modals cover the topbar");

const managerStart = app.indexOf("const popoverManager = (() => {");
const managerEnd = app.indexOf("// ---------- popover drag helper", managerStart);
assert.ok(managerStart >= 0 && managerEnd > managerStart, "popover manager is present");
const context = {};
vm.createContext(context);
vm.runInContext(`${app.slice(managerStart, managerEnd)}\nthis.manager = popoverManager;`, context);

const closed = [];
const closeA = () => closed.push("a");
const closeB = () => closed.push("b");
context.manager.open(closeA);
context.manager.open(closeB);
assert.deepEqual(closed, ["a"], "opening a surface closes the previous one");
assert.equal(context.manager.closeTop(), true, "Escape path reports a closed top surface");
assert.deepEqual(closed, ["a", "b"], "the current top surface closes once");
assert.equal(context.manager.closeTop(), false, "no second surface remains to close");

assert.match(app, /popoverManager\.open\(closeFilterDrawer\)/,
  "the filter participates in single-surface arbitration");
assert.match(app, /if \(popoverManager\.closeTop\(\)\) \{[\s\S]*?stopImmediatePropagation\(\);[\s\S]*?return;/,
  "Escape stops after closing the top surface");

console.log("timeline surface order: stack and arbitration passed");
