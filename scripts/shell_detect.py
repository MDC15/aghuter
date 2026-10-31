#!/usr/bin/env python3
"""Detect the current OS and likely interactive shell; read-only."""
import json, os, platform, shutil, sys

def detect():
    system = platform.system().lower()
    if system == 'windows': os_name = 'windows'
    elif system == 'darwin': os_name = 'macos'
    elif system == 'linux': os_name = 'linux'
    else: os_name = system or 'unknown'
    shell_path = os.environ.get('SHELL') or os.environ.get('COMSPEC') or ''
    base = os.path.basename(shell_path).lower()
    ps = os.environ.get('PSModulePath')
    if ps or base in ('pwsh', 'powershell.exe', 'powershell'):
        shell = 'powershell'
    elif base in ('cmd.exe', 'cmd') or (os_name == 'windows' and not shell_path):
        shell = 'cmd'
    elif base in ('zsh',): shell = 'zsh'
    elif base in ('fish',): shell = 'fish'
    elif base in ('bash',): shell = 'bash'
    elif base in ('sh', 'dash', 'ash'): shell = 'posix-sh'
    else: shell = 'unknown'
    return {'os': os_name, 'shell': shell, 'shell_path': shell_path or None,
            'python': platform.python_version(), 'available_tools': {
                name: shutil.which(name) is not None for name in ('git','python','node','npm','pnpm','yarn','docker','pwsh','bash')}}

if __name__ == '__main__':
    data = detect()
    if '--json' in sys.argv: print(json.dumps(data, indent=2))
    else:
        print(f"OS: {data['os']}\nShell: {data['shell']}\nShell path: {data['shell_path'] or 'unknown'}")
        print('Available tools: ' + ', '.join(k for k,v in data['available_tools'].items() if v))
