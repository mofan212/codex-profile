import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path


INSTALL_PATH = Path(__file__).resolve().parents[1] / "opencode" / "install.py"
SPEC = importlib.util.spec_from_file_location("opencode_install", INSTALL_PATH)
INSTALL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALL)


class ValidateBaseUrlTest(unittest.TestCase):
    def test_accepts_http_and_https_urls(self):
        self.assertEqual(INSTALL.validate_base_url("https://example.com/v1"), "https://example.com/v1")
        self.assertEqual(INSTALL.validate_base_url("http://localhost:8080/v1"), "http://localhost:8080/v1")

    def test_rejects_invalid_urls(self):
        for value in ("", "example.com/v1", "ftp://example.com", "https://example.com:invalid", "https://bad host"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                INSTALL.validate_base_url(value)


class ResolveBaseUrlTest(unittest.TestCase):
    def test_uses_environment_variable_without_prompting(self):
        value = INSTALL.resolve_base_url(
            False,
            environ={INSTALL.BASE_URL_ENV_NAME: "https://example.com/v1"},
            interactive=False,
        )
        self.assertEqual(value, "https://example.com/v1")

    def test_dry_run_does_not_prompt_when_variable_is_missing(self):
        value = INSTALL.resolve_base_url(True, environ={}, interactive=True, input_func=lambda _: self.fail("prompted"))
        self.assertIsNone(value)

    def test_prompts_until_input_is_valid(self):
        values = iter(["invalid", "https://example.com/v1"])
        with redirect_stderr(io.StringIO()):
            value = INSTALL.resolve_base_url(False, environ={}, interactive=True, input_func=lambda _: next(values))
        self.assertEqual(value, "https://example.com/v1")

    def test_non_interactive_install_requires_environment_variable(self):
        with self.assertRaises(SystemExit):
            INSTALL.resolve_base_url(False, environ={}, interactive=False)


class RenderConfigTest(unittest.TestCase):
    def test_replaces_only_placeholder_and_escapes_value(self):
        source = '{"baseURL": "{env:OPENCODE_CUSTOM_BASE_URL}"}'
        rendered = INSTALL.render_config(source, 'https://example.com/a"b')
        self.assertEqual(rendered, '{"baseURL": "https://example.com/a\\"b"}')

    def test_requires_exactly_one_placeholder(self):
        with self.assertRaises(SystemExit):
            INSTALL.render_config("{}", "https://example.com")


class InstallIntegrationTest(unittest.TestCase):
    def test_real_install_injects_url_without_printing_it(self):
        base_url = "https://private.example.test/v1"
        with tempfile.TemporaryDirectory() as config_home:
            environ = os.environ.copy()
            environ[INSTALL.BASE_URL_ENV_NAME] = base_url
            result = subprocess.run(
                [sys.executable, str(INSTALL_PATH), "--config-home", config_home],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=environ,
            )

            installed = (Path(config_home) / INSTALL.SOURCE_NAME).read_text(encoding="utf-8")
            source = (INSTALL_PATH.parent / INSTALL.SOURCE_NAME).read_text(encoding="utf-8")
            self.assertIn(base_url, installed)
            self.assertNotIn(INSTALL.BASE_URL_PLACEHOLDER, installed)
            self.assertIn(INSTALL.BASE_URL_PLACEHOLDER, source)
            self.assertNotIn(base_url, result.stdout)
            self.assertNotIn(base_url, result.stderr)


if __name__ == "__main__":
    unittest.main()
