#!/usr/bin/env node
"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(ROOT, "assets/app.js"), "utf8");
const start = source.indexOf("function computeLaneLabelPlacements(");
const end = source.indexOf("// ---------- render: dots -----------", start);
assert.ok(start >= 0 && end > start, "lane label placement function is present");

const context = {};
vm.createContext(context);
vm.runInContext(`${source.slice(start, end)}\nthis.place = computeLaneLabelPlacements;`, context);

const viewportCases = [
  { width: 390, laneHeight: 64 },
  { width: 768, laneHeight: 96 },
  { width: 1440, laneHeight: 96 },
  { width: 1920, laneHeight: 96 },
];

function fixture(laneHeight) {
  const points = [];
  for (let lane = 0; lane < 3; lane++) {
    const center = lane * laneHeight + laneHeight / 2;
    const offsets = laneHeight <= 72 ? [-20, -10, 0, 10, 20] : [-36, -24, 0, 24, 36];
    offsets.forEach((offset, i) => {
      points.push({
        thinker: { id: `lane-${lane}-${i}`, name: `A deliberately long label ${lane}-${i}` },
        lane,
        x: 240 + i * 3,
        y: center + offset,
      });
    });
  }
  return points;
}

for (const { width, laneHeight } of viewportCases) {
  const points = fixture(laneHeight);
  const placements = context.place(points, {
    laneHeight,
    plotBottom: laneHeight * 3,
    laneLocal: true,
  });
  assert.equal(placements.size, points.length, `${width}px: every label is placed`);

  for (const point of points) {
    const box = placements.get(point.thinker.id);
    const inset = laneHeight <= 72 ? 1 : 3;
    const laneTop = point.lane * laneHeight + inset;
    const laneBottom = (point.lane + 1) * laneHeight - inset;
    assert.ok(box.y1 >= laneTop, `${width}px ${point.thinker.id}: label top stays in lane`);
    assert.ok(box.y2 <= laneBottom, `${width}px ${point.thinker.id}: label bottom stays in lane`);

    if (box.where === "above") {
      assert.equal(box.y2, point.y - box.dy,
        `${width}px ${point.thinker.id}: above connector uses the rendered dy`);
      assert.ok(point.y - 4 >= laneTop && point.y - 4 <= laneBottom,
        `${width}px ${point.thinker.id}: above connector endpoint stays in lane`);
    } else {
      assert.equal(box.y1, point.y + box.dy,
        `${width}px ${point.thinker.id}: below connector uses the rendered dy`);
      assert.ok(point.y + 4 >= laneTop && point.y + 4 <= laneBottom,
        `${width}px ${point.thinker.id}: below connector endpoint stays in lane`);
    }
  }
}

console.log("timeline lane-label geometry: 4 viewport widths passed");
