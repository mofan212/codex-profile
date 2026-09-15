"""校验 Skill 的显式触发声明在 SKILL.md 与 agents/openai.yaml 中一致。"""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "profile" / "skills"
FRONTMATTER_KEY = "disable-model-invocation"
POLICY_KEY = "allow_implicit_invocation"
BOOLEAN_LITERALS = {
    "true": True, "yes": True, "on": True, "1": True,
    "false": False, "no": False, "off": False, "0": False,
}


def parse_boolean_literal(raw_value, source):
    literal = raw_value.strip().strip('"').strip("'").lower()
    if literal not in BOOLEAN_LITERALS:
        raise ValueError(f"{source}: 不支持的布尔值 {raw_value.strip()}")
    return BOOLEAN_LITERALS[literal]


def frontmatter_declares_manual_only(skill_file):
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        if line.strip() == "---":
            return False
        key, separator, raw_value = line.partition(":")
        if separator and key.strip() == FRONTMATTER_KEY:
            return parse_boolean_literal(raw_value, skill_file)
    return False


def openai_yaml_declares_manual_only(openai_file):
    in_policy = False
    for line in openai_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, separator, raw_value = stripped.partition(":")
        if indent == 0:
            in_policy = key.strip() == "policy"
            continue
        if in_policy and separator and key.strip() == POLICY_KEY:
            # allow_implicit_invocation 与显式触发互为反义。
            return not parse_boolean_literal(raw_value, openai_file)
    return False


def collect_policy_violations(skills_root):
    violations = []
    for openai_file in sorted(skills_root.glob("*/agents/openai.yaml")):
        skill_file = openai_file.parent.parent / "SKILL.md"
        frontmatter_only = frontmatter_declares_manual_only(skill_file)
        openai_only = openai_yaml_declares_manual_only(openai_file)
        if frontmatter_only != openai_only:
            violations.append(
                f"{skill_file.parent.name}: SKILL.md 显式触发={frontmatter_only}，"
                f"agents/openai.yaml 显式触发={openai_only}"
            )
    return violations


class SkillInvocationPolicyTest(unittest.TestCase):
    def test_repository_skills_declare_consistent_invocation_policy(self):
        self.assertEqual(collect_policy_violations(SKILLS_ROOT), [])


if __name__ == "__main__":
    unittest.main()
