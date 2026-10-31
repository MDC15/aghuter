#!/usr/bin/env python3
"""Strict structural checks for the Aghuter workflow catalogue."""
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'workflows' / 'workflows.json'
VALID_RISKS = {'read-only', 'local-execution', 'local-write', 'external', 'destructive', 'approval-required', 'read-only-unless-checks-execute', 'read-only-unless-audit-uses-network'}
VALID_KINDS = {'guidance', 'command', 'approval'}

def validate(data):
    errors, ids, aliases = [], set(), set()
    items = data.get('workflows') if isinstance(data, dict) else None
    if not isinstance(items, list) or not items: return ['workflows must be a non-empty array']
    for i, wf in enumerate(items):
        where = f'workflows[{i}]'
        if not isinstance(wf, dict): errors.append(f'{where} must be an object'); continue
        wid = wf.get('id')
        if not isinstance(wid, str) or not wid.strip(): errors.append(f'{where}.id is required')
        elif wid in ids: errors.append(f'duplicate workflow id: {wid}')
        else: ids.add(wid)
        for alias in wf.get('aliases', []):
            if alias in aliases: errors.append(f'duplicate alias: {alias}')
            aliases.add(alias)
        if wf.get('risk') not in VALID_RISKS: errors.append(f'{where}.risk is missing or unknown')
        steps = wf.get('steps')
        if not isinstance(steps, list) or not steps: errors.append(f'{where}.steps must be a non-empty array'); continue
        for j, step in enumerate(steps):
            loc = f'{where}.steps[{j}]'
            if step.get('kind') not in VALID_KINDS: errors.append(f'{loc}.kind is invalid')
            if step.get('kind') == 'command':
                argv = step.get('argv')
                if not isinstance(argv, list) or not argv or not all(isinstance(x, str) for x in argv): errors.append(f'{loc}.argv must be a non-empty string array')
                if step.get('risk') not in VALID_RISKS: errors.append(f'{loc}.risk is missing or unknown')
                if any(x in {'&&','||',';','|','>','>>','<'} for x in (argv or [])): errors.append(f'{loc}.argv must not encode shell operators')
    return errors

def main():
    try: data = json.loads(CATALOG.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc: print(f'FAIL: {exc}'); return 1
    errors = validate(data)
    if errors:
        print('\n'.join('FAIL: '+e for e in errors)); return 1
    print(f"OK: {len(data['workflows'])} workflows; unique IDs/aliases; valid step structures.")
    print('Policy: catalogue validation only; no workflow commands were executed.')
    return 0
if __name__ == '__main__': raise SystemExit(main())
