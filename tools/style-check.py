#!/usr/bin/env python3
"""tools/style-check.py — automated ratification checklist.

Validates a canonical/ artifact (SKILL.md / AGENT.md / COMMAND.md) against the
checklist in docs/canonical-form-spec.md. Report-only — no auto-fix.

Checks:
  SC1  FAIL       frontmatter parses; name + description present, non-empty
  SC2  FAIL       name is kebab-case AND equals the artifact directory name
  SC3  WARN       argument-hint present
  SC4  FAIL/WARN  allowed-tools absent: FAIL if body has a bash/sh/shell/zsh
                  fenced block, else WARN
  SC5  FAIL       description is trigger-shaped ("use when" + >=3 triggers)
  SC6  FAIL       description is <=2 sentences
  SC7  FAIL       no marketing words anywhere in the file
  SC8  FAIL       no stack-specific terms in the body (suppressible via
                  <!-- stack-ok --> per line, or <!-- stack-ok: file --> for
                  the whole file — downgrades to WARN "SC8 suppressed")
  SC9  FAIL       body <=400 lines OR references/ has >=1 file
  SC10 FAIL       body has ## Anti-patterns AND (## Behavior or ## Modes)
  SC11 WARN       body has ## Output
  SC12 FAIL       provenance.json exists and is valid JSON (existence only —
                  content validation is tools/verify-provenance.py's job)
  SC13 FAIL       _source/ exists and contains >=1 file
  SC14 WARN       first non-blank line after the H1 is prose, not a
                  heading/table

Scope: this tool validates SKILL.md style + layout existence only.
provenance.json CONTENT validation (the 8 schema rules) is
tools/verify-provenance.py's job (T3-03) — out of scope here.

Usage:
  python3 tools/style-check.py <artifact-dir> [<artifact-dir> ...]
  python3 tools/style-check.py --all
  python3 tools/style-check.py --self-test
  python3 tools/style-check.py [...] --format json

Exit codes: 0 = pass (WARNs allowed), 1 = >=1 FAIL, 2 = usage error.
"""

import argparse
import json
import os
import re
import sys
import tempfile

PRIMARY_NAMES = ["SKILL.md", "AGENT.md", "COMMAND.md"]

MARKETING_WORDS = [
    "powerful", "comprehensive", "robust", "seamless", "seamlessly",
    "advanced", "intelligent", "cutting-edge", "state-of-the-art",
]

STACK_TERMS = [
    "npm", "npx", "yarn", "pnpm", "eslint", "prettier", "typescript", "tsc",
    "jest", "vitest", "pytest", "rubocop", "rspec", "bundler", "cargo",
    "rustc", "gradle", "maven", "webpack", "vite", "rails", "django",
    "flask", "react", "vue", "svelte", "next.js",
]

FAIL, WARN = "FAIL", "WARN"


def _word_re(word):
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(word) + r"(?![A-Za-z0-9_])", re.IGNORECASE)


def _marketing_re(word):
    # Leading boundary only, so adverb forms ("comprehensively") still flag —
    # marketing words are a heuristic seed, not exact-token matching.
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(word), re.IGNORECASE)


# ---------------------------------------------------------------------------
# Minimal frontmatter parser (stdlib-only; house style has zero third-party
# YAML-library imports as of 2026-07-06 — see Assumption 5 in the war game).
# ---------------------------------------------------------------------------

def _fold_block(lines, literal):
    if literal:
        return "\n".join(lines).rstrip("\n")
    paragraphs, current = [], []
    for line in lines:
        if line.strip() == "":
            if current:
                paragraphs.append(" ".join(current))
                current = []
        else:
            current.append(line.strip())
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(paragraphs).strip()


