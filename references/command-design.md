# Command design and simplification

## Principle
Optimize for reviewability and correct failure handling, not minimum character count. A short command can still be opaque or destructive.

## Preferred sequence
1. Inspect state.
2. Perform one logical operation.
3. Verify its result.
4. Continue only when the prior result supports it.

## Avoid
- Long `&&` chains that hide which stage failed.
- `eval`, generated shell fragments, and commands assembled from untrusted input.
- Broad globs and implicit all-files staging.
- Piping network-fetched content directly to a shell.
- Hiding destructive behavior behind aliases or friendly task names.

## Prefer
- Host-native tools and structured argument arrays.
- Existing project scripts discovered from manifests/docs.
- Explicit paths and `--` before path arguments where supported.
- Separate commands when they have different side effects or approval needs.
