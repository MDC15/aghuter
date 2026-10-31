#!/usr/bin/env python3
"""Conservative heuristic risk review for an argv array; not a security sandbox."""
import argparse, json, sys
DESTRUCTIVE = {'rm','rmdir','del','erase','format','mkfs','dd','shutdown','reboot'}
NETWORK = {'curl','wget','ssh','scp','ftp','nc','netcat'}
PUBLISH = {('git','push'),('npm','publish'),('pnpm','publish'),('yarn','publish'),('docker','push'),('helm','upgrade'),('terraform','apply')}

def assess(argv):
    if not isinstance(argv,list) or not argv or not all(isinstance(x,str) for x in argv):
        raise ValueError('argv must be a non-empty array of strings')
    exe=argv[0].lower().replace('\\','/').split('/')[-1]
    args=[x.lower() for x in argv[1:]]
    reasons=[]; risk='read-only'
    if exe in DESTRUCTIVE or (exe=='git' and len(args)>0 and args[0] in ('reset','clean')):
        risk='destructive'; reasons.append('Potentially destructive operation; inspect exact target and impact.')
    elif exe in NETWORK:
        risk='external'; reasons.append('Network or remote interaction may occur.')
    elif any(tuple([exe]+args[:len(prefix)-1]) == prefix for prefix in PUBLISH):
        risk='external'; reasons.append('May publish, push, deploy, or change a shared system.')
    elif exe in {'git'} and args and args[0] in {'add','commit','merge','rebase','checkout','switch'}:
        risk='local-write'; reasons.append('Changes local repository state.')
    elif exe in {'npm','pnpm','yarn','pip','uv','cargo'} and args and args[0] in {'install','ci','sync','add','remove','update'}:
        risk='local-write'; reasons.append('May modify dependencies, lockfiles, or environment.')
    if any(x in {'>','>>','<','2>','2>>'} or x.startswith(('>','2>')) for x in argv):
        if risk=='read-only': risk='local-write'
        reasons.append('Redirection may read or write files; inspect target path.')
    if any(x in {'-force','--force','-f'} for x in args):
        if risk!='destructive': risk='external' if risk=='external' else 'unknown'
        reasons.append('Force flag increases impact; verify scope.')
    if not reasons: reasons.append('No known high-risk pattern detected; this is not proof of safety.')
    return {'risk':risk,'argv':argv,'reasons':reasons,'execution':'not performed','limitations':'Heuristic only; wrappers, scripts, aliases, shell syntax, and tool-specific behavior may change the actual effect.'}

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--argv-json',required=True); a=p.parse_args()
    try: result=assess(json.loads(a.argv_json))
    except (ValueError,json.JSONDecodeError) as e: print(f'ERROR: {e}',file=sys.stderr); return 2
    print(json.dumps(result,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
