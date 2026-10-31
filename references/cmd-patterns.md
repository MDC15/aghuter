# Windows CMD guidance

- CMD quoting and metacharacter rules are context-sensitive. Prefer PowerShell or a structured process API for non-trivial tasks.
- Avoid dynamic command construction, delayed expansion surprises, and nested `cmd /c` unless required.
- Treat `&`, `|`, `<`, `>`, `^`, `%`, and `!` as special syntax; do not interpolate untrusted input.
- For complex repeatable work, use a reviewed `.ps1` or Python script rather than a long `.bat` one-liner.
