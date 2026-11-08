#!/bin/sh
# Build and commit Gītā chapter readers onto origin/main in a clean worktree; never push.
#
#   sh scripts/deploy_gita_chapter.sh N "commit message"
#   sh scripts/deploy_gita_chapter.sh "2 3 4" "commit message" [--whole-gita]
#
# docs/GITA_CH12_PIPELINE_AUDIT.md §5.8, amended 2026-11-08 (lead): the working tree is shared with
# other agents and holds their uncommitted edits, so the real build happens in the worktree, never
# in the working tree (which only ever runs the builder with --check-only):
#   1. origin/main is fetched over HTTPS with `gh auth git-credential` (no SSH keys here) into a new
#      detached worktree at <tmp>/vedanta-timeline, beside a `prakriya` link, so evidence loci resolve;
#   2. the term policy and, per chapter, the builder's inputs (internal/sanskrit_reviews/gita/chN:
#      packet.json, producer-*.json, independent-review-*.json) and the recitation files
#      (gita/chN/audio.js, recitation.mp3) are copied in;
#   3. the working tree's builder (scripts/build_gita_chapter_reader.py N --root <worktree>) builds
#      each chapter there, fail-closed, and registers it in the worktree's assets/app.js and
#      data/articles/manifest.json (status "provisional" for a new entry: rule D-3);
#   4. with --whole-gita, scripts/gita/build_whole_gita.py writes gita/bhagavad-gita/ and registers
#      the one-article reader there;
#   5. the builder's private outputs under internal/ are removed (tracked ones restored);
#      scripts/run_checks.sh runs inside the worktree, on exactly what would be pushed;
#   6. paths are staged by name, any other staged path is refused, one commit is made with the
#      message given, and the push command is printed for the lead. The worktree is kept.
# apparatus.json is committed only if the registration loads it (D-2).
#
# Test hooks: DEPLOY_REMOTE_URL (fetch/push URL instead of origin's), DEPLOY_SKIP_BUILD=1 (copy the
# working tree's gita/chN/verses.js and index.html instead of building; register with
# --register-only), DEPLOY_CHECKS (command run in the worktree instead of `sh scripts/run_checks.sh`).
set -eu

die() { printf 'deploy: %s\n' "$*" >&2; exit 1; }

[ $# -ge 2 ] && [ $# -le 3 ] || die "usage: sh scripts/deploy_gita_chapter.sh \"N [N …]\" \"commit message\" [--whole-gita]"
CHAPTERS=$(printf %s "$1" | tr ',' ' ')
MSG=$2
WHOLE=0
if [ $# -eq 3 ]; then
    [ "$3" = "--whole-gita" ] || die "unknown option: $3"
    WHOLE=1
fi
[ -n "$CHAPTERS" ] || die "no chapter given"
for N in $CHAPTERS; do
    case "$N" in ''|*[!0-9]*) die "chapter must be a number: $N" ;; esac
done
[ -n "$MSG" ] || die "commit message is empty"

REPO=$(git rev-parse --show-toplevel)
cd "$REPO"
ORIGIN_URL=${DEPLOY_REMOTE_URL:-$(git remote get-url origin)}
case "$ORIGIN_URL" in
    git@github.com:*) URL="https://github.com/${ORIGIN_URL#git@github.com:}" ;;
    ssh://git@github.com/*) URL="https://github.com/${ORIGIN_URL#ssh://git@github.com/}" ;;
    *) URL=$ORIGIN_URL ;;
esac
git_https() { git -c credential.helper= -c 'credential.helper=!gh auth git-credential' "$@"; }

[ -f data/glossary/term_policy.json ] || die "data/glossary/term_policy.json missing"
POLICY_SHA=$(python3 scripts/build_gita_chapter_reader.py --policy-hash)

# 1. clean worktree at origin/main, named vedanta-timeline beside a prakriya link
git_https fetch --quiet "$URL" main || die "fetch of $URL main failed"
BASE=$(git rev-parse FETCH_HEAD)
DIR=$(mktemp -d "${TMPDIR:-/tmp}/gita-deploy.XXXXXX")
TMP="$DIR/vedanta-timeline"
git worktree add --quiet --detach "$TMP" "$BASE" || die "cannot create worktree at $TMP"
[ -d "$REPO/../prakriya" ] && ln -s "$(cd "$REPO/.." && pwd)/prakriya" "$DIR/prakriya"

