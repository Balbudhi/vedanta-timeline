# Editorial workflow for agents

This is executable policy, not a prompt preference.

1. Before changing public intellectual content, read `data/editorial/authoring_contract.json` and the relevant primary witness.
2. Add or update a source record in `data/editorial/source_ledger.json` before writing new v1 claims. Give it a repo-local witness path and stable `cite://` prefix.
3. Run `node scripts/report_content_impacts.js --changed <source-path>`. Review every listed thinker and glossary entry; record a source-limit claim where the text cannot support a revision.
4. A v1 entry declares `editorial_contract: "v1"`, names its `source_record_ids`, and expresses public prose as ordered `intro_claims` or `definition_claims`. Each published claim has a status and a locus covered by the source ledger.
5. Run `scripts/preflight_content_change.sh <changed-paths>`, then the full validation suite. Do not make an interpretation simply because a citation namespace exists.
6. For UI work, verify the changed flow in the in-app Browser at desktop and mobile widths before publishing.

Install the local content gate for a clone with `git config core.hooksPath .githooks`. CI runs the contract validator independently; the hook is a fast local guard, not the only protection.