def parse_frontmatter(text):
    """Returns (data_dict_or_None, body_str). data is None if no/malformed frontmatter."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1:])

    data = {}
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val and val[0] in (">", "|"):
            literal = val[0] == "|"
            block, base_indent = [], None
            i += 1
            while i < len(fm_lines):
                nxt = fm_lines[i]
                if nxt.strip() == "":
                    block.append("")
                    i += 1
                    continue
                indent = len(nxt) - len(nxt.lstrip(" "))
                if base_indent is None:
                    base_indent = indent
                if indent < base_indent:
                    break
                block.append(nxt[base_indent:])
                i += 1
            data[key] = _fold_block(block, literal)
            continue
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        data[key] = val
        i += 1
    return data, body


def count_sentences(desc):
    masked = re.sub(r"'[^']*'|\"[^\"]*\"", lambda m: m.group(0).replace(".", ""), desc)
    return len(re.findall(r"\.(?=\s|$)", masked.strip()))


def find_primary_file(artifact_dir):
    return [n for n in PRIMARY_NAMES if os.path.isfile(os.path.join(artifact_dir, n))]


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_artifact(artifact_dir):
    findings = []
    name_dir = os.path.basename(os.path.normpath(artifact_dir))
    primary = find_primary_file(artifact_dir)[0]
    text = open(os.path.join(artifact_dir, primary), encoding="utf-8").read()
    data, body = parse_frontmatter(text)

    name = (data or {}).get("name", "").strip()
    description = (data or {}).get("description", "").strip()

    # SC1
    if data is None or not name or not description:
        findings.append(("SC1", FAIL, "frontmatter missing, or name/description empty"))

    # SC2
    if name:
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name) or name != name_dir:
            findings.append(("SC2", FAIL, f"name {name!r} must be kebab-case and match directory name {name_dir!r}"))

    # SC3
    if not (data or {}).get("argument-hint", "").strip():
        findings.append(("SC3", WARN, "argument-hint missing (omit-if-none, but note it)"))

    # SC4
    allowed_tools = (data or {}).get("allowed-tools", "").strip()
    has_bash_fence = bool(re.search(r"```\s*(bash|sh|shell|zsh)\b", body, re.IGNORECASE))
    if not allowed_tools:
        if has_bash_fence:
            findings.append(("SC4", FAIL, "allowed-tools missing while body has a bash/sh/shell/zsh fenced block"))
        else:
            findings.append(("SC4", WARN, "allowed-tools missing"))

    # SC5
    if description:
        if "use when" not in description.lower():
            findings.append(("SC5", FAIL, "description does not contain 'use when'"))
        else:
            quoted = re.findall(r"'[^']+'|\"[^\"]+\"", description)
            if quoted:
                trigger_count = len(quoted)
            else:
                m = re.search(r"use when\s*:?\s*(.*)", description, re.IGNORECASE)
                clause = re.split(r"\.(?=\s|$)", m.group(1))[0] if m else ""
                trigger_count = len([p for p in clause.split(",") if p.strip()])
            if trigger_count < 3:
                findings.append(("SC5", FAIL, f"description has only {trigger_count} trigger phrase(s), need >=3"))

    # SC6
    if description:
        sentences = count_sentences(description)
        if sentences > 2:
            findings.append(("SC6", FAIL, f"description has {sentences} sentences, must be <=2"))

    # SC7
    hits = [w for w in MARKETING_WORDS if _marketing_re(w).search(text)]
    if hits:
        findings.append(("SC7", FAIL, "marketing word(s) found: " + ", ".join(hits)))

    # SC8
    whole_file_suppressed = bool(re.search(r"<!--\s*stack-ok\s*:\s*file\s*-->", body, re.IGNORECASE))
    unsuppressed_hit, suppressed_hit = None, None
    for line in body.split("\n"):
        line_suppressed = whole_file_suppressed or bool(re.search(r"<!--\s*stack-ok\s*-->", line, re.IGNORECASE))
        for term in STACK_TERMS:
            if _word_re(term).search(line):
                if line_suppressed:
                    suppressed_hit = suppressed_hit or term
                else:
                    unsuppressed_hit = unsuppressed_hit or term
    if unsuppressed_hit:
        findings.append(("SC8", FAIL, f"stack-specific term {unsuppressed_hit!r} found in body"))
    elif suppressed_hit:
        findings.append(("SC8", WARN, f"SC8 suppressed (noted intentional exception: {suppressed_hit!r})"))

    # SC9
    body_lines = len(body.strip("\n").split("\n")) if body.strip() else 0
    references_dir = os.path.join(artifact_dir, "references")
    has_references = os.path.isdir(references_dir) and len(os.listdir(references_dir)) >= 1
    if body_lines > 400 and not has_references:
        findings.append(("SC9", FAIL, f"body is {body_lines} lines (>400) and no references/ dir"))

    # SC10
    has_anti = bool(re.search(r"^##\s+Anti-patterns\s*$", body, re.MULTILINE))
    has_behavior_or_modes = bool(re.search(r"^##\s+(Behavior|Modes)\s*$", body, re.MULTILINE))
    if not (has_anti and has_behavior_or_modes):
        findings.append(("SC10", FAIL, "missing ## Anti-patterns and/or ## Behavior / ## Modes"))

    # SC11
    if not re.search(r"^##\s+Output\s*$", body, re.MULTILINE):
        findings.append(("SC11", WARN, "## Output section missing"))

    # SC12
    prov_path = os.path.join(artifact_dir, "provenance.json")
    if not os.path.isfile(prov_path):
        findings.append(("SC12", FAIL, "provenance.json missing"))
    else:
        try:
            with open(prov_path, encoding="utf-8") as f:
                json.load(f)
        except (json.JSONDecodeError, OSError):
            findings.append(("SC12", FAIL, "provenance.json exists but is not valid JSON"))

    # SC13
    source_dir = os.path.join(artifact_dir, "_source")
    if not (os.path.isdir(source_dir) and len(os.listdir(source_dir)) >= 1):
        findings.append(("SC13", FAIL, "_source/ missing or empty"))

    # SC14
    h1 = re.search(r"^#\s+.+$", body, re.MULTILINE)
    if h1:
        rest = body[h1.end():].split("\n")
        next_line = next((l for l in rest if l.strip()), None)
        if next_line is not None and (next_line.lstrip().startswith("#") or next_line.lstrip().startswith("|")):
            findings.append(("SC14", WARN, "first non-blank line after H1 is a heading/table, not prose"))

    verdict = "fail" if any(level == FAIL for _, level, _ in findings) else "pass"
    return {
        "path": artifact_dir,
        "verdict": verdict,
        "findings": [{"id": i, "level": l, "message": m} for i, l, m in findings],
    }


# ---------------------------------------------------------------------------
# Discovery / CLI plumbing
# ---------------------------------------------------------------------------

def discover_all():
    dirs = []
    for kind in ("skills", "agents", "commands"):
        base = os.path.join("canonical", kind)
        if os.path.isdir(base):
            for entry in sorted(os.listdir(base)):
                full = os.path.join(base, entry)
                if os.path.isdir(full):
                    dirs.append(full)
    return dirs


def collect_reports(paths):
    results = []
    for p in paths:
        if not os.path.isdir(p):
            print(f"error: not a directory: {p}", file=sys.stderr)
            sys.exit(2)
        primaries = find_primary_file(p)
        if len(primaries) != 1:
            print(f"error: {p} must contain exactly one of {PRIMARY_NAMES}, found {primaries}", file=sys.stderr)
            sys.exit(2)
        results.append(check_artifact(p))
    return results


def render(results, fmt):
    overall = "fail" if any(r["verdict"] == "fail" for r in results) else "pass"
    if fmt == "json":
        print(json.dumps({"artifacts": results, "verdict": overall}))
    else:
        for r in results:
            for f in r["findings"]:
                print(f"{r['path']} {f['id']} {f['level']} {f['message']}")
            if not r["findings"]:
                print(f"{r['path']}: pass (no findings)")
        print(f"verdict: {overall}")
    return overall


# ---------------------------------------------------------------------------
# --self-test — fixture suite (canonical/ has zero real artifacts today)
# ---------------------------------------------------------------------------

GOOD_SKILL_MD = """---
name: good-skill
description: Use when 'review this code', 'check for bugs', or 'is this ready to merge'.
argument-hint: "[pr-url]"
allowed-tools: Read, Grep
---

