#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


MANIFEST_NAME = ".codex-profile-install.json"
MANIFEST_SCHEMA_VERSION = 1
REFERENCE_URL = "https://github.com/mofan212/codex-profile"
INSTALL_WARNING = (
    "重要提示：真实安装会整体替换目标 Codex skills 目录中的同名 Skill，"
    "不会合并目录，也不会保留目标同名 Skill 目录中的额外文件。"
    "同时会删除本脚本上次安装过、但当前 profile/skills 中已不存在的 Skill。"
)


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
        raise SystemExit(f"Refusing to install into repository path: {codex_home}")
    if codex_home == codex_home.parent:
        raise SystemExit(f"Refusing to install into filesystem root: {codex_home}")


def copy_file(source, target, dry_run):
    print(f"copy {source} -> {target}")
    if dry_run:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def replace_directory(source, target, dry_run):
    print(f"replace {target} <- {source}")
    if dry_run:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    shutil.copytree(source, target)


def is_safe_skill_name(name):
    return (
        isinstance(name, str)
        and name
        and name not in {".", ".."}
        and "/" not in name
        and "\\" not in name
        and not Path(name).is_absolute()
    )


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def current_timezone():
    offset = datetime.now().astimezone().strftime("%z")
    if not offset:
        return "local"
    return f"UTC{offset[:3]}:{offset[3:]}"


def load_manifest(manifest_path):
    if not manifest_path.is_file():
        return {"skills": set(), "created_at": None}

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

    created_at = data.get("created_at")
    if created_at is not None and not isinstance(created_at, str):
        raise SystemExit(f"Invalid install manifest created_at: {manifest_path}")

    return {"skills": set(skills), "created_at": created_at}


def write_manifest(manifest_path, skill_names, previous_manifest, dry_run):
    print(f"write manifest {manifest_path}")
    if dry_run:
        return
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    now = current_timestamp()
    data = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "created_at": previous_manifest.get("created_at") or now,
        "updated_at": now,
        "timezone": current_timezone(),
        "reference": REFERENCE_URL,
        "skills": sorted(skill_names),
    }
    with manifest_path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def remove_installed_skill(skill_name, skills_target, dry_run):
    if not is_safe_skill_name(skill_name):
        raise SystemExit(f"Refusing to remove invalid skill name: {skill_name}")

    target = (skills_target / skill_name).resolve()
    resolved_skills_target = skills_target.resolve()
    if not is_relative_to(target, resolved_skills_target):
        raise SystemExit(f"Refusing to remove path outside skills directory: {target}")

    if not target.exists() and not target.is_symlink():
        print(f"skip missing removed skill {target}")
        return

    print(f"remove removed skill {target}")
    if dry_run:
        return
    if target.is_symlink() or target.is_file():
        target.unlink()
    else:
        shutil.rmtree(target)


def main():
    configure_stdout()

    parser = argparse.ArgumentParser(description="Install Codex profile files.")
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

    repo_root = Path(__file__).resolve().parent
    codex_home = Path(args.codex_home).expanduser().resolve()
    validate_codex_home(codex_home, repo_root)

    profile_root = repo_root / "profile"
    agents_source = profile_root / "AGENTS.md"
    skills_source = profile_root / "skills"
    skills_target = codex_home / "skills"
    manifest_path = codex_home / MANIFEST_NAME

    if not agents_source.is_file():
        raise SystemExit("profile/AGENTS.md not found")
    if not skills_source.is_dir():
        raise SystemExit("profile/skills directory not found")

    skill_dirs = sorted(path for path in skills_source.iterdir() if path.is_dir())
    current_skill_names = {skill_dir.name for skill_dir in skill_dirs}
    previous_manifest = load_manifest(manifest_path)
    previous_skill_names = previous_manifest["skills"]

    print(INSTALL_WARNING)
    copy_file(agents_source, codex_home / "AGENTS.md", args.dry_run)

    for skill_name in sorted(previous_skill_names - current_skill_names):
        remove_installed_skill(skill_name, skills_target, args.dry_run)

    for skill_dir in skill_dirs:
        replace_directory(skill_dir, skills_target / skill_dir.name, args.dry_run)

    write_manifest(manifest_path, current_skill_names, previous_manifest, args.dry_run)

    if args.dry_run:
        print(f"Dry run completed for {codex_home}")
    else:
        print(f"Codex profile installed to {codex_home}")


if __name__ == "__main__":
    main()
