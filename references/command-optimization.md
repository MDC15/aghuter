# Command optimization principles

1. Optimize total task cost: tool calls, tokens, latency, failure recovery, and human review—not character count alone.
2. Prefer native structured tool calls and argument arrays over shell strings.
3. Batch read-only queries when the output remains understandable; separate actions with distinct side effects or approval boundaries.
4. Replace repeated complex shell fragments with a small tested script checked into the project only when reuse justifies it.
5. Preserve semantics. State any changed behavior, filters, ordering, error handling, or platform assumptions.
6. Keep output bounded: request machine-readable output where stable, filter at source, and summarize without discarding actionable errors.
7. Never claim a heuristic command renderer or risk classifier is a security boundary.
