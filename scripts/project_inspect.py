#!/usr/bin/env python3
"""Read-only project inventory for Aghuter; never runs project scripts."""
from __future__ import annotations
import argparse, json, os, subprocess
from pathlib import Path

MANIFESTS = {
    'package.json': 'JavaScript/TypeScript (inspect package manager from lockfiles)',
    'pyproject.toml': 'Python', 'requirements.txt': 'Python', 'Pipfile': 'Python',
    'Cargo.toml': 'Rust', 'go.mod': 'Go', 'Gemfile': 'Ruby',
    'pom.xml': 'Java/Maven', 'build.gradle': 'Java/Kotlin/Gradle',
    'composer.json': 'PHP', '.csproj': '.NET',
}
LOCKFILES = ['pnpm-lock.yaml', 'yarn.lock', 'package-lock.json', 'bun.lockb', 'bun.lock', 'uv.lock', 'poetry.lock', 'Pipfile.lock', 'Cargo.lock', 'go.sum']
GUIDANCE = ['AGENTS.md', 'CLAUDE.md', 'CONTRIBUTING.md', 'README.md']

def git(root: Path, *args: str) -> dict:
    try:
        p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, timeout=5, check=False)
        return {'available': True, 'exit_code': p.returncode, 'stdout': p.stdout.strip()[:5000], 'stderr': p.stderr.strip()[:1000]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'available': False, 'error': str(exc)}

def inspect(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f'Not a directory: {root}')
    present = [name for name in MANIFESTS if (root / name).is_file()]
    if (root / 'src').is_dir() and any(x.endswith('.csproj') for x in os.listdir(root)):
        present.append('.csproj')
    locks = [name for name in LOCKFILES if (root / name).exists()]
    guidance = [name for name in GUIDANCE if (root / name).is_file()]
    nested_guidance = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.venv', 'venv', 'vendor', 'dist', 'build'}]
        if 'AGENTS.md' in files and Path(base) != root:
            nested_guidance.append(str(Path(base).relative_to(root) / 'AGENTS.md'))
        if len(nested_guidance) >= 30:
            break
    package = None
    package_path = root / 'package.json'
    if package_path.is_file():
        try:
            data = json.loads(package_path.read_text(encoding='utf-8'))
            package = {'name': data.get('name'), 'package_scripts': sorted((data.get('scripts') or {}).keys())}
        except (OSError, json.JSONDecodeError):
            package = {'warning': 'package.json exists but could not be parsed'}
    return {
        'project_root': str(root), 'detected_ecosystems': sorted({MANIFESTS[x] for x in present if x in MANIFESTS}),
        'manifests': present, 'lockfiles': locks, 'guidance_files': guidance,
        'nested_agent_guidance': nested_guidance, 'package_json': package,
        'git_status': git(root, 'status', '--short', '--branch'),
        'policy': 'READ_ONLY: no project scripts, builds, tests, installs, or shell commands were executed.'
    }

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('path', nargs='?', default='.', help='Project directory (default: current directory)')
    ap.add_argument('--json', action='store_true', help='Print machine-readable JSON')
    args = ap.parse_args()
    try: result = inspect(Path(args.path))
    except ValueError as exc:
        ap.error(str(exc))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Project: {result['project_root']}")
        for key, label in [('detected_ecosystems','Ecosystems'),('manifests','Manifests'),('lockfiles','Lockfiles'),('guidance_files','Root guidance'),('nested_agent_guidance','Nested AGENTS.md')]:
            print(f"{label}: {', '.join(result[key]) or 'not found'}")
        if result['package_json']: print(f"Package scripts: {', '.join(result['package_json'].get('package_scripts', [])) or 'none'}")
        gs = result['git_status']; print('Git: ' + (gs.get('stdout') or 'not a Git worktree'))
        print(result['policy'])
    return 0
if __name__ == '__main__': raise SystemExit(main())
