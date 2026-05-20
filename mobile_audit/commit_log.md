# Commit log — forensic record of polluted commits

Auto-maintained note when a commit's message does not match its diff. Recovery convention defined in `AGENTS.md` § Recovery.

## 2026-05-19 — concurrent-agent sweep

Four agents (UI pass: search-popover + dark theme + click-bounce + glossary regex; content pass: Sāṅkhya rename + stub audit; song page: drag-to-seek + lyrics polish; karaoke timings) ran in parallel without an `AGENTS.md` scope rule. The song-page agent ran `git add -A` and swept everyone's uncommitted work into its own commits with song-page-themed messages. Working tree was clean post-push and the live site deployed correctly; only the git log is misleading.

| SHA | Wrong message | Actually contains |
|---|---|---|
| `f21d34e` | "Song: final polish — English closer in size to roman, player seamless with body, ×N badge fully legible" | Sāṅkhya rename across `data/articles/source/sankhya-anirban.md`, file renames `data/polemic_chains/brahma-sutra-bhasya-samkhya-refutation.json → -sankhya-refutation.json` and `data/thinkers/gaudapada-samkhya.json → gaudapada-sankhya.json`, `data/citation_index.json` + `data/primary_text_manifest.json` regen, 175 lines of `assets/style.css` dark-theme work, 206 lines of `assets/app.js` UI pass, `docs/_audit_data/quality_audit_v2.tsv`, `scripts/build_site_sources.py` rebuild — plus the song-page typography polish that the message actually describes |
| `28c5ab3` | "Song page: drag-to-seek on the player + centered lyrics" | 32 mobile-audit screenshots under `mobile_audit/screenshots/2026-05-19-pass2/` (4 viewports × 2 themes × 4 shots), `mobile_audit/screenshot_pass2.py` Playwright script, `mobile_audit/2026-05-19_fixes.md` UI-pass diagnosis log, dark-theme palette additions, search-popover relocation, click-bounce fix in `assets/style.css` `.thinker-dot` z-index gating — plus the drag-to-seek + centered-lyrics work the message actually describes |
| `199727b` | "Content: audit list of stub-emitting paths and genuinely-missing translations" | Correctly named. The content agent's stub-audit list. |
| `c21dca5` | "Song: drop English italics, remove time numbers from player" | Likely correct (song-only). Spot-check before relying on it. |

**Going forward**: `AGENTS.md` is now in place. New agents reading the repo will scope-stage and commit their own logical change. Do not rewrite the polluted history above; it will mislead future bisects, but force-pushing `main` is worse.

**If you need to bisect across this range**: use `git log -- <path>` filtered by file, not commit subjects.
