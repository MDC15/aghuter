# Agent tool selection workflow

1. State the desired outcome and acceptance criteria.
2. Check available native tools/connectors and their permissions.
3. Compare native tool, project script, CLI, API/SDK on reliability, auditability, portability, auth, and output.
4. Select one primary path; avoid duplicate shell calls that repeat native-tool work.
5. Use CLI only for capabilities unavailable or materially worse through higher-level tools.
6. Explain approval boundaries and verify the final state.
