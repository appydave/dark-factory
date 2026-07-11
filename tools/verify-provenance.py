#!/usr/bin/env python3
"""Validate canonical/<type>/<name>/provenance.json against docs/provenance-spec.md
"Validation rules" (8 numbered rules, R1-R8) and the "recommended" field markers
in the same doc's field-rules table.

Exit codes: 0 = every checked artifact passes all 8 rules (an empty --all library
is not an error). 1 = at least one FAIL finding. 2 = usage/IO error.

R3 (verbatim_copy exists) and R4 (no orphan _source/ files) are directory-tolerant:
a verbatim_copy may name a directory (multi-file origins), and files under a
referenced directory count as referenced for R4 (provenance-spec.md "Verbatim
copy rules").
"""

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_TOP_FIELDS = [
    "canonical_id",
    "canonical_type",
    "canonical_name",
    "version",
    "rewrite_status",
    "rewrite_date",
    "rewrite_author",
    "origins",
    "version_history",
]

REQUIRED_ORIGIN_FIELDS = [
    "source_repo",
    "source_path",
    "harvested_at",
    "verbatim_copy",
    "kept",
    "modified",
    "set_aside",
]

VALID_STATUSES = {"draft", "in-style", "ratified"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CANONICAL_ID_RE = re.compile(r"^dark-factory:[^:]+:[^:]+$")


def load_provenance(artifact_dir):
    prov_path = artifact_dir / "provenance.json"
    text = prov_path.read_text()
    return json.loads(text)


def check_r2_required_fields(data):
    findings = []
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            findings.append(f"R2: missing required field {field}")
    origins = data.get("origins")
    if "origins" not in data:
        pass
    elif not isinstance(origins, list) or len(origins) == 0:
        findings.append("R2: origins must be a non-empty list")
    elif isinstance(origins, list):
        for i, origin in enumerate(origins):
            if not isinstance(origin, dict):
                findings.append(f"R2: origins[{i}] must be an object")
                continue
            for field in REQUIRED_ORIGIN_FIELDS:
                if field not in origin:
                    findings.append(f"R2: missing required field origins[{i}].{field}")
    if "version_history" in data and not isinstance(data["version_history"], list):
        findings.append("R2: version_history must be a list")
    return findings


def check_r3_verbatim_copy(data, artifact_dir):
    findings = []
    origins = data.get("origins")
    if not isinstance(origins, list):
        return findings
    for i, origin in enumerate(origins):
        if not isinstance(origin, dict) or "verbatim_copy" not in origin:
            continue
        verbatim_copy = origin["verbatim_copy"]
        if not isinstance(verbatim_copy, str):
            findings.append(f"R3: origins[{i}].verbatim_copy is not a path string")
            continue
        target = artifact_dir / verbatim_copy
        if not target.exists():
            findings.append(f"R3: origins[{i}].verbatim_copy does not exist: {verbatim_copy}")
    return findings


def check_r4_no_orphans(data, artifact_dir):
    findings = []
    source_dir = artifact_dir / "_source"
    if not source_dir.is_dir():
        return findings

    referenced_files = set()
    referenced_dirs = set()
    origins = data.get("origins")
    if isinstance(origins, list):
        for origin in origins:
            if not isinstance(origin, dict):
                continue
            verbatim_copy = origin.get("verbatim_copy")
            if not isinstance(verbatim_copy, str):
                continue
            target = artifact_dir / verbatim_copy
            if target.is_dir():
                referenced_dirs.add(target.resolve())
            else:
                referenced_files.add(target.resolve())

    for path in sorted(source_dir.rglob("*")):
        if path.is_dir():
            continue
        if path.name == ".DS_Store":
            continue
        resolved = path.resolve()
        if resolved in referenced_files:
            continue
        if any(_is_under(resolved, d) for d in referenced_dirs):
            continue
        rel = path.relative_to(artifact_dir)
        findings.append(f"R4: orphan file in _source/ not referenced by any origin: {rel}")
    return findings


def _is_under(path, directory):
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def check_r5_rewrite_status(data):
    if "rewrite_status" not in data:
        return []
    if data["rewrite_status"] not in VALID_STATUSES:
        return [f"R5: rewrite_status {data['rewrite_status']!r} not one of {sorted(VALID_STATUSES)}"]
    return []


def check_r6_version(data):
    if "version" not in data:
        return []
    version = data["version"]
    if type(version) is not int or version < 1:
        return [f"R6: version must be a positive integer, got {version!r}"]
    return []


def check_r7_version_history(data):
    if "version" not in data or "version_history" not in data:
        return []
    version = data["version"]
    if type(version) is not int or version < 1:
        return []
    history = data["version_history"]
    if not isinstance(history, list):
        return []
    expected = version - 1
    if len(history) != expected:
        return [f"R7: version_history has {len(history)} entries, expected {expected} (version {version})"]
    return []


def check_r8_kept(data):
    findings = []
    origins = data.get("origins")
    if not isinstance(origins, list):
        return findings
    for i, origin in enumerate(origins):
        if not isinstance(origin, dict):
            continue
        kept = origin.get("kept")
        if kept is not None and (not isinstance(kept, list) or len(kept) == 0):
            findings.append(f"R8: origins[{i}].kept is empty")
    return findings


def check_warnings(data):
    warnings = []
    origins = data.get("origins")
    if isinstance(origins, list):
        for i, origin in enumerate(origins):
            if not isinstance(origin, dict):
                continue
            if not origin.get("source_commit"):
                warnings.append(f"origins[{i}] missing recommended field source_commit")
            if not origin.get("source_url"):
                warnings.append(f"origins[{i}] missing recommended field source_url")
            harvested_at = origin.get("harvested_at")
            if isinstance(harvested_at, str) and not DATE_RE.match(harvested_at):
                warnings.append(f"origins[{i}].harvested_at is not YYYY-MM-DD: {harvested_at}")

    if "research_sources" not in data:
        warnings.append("missing recommended field research_sources")

    canonical_id = data.get("canonical_id")
    canonical_type = data.get("canonical_type")
    canonical_name = data.get("canonical_name")
    if isinstance(canonical_id, str):
        if not CANONICAL_ID_RE.match(canonical_id):
            warnings.append(f"canonical_id does not match dark-factory:<type>:<name>: {canonical_id}")
        elif canonical_type and canonical_name:
            expected = f"dark-factory:{canonical_type}:{canonical_name}"
            if canonical_id != expected:
                warnings.append(f"canonical_id {canonical_id!r} does not match dark-factory:<canonical_type>:<canonical_name>")

    rewrite_date = data.get("rewrite_date")
    if isinstance(rewrite_date, str) and not DATE_RE.match(rewrite_date):
        warnings.append(f"rewrite_date is not YYYY-MM-DD: {rewrite_date}")

    return warnings


def validate_artifact(artifact_dir):
    """Return (fail_lines, warn_lines) for one artifact dir, each already
    formatted minus the 'FAIL <dir> ' / 'WARN <dir> ' prefix's detail part."""
    try:
        data = load_provenance(artifact_dir)
    except json.JSONDecodeError as e:
        return ([f"R1: provenance.json does not parse as JSON: {e}"], [])

    fails = []
    fails += check_r2_required_fields(data)
    fails += check_r3_verbatim_copy(data, artifact_dir)
    fails += check_r4_no_orphans(data, artifact_dir)
    fails += check_r5_rewrite_status(data)
    fails += check_r6_version(data)
    fails += check_r7_version_history(data)
    fails += check_r8_kept(data)

    warns = check_warnings(data)
    return (fails, warns)


def run_validation(artifact_dirs):
    """Print findings for each artifact dir; return overall exit code (0 or 1)."""
    total = 0
    passed = 0
    any_fail = False
    for artifact_dir in artifact_dirs:
        total += 1
        fails, warns = validate_artifact(artifact_dir)
        for line in fails:
            # line already starts with "R<n>: detail"
            print(f"FAIL {artifact_dir} {line}")
        for line in warns:
            print(f"WARN {artifact_dir}: {line}")
        if fails:
            any_fail = True
        else:
            passed += 1
    print(f"checked {total} artifact(s): {passed} pass, {total - passed} fail")
    return 1 if any_fail else 0


def resolve_artifact_dirs(args_dirs):
    """Validate the named dirs exist and contain provenance.json. Returns Paths
    or None + prints an error (caller should exit 2)."""
    resolved = []
    for raw in args_dirs:
        d = Path(raw)
        if not d.is_dir():
            print(f"error: not a directory: {raw}", file=sys.stderr)
            return None
        if not (d / "provenance.json").is_file():
            print(f"error: no provenance.json found in: {raw}", file=sys.stderr)
            return None
        resolved.append(d)
    return resolved


def find_all_artifacts():
    canonical_dir = REPO_ROOT / "canonical"
    return sorted(canonical_dir.glob("*/*/provenance.json"))


# --- self-test -------------------------------------------------------------

def _write_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def _base_provenance():
    return {
        "canonical_id": "dark-factory:skill:demo",
        "canonical_type": "skill",
        "canonical_name": "demo",
        "version": 2,
        "rewrite_status": "in-style",
        "rewrite_date": "2026-07-06",
        "rewrite_author": "Claude (under direction)",
        "origins": [
            {
                "source_repo": "repo-a",
                "source_path": "/tmp/upstream/repo-a/skill.md",
                "source_commit": "main@abc1234",
                "source_url": "https://example.com/repo-a/skill.md",
                "harvested_at": "2026-07-06",
                "verbatim_copy": "_source/repo-a--skill.md",
                "kept": ["core mechanism"],
                "modified": ["voice"],
                "set_aside": [],
            },
            {
                "source_repo": "repo-b",
                "source_path": "/tmp/upstream/repo-b/bundle",
                "source_commit": "main@def5678",
                "source_url": "https://example.com/repo-b/bundle",
                "harvested_at": "2026-07-06",
                "verbatim_copy": "_source/repo-b--bundle",
                "kept": ["reference structure"],
                "modified": [],
                "set_aside": [],
            },
        ],
        "research_sources": {
            "distillation": "research/distillations/demo.md",
        },
        "version_history": [
            {
                "version": 1,
                "ratified_at": "2026-06-01",
                "superseded_at": "2026-07-06",
                "superseded_reason": "test fixture bump",
                "diff_summary": "n/a",
            }
        ],
    }


def _build_clean_artifact(base_dir):
    artifact_dir = base_dir / "clean"
    source_dir = artifact_dir / "_source"
    source_dir.mkdir(parents=True)
    (source_dir / "repo-a--skill.md").write_text("verbatim content a")
    bundle_dir = source_dir / "repo-b--bundle"
    bundle_dir.mkdir()
    (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
    refs_dir = bundle_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "notes.md").write_text("verbatim bundle notes")
    _write_json(artifact_dir / "provenance.json", _base_provenance())
    return artifact_dir


def self_test():
    tmp = Path(tempfile.mkdtemp(prefix="verify-provenance-selftest-"))
    results = []
    try:
        # 1. clean
        artifact_dir = _build_clean_artifact(tmp)
        fails, warns = validate_artifact(artifact_dir)
        results.append(("clean", len(fails) == 0, f"expected 0 FAIL, got {fails}"))

        # 2. r1-garbage
        artifact_dir = tmp / "r1-garbage"
        artifact_dir.mkdir()
        (artifact_dir / "provenance.json").write_text("{not json")
        fails, warns = validate_artifact(artifact_dir)
        rule_ids = {f.split(":")[0] for f in fails}
        results.append(("r1-garbage", rule_ids == {"R1"}, f"expected only R1, got {rule_ids}"))

        # 3. r2-missing-fields
        artifact_dir = tmp / "r2-missing-fields"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        data = _base_provenance()
        del data["rewrite_author"]
        del data["origins"][0]["set_aside"]
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        r2_fails = [f for f in fails if f.startswith("R2:")]
        has_author = any("rewrite_author" in f for f in r2_fails)
        has_set_aside = any("origins[0].set_aside" in f for f in r2_fails)
        ok = len(r2_fails) == 2 and has_author and has_set_aside and len(fails) == len(r2_fails)
        results.append(("r2-missing-fields", ok, f"expected exactly 2 R2 lines naming rewrite_author and origins[0].set_aside, got {fails}"))

        # 4. r3-missing-verbatim
        artifact_dir = tmp / "r3-missing-verbatim"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        data = _base_provenance()
        data["origins"][0]["verbatim_copy"] = "_source/repo-a--missing.md"
        del data["origins"][1]
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        rule_ids = {f.split(":")[0] for f in fails}
        results.append(("r3-missing-verbatim", "R3" in rule_ids, f"expected R3 present, got {fails}"))

        # 5. r4-orphan
        artifact_dir = tmp / "r4-orphan"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        (source_dir / "stray.md").write_text("unreferenced")
        _write_json(artifact_dir / "provenance.json", _base_provenance())
        fails, warns = validate_artifact(artifact_dir)
        r4_fails = [f for f in fails if f.startswith("R4:")]
        ok = len(r4_fails) >= 1 and any("stray.md" in f for f in r4_fails)
        results.append(("r4-orphan", ok, f"expected FAIL R4 naming stray.md, got {fails}"))

        # 6. r5-bad-status
        artifact_dir = tmp / "r5-bad-status"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        data = _base_provenance()
        data["rewrite_status"] = "final"
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        rule_ids = {f.split(":")[0] for f in fails}
        results.append(("r5-bad-status", "R5" in rule_ids, f"expected R5 present, got {fails}"))

        # 7. r6-zero
        artifact_dir = tmp / "r6-zero"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        data = _base_provenance()
        data["version"] = 0
        data["version_history"] = []
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        rule_ids = {f.split(":")[0] for f in fails}
        results.append(("r6-zero", "R6" in rule_ids, f"expected R6 present, got {fails}"))

        # 8. r6-bool
        artifact_dir = tmp / "r6-bool"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        data = _base_provenance()
        data["version"] = True
        data["version_history"] = []
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        rule_ids = {f.split(":")[0] for f in fails}
        results.append(("r6-bool", "R6" in rule_ids, f"expected R6 present (bool trap), got {fails}"))

        # 9. r7-history-mismatch
        artifact_dir = tmp / "r7-history-mismatch"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        data = _base_provenance()
        data["version"] = 3
        data["version_history"] = [data["version_history"][0]]
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        rule_ids = {f.split(":")[0] for f in fails}
        results.append(("r7-history-mismatch", "R7" in rule_ids, f"expected R7 present, got {fails}"))

        # 10. r8-empty-kept
        artifact_dir = tmp / "r8-empty-kept"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        data = _base_provenance()
        data["origins"][0]["kept"] = []
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        rule_ids = {f.split(":")[0] for f in fails}
        results.append(("r8-empty-kept", "R8" in rule_ids, f"expected R8 present, got {fails}"))

        # 11. warn-only
        artifact_dir = tmp / "warn-only"
        source_dir = artifact_dir / "_source"
        source_dir.mkdir(parents=True)
        (source_dir / "repo-a--skill.md").write_text("verbatim content a")
        bundle_dir = source_dir / "repo-b--bundle"
        bundle_dir.mkdir()
        (bundle_dir / "SKILL.md").write_text("verbatim bundle skill")
        (bundle_dir / "references").mkdir()
        (bundle_dir / "references" / "notes.md").write_text("verbatim bundle notes")
        data = _base_provenance()
        del data["research_sources"]
        for origin in data["origins"]:
            del origin["source_commit"]
            del origin["source_url"]
        _write_json(artifact_dir / "provenance.json", data)
        fails, warns = validate_artifact(artifact_dir)
        ok = len(fails) == 0 and len(warns) >= 1
        results.append(("warn-only", ok, f"expected 0 FAIL and >=1 WARN, got fails={fails} warns={warns}"))

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    ok_count = 0
    for name, passed, detail in results:
        if passed:
            print(f"ok {name}")
            ok_count += 1
        else:
            print(f"FAILED {name}: {detail}")

    print(f"self-test: {ok_count}/{len(results)} cases ok")
    return 0 if ok_count == len(results) else 1


# --- CLI ---------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(
        prog="verify-provenance.py",
        description="Validate provenance.json against docs/provenance-spec.md's 8 validation rules.",
    )
    parser.add_argument("artifact_dirs", nargs="*", help="artifact dir(s) containing provenance.json")
    parser.add_argument("--all", action="store_true", help="validate every canonical/*/*/provenance.json")
    parser.add_argument("--self-test", action="store_true", help="run the built-in fixture self-test")

    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if args.all:
        prov_files = find_all_artifacts()
        if not prov_files:
            print("no artifacts found under canonical/")
            return 0
        artifact_dirs = [p.parent for p in prov_files]
        return run_validation(artifact_dirs)

    if not args.artifact_dirs:
        parser.error("no artifact directory given (pass one or more dirs, or --all, or --self-test)")
        return 2  # unreachable; parser.error exits

    artifact_dirs = resolve_artifact_dirs(args.artifact_dirs)
    if artifact_dirs is None:
        return 2

    return run_validation(artifact_dirs)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
