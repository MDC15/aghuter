# Tool selection matrix

Choose the most reliable interface available for the task.

| Need | Preferred interface |
|---|---|
| Read/edit repository files | Agent-native file tools |
| Search code and symbols | Agent search tools, then `rg` if needed |
| Git status/diff/history | Git integration or read-only Git CLI |
| Tests/build/lint | Project-documented scripts via authorized terminal |
| Cloud provider / issue tracker / CI | Purpose-built API or connected integration |
| Repeated local workflow | Reviewed script with documented inputs and outputs |
| One-off system operation | CLI, split into explainable steps |

Do not choose an integration merely because it exists. Consider permissions, auditability, freshness, and whether it can safely perform the requested operation.