# Good Skill

Reviews changes and reports findings in operator voice.

## Behavior

Read the diff. Report findings, most severe first.

## Output

A findings list: file, line, and one-sentence description per finding.

## Anti-patterns

- Don't skip verification.
- Don't auto-fix silently.
"""

BAD_FRONTMATTER_MD = """---
name: bad-frontmatter
argument-hint: "[none]"
allowed-tools: Read
---

# Bad Frontmatter

Missing the description field entirely.

## Behavior

Do a thing.

## Output

A thing.

## Anti-patterns

- Don't do this.
"""

BAD_DESCRIPTION_MD = """---
name: bad-description
description: This skill will read all the comments, decide which are valid, then fix them.
argument-hint: "[none]"
allowed-tools: Read
---

# Bad Description

A workflow-summary description that never says "use when".

## Behavior

Do the workflow.

## Output

A patch.

## Anti-patterns

- Don't summarize the workflow in the description.
"""

BAD_MARKETING_MD = """---
name: bad-marketing
description: Use when 'reviewing pull requests', 'auditing code quality', or 'checking style compliance'.
argument-hint: "[none]"
allowed-tools: Read
---

# Bad Marketing

A comprehensive and powerful review process.

## Behavior

Do the review.

## Output

A report.

## Anti-patterns

