# Bash / POSIX shell guidance

- Prefer one clear command per logical action; avoid long `&&` chains when intermediate results need review.
- Quote expansions (`"$path"`), use `--` before path operands when supported, and avoid `eval`.
- Use arrays for argument lists in Bash; do not build commands by concatenating untrusted strings.
- Pipelines should have a clear data purpose. In Bash scripts, consider `set -o pipefail` when pipeline failure must be detected.
- Do not assume GNU flags on macOS/BSD. Check `command --help` or project docs.
