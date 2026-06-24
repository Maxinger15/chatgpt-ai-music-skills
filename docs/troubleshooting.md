# Troubleshooting

## Config Not Found

**Problem:** "Config not found at ~/.maxinger15-music/config.yaml"

**Solution:**
```bash
mkdir -p ~/.maxinger15-music
cp config/config.example.yaml ~/.maxinger15-music/config.yaml
nano ~/.maxinger15-music/config.yaml  # edit with your settings
```

Or use the interactive config tool:
```
$maxinger15-music:configure
```

## Album Not Found When Resuming

**Problem:** `$maxinger15-music:resume my-album` can't find the album

**Possible causes:**
1. **Wrong album name** — album names are case-sensitive. Try `$maxinger15-music:resume` (without name) to see all albums
2. **Wrong path in config** — check `paths.content_root` in `~/.maxinger15-music/config.yaml`
3. **Album in wrong location** — albums must be in: `{content_root}/artists/{artist}/albums/{genre}/{album}/`

## Path Resolution Issues

**Problem:** Files created in wrong locations, "path not found" errors

**The rule:** Always read `~/.maxinger15-music/config.yaml` first to get paths. Never assume or hardcode.

```
{content_root}/artists/{artist}/albums/{genre}/{album}/    # Content
{audio_root}/artists/{artist}/albums/{genre}/{album}/      # Audio (mirrored)
{documents_root}/artists/{artist}/albums/{genre}/{album}/  # Documents (mirrored)
```

## Python Dependency Issues (Mastering)

**Problem:** Mastering fails with import errors

**Solution:**
```bash
python3 -m venv ~/.maxinger15-music/venv
~/.maxinger15-music/venv/bin/pip install -r requirements.txt
```

## Playwright Setup (Document Hunter)

**Problem:** `$maxinger15-music:document-hunter` fails with browser errors

**Solution:**
```bash
pip install playwright
playwright install chromium
```

## Plugin Updates Breaking Things

**Common causes:**
1. Config schema changed — compare your config with `config/config.example.yaml`
2. Template changes — existing albums may use old format
3. Skill renamed or removed — check [CHANGELOG.md](../CHANGELOG.md)

## Skills Not Showing Up

**Check:**
1. Plugin installed correctly: `codex plugin list`
2. Skill files exist in the installed Codex plugin cache or in your local checkout under `skills/`
3. Try restarting Codex

## Still Stuck?

[Open an issue](https://github.com/Maxinger15/chatgpt-ai-music-skills/issues) with:
- What you tried to do
- What happened (error messages, unexpected behavior)
- Your OS and Codex version
- Relevant config (redact personal info)
