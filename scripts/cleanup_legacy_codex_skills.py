#!/usr/bin/env python3
"""一次性清理脚本：删除根目录 install.py 旧版本安装到 ~/.codex/skills 中的 Skill。

只删除旧 manifest (~/.codex/.codex-profile-install.json) 中记录过的 Skill，
不会触碰 ~/.codex/skills 中的其他目录。清理完成后删除旧 manifest 本身。
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path


OLD_MANIFEST_NAME = ".codex-profile-install.json"


def default_codex_home():
    if os.name == "nt" and os.environ.get("USERPROFILE"):
        return Path(os.environ["USERPROFILE"]) / ".codex"
    return Path.home() / ".codex"


def configure_stdout():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def is_relative_to(path, parent):
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_codex_home(codex_home, repo_root):
    if is_relative_to(codex_home, repo_root):
        raise SystemExit(f"Refusing to clean repository path: {codex_home}")
    if codex_home == codex_home.parent:
        raise SystemExit(f"Refusing to clean filesystem root: {codex_home}")


def is_safe_skill_name(name):
    return (
        isinstance(name, str)
        and name
        and name not in {".", ".."}
        and "/" not in name
        and "\\" not in name
        and not Path(name).is_absolute()
    )


def load_old_manifest(manifest_path):
    if not manifest_path.is_file():
        return None

    try:
        with manifest_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid install manifest: {manifest_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(f"Invalid install manifest format: {manifest_path}")

    skills = data.get("skills", [])
    if not isinstance(skills, list):
        raise SystemExit(f"Invalid install manifest skills list: {manifest_path}")

    invalid_names = [name for name in skills if not is_safe_skill_name(name)]
    if invalid_names:
        raise SystemExit(f"Invalid skill names in install manifest: {invalid_names}")

    return set(skills)


def remove_skill(skill_name, skills_target, dry_run):
    target = (skills_target / skill_name).resolve()
    resolved_skills_target = skills_target.resolve()
    if not is_relative_to(target, resolved_skills_target):
        raise SystemExit(f"Refusing to remove path outside skills directory: {target}")

    if not target.exists() and not target.is_symlink():
        print(f"skip missing skill {target}")
        return

    print(f"remove {target}")
    if dry_run:
        return
    if target.is_symlink() or target.is_file():
        target.unlink()
    else:
        shutil.rmtree(target)


def main():
    configure_stdout()

    parser = argparse.ArgumentParser(
        description="Remove skills previously installed into ~/.codex/skills by the old install.py."
    )
    parser.add_argument(
        "--codex-home",
        default=str(default_codex_home()),
        help="Codex home directory. Default: ~/.codex",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    codex_home = Path(args.codex_home).expanduser().resolve()
    validate_codex_home(codex_home, repo_root)

    manifest_path = codex_home / OLD_MANIFEST_NAME
    skills_target = codex_home / "skills"

    skill_names = load_old_manifest(manifest_path)
    if skill_names is None:
        print(f"No old manifest found at {manifest_path}, nothing to clean.")
        return

    print(
        f"重要提示：本脚本会删除旧版本 install.py 安装到 {skills_target} 中的 Skill，"
        f"以及旧 manifest 文件 {manifest_path}。请先使用 --dry-run 确认清理范围再执行。"
    )
    for skill_name in sorted(skill_names):
        remove_skill(skill_name, skills_target, args.dry_run)

    print(f"remove manifest {manifest_path}")
    if not args.dry_run:
        manifest_path.unlink()
        print(f"Cleanup completed for {codex_home}")
    else:
        print(f"Dry run completed for {codex_home}")


if __name__ == "__main__":
    main()
