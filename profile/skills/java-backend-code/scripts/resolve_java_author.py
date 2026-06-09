#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict


AUTHOR_RE = re.compile(r"@author\s+([^\r\n*]+)")
COMMIT_BATCH_SIZES = (30, 20, 20, 30, 50, 50)


def git(repo, *args):
    result = subprocess.run(
        ["git", "-C", repo, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def git_blob_texts(repo, refs):
    if not refs:
        return {}

    ordered_refs = list(dict.fromkeys(refs))
    result = subprocess.run(
        ["git", "-C", repo, "cat-file", "--batch"],
        input=("".join(f"{commit}:{path}\n" for commit, path in ordered_refs)).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return {}

    output = result.stdout
    pos = 0
    texts = {}
    ref_index = 0
    while pos < len(output) and ref_index < len(ordered_refs):
        ref = ordered_refs[ref_index]
        ref_index += 1
        line_end = output.find(b"\n", pos)
        if line_end < 0:
            break

        header = output[pos:line_end].decode("utf-8", errors="replace")
        pos = line_end + 1
        parts = header.rsplit(" ", 2)
        if len(parts) != 3 or parts[1] == "missing":
            continue

        _, obj_type, size_text = parts
        try:
            size = int(size_text)
        except ValueError:
            break

        data = output[pos:pos + size]
        pos += size + 1
        if obj_type == "blob":
            texts[ref] = data.decode("utf-8", errors="replace")

    return texts


def current_user_java_additions(repo, identity, user_email, user_name, offset, limit):
    log = git(repo, "log", "--all", f"--author={identity}", f"--skip={offset}", f"--max-count={limit}",
              "--diff-filter=A", "--name-only",
              "--format=@@%H%x00%an%x00%ae", "--", "*.java")
    commit = None
    candidates = []
    seen_files = set()

    for line in log.splitlines():
        if line.startswith("@@"):
            commit_id, author_name, author_email = line[2:].split("\0", 2)
            same_email = user_email and author_email == user_email
            same_name = not user_email and user_name and author_name == user_name
            commit = commit_id if same_email or same_name else None
            continue
        if not commit or not line.endswith(".java"):
            continue

        key = (commit, line)
        if key not in seen_files:
            seen_files.add(key)
            candidates.append(key)

    return candidates


def resolve(repo):
    root = git(repo, "rev-parse", "--show-toplevel")
    if not root:
        raise SystemExit("当前目录不在 Git 仓库中，无法解析 Java author")

    user_name = git(root, "config", "--get", "user.name")
    user_email = git(root, "config", "--get", "user.email")
    identity = user_email or user_name

    offset = 0
    for limit in (COMMIT_BATCH_SIZES if identity else []):
        candidates = current_user_java_additions(root, identity, user_email, user_name, offset, limit)
        offset += limit
        counts = Counter()
        evidence = defaultdict(list)
        first_seen = {}

        for (commit, line), text in git_blob_texts(root, candidates).items():
            match = AUTHOR_RE.search(text)
            if match:
                author = match.group(1).strip()
                counts[author] += 1
                first_seen.setdefault(author, len(first_seen))
                evidence[author].append({"path": line, "commit": commit})

        if counts:
            author = max(counts, key=lambda item: (counts[item], -first_seen[item]))
            return {
                "author": author,
                "source": "current-user-added-java-files",
                "evidence": evidence[author][:5],
                "repo": root,
            }

    return {
        "author": user_name,
        "source": "git-config-user-name" if user_name else "unresolved",
        "evidence": [],
        "repo": root,
    }


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = sys.argv[1:]
    plain_arg = "--plain" in args
    if "--repo" in args and args.index("--repo") + 1 >= len(args):
        raise SystemExit("用法：resolve_java_author.py [--repo PATH] [--plain]")
    repo_arg = args[args.index("--repo") + 1] if "--repo" in args else "."
    result = resolve(repo_arg)
    if plain_arg:
        if result["author"]:
            print(result["author"])
            raise SystemExit(0)
        raise SystemExit("无法解析 Java author，且 git config user.name 为空")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["author"]:
        raise SystemExit(2)
