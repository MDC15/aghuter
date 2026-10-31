import importlib.util, json, pathlib, subprocess, sys, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name, ROOT/'scripts'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class V03Tests(unittest.TestCase):
    def test_shell_detect_schema(self):
        m=load('shell_detect'); d=m.detect(); self.assertIn(d['os'], {'windows','macos','linux','unknown'})
        self.assertIn('shell',d); self.assertIn('available_tools',d)
    def test_bash_render(self):
        m=load('command_optimize'); self.assertEqual(m.render(['echo','hello world'],'bash'), "echo 'hello world'")
    def test_powershell_quote(self):
        m=load('command_optimize'); self.assertEqual(m.render(['Write-Output',"it's ok"],'powershell'), "Write-Output 'it''s ok'")
    def test_cmd_reject_metacharacters(self):
        m=load('command_optimize')
        with self.assertRaises(ValueError): m.render(['echo','a & b'],'cmd')
    def test_invalid_argv(self):
        m=load('command_optimize')
        with self.assertRaises(ValueError): m.render('git status','bash')
    def test_risk_git_push(self):
        m=load('command_validate'); self.assertEqual(m.assess(['git','push'])['risk'],'external')
    def test_risk_rm(self):
        m=load('command_validate'); self.assertEqual(m.assess(['rm','-rf','tmp'])['risk'],'destructive')
    def test_risk_read_only_caveat(self):
        m=load('command_validate'); self.assertIn('not proof of safety',m.assess(['git','status'])['reasons'][0])
    def test_workflow_catalog_valid(self):
        m=load('hcli'); d=m.load_catalog(); self.assertEqual(m.validate_catalog(d),[])
    def test_workflow_aliases_unique(self):
        m=load('hcli'); m.index_workflows(m.load_catalog())
    def test_all_adapters_present(self):
        for f in ['codex.md','claude-code.md','github-copilot.md','opencode.md','cursor.md','gemini-cli.md']:
            self.assertTrue((ROOT/'adapters'/f).is_file())
    def test_recipe_files_present(self):
        for f in ['cross-platform-command.md','long-command-refactor.md','agent-tool-selection.md']:
            self.assertTrue((ROOT/'workflows'/'recipes'/f).is_file())

if __name__=='__main__': unittest.main()