# 2–3. inputs, then the build (or, under DEPLOY_SKIP_BUILD, the working tree's built files)
mkdir -p "$TMP/data/glossary"
cp data/glossary/term_policy.json "$TMP/data/glossary/term_policy.json"
EXPECT="data/glossary/term_policy.json assets/app.js data/articles/manifest.json"
for N in $CHAPTERS; do
    OWN="gita/ch$N"
    IN="internal/sanskrit_reviews/gita/ch$N"
    mkdir -p "$TMP/$OWN" "$TMP/$IN"
    for f in audio.js recitation.mp3; do
        [ -f "$OWN/$f" ] && cp "$OWN/$f" "$TMP/$OWN/$f"
    done
    if [ "${DEPLOY_SKIP_BUILD:-0}" = 1 ]; then
        for f in verses.js index.html; do
            [ -f "$OWN/$f" ] || die "$OWN/$f missing (DEPLOY_SKIP_BUILD copies the working tree's build)"
            cp "$OWN/$f" "$TMP/$OWN/$f"
        done
        python3 scripts/build_gita_chapter_reader.py "$N" --register-only --root "$TMP" || die "registration of chapter $N failed in $TMP"
    else
        [ -f "$IN/packet.json" ] || die "$IN/packet.json missing"
        ls "$IN"/producer-*.json >/dev/null 2>&1 || die "$IN has no producer shards"
        cp "$IN/packet.json" "$TMP/$IN/"
        cp "$IN"/producer-*.json "$TMP/$IN/"
        cp "$IN"/independent-review-*.json "$TMP/$IN/" 2>/dev/null || true
        python3 scripts/build_gita_chapter_reader.py "$N" --root "$TMP" || die "the builder refused chapter $N in $TMP (worktree kept)"
    fi
    for f in verses.js index.html audio.js recitation.mp3; do
        [ -f "$TMP/$OWN/$f" ] && EXPECT="$EXPECT $OWN/$f"
    done
    if [ -f "$TMP/$OWN/apparatus.json" ] && grep -q "\"gita-ch$N\"[^}]*apparatus.json" "$TMP/assets/app.js"; then
        EXPECT="$EXPECT $OWN/apparatus.json"
    fi
done

# 4. the whole-Gītā article
if [ "$WHOLE" = 1 ]; then
    python3 scripts/gita/build_whole_gita.py --root "$TMP" --register || die "whole-Gītā article failed in $TMP"
    EXPECT="$EXPECT gita/bhagavad-gita/index.html gita/bhagavad-gita/reader.js gita/bhagavad-gita/chapters.js"
fi

# 5. drop the builder's private outputs, then the repository's checks on exactly what would be pushed
(cd "$TMP" && git checkout --quiet -- internal 2>/dev/null; git clean -fdq -- internal) || die "cannot clean internal/ in $TMP"
if [ -n "${DEPLOY_CHECKS:-}" ]; then
    (cd "$TMP" && sh -c "$DEPLOY_CHECKS") || die "checks failed in $TMP (worktree kept for inspection)"
else
    (cd "$TMP" && sh scripts/run_checks.sh) || die "scripts/run_checks.sh failed in $TMP (worktree kept for inspection)"
fi

# 6. stage by path, refuse anything else, commit
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
[ -z "$UNSTAGED" ] || die "the build or the checks left other changes in the worktree:
$UNSTAGED"
git diff --cached --quiet && die "nothing to commit: chapter(s) $CHAPTERS on origin/main already identical"
git diff --cached --stat
git commit --quiet -m "$MSG" || die "commit failed"
HEAD_SHA=$(git rev-parse HEAD)

printf '\nCommitted %s (chapters %s%s) on top of origin/main %s (policy %s) in %s\n' "$HEAD_SHA" "$CHAPTERS" \
    "$([ "$WHOLE" = 1 ] && printf ' + whole-Gītā article')" "$BASE" "$(printf %s "$POLICY_SHA" | cut -c1-12)" "$TMP"
printf 'Not pushed. To publish:\n'
printf "  git -C '%s' -c credential.helper= -c 'credential.helper=!gh auth git-credential' push '%s' HEAD:main\n" "$TMP" "$URL"
printf "  git -C '%s' worktree remove '%s'\n" "$REPO" "$TMP"
