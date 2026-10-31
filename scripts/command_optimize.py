#!/usr/bin/env python3
"""Render an argv array for a target shell. Never executes the rendered command."""
import argparse, json, shlex, sys

SUPPORTED = {'bash','zsh','posix-sh','fish','powershell','cmd'}

def quote_posix(value): return shlex.quote(value)
def quote_powershell(value):
    # Bare simple tokens are readable; all other values use single-quoted literals.
    import re
    if re.fullmatch(r'[A-Za-z0-9_./:@%+=,-]+', value): return value
    return "'" + value.replace("'", "''") + "'"
def quote_cmd(value):
    # cmd.exe quoting is context-sensitive; deliberately reject ambiguous metacharacters.
    if any(c in value for c in '&|<>^%!\n\r'):
        raise ValueError('CMD cannot safely render this argument with this helper; use a .cmd file or structured process API.')
    if not value or any(c.isspace() or c=='"' for c in value):
        return '"' + value.replace('"','\\"') + '"'
    return value

def render(argv, shell):
    if shell not in SUPPORTED: raise ValueError(f'Unsupported shell: {shell}')
    if not isinstance(argv,list) or not argv or not all(isinstance(x,str) for x in argv):
        raise ValueError('argv must be a non-empty JSON array of strings')
    if any('\x00' in x for x in argv): raise ValueError('NUL bytes are not valid command arguments')
    if shell == 'cmd': return ' '.join(quote_cmd(x) for x in argv)
    quote = quote_powershell if shell == 'powershell' else quote_posix
    return ' '.join(quote(x) for x in argv)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--shell', required=True, choices=sorted(SUPPORTED))
    p.add_argument('--argv-json', required=True, help='JSON array, e.g. ["git","status","--short"]')
    a=p.parse_args()
    try:
        argv=json.loads(a.argv_json); command=render(argv,a.shell)
    except (ValueError, json.JSONDecodeError) as e:
        print(f'ERROR: {e}',file=sys.stderr); return 2
    print(f'Shell: {a.shell}\nCommand (display only; not executed):\n{command}')
    print('Note: Prefer passing argv directly to a process API instead of invoking a shell.')
    return 0
if __name__=='__main__': raise SystemExit(main())
