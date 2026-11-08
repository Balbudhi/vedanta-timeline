#!/bin/sh
# Commit one Gītā chapter reader onto origin/main from a clean worktree; never push.
#
#   sh scripts/deploy_gita_chapter.sh N "commit message"
#
# docs/GITA_CH12_PIPELINE_AUDIT.md §5.8. The working tree is shared with other agents and
# holds their uncommitted edits, so nothing here pulls, rebases, stashes or stages in it:
#   1. the fail-closed builder runs in the working tree (it writes gita/chN/ only if every
#      check passes);
#   2. origin/main is fetched over HTTPS with `gh auth git-credential` (no SSH keys here)
#      into a new detached worktree;
#   3. only the chapter's own files and the term policy are copied into it, and the reader
#      registration is applied to that worktree's assets/app.js and data/articles/manifest.json
#      (`--register-only --root`, status "provisional" for a new entry: rule D-3);
#   4. scripts/run_checks.sh runs inside the worktree, on exactly what would be pushed;
#   5. paths are staged by name, any other staged path is refused, and the commit is made
#      with the message given;
#   6. the push command is printed for the lead. The worktree is kept for that push.
# apparatus.json is not copied (D-2: the reader does not load it).
#
# Test hooks: DEPLOY_REMOTE_URL (fetch/push URL instead of origin's), DEPLOY_SKIP_BUILD=1,
# DEPLOY_CHECKS (command run in the worktree instead of `sh scripts/run_checks.sh`).
set -eu

die() { printf 'deploy: %s\n' "$*" >&2; exit 1; }

[ $# -eq 2 ] || die "usage: sh scripts/deploy_gita_chapter.sh N \"commit message\""
N=$1
MSG=$2
case "$N" in ''|*[!0-9]*) die "chapter must be a number: $N" ;; esac
[ -n "$MSG" ] || die "commit message is empty"

REPO=$(git rev-parse --show-toplevel)
cd "$REPO"
OWN="gita/ch$N"

ORIGIN_URL=${DEPLOY_REMOTE_URL:-$(git remote get-url origin)}
case "$ORIGIN_URL" in
    git@github.com:*) URL="https://github.com/${ORIGIN_URL#git@github.com:}" ;;
    ssh://git@github.com/*) URL="https://github.com/${ORIGIN_URL#ssh://git@github.com/}" ;;
    *) URL=$ORIGIN_URL ;;
esac
git_https() { git -c credential.helper= -c 'credential.helper=!gh auth git-credential' "$@"; }

# 1. fail-closed build in the working tree
if [ "${DEPLOY_SKIP_BUILD:-0}" != 1 ]; then
    python3 scripts/build_gita_chapter_reader.py "$N" || die "the builder refused chapter $N; nothing deployed"
fi
[ -f "$OWN/verses.js" ] && [ -f "$OWN/index.html" ] || die "$OWN/verses.js and index.html must exist"
[ -f data/glossary/term_policy.json ] || die "data/glossary/term_policy.json missing"
POLICY_SHA=$(python3 scripts/build_gita_chapter_reader.py --policy-hash)

# 2. clean worktree at origin/main
git_https fetch --quiet "$URL" main || die "fetch of $URL main failed"
BASE=$(git rev-parse FETCH_HEAD)
TMP=$(mktemp -d "${TMPDIR:-/tmp}/gita-deploy-ch$N.XXXXXX")
git worktree add --quiet --detach "$TMP" "$BASE" || die "cannot create worktree at $TMP"

# 3. chapter scope only, then the registration
mkdir -p "$TMP/$OWN" "$TMP/data/glossary"
EXPECT=""
for f in verses.js index.html audio.js recitation.mp3; do
    if [ -f "$OWN/$f" ]; then
        cp "$OWN/$f" "$TMP/$OWN/$f"
        EXPECT="$EXPECT $OWN/$f"
    fi
done
cp data/glossary/term_policy.json "$TMP/data/glossary/term_policy.json"
python3 scripts/build_gita_chapter_reader.py "$N" --register-only --root "$TMP" || die "registration failed in $TMP"
EXPECT="$EXPECT data/glossary/term_policy.json assets/app.js data/articles/manifest.json"

# 4. the repository's checks, on exactly what would be pushed
if [ -n "${DEPLOY_CHECKS:-}" ]; then
    (cd "$TMP" && sh -c "$DEPLOY_CHECKS") || die "checks failed in $TMP (worktree kept for inspection)"
else
    (cd "$TMP" && sh scripts/run_checks.sh) || die "scripts/run_checks.sh failed in $TMP (worktree kept for inspection)"
fi

# 5. stage by path, refuse anything else, commit
cd "$TMP"
for f in $EXPECT; do
    [ -e "$f" ] && git add -- "$f"
done
for f in $(git diff --cached --name-only); do
    case " $EXPECT " in
        *" $f "*) ;;
        *) die "unexpected staged path: $f" ;;
    esac
done
UNSTAGED=$(git status --porcelain --untracked-files=all | grep -v '^[AM] ' || true)
[ -z "$UNSTAGED" ] || die "the checks left other changes in the worktree:
$UNSTAGED"
git diff --cached --quiet && die "nothing to commit: chapter $N on origin/main is already identical"
git diff --cached --stat
git commit --quiet -m "$MSG" || die "commit failed"
HEAD_SHA=$(git rev-parse HEAD)

# 6. the push is the lead's
printf '\nCommitted %s on top of origin/main %s (policy %s) in %s\n' "$HEAD_SHA" "$BASE" "$(printf %s "$POLICY_SHA" | cut -c1-12)" "$TMP"
printf 'Not pushed. To publish:\n'
printf "  git -C '%s' -c credential.helper= -c 'credential.helper=!gh auth git-credential' push '%s' HEAD:main\n" "$TMP" "$URL"
printf "  git -C '%s' worktree remove '%s'\n" "$REPO" "$TMP"
