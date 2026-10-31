#!/usr/bin/env python3
"""Aghuter helper. Plans and explains commands; never executes them."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "workflows" / "workflows.json"

READ_ONLY_PREFIXES = {
    ("pwd",), ("ls",), ("dir",), ("git", "status"), ("git", "diff"),
    ("git", "log"), ("git", "show"), ("git", "branch", "--show-current"),
    ("git", "rev-parse"), ("git", "ls-files"), ("git", "remote", "-v"),
    ("rg",), ("grep",), ("find",), ("head",), ("tail",), ("cat",),
    ("sed",), ("type",), ("where",), ("which",), ("file",), ("stat",),
}
DESTRUCTIVE_PREFIXES = {
    ("rm",), ("rmdir",), ("del",), ("erase",), ("mkfs",), ("dd",),
    ("shutdown",), ("reboot",), ("git", "reset"), ("git", "clean"),
    ("git", "push", "--force"), ("git", "push", "-f"),
    ("kubectl", "delete"), ("terraform", "destroy"),
}
EXTERNAL_PREFIXES = {
    ("git", "push"), ("git", "fetch"), ("git", "pull"),
    ("npm", "publish"), ("pnpm", "publish"), ("yarn", "publish"),
    ("docker", "push"), ("helm", "upgrade"), ("terraform", "apply"),
    ("curl",), ("wget",), ("ssh",), ("scp",),
}
LOCAL_WRITE_PREFIXES = {
    ("git", "add"), ("git", "commit"), ("git", "merge"),
    ("git", "rebase"), ("git", "checkout"), ("git", "switch"),
    ("npm", "install"), ("npm", "ci"), ("pnpm", "install"),
    ("yarn", "install"), ("pip", "install"), ("uv", "sync"),
    ("cargo", "build"), ("cargo", "fmt"), ("prettier", "--write"),
    ("black",), ("ruff", "format"),
}
SHELL_OPERATORS = {"&&", "||", ";", "|", "&"}


class CatalogError(Exception):
    pass


def load_catalog() -> Dict[str, Any]:
    try:
        data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CatalogError(f"Workflow catalogue not found: {CATALOG_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise CatalogError(f"Invalid JSON in workflow catalogue: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("workflows"), list):
        raise CatalogError("Catalogue must contain a 'workflows' array.")
    return data


def validate_catalog(data: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    seen_ids = set()
    for index, workflow in enumerate(data.get("workflows", [])):
        prefix = f"workflows[{index}]"
        if not isinstance(workflow, dict):
            errors.append(f"{prefix} must be an object")
            continue
        workflow_id = workflow.get("id")
        if not isinstance(workflow_id, str) or not workflow_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif workflow_id in seen_ids:
            errors.append(f"Duplicate workflow id: {workflow_id}")
        else:
            seen_ids.add(workflow_id)
        for field in ("title", "summary", "risk"):
            if not isinstance(workflow.get(field), str) or not workflow[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        if not isinstance(workflow.get("aliases", []), list):
            errors.append(f"{prefix}.aliases must be an array")
        steps = workflow.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{prefix}.steps must be a non-empty array")
            continue
        for step_index, step in enumerate(steps):
            step_prefix = f"{prefix}.steps[{step_index}]"
            if not isinstance(step, dict):
                errors.append(f"{step_prefix} must be an object")
                continue
            if step.get("kind") not in {"guidance", "command", "approval"}:
                errors.append(f"{step_prefix}.kind must be guidance, command, or approval")
            if not isinstance(step.get("purpose"), str) or not step["purpose"].strip():
                errors.append(f"{step_prefix}.purpose must be a non-empty string")
            if step.get("kind") == "command":
                argv = step.get("argv")
                if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) for arg in argv):
                    errors.append(f"{step_prefix}.argv must be a non-empty array of strings (not a shell string)")
                if step.get("risk") not in {"read-only", "local-write", "external", "destructive", "unknown"}:
                    errors.append(f"{step_prefix}.risk must be a recognized risk label")
    return errors


def index_workflows(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    lookup: Dict[str, Dict[str, Any]] = {}
    for workflow in data["workflows"]:
        for key in [workflow["id"], *workflow.get("aliases", [])]:
            normalized = str(key).strip().lower()
            if normalized in lookup:
                raise CatalogError(f"Duplicate workflow id/alias: {normalized}")
            lookup[normalized] = workflow
    return lookup


def render_list(data: Dict[str, Any]) -> str:
    lines = ["Aghuter workflows", ""]
    for workflow in data["workflows"]:
        aliases = ", ".join(workflow.get("aliases", []))
        suffix = f"  (aliases: {aliases})" if aliases else ""
        lines.append(f"{workflow['id']:<20} {workflow['title']}{suffix}")
        lines.append(f"{'':<20} {workflow['summary']}")
    lines.extend(["", "Use: hcli plan <workflow-id-or-alias>"])
    return "\n".join(lines)


def make_plan(workflow: Dict[str, Any]) -> Dict[str, Any]:
    steps = []
    for number, step in enumerate(workflow["steps"], start=1):
        item = {"number": number, "kind": step["kind"], "purpose": step["purpose"]}
        if "argv" in step:
            item["argv"] = step["argv"]
            item["risk"] = step.get("risk", "unknown")
        steps.append(item)
    return {
        "id": workflow["id"],
        "title": workflow["title"],
        "summary": workflow["summary"],
        "overall_risk": workflow["risk"],
        "execution_policy": "PLAN_ONLY: this helper never executes commands",
        "steps": steps,
    }


def render_plan(plan: Dict[str, Any]) -> str:
    lines = [plan["title"], "=" * len(plan["title"]), plan["summary"],
             f"Overall risk: {plan['overall_risk']}",
             "Mode: plan only — commands are displayed, never executed.", "", "Steps:"]
    for step in plan["steps"]:
        lines.append(f"{step['number']}. [{step['kind']}] {step['purpose']}")
        if "argv" in step:
            lines.append(f"   $ {shlex.join(step['argv'])}")
            lines.append(f"   Risk: {step['risk']}")
    return "\n".join(lines)


def split_shell_segments(command: str) -> List[Tuple[str, str]]:
    """Split only top-level-looking common separators; best-effort, not a shell parser."""
    segments: List[Tuple[str, str]] = []
    buf: List[str] = []
    quote = None
    escaped = False
    i = 0
    pending_operator = "start"
    while i < len(command):
        ch = command[i]
        if escaped:
            buf.append(ch)
            escaped = False
            i += 1
            continue
        if ch == "\\" and quote != "'":
            buf.append(ch)
            escaped = True
            i += 1
            continue
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            i += 1
            continue
        operator = None
        if command.startswith("&&", i) or command.startswith("||", i):
            operator = command[i:i + 2]
        elif ch in ";|&":
            operator = ch
        if operator:
            segment = "".join(buf).strip()
            if segment:
                segments.append((pending_operator, segment))
            pending_operator = operator
            buf = []
            i += len(operator)
            continue
        buf.append(ch)
        i += 1
    final_segment = "".join(buf).strip()
    if final_segment:
        segments.append((pending_operator, final_segment))
    return segments


def _matches_prefix(argv: Sequence[str], prefixes: set) -> bool:
    lower = tuple(arg.lower() for arg in argv)
    return any(len(lower) >= len(prefix) and lower[:len(prefix)] == prefix for prefix in prefixes)


def classify_command(argv: Sequence[str], raw: str) -> Tuple[str, str]:
    if not argv:
        return "unknown", "Could not identify a command."

    # Treat common privilege wrappers as a hint, but do not try to fully parse them.
    effective = list(argv)
    while effective and effective[0] in {"sudo", "command", "time"}:
        effective = effective[1:]
    if effective and effective[0] == "env":
        effective = effective[1:]
        while effective and "=" in effective[0] and not effective[0].startswith("-"):
            effective = effective[1:]
    if not effective:
        return "unknown", "Could not identify the command behind its wrapper."

    lower = [item.lower() for item in effective]
    note = ""
    has_redirection = any(marker in raw for marker in (">", "<", "<<"))
    has_expansion = any(marker in raw for marker in ("$(", "`", "<(", ">("))
    if has_redirection or has_expansion:
        note = "Shell redirection or expansion is present; review the full shell semantics. "

    if _matches_prefix(effective, DESTRUCTIVE_PREFIXES):
        return "destructive", note + "Likely destructive or hard to reverse; stop and confirm exact impact."
    if effective[0] == "find" and any(flag in lower for flag in ("-delete", "-exec", "-execdir")):
        return "unknown", note + "The find expression can perform arbitrary actions; inspect every predicate/action."
    if effective[0] == "git" and len(lower) > 1 and lower[1] == "branch" and "-d" in lower[2:]:
        return "local-write", note + "Likely deletes a local branch; inspect merged/unmerged state first."
    if effective[0] == "git" and len(lower) > 1 and lower[1] == "diff" and any(flag.startswith("--output") for flag in lower[2:]):
        return "local-write", note + "The diff output option writes to a file."
    if effective[0] in {"sed", "perl"} and any(flag in lower for flag in ("-i", "--in-place")):
        return "local-write", note + "In-place editing modifies files."
    if effective[0] in {"tee", "touch", "mkdir", "cp", "mv", "install", "patch"}:
        return "local-write", note + "Likely writes or changes local files."
    if has_redirection:
        return "unknown", note + "Redirection may write or truncate files; inspect the target and shell behavior."
    if _matches_prefix(effective, EXTERNAL_PREFIXES):
        return "external", note + "Likely contacts or changes a remote/external system."
    if _matches_prefix(effective, LOCAL_WRITE_PREFIXES):
        return "local-write", note + "Likely changes the local repository or environment."
    if _matches_prefix(effective, READ_ONLY_PREFIXES):
        return "read-only", note + "Commonly read-only, but flags and aliases can change behavior."
    return "unknown", note + "Effect not classified; inspect the command and its documentation before running."


def explain_command(command: str) -> Dict[str, Any]:
    segments = split_shell_segments(command)
    results = []
    for index, (operator, raw) in enumerate(segments, start=1):
        try:
            argv = shlex.split(raw, posix=True)
            parse_error = None
        except ValueError as exc:
            argv = []
            parse_error = str(exc)
        risk, explanation = classify_command(argv, raw)
        results.append({
            "number": index,
            "preceded_by": operator,
            "raw": raw,
            "argv_guess": argv,
            "risk_guess": risk,
            "explanation": explanation,
            "parse_error": parse_error,
        })
    warnings = ["Best-effort analysis only; this is not a full POSIX/PowerShell/CMD parser.",
                "No command was executed, modified, or rewritten."]
    if any(token in command for token in ("$(", "`", "<<", ">", "<(", ">(")):
        warnings.append("Command substitution, heredoc, redirection, or process substitution may change behavior; inspect it manually.")
    if "\n" in command:
        warnings.append("Multi-line shell input may contain constructs not represented by this segment breakdown.")
    return {"mode": "explain-only", "segments": results, "warnings": warnings}


def render_explanation(result: Dict[str, Any]) -> str:
    lines = ["Command breakdown (best effort)", "No command has been executed.", ""]
    for segment in result["segments"]:
        relation = "first command" if segment["preceded_by"] == "start" else f"after {segment['preceded_by']}"
        lines.append(f"{segment['number']}. {segment['raw']}")
        lines.append(f"   Relation: {relation}")
        lines.append(f"   Likely effect: {segment['risk_guess']} — {segment['explanation']}")
        if segment["parse_error"]:
            lines.append(f"   Parse note: {segment['parse_error']}")
    lines.append("\nCautions:")
    lines.extend(f"- {warning}" for warning in result["warnings"])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hcli", description="Aghuter: plan and explain; never execute shell commands.")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    subparsers.add_parser("list", help="List available workflow recipes")
    plan_parser = subparsers.add_parser("plan", help="Render a workflow without executing it")
    plan_parser.add_argument("workflow", help="Workflow ID or alias")
    plan_parser.add_argument("--format", choices=("text", "json"), default="text")
    explain_parser = subparsers.add_parser("explain", help="Explain a supplied command without executing it")
    explain_parser.add_argument("--command", required=True, help="Command text to inspect")
    explain_parser.add_argument("--format", choices=("text", "json"), default="text")
    subparsers.add_parser("validate", help="Validate the workflow catalogue")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        data = load_catalog()
        if args.subcommand == "validate":
            errors = validate_catalog(data)
            try:
                index_workflows(data)
            except CatalogError as exc:
                errors.append(str(exc))
            if errors:
                print("Catalogue validation failed:", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 1
            print(f"OK: {len(data['workflows'])} workflows validated. No commands are executed.")
            return 0
        if args.subcommand == "list":
            print(render_list(data))
            return 0
        if args.subcommand == "plan":
            workflow = index_workflows(data).get(args.workflow.strip().lower())
            if not workflow:
                print(f"Unknown workflow: {args.workflow}", file=sys.stderr)
                print("Run 'hcli list' to see available workflows.", file=sys.stderr)
                return 2
            plan = make_plan(workflow)
            print(json.dumps(plan, indent=2, ensure_ascii=False) if args.format == "json" else render_plan(plan))
            return 0
        if args.subcommand == "explain":
            result = explain_command(args.command)
            print(json.dumps(result, indent=2, ensure_ascii=False) if args.format == "json" else render_explanation(result))
            return 0
    except CatalogError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
