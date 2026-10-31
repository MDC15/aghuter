import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import hcli
import project_inspect
import workflow_lint


class AghuterTests(unittest.TestCase):
    def test_catalog_is_valid(self):
        data = hcli.load_catalog()
        self.assertEqual([], hcli.validate_catalog(data))

    def test_strict_workflow_lint_passes(self):
        data = hcli.load_catalog()
        self.assertEqual([], workflow_lint.validate(data))

    def test_project_inspector_is_read_only_and_detects_project(self):
        result = project_inspect.inspect(ROOT)
        self.assertEqual(str(ROOT.resolve()), result['project_root'])
        self.assertIn('README.md', result['guidance_files'])
        self.assertIn('READ_ONLY', result['policy'])

    def test_all_workflow_playbooks_exist(self):
        data = hcli.load_catalog()
        for workflow in data['workflows']:
            slug = workflow['id'].replace('.', '-')
            self.assertTrue((ROOT / 'workflows' / 'recipes' / f'{slug}.md').is_file())

    def test_alias_resolves(self):
        data = hcli.load_catalog()
        workflows = hcli.index_workflows(data)
        self.assertEqual("git.review", workflows["review"]["id"])

    def test_plan_is_non_executing(self):
        data = hcli.load_catalog()
        plan = hcli.make_plan(hcli.index_workflows(data)["git.review"])
        self.assertIn("PLAN_ONLY", plan["execution_policy"])
        self.assertTrue(any(step.get("argv") == ["git", "status", "--short", "--branch"] for step in plan["steps"]))

    def test_split_command_chain(self):
        result = hcli.explain_command("git status --short && git diff --stat")
        self.assertEqual(2, len(result["segments"]))
        self.assertEqual("&&", result["segments"][1]["preceded_by"])
        self.assertEqual("read-only", result["segments"][0]["risk_guess"])

    def test_quoted_operator_is_not_split(self):
        result = hcli.explain_command("echo 'one && two'")
        self.assertEqual(1, len(result["segments"]))

    def test_risky_command_is_flagged(self):
        result = hcli.explain_command("git push --force")
        self.assertEqual("destructive", result["segments"][0]["risk_guess"])

    def test_explainer_never_executes(self):
        result = hcli.explain_command("rm -rf build")
        self.assertIn("No command was executed", result["warnings"][1])

    def test_find_delete_is_not_read_only(self):
        result = hcli.explain_command("find . -delete")
        self.assertEqual("unknown", result["segments"][0]["risk_guess"])

    def test_redirection_is_not_mislabelled_read_only(self):
        result = hcli.explain_command("cat notes.txt > output.txt")
        self.assertEqual("unknown", result["segments"][0]["risk_guess"])

    def test_sudo_rm_is_flagged_destructive(self):
        result = hcli.explain_command("sudo rm -rf ./build")
        self.assertEqual("destructive", result["segments"][0]["risk_guess"])


if __name__ == "__main__":
    unittest.main()
