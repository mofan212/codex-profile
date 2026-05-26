#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path


def default_codex_home():
    if os.name == "nt" and os.environ.get("USERPROFILE"):
        return Path(os.environ["USERPROFILE"]) / ".codex"
    return Path.home() / ".codex"


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


def main():
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

    if not agents_source.is_file():
        raise SystemExit("profile/AGENTS.md not found")
    if not skills_source.is_dir():
        raise SystemExit("profile/skills directory not found")

    copy_file(agents_source, codex_home / "AGENTS.md", args.dry_run)

    for skill_dir in sorted(path for path in skills_source.iterdir() if path.is_dir()):
        replace_directory(skill_dir, skills_target / skill_dir.name, args.dry_run)

    if args.dry_run:
        print(f"Dry run completed for {codex_home}")
    else:
        print(f"Codex profile installed to {codex_home}")


if __name__ == "__main__":
    main()
