#!/usr/bin/env python3
"""PostToolUse hook: Check Codex plugin metadata stays coherent.

Only activates when editing .codex-plugin/plugin.json or the Codex marketplace.
"""
import json
import os
import re
import sys


MANIFEST_FILES = {"plugin.json", "marketplace.json"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def is_manifest_file(file_path: str) -> bool:
    return (
        os.path.basename(file_path) in MANIFEST_FILES
        and (".codex-plugin" in file_path or ".agents/plugins" in file_path)
    )


def check_sync(data: dict) -> list[str]:
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not is_manifest_file(file_path):
        return []

    if ".codex-plugin" in file_path:
        root_dir = os.path.dirname(os.path.dirname(file_path))
    else:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))

    plugin_path = os.path.join(root_dir, ".codex-plugin", "plugin.json")
    marketplace_path = os.path.join(root_dir, ".agents", "plugins", "marketplace.json")

    if not os.path.exists(plugin_path) or not os.path.exists(marketplace_path):
        return []

    try:
        with open(plugin_path) as f:
            plugin_data = json.load(f)
        with open(marketplace_path) as f:
            marketplace_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    issues = []

    plugin_name = plugin_data.get("name", "")
    plugin_version = plugin_data.get("version", "")
    if not plugin_name:
        issues.append("plugin.json is missing name.")
    if not isinstance(plugin_version, str) or not SEMVER_RE.match(plugin_version):
        issues.append(f"plugin.json version must be semver, got {plugin_version!r}.")

    plugins = marketplace_data.get("plugins", [])
    if plugin_name and not any(
        isinstance(entry, dict) and entry.get("name") == plugin_name
        for entry in plugins
    ):
        issues.append(f"marketplace.json has no entry for {plugin_name!r}.")

    return issues


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    issues = check_sync(data)
    if issues:
        msg = "Codex plugin metadata check failed:\n" + "\n".join(f"  - {i}" for i in issues)
        print(msg, file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
