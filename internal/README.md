# internal/

Working material from the project's own construction: audit passes, methodology
drafts, mobile-layout investigations, and one-off tooling. It is kept in the
repository because several editorial decisions cite it as their record, and
because deleting the reasoning behind a decision makes the decision unreviewable.

It is **not** part of the site. The Pages build publishes an explicit allow-list
(`.github/workflows/deploy-pages.yml`); nothing here is served from
`vedanta.eeshan.xyz`.

| Directory | What it is |
|---|---|
| `mobile_audit/` | Responsive-layout audit passes, the issue list, and `commit_log.md` — the record of which logical change is actually in which commit when a commit message is wrong. Screenshots were dropped in 2026-08; `screenshot_pass2.py` and `screenshot_pass3.py` regenerate them. |
| `primitives_revision/`, `primitives_v2/` | Audit and rewrite record for the analytic-primitive framework. `primitives_revision/audit.md` is cited by `data/articles/source/primitive-graph.md`. |
| `scope_register_methodology/` | Execution reports for the scope/register taxonomy. The framework document itself lives in the local working corpus and is not mirrored here; the article references to it are therefore unresolved in this repository. |
| `kcb_investigation/` | Completion report for a Kant/K.C. Bhattacharyya acquisition pass. Retained as an acquisition record; the material it describes is not in this repository. |
| `tools/` | One-off glossary-wave scripts from a 2026-05 expansion. Repeatable, maintained checks live in `scripts/` instead. |
