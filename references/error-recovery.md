# Error recovery

- Capture exit code, concise stderr, command/tool identity, working directory, and relevant environment facts without exposing secrets.
- Classify failure: command missing, wrong shell/syntax, bad path, permissions, dependency/configuration, test failure, network/service, or unknown.
- Do not blindly retry. Retry only transient failures and only when the operation is safe/idempotent.
- Before changing shell syntax, verify the detected shell and executable version.
- Before installing dependencies or changing configuration, explain scope and obtain approval when required.
- After a fix, rerun the narrowest failing check, then the broader relevant verification.
