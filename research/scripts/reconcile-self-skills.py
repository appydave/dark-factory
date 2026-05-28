#!/usr/bin/env python3
"""
Reconcile David's own skill inventory into research/artifacts.jsonl.

Three operations (all idempotent):
  1. Add 2 missing appydave-plugins skills (k-fleet, pr-lifecycle) created
     after the last recon scan.
  2. Mark grab-downloads as archived (moved to _archived/appydave-skills/),
     set status: archived, update file_path.
  3. Add ~/.claude/skills/ real directories (non-symlink) as a new
     provider: david-local. These are user-installed local skills that
     never went through the plugin pipeline.

Backs up artifacts.jsonl before writing. Safe to re-run.
"""
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path('/Users/davidcruwys/dev/ad/apps/dark-factory')
ARTIFACTS = REPO_ROOT / 'research/artifacts.jsonl'
BACKUP = REPO_ROOT / f'research/artifacts.jsonl.bak-{datetime.now():%Y%m%d-%H%M%S}'

APPYDAVE_PLUGINS = Path.home() / 'dev/ad/appydave-plugins'
GLOBAL_SKILLS = Path.home() / '.claude/skills'

TODAY = datetime.now().strftime('%Y-%m-%d')
SCAN_VERSION = '0.0.4-reconcile'


def parse_frontmatter(skill_md_path: Path) -> dict | None:
    try:
        text = skill_md_path.read_text()
    except Exception:
        return None
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return None
    fm_text = m.group(1)
    fm = {}
    current_key = None
    current_val = []
    for line in fm_text.split('\n'):
        m2 = re.match(r'^([a-zA-Z_-]+):\s*(.*)$', line)
        if m2 and not line.startswith(' '):
            if current_key:
                fm[current_key] = '\n'.join(current_val).strip().strip('"')
            current_key = m2.group(1)
            current_val = [m2.group(2)]
        elif current_key:
            current_val.append(line)
    if current_key:
        fm[current_key] = '\n'.join(current_val).strip().strip('"')
    return fm


def make_record(repo: str, artifact_type: str, name: str,
                file_path: Path, fm: dict) -> dict:
    desc = fm.get('description', '').strip()
    # description_normalized is a brief reduction — census will refine
    norm = desc[:240]
    return {
        'id': f'{repo}:{artifact_type}:{name}',
        'repo': repo,
        'file_path': str(file_path),
        'artifact_type': artifact_type,
        'name': name,
        'description_raw': desc,
        'description_normalized': norm,
        'discovered_at': TODAY,
        'discovered_by_version': SCAN_VERSION,
        'prompt_patterns_used': [],
        'cluster_facet': [],
        'frontmatter_yaml': {'name': name, 'description': desc},
    }


def main():
    records = []
    existing_ids = set()
    with open(ARTIFACTS) as f:
        for line in f:
            r = json.loads(line)
            records.append(r)
            existing_ids.add(r['id'])

    initial_count = len(records)
    print(f'Existing records: {initial_count}')

    shutil.copy2(ARTIFACTS, BACKUP)
    print(f'Backup written: {BACKUP.name}')

    added = []
    updated = []

    # 1. Missing appydave-plugins skills
    for name in ['k-fleet', 'pr-lifecycle']:
        skill_md = APPYDAVE_PLUGINS / 'appydave/skills' / name / 'SKILL.md'
        if not skill_md.exists():
            print(f'  ! skip {name}: file not found at {skill_md}')
            continue
        fm = parse_frontmatter(skill_md)
        if not fm:
            print(f'  ! skip {name}: no frontmatter')
            continue
        rid = f'appydave-plugins:skill:{name}'
        if rid in existing_ids:
            print(f'  = already present: {rid}')
            continue
        rec = make_record('appydave-plugins', 'skill', name, skill_md, fm)
        records.append(rec)
        existing_ids.add(rid)
        added.append(rid)

    # 2. Mark grab-downloads as archived
    archived_path = APPYDAVE_PLUGINS / '_archived/appydave-skills/grab-downloads/SKILL.md'
    for r in records:
        if r['id'] == 'appydave-plugins:skill:grab-downloads':
            if r.get('status') == 'archived':
                continue
            if archived_path.exists():
                r['file_path'] = str(archived_path)
            r['status'] = 'archived'
            r['archived_at'] = TODAY
            updated.append(r['id'])

    # 3. david-local: real (non-symlink) dirs in ~/.claude/skills/
    if GLOBAL_SKILLS.exists():
        for entry in sorted(GLOBAL_SKILLS.iterdir()):
            # is_symlink() check has to be on the unfollowed entry
            if entry.is_symlink() or not entry.is_dir():
                continue
            skill_md = entry / 'SKILL.md'
            if not skill_md.exists():
                continue
            name = entry.name
            fm = parse_frontmatter(skill_md)
            if not fm:
                print(f'  ! skip david-local/{name}: no frontmatter')
                continue
            rid = f'david-local:skill:{name}'
            if rid in existing_ids:
                continue
            rec = make_record('david-local', 'skill', name, skill_md, fm)
            records.append(rec)
            existing_ids.add(rid)
            added.append(rid)

    with open(ARTIFACTS, 'w') as f:
        for r in records:
            f.write(json.dumps(r) + '\n')

    print()
    print(f'Added: {len(added)}')
    for x in added:
        print(f'  + {x}')
    print()
    print(f'Updated: {len(updated)}')
    for x in updated:
        print(f'  ~ {x}')
    print()
    print(f'Total records: {len(records)}  (was {initial_count}, delta +{len(records)-initial_count})')


if __name__ == '__main__':
    main()
