import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_PATH = REPO_ROOT / "install.py"
CLEANUP_PATH = REPO_ROOT / "scripts" / "cleanup_legacy_codex_skills.py"


class CodexInstallConfirmationTest(unittest.TestCase):
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
