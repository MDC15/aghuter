# Long command refactor workflow

1. Preserve the original command and identify its intended outcome.
2. Identify shell-specific syntax, operators, redirections, substitutions, quoting, and working-directory assumptions.
3. Split it into logical stages and document data flow and failure behavior.
4. Determine whether a native agent tool, API, project script, or structured argv is clearer.
5. Propose a semantically equivalent readable alternative; call out any behavior changes.
6. Review risk and approval requirements before execution.
7. Compare outcomes and report what was changed or not verified.
