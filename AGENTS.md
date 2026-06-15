# Agent Working Rules — vedanta-timeline

Multiple Claude/Codex agents may operate on this repo concurrently. The rules below exist because we have already lost commit-message fidelity once (2026-05-19): a song-page agent ran `git add -A` and swept four other agents' uncommitted work (Sāṅkhya rename, dark theme, search-popover relocation, glossary regex extension) into commits titled "Song page: drag-to-seek" and "Song: final polish — English closer in size to roman." Working tree was clean and the site deployed correctly, but the git log no longer reflects which logical change is in which physical commit.

These rules prevent the recurrence.

## How we translate Sanskrit

All Sanskrit on this site — root text **and** commentary — is translated and
presented per **`docs/SANSKRIT_TRANSLATION_STANDARD.md`**: literal and faithful to
the grammar, **word-by-word interactive** (tap a word for its morpheme-by-morpheme
translation + grammar + glossary link), bidirectional highlight, voice-by-voice
commentary, IAST on screen (Devanāgarī kept in data), and integrated with the
site glossary. Reference implementation: `gita/sthitaprajna/` + `assets/gita.js`
(`window.GitaReader`). Follow this standard for any new Sanskrit text.

## Hard rules

1. **Stage by path, never by wildcard.** Do not run `git add -A`, `git add .`, `git add -u`, or `git commit -a`. Stage the specific files you changed: `git add path/to/file1 path/to/dir/file2`. If you do not know which files are yours, run `git diff --name-only` *before* you start and again before you commit; the delta is your scope.

1a. **Verify the staged diff before committing.** Even after `git add <file>`, another agent's unstaged edits to that same file get caught in your commit. Run `git diff --cached` immediately before `git commit` and confirm the diff only contains your scope. If it contains other agents' work, **`git restore --staged <file>` and break your edits out into a path-scoped patch** (e.g. apply your changes to a separate working copy, or use `git add -p` to interactively pick only your hunks). The 2026-05-19 dark-theme commit (`00fde3a`) bundled the search-merge agent's `.search-popover` deletion alongside the dark-theme rewrite because this check was skipped.

2. **Commit your own scope, do not adopt other agents' uncommitted work.** If `git status` shows modifications outside your scope at commit time, those belong to another agent. Do not stage them. Do not stash them blindly either — the other agent may be mid-edit. Leave them alone.

3. **One coherent logical change per commit.** Commit messages must accurately describe the diff. If your changes span two unrelated logical units, write two commits.

4. **Pull before push, push immediately after commit.** Rebase any local commits onto `origin/main` (`git pull --rebase origin main`) before pushing. Do not let local commits accumulate; the longer you sit on local commits, the more likely another agent has already pushed.

5. **Never force-push to `main`.** History on `main` is shared. Even when a commit message is wrong, leave it — see the recovery section.

6. **Do not edit files outside your declared scope.** If you discover a bug in another scope while reading code, file it as an issue or note it in `mobile_audit/issues_seen/` rather than fixing it in your commit.

## Scope conventions

Agents are expected to declare a scope before they start. Typical scopes:

- **Content / data** — touches `data/`, `docs/`, `scripts/`, `README.md`, content-side audit files. Does not touch `assets/`, `index.html`, or `mobile_audit/screenshots/`.
- **UI / UX** — touches `index.html`, `assets/app.js`, `assets/style.css`, `assets/song.js` (only the UI of the song page, not its lyrics data), `mobile_audit/`.
- **Song page** — touches `assets/song.js`, `assets/song.css`, `bhakti/`, the song's data files. Does not touch `index.html` (which is the timeline app's shell) or `assets/app.js` (timeline-app logic).
- **Audit / scripts** — touches `scripts/`, `audit/`, `tools/`. May read everything; only writes to its scope.

Cross-scope edits are allowed when genuinely necessary, but they must be called out in the commit message: `UI: dark-theme [+ content: 3 string fixes in data/glossary/]`.

## Working-directory hygiene

Before starting, run `git status` and `git diff --name-only`. Save the output mentally as your "pre-state." Anything outside that diff at commit time is foreign.

If you must stash to switch contexts, use a named stash: `git stash push -u -m "agent-A: <description>"`. Pop your *own* stash by name, never `git stash pop` blindly.

If you are running with the Bash sandbox restrictions and `git commit -a` looks tempting because individual paths trigger a prompt, **prompt the user instead.** Don't bypass scope by widening the stage.

## Commit message format

```
<scope>: <one-line summary of the actual diff>

<paragraph explaining why, if non-trivial>
```

Examples that are correct:
- `Content: rename Sāṃkhya → Sāṅkhya throughout editorial text`
- `UI: move glossary search from topbar into a popover with a summon button`
- `UI: dark theme — sun/moon toggle, CSS-variable palette, persisted in localStorage`
- `Song: drag-to-seek progress bar, centered lyrics column`

Examples that should never appear (real cases from 2026-05-19, do not repeat):
- "Song page: drag-to-seek on the player + centered lyrics" *with* a diff that touches `assets/style.css` dark-theme tokens, `data/articles/source/sankhya-anirban.md`, and 32 mobile-audit screenshots.
- "Song: final polish — English closer in size to roman" *with* a diff that renames `data/thinkers/gaudapada-samkhya.json → gaudapada-sankhya.json`.

## Recovery — what to do when you find a polluted commit

Do not rewrite history. Instead:

1. Add a clarifying note to `mobile_audit/commit_log.md` (the agent-maintained log of "what is actually in which commit when the message is wrong"). Format:
   ```
   - <sha> "<wrong message>" → actually contains: <real list of logical changes>
   ```
2. Make sure subsequent commits are correctly labeled.
3. If a future commit needs to reference a polluted predecessor, use the actual `git log -- <path>` data, not the commit subjects.

## Live site

The repo deploys to `https://vedanta.eeshan.xyz/` (alias of `https://balbudhi.github.io/vedanta-timeline/`) on every push to `main`. Verify HTTP 200 + spot-check your specific fix is visible after pushing. Auto-deploy takes ~30–90 seconds.

## Coordination signals

If you see another agent's modifications in `git status` and you need to commit, you have two options:

- **Wait** — finish reading, idle for 60 seconds, re-check `git status`. If the other agent is actively editing, files will keep changing.
- **Stash your own work, let the other agent finish, then re-apply** — `git stash push -u -m "<your-scope>"`, wait for the other agent's commit on `origin/main`, `git pull --rebase`, then `git stash pop`.

If you cannot determine whether files belong to you or another agent, **stop and ask the user.** Better to pause than to mis-attribute a diff.