- Don't skip steps.
"""

BAD_STACK_MD = """---
name: bad-stack
description: Use when 'running the test suite', 'checking build status', or 'validating the pipeline'.
argument-hint: "[none]"
allowed-tools: Read
---

# Bad Stack

Runs the project's test command.

## Behavior

Run `npm test` to check tests pass.

## Output

A pass/fail summary.

## Anti-patterns

- Don't hardcode the package manager.
"""

STACK_OK_SUPPRESSED_MD = """---
name: stack-ok-suppressed
description: Use when 'running the test suite', 'checking build status', or 'validating the pipeline'.
argument-hint: "[none]"
allowed-tools: Read
---

# Stack Ok Suppressed

Runs the project's test command, with a noted intentional exception.

## Behavior

Run `npm test` to check tests pass. <!-- stack-ok -->

## Output

A pass/fail summary.

## Anti-patterns

- Don't hardcode the package manager.
"""

BAD_LAYOUT_MD = """---
name: bad-layout
description: Use when 'checking layout', 'auditing artifact structure', or 'validating provenance existence'.
argument-hint: "[none]"
allowed-tools: Read
---

# Bad Layout

Missing provenance.json and any verbatim source copies.

## Behavior

Check the artifact directory contents.

## Output

A layout report.

## Anti-patterns

- Don't ship without provenance.
"""

BAD_SECTIONS_MD = """---
name: bad-sections
description: Use when 'checking section headers', 'auditing body structure', or 'validating template shape'.
argument-hint: "[none]"
allowed-tools: Read
---

# Bad Sections

Missing the Anti-patterns section entirely.

## Behavior

Check the body headings.

## Output

