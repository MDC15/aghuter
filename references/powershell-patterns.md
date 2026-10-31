# PowerShell guidance

- Prefer structured cmdlets and objects (`Get-ChildItem`, `Where-Object`, `Select-Object`) over parsing formatted table output.
- Use `-LiteralPath` for paths that must not interpret wildcard characters; quote values and use `--%` only when its limitations are understood.
- Distinguish Windows PowerShell 5.1 from PowerShell 7+; do not assume every cmdlet/parameter is identical.
- Check `$LASTEXITCODE` for native executables and `$?` for PowerShell command success; they are not interchangeable.
- Avoid `Invoke-Expression`. Prefer `Start-Process -ArgumentList` carefully or .NET `ProcessStartInfo.ArgumentList` for structured arguments.
