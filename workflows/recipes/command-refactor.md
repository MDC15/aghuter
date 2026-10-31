# Refactor long command

Explain a long shell command and propose a clearer equivalent without silently changing semantics.

Risk classification: `approval-required`. This recipe is guidance, not execution authorization.

1. Parse logical stages, operators, quoting, redirection, and shell assumptions.
2. Compare native tools, API, project scripts, and structured argv.
3. Review proposed behavior and approval boundaries before execution.
4. Verify equivalence and report limitations.

Adapt every step to the live repository, detected shell, available tools, and approval policy. Verify results before reporting completion.