A section report.
"""


def _make_fixture(base, name, skill_md, provenance=True, source_files=("origin.md",)):
    d = os.path.join(base, name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)
    if provenance:
        with open(os.path.join(d, "provenance.json"), "w", encoding="utf-8") as f:
            f.write("{}")
    src_dir = os.path.join(d, "_source")
    os.makedirs(src_dir, exist_ok=True)
    for fn in source_files:
        with open(os.path.join(src_dir, fn), "w", encoding="utf-8") as f:
            f.write("origin content\n")
    return d


def run_self_test():
    passed, total = 0, 0

    def check(label, cond):
        nonlocal passed, total
        total += 1
        print(f"self-test: {label}: {'ok' if cond else 'FAIL'}")
        if cond:
            passed += 1

    with tempfile.TemporaryDirectory() as tmp:
        def ids(r):
            return {f["id"] for f in r["findings"]}

        r = check_artifact(_make_fixture(tmp, "good-skill", GOOD_SKILL_MD))
        check("good verdict == pass", r["verdict"] == "pass")

        r = check_artifact(_make_fixture(tmp, "bad-frontmatter", BAD_FRONTMATTER_MD))
        check("bad-frontmatter verdict == fail", r["verdict"] == "fail")
        check("bad-frontmatter has SC1", "SC1" in ids(r))

        r = check_artifact(_make_fixture(tmp, "bad-description", BAD_DESCRIPTION_MD))
        check("bad-description verdict == fail", r["verdict"] == "fail")
        check("bad-description has SC5", "SC5" in ids(r))

        r = check_artifact(_make_fixture(tmp, "bad-marketing", BAD_MARKETING_MD))
        check("bad-marketing verdict == fail", r["verdict"] == "fail")
        check("bad-marketing has SC7", "SC7" in ids(r))

        r = check_artifact(_make_fixture(tmp, "bad-stack", BAD_STACK_MD))
        check("bad-stack verdict == fail", r["verdict"] == "fail")
        check("bad-stack has SC8", "SC8" in ids(r))

        r = check_artifact(_make_fixture(tmp, "stack-ok-suppressed", STACK_OK_SUPPRESSED_MD))
        check("stack-ok-suppressed verdict == pass", r["verdict"] == "pass")

        r = check_artifact(_make_fixture(tmp, "bad-layout", BAD_LAYOUT_MD, provenance=False, source_files=()))
        check("bad-layout verdict == fail", r["verdict"] == "fail")
        check("bad-layout has SC12", "SC12" in ids(r))
        check("bad-layout has SC13", "SC13" in ids(r))

        r = check_artifact(_make_fixture(tmp, "bad-sections", BAD_SECTIONS_MD))
        check("bad-sections verdict == fail", r["verdict"] == "fail")
        check("bad-sections has SC10", "SC10" in ids(r))

    print(f"self-test: {passed}/{total} passed")
    return passed == total


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="style-check.py",
        description=(
            "Automated ratification checklist (SC1-SC14) for canonical/ artifacts. "
            "provenance.json CONTENT validation is tools/verify-provenance.py's job."
        ),
        epilog=(
            "Modes:\n"
            "  style-check.py <artifact-dir> [<artifact-dir> ...]  check named artifacts\n"
            "  style-check.py --all                                scan canonical/{skills,agents,commands}/*/\n"
            "  style-check.py --self-test                          run the built-in fixture suite\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("artifact_dirs", nargs="*", help="artifact directories to check")
    parser.add_argument("--all", action="store_true", help="scan canonical/{skills,agents,commands}/*/")
    parser.add_argument("--self-test", action="store_true", help="run the built-in fixture self-test suite")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="output format")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        sys.exit(0 if run_self_test() else 1)

    if args.all:
        dirs = discover_all()
        if not dirs:
            if args.format == "json":
                print(json.dumps({"artifacts": [], "verdict": "pass"}))
            else:
                print("no artifacts found under canonical/ — nothing to check")
            sys.exit(0)
        results = collect_reports(dirs)
    else:
        if not args.artifact_dirs:
            parser.print_help()
            sys.exit(2)
        results = collect_reports(args.artifact_dirs)

    overall = render(results, args.format)
    sys.exit(0 if overall == "pass" else 1)


if __name__ == "__main__":
    main()
