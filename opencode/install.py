#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse


SOURCE_NAME = "opencode.jsonc"
BASE_URL_ENV_NAME = "OPENCODE_CUSTOM_BASE_URL"
BASE_URL_PLACEHOLDER = f"{{env:{BASE_URL_ENV_NAME}}}"


def default_config_home():
    return Path.home() / ".config" / "opencode"


def configure_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def confirm_install(skip_confirmation, input_func=None):
    if skip_confirmation:
        return

    input_func = input if input_func is None else input_func
    try:
        answer = input_func("确认按上述范围执行安装？[y/N]：").strip().lower()
    except (EOFError, KeyboardInterrupt) as exc:
        raise SystemExit("安装已取消。非交互执行请使用 --yes。") from exc
    if answer not in {"y", "yes"}:
        raise SystemExit("安装已取消。")


def is_relative_to(path, parent):
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_config_home(config_home, repo_root):
    if is_relative_to(config_home, repo_root):
        raise SystemExit(f"Refusing to install into repository path: {config_home}")
    if config_home == config_home.parent:
        raise SystemExit(f"Refusing to install into filesystem root: {config_home}")


def validate_base_url(value):
    base_url = value.strip()
    if not base_url:
        raise ValueError("URL 不能为空")
    if any(character.isspace() for character in base_url):
        raise ValueError("URL 不能包含空白字符")

    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL 必须是包含主机名的 HTTP 或 HTTPS 地址")
    try:
        parsed.port
    except ValueError as exc:
        raise ValueError("URL 端口无效") from exc
    return base_url


def resolve_base_url(allow_prompt, environ=None, interactive=None, input_func=None):
    environ = os.environ if environ is None else environ
    raw_value = environ.get(BASE_URL_ENV_NAME)
    if raw_value and raw_value.strip():
        try:
            return validate_base_url(raw_value)
        except ValueError as exc:
            raise SystemExit(f"Environment variable {BASE_URL_ENV_NAME} is invalid: {exc}") from exc

    if not allow_prompt:
        return None

    interactive = sys.stdin.isatty() if interactive is None else interactive
    if not interactive:
        raise SystemExit(
            f"Environment variable {BASE_URL_ENV_NAME} is not set and input is not interactive."
        )

    input_func = input if input_func is None else input_func
    while True:
        try:
            raw_value = input_func(f"请输入 {BASE_URL_ENV_NAME}：")
        except (EOFError, KeyboardInterrupt) as exc:
            raise SystemExit("Input cancelled.") from exc
        try:
            return validate_base_url(raw_value)
        except ValueError as exc:
            print(f"输入无效：{exc}", file=sys.stderr)


def render_config(source_text, base_url):
    placeholder_count = source_text.count(BASE_URL_PLACEHOLDER)
    if placeholder_count != 1:
        raise SystemExit(
            f"Expected exactly one {BASE_URL_PLACEHOLDER} placeholder, found {placeholder_count}."
        )
    escaped_base_url = json.dumps(base_url, ensure_ascii=False)[1:-1]
    return source_text.replace(BASE_URL_PLACEHOLDER, escaped_base_url)


def main():
    configure_output()

    parser = argparse.ArgumentParser(description="Install OpenCode config file.")
    parser.add_argument(
        "--config-home",
        default=str(default_config_home()),
        help="OpenCode config directory. Default: ~/.config/opencode",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt for a real install.",
    )
    args = parser.parse_args()

    opencode_root = Path(__file__).resolve().parent
    repo_root = opencode_root.parent
    config_home = Path(args.config_home).expanduser().resolve()
    validate_config_home(config_home, repo_root)

    source = opencode_root / SOURCE_NAME
    target = config_home / SOURCE_NAME

    if not source.is_file():
        raise SystemExit(f"{source} not found")

    source_text = source.read_text(encoding="utf-8")
    base_url = resolve_base_url(allow_prompt=False)

    print(
        f"重要提示：真实安装会用 {source} 整体覆盖 {target}，"
        "不会合并内容。请先使用 --dry-run 确认再执行。"
    )
    if base_url is None:
        print(
            f"Environment variable {BASE_URL_ENV_NAME} is not set; "
            "a real interactive install will request it."
        )
    else:
        print(f"Environment variable {BASE_URL_ENV_NAME} is set and valid.")
    print(f"render {source} -> {target}")
    if not args.dry_run:
        confirm_install(args.yes)
        if base_url is None:
            base_url = resolve_base_url(allow_prompt=True)
        rendered_config = render_config(source_text, base_url)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8", newline="\n") as file:
            file.write(rendered_config)
        print(f"OpenCode config installed to {target}")
    else:
        print(f"Dry run completed for {config_home}")


if __name__ == "__main__":
    main()
