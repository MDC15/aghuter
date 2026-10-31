# Aghuter v0.3.1

Aghuter is a portable Agent Skill that helps coding agents translate human goals into concise, explainable, cross-platform workflows. It optimizes the *whole task* rather than blindly shortening shell strings.

## What it does

- Detects likely OS and shell (Windows, macOS, Linux; Bash, Zsh, POSIX sh, Fish, PowerShell, CMD).
- Guides hybrid selection: agent-native tools first, then project automation, authorized API/MCP/SDK, CLI, and reusable scripts.
- Explains and refactors long command sequences without silently changing semantics.
- Renders structured argument arrays for display in common shells; it never executes rendered commands.
- Provides a conservative risk heuristic and explicit approval boundaries.
- Includes workflow recipes and adapter guidance for Codex, Claude Code, GitHub Copilot, OpenCode, Cursor, and Gemini CLI.

## Quick start

Run from this directory:

```bash
python scripts/hcli.py list
python scripts/hcli.py plan cross-platform.command
python scripts/shell_detect.py --json
python scripts/command_optimize.py --shell powershell --argv-json '["git","status","--short"]'
python scripts/command_validate.py --argv-json '["git","push"]'
python scripts/workflow_lint.py
python -m unittest discover -s tests -v
```

On Windows, use `py` instead of `python` if that is how Python is installed.

## Install

Copy this folder into the skill directory recognized by your agent. Common project-level locations include:

- Codex: `.agents/skills/aghuter/`
- Claude Code: `.claude/skills/aghuter/`
- GitHub Copilot: `.github/skills/aghuter/` where Agent Skills are supported

For OpenCode, Cursor, and Gemini CLI, consult the adapter note and the current version's official documentation for the supported skill discovery path. Product support and paths can vary by release.

With the Skills CLI, from the project root after extracting this folder:

```bash
npx skills add ./aghuter --agent codex --copy
```

Check the CLI's current help for the exact supported agent identifiers and installation paths:

```bash
npx skills add --help
```

## Safety and limitations

- The bundled Python helpers are **non-executing**: they inspect, validate, explain, or render command text only.
- `command_optimize.py` renders an argv array for display. Prefer passing argv directly to a process API. CMD quoting is intentionally conservative and rejects ambiguous metacharacters.
- `command_validate.py` is a heuristic, not a sandbox, shell parser, authorization system, or security guarantee. It cannot reliably understand aliases, scripts, wrappers, substitutions, or every tool's behavior.
- The host coding agent remains responsible for execution, permissions, approval prompts, and policy enforcement.
- Never use the skill to bypass approvals, hide side effects, or expose secrets.

## Layout

- `SKILL.md`: shared behavior contract and workflow instructions.
- `scripts/`: non-executing helper utilities.
- `workflows/`: machine-readable catalogue and human playbooks.
- `references/`: shell syntax, hybrid selection, safety, optimization, and recovery guidance.
- `adapters/`: per-agent integration notes.
- `bin/`: thin launcher shims for the `hcli` helper (POSIX, CMD, PowerShell).
- `agents/openai.yaml`: agent manifest for OpenAI-compatible skill loaders.
- `examples/tasks.example.toml`: example task definitions.
- `tests/`: automated tests.

License: MIT. See `LICENSE`.
