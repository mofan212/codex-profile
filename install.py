#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path


def default_codex_home():
    if os.name == "nt" and os.environ.get("USERPROFILE"):
        return Path(os.environ["USERPROFILE"]) / ".codex"
    return Path.home() / ".codex"


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
    skills_source = repo_root / "skills"
    skills_target = codex_home / "skills"

    if not (repo_root / "AGENTS.md").is_file():
        raise SystemExit("AGENTS.md not found in repository root")
    if not skills_source.is_dir():
        raise SystemExit("skills directory not found in repository root")

    copy_file(repo_root / "AGENTS.md", codex_home / "AGENTS.md", args.dry_run)

    for skill_dir in sorted(path for path in skills_source.iterdir() if path.is_dir()):
        replace_directory(skill_dir, skills_target / skill_dir.name, args.dry_run)

    if args.dry_run:
        print(f"Dry run completed for {codex_home}")
    else:
        print(f"Codex profile installed to {codex_home}")


if __name__ == "__main__":
    main()
