$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $PSScriptRoot '..\scripts\hcli.py'
python $scriptPath @args
exit $LASTEXITCODE
