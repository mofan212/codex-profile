import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_PATH = REPO_ROOT / "install.py"
CLEANUP_PATH = REPO_ROOT / "scripts" / "cleanup_legacy_codex_skills.py"


class CodexInstallConfirmationTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / "user"
        self.home.mkdir()
        self.codex_home = self.root / "custom-codex"
        self.agents_home = self.root / "custom-agents"
        self.dsh_home = self.home / ".dsh"
        self.workbuddy_home = self.home / ".workbuddy"
        environment = patch.dict(os.environ, {
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "PYTHONUTF8": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        })
        environment.start()
        self.addCleanup(environment.stop)

    def run_install(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, str(INSTALL_PATH),
             "--codex-home", str(self.codex_home),
             "--agents-home", str(self.agents_home), *args],
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def snapshot(self):
        return {
            path.relative_to(self.root): path.read_bytes() if path.is_file() else None
            for path in self.root.rglob("*")
        }

    def prepare_optional_targets(self):
        self.dsh_home.mkdir()
        (self.dsh_home / "AGENTS.md").write_text("原有规则", encoding="utf-8")
        stale_skill = self.workbuddy_home / "skills" / "removed-skill"
        stale_skill.mkdir(parents=True)
        (stale_skill / "SKILL.md").write_text("旧 Skill", encoding="utf-8")
        (self.workbuddy_home / ".agents-profile-install.json").write_text(
            json.dumps({"skills": ["removed-skill"]}), encoding="utf-8"
        )

    def test_dry_run_names_global_rules_source_and_install_target(self):
        with tempfile.TemporaryDirectory() as codex_home, tempfile.TemporaryDirectory() as agents_home:
            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALL_PATH),
                    "--codex-home",
                    codex_home,
                    "--agents-home",
                    agents_home,
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        self.assertIn("codex-global-rules.md", result.stdout)
        self.assertIn(str(Path(codex_home) / "AGENTS.md"), result.stdout)
        self.assertNotIn("AGENTS.md 会写入", result.stdout)

    def test_help_names_global_rules_source_and_install_target(self):
        result = subprocess.run(
            [sys.executable, str(INSTALL_PATH), "--help"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertIn("profile/codex-global-rules.md", result.stdout)
        self.assertIn("~/.codex/AGENTS.md", result.stdout)
        self.assertIn("~/.dsh/AGENTS.md", result.stdout)
        self.assertIn("~/.workbuddy/skills", result.stdout)

    def test_real_install_requires_confirmation_before_writing(self):
        with tempfile.TemporaryDirectory() as codex_home, tempfile.TemporaryDirectory() as agents_home:
            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALL_PATH),
                    "--codex-home",
                    codex_home,
                    "--agents-home",
                    agents_home,
                ],
                input="no\n",
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(codex_home) / "AGENTS.md").exists())
            self.assertFalse((Path(agents_home) / "skills").exists())

    def test_yes_flag_allows_non_interactive_install(self):
        with tempfile.TemporaryDirectory() as codex_home, tempfile.TemporaryDirectory() as agents_home:
            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALL_PATH),
                    "--codex-home",
                    codex_home,
                    "--agents-home",
                    agents_home,
                    "--yes",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertTrue((Path(codex_home) / "AGENTS.md").is_file())
            self.assertTrue((Path(agents_home) / "skills").is_dir())
            self.assertIn(
                f"profile/codex-global-rules.md -> {Path(codex_home) / 'AGENTS.md'}",
                result.stdout,
            )
            self.assertFalse(self.dsh_home.exists())
            self.assertFalse(self.workbuddy_home.exists())

    def test_installs_rules_when_only_dsh_directory_exists(self):
        self.dsh_home.mkdir()
        (self.dsh_home / "AGENTS.md").write_text("原有规则", encoding="utf-8")

        result = self.run_install("--yes")

        self.assertEqual(result.returncode, 0, result.stderr)
        rules = (REPO_ROOT / "profile" / "codex-global-rules.md").read_bytes()
        self.assertEqual((self.dsh_home / "AGENTS.md").read_bytes(), rules)
        self.assertEqual((self.codex_home / "AGENTS.md").read_bytes(), rules)
        self.assertFalse(self.workbuddy_home.exists())

    def test_creates_skills_when_only_workbuddy_directory_exists(self):
        self.workbuddy_home.mkdir()

        result = self.run_install("--yes")

        self.assertEqual(result.returncode, 0, result.stderr)
        source = REPO_ROOT / "profile" / "skills"
        for target_home in (self.agents_home, self.workbuddy_home):
            for source_file in source.rglob("*"):
                if source_file.is_file():
                    installed_file = target_home / "skills" / source_file.relative_to(source)
                    self.assertEqual(installed_file.read_bytes(), source_file.read_bytes())
            manifest = json.loads((target_home / ".agents-profile-install.json").read_text(encoding="utf-8"))
            self.assertEqual(set(manifest["skills"]), {p.name for p in source.iterdir() if p.is_dir()})
        self.assertFalse(self.dsh_home.exists())

    def test_skips_optional_paths_that_are_files(self):
        for path in (self.dsh_home, self.workbuddy_home):
            path.write_text("保留", encoding="utf-8")

        result = self.run_install("--yes")

        self.assertEqual(result.returncode, 0, result.stderr)
        for path in (self.dsh_home, self.workbuddy_home):
            self.assertEqual(path.read_text(encoding="utf-8"), "保留")

    def test_each_skills_destination_replaces_and_cleans_independently(self):
        self.dsh_home.mkdir()
        source = REPO_ROOT / "profile" / "skills"
        current_names = {p.name for p in source.iterdir() if p.is_dir()}
        replaced_name = sorted(current_names)[0]
        targets = ((self.agents_home, "agents-old"), (self.workbuddy_home, "workbuddy-old"))
        for target_home, tracked_name in targets:
            for name in ("agents-old", "workbuddy-old", "personal", replaced_name):
                directory = target_home / "skills" / name
                directory.mkdir(parents=True)
                (directory / "local-extra.txt").write_text("保留或替换", encoding="utf-8")
            (target_home / ".agents-profile-install.json").write_text(
                json.dumps({"skills": [tracked_name, replaced_name], "created_at": tracked_name}),
                encoding="utf-8",
            )

        result = self.run_install("--yes")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.dsh_home / "AGENTS.md").read_bytes(),
            (REPO_ROOT / "profile" / "codex-global-rules.md").read_bytes(),
        )
        for target_home, tracked_name in targets:
            self.assertFalse((target_home / "skills" / tracked_name).exists())
            self.assertFalse((target_home / "skills" / replaced_name / "local-extra.txt").exists())
            for untracked in {"agents-old", "workbuddy-old", "personal"} - {tracked_name}:
                self.assertEqual(
                    (target_home / "skills" / untracked / "local-extra.txt").read_text(encoding="utf-8"),
                    "保留或替换",
                )
            manifest = json.loads((target_home / ".agents-profile-install.json").read_text(encoding="utf-8"))
            self.assertEqual(set(manifest["skills"]), current_names)
            self.assertEqual(manifest["created_at"], tracked_name)

    def test_dry_run_lists_optional_operations_without_writing(self):
        self.prepare_optional_targets()
        before = self.snapshot()

        result = self.run_install("--dry-run")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.dsh_home / "AGENTS.md"), result.stdout)
        self.assertIn(str(self.workbuddy_home / "skills"), result.stdout)
        self.assertIn(f"remove removed skill {self.workbuddy_home / 'skills' / 'removed-skill'}", result.stdout)
        self.assertIn(str(self.workbuddy_home / ".agents-profile-install.json"), result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_declining_confirmation_preserves_all_targets(self):
        self.prepare_optional_targets()
        before = self.snapshot()

        result = self.run_install(input_text="no\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(self.dsh_home / "AGENTS.md"), result.stdout)
        self.assertIn(str(self.workbuddy_home / "skills"), result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_workbuddy_manifest_aborts_before_any_write(self):
        self.prepare_optional_targets()
        (self.workbuddy_home / ".agents-profile-install.json").write_text("{", encoding="utf-8")
        before = self.snapshot()

        result = self.run_install("--yes")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid install manifest", result.stderr)
        self.assertEqual(self.snapshot(), before)


class CleanupConfirmationTest(unittest.TestCase):
    def test_cleanup_requires_confirmation_before_deleting(self):
        with tempfile.TemporaryDirectory() as codex_home:
            home = Path(codex_home)
            skill_dir = home / "skills" / "example"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("example", encoding="utf-8")
            manifest = home / ".codex-profile-install.json"
            manifest.write_text('{"skills": ["example"]}', encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(CLEANUP_PATH), "--codex-home", codex_home],
                input="no\n",
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(skill_dir.is_dir())
            self.assertTrue(manifest.is_file())


if __name__ == "__main__":
    unittest.main()
