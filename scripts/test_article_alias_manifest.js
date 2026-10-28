#!/usr/bin/env node
"use strict";

// CLI acceptance contract for scripts/check_article_aliases.js:
//   node scripts/check_article_aliases.js --manifest <path>
// Exit 0 for valid article slug/alias ownership; nonzero with a diagnostic for
// malformed metadata or collisions. Content integration is a separate gate.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const root = path.resolve(__dirname, "..");
const validator = path.join(__dirname, "check_article_aliases.js");
const entry = (slug, aliases) => ({ slug, title: slug, ...(aliases === undefined ? {} : { aliases }) });
const manifest = (...articles) => ({ articles });
const cases = [
  ["canonical articles without alias metadata", manifest(entry("first"), entry("second")), true],
  ["empty alias list", manifest(entry("first", [])), true],
  ["distinct direct aliases", manifest(entry("first", ["old-first", "older-first"]), entry("second", ["old-second"])), true],
  ["empty article manifest", manifest(), true],
  ["missing articles array", {}, false],
  ["articles is not an array", { articles: {} }, false],
  ["null article entry", manifest(null), false],
  ["missing canonical slug", manifest({ title: "No slug" }), false],
  ["duplicate canonical slug", manifest(entry("same"), entry("same")), false],
  ["aliases supplied as a string", manifest(entry("first", "old-first")), false],
  ["aliases supplied as null", manifest(entry("first", null)), false],
  ["aliases supplied as an object", manifest(entry("first", {})), false],
  ["non-string alias", manifest(entry("first", [42])), false],
  ["null alias", manifest(entry("first", [null])), false],
  ["empty alias", manifest(entry("first", [""])), false],
  ["whitespace-only alias", manifest(entry("first", [" "])), false],
  ["alias with surrounding whitespace", manifest(entry("first", [" old-first "])), false],
  ["alias with an embedded space", manifest(entry("first", ["old first"])), false],
  ["alias with path separator", manifest(entry("first", ["old/first"])), false],
  ["alias with query separator", manifest(entry("first", ["old?first"])), false],
  ["alias with hash separator", manifest(entry("first", ["old#first"])), false],
  ["duplicate alias in one owner", manifest(entry("first", ["old", "old"])), false],
  ["self-alias", manifest(entry("first", ["first"])), false],
  ["two owners of one alias", manifest(entry("first", ["old"]), entry("second", ["old"])), false],
  ["alias collides with later canonical slug", manifest(entry("first", ["second"]), entry("second")), false],
  ["alias collides with earlier canonical slug", manifest(entry("second"), entry("first", ["second"])), false],
  ["alias cycle through canonical owners", manifest(entry("first", ["second"]), entry("second", ["first"])), false],
];

if (!fs.existsSync(validator)) {
  console.error("FAIL prerequisite: scripts/check_article_aliases.js has not been implemented.");
  console.error(`BLOCKED: ${cases.length} fixture cases plus actual-manifest and malformed-JSON checks; none were counted as passed.`);
  process.exitCode = 1;
} else {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "vedanta-article-alias-tests-"));
  let passed = 0, failed = 0;
  function check(name, file, expectedValid) {
    try {
      const result = spawnSync(process.execPath, [validator, "--manifest", file], {
        cwd: root, encoding: "utf8", timeout: 5000, maxBuffer: 128 * 1024,
      });
      assert.ifError(result.error);
      assert.equal(result.signal, null, "validator did not terminate abnormally");
      if (expectedValid) assert.equal(result.status, 0, result.stdout + result.stderr);
      else {
        assert.notEqual(result.status, 0, "invalid ownership must fail validation");
        assert.ok((result.stdout + result.stderr).trim(), "rejection has a diagnostic");
      }
      passed++; console.log("PASS " + name);
    } catch (error) { failed++; console.error("FAIL " + name + "\n" + error.stack); }
  }
  try {
    cases.forEach(([name, data, valid], i) => {
      const file = path.join(temporary, `fixture-${i}.json`);
      fs.writeFileSync(file, JSON.stringify(data));
      check(name, file, valid);
    });
    const invalidJson = path.join(temporary, "malformed.json");
    fs.writeFileSync(invalidJson, '{ "articles": [');
    check("malformed JSON is rejected with a diagnostic", invalidJson, false);
    check("actual manifest has valid slug/alias ownership", path.join(root, "data/articles/manifest.json"), true);
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
  console.log(`${passed} passed; ${failed} failed`);
  if (failed) process.exitCode = 1;
}
