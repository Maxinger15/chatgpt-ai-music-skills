---
name: health-check
description: "Runs plugin health checks (venv packages and skill registration). Use when the user asks to check plugin health, verify setup, or troubleshoot missing skills."
---

# Health Check

## Your Task

Run the `health_check` MCP tool and report results to the user.

## Workflow

**IMPORTANT: Do NOT use Bash for any step. Use only the tools listed below.**

1. Use the `ToolSearch` tool with query `select:mcp__plugin_maxinger15-music_maxinger15-music-mcp__health_check` to load the MCP tool schema
2. Call `mcp__plugin_maxinger15-music_maxinger15-music-mcp__health_check` (the MCP tool, not a CLI command)
3. Report results clearly using the format below

## Report Format

### All OK

```
HEALTH CHECK: OK
  Venv: N packages verified
  Skills: N skills registered
```

### Warnings

```
HEALTH CHECK: WARN

VENV [warn]
  N outdated: pkg1 (1.0 -> 1.1), pkg2 (2.0 -> 2.1)
  N missing: pkg3, pkg4
  Fix: ~/.maxinger15-music/venv/bin/pip install -r .../requirements.txt

SKILLS [warn]
  Missing Codex plugin files: .codex-plugin/plugin.json
  Fix: repair the local Codex plugin files and restart Codex

For comprehensive diagnostics, run the `diagnose` MCP tool.
```

### Failure

```
HEALTH CHECK: FAIL

VENV [fail]
  Venv not found at ~/.maxinger15-music/venv
  Fix: $maxinger15-music:setup
```

## Remember

1. **Be concise** — this is a status report
2. **Show fix commands** — always include the fix command when status is not ok
3. **Suggest diagnose** — if warnings are found, mention `diagnose` MCP tool for deeper checks
