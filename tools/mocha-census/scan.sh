#!/usr/bin/env bash
# mocha-census scanner — find every Mochaccino design page on a machine and emit one TSV row each.
# Runs locally or piped over ssh:  ssh host 'bash -s' < scan.sh -- <machine-label>
# Columns: machine \t kind \t root \t design_id \t path \t mtime \t title
# kind = source | build  (build = served/compiled copy under dist|public|client/dist — dedupe these)
set -euo pipefail
MACHINE="${1:-$(hostname -s)}"
ROOTDIR="${MOCHA_SCAN_ROOT:-$HOME/dev}"

find "$ROOTDIR" \
    \( -path '*/.mochaccino/designs/*/index.html' -o -path '*/mochaccino/designs/*/index.html' \) \
    -not -path '*/node_modules/*' -not -path '*/.claude/skills/*' -not -path '*/worktrees/*' \
    -not -path '*/designs/designs/*' 2>/dev/null |
while IFS= read -r f; do
  root="$(printf '%s' "$f" | sed -E 's#/(\.?mochaccino)/designs/.*#/\1#')"
  # design_id = full sub-path between designs/ and /index.html (handles nested e.g. components/foo)
  did="$(printf '%s' "$f" | sed -E 's#.*/designs/(.+)/index\.html#\1#')"
  case "$root" in
    */dist/*|*/public/*|*/client/dist/*) kind=build ;;
    *) kind=source ;;
  esac
  mt="$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)"
  title="$(grep -m1 -oE '<title>[^<]*' "$f" 2>/dev/null | sed 's/<title>//' | tr '\t\n' '  ')"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$MACHINE" "$kind" "$root" "$did" "$f" "$mt" "$title"
done
