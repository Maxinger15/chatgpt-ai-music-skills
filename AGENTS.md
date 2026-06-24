# AI Music Skills - Codex Instructions

This is an AI music generation workflow using Suno. Skills contain domain expertise; this file contains workflow rules and structure that apply every session.

---

## ⚠️ CRITICAL: Finding Albums When User Mentions Them

**WHENEVER the user mentions an album name**, use the resume skill:
```
$maxinger15-music:resume my-album
```

**If skill unavailable**, manual approach:
1. Read `~/.maxinger15-music/cache/state.json` — search `state.albums` keys (case-insensitive)
2. If cache missing/stale: read config → glob `{content_root}/artists/{artist}/albums/*/*/README.md` → rebuild cache with `rebuild_state()` MCP tool

**DO NOT**: search from cwd, use complex globs, assume paths, or use `ls`/`find`.

---

## Configuration & Path Resolution

Config is **always** at: `~/.maxinger15-music/config.yaml`

**ALWAYS read config fresh before** moving/creating files, resolving path variables, or using artist name in paths. Never assume or remember values.

**Path variables** (from config):
- `{content_root}` = `paths.content_root`
- `{audio_root}` = `paths.audio_root`
- `{documents_root}` = `paths.documents_root`
- `{tools_root}` = `~/.maxinger15-music`
- `{plugin_root}` = the directory containing this AGENTS.md file (= `{plugin_root}` in skills)
- `[artist]` = `artist.name`

**IMPORTANT — Mirrored path structure**:
```
{content_root}/artists/[artist]/albums/[genre]/[album]/   # Album files (in git)
{audio_root}/artists/[artist]/albums/[genre]/[album]/     # Mastered audio
{documents_root}/artists/[artist]/albums/[genre]/[album]/ # PDFs (not in git)
```
Audio and document paths include `[artist]/` after the root. Common mistake: omitting the artist folder.

First-time setup: `cp config/config.example.yaml ~/.maxinger15-music/config.yaml` — see `config/README.md`.

---

## MCP Server — Preferred Data Access

The `maxinger15-music-mcp` server is the **preferred way to query project state**. Use MCP tools instead of reading files directly — they're faster (single call vs multiple file reads) and return structured data.

**Use MCP tools for:**
- **Albums/tracks** → `list_albums`, `find_album`, `get_track` (not reading state.json or globbing for READMEs)
- **Skills** → `list_skills`, `get_skill` (not reading individual SKILL.md files)
- **Ideas** → `get_ideas` (not reading IDEAS.md)
- **Pending verifications** → `get_pending_verifications`
- **Config** → `get_config` (not reading config.yaml for simple lookups)
- **Session context** → `get_session`, `update_session`
- **Cross-scope search** → `search`
- **Stale cache** → `rebuild_state`

**Fall back to direct file access only when:** MCP server is unavailable, you need to edit files (MCP is read-only), or you need raw file content not exposed through MCP (e.g., full lyrics, research docs).

---

## Session Start

At the beginning of a fresh session:

1. **Verify setup** — Quick dependency check:
   ```bash
   ~/.maxinger15-music/venv/bin/python3 -c "import mcp" 2>&1 >/dev/null && echo "✅ MCP ready" || echo "❌ MCP missing"
   ```
   - If MCP missing → **Stop immediately** and suggest: `$maxinger15-music:setup mcp`
   - If config missing → suggest: `$maxinger15-music:configure`
   - Don't proceed with session start until setup is complete
1.5. **Health check** — Use `health_check` MCP tool (checks venv + skill registration):
   - Venv `status: "ok"` → continue silently
   - Venv `status: "stale"` → warn with mismatches and fix command, continue session
   - Venv `status: "no_venv"` → **stop** and suggest `$maxinger15-music:setup`
   - Venv `status: "error"` → warn and continue
   - Skills `status: "ok"` → continue silently
   - Skills `status: "stale"` → warn with missing Codex metadata files and fix message, continue session
2. **Load config** — Read `~/.maxinger15-music/config.yaml`. If missing, tell user to run `$maxinger15-music:configure`.
3. **Load overrides** — Check `paths.overrides` (default: `{content_root}/overrides`):
   - `{overrides}/AGENTS.md` → incorporate instructions
   - `{overrides}/pronunciation-guide.md` → merge with base guide
   - Skip silently if missing (overrides are optional)
4. **Load state via MCP** — Use MCP tools to query project state:
   - `get_config` → verify config is loaded
   - `list_albums` → get album statuses
   - `get_ideas` → get idea counts
   - `get_pending_verifications(summary_only=True)` → check for pending source verifications (count only)
   - `get_session` → resume last session context
   - If MCP returns errors about missing/stale cache → `rebuild_state()` MCP tool
4.5. **Check for plugin upgrades** — Compare `plugin_version` in state.json vs `.codex-plugin/plugin.json`:
   - If `plugin_version` is null → first run, set to current version, skip migrations
   - If stored < current → read `{plugin_root}/migrations/*.md` for applicable versions, process actions
   - If versions match → no action
5. _(Removed — skills use tier aliases (`opus`/`sonnet`/`haiku`) that auto-track the frontier model, and the test suite (`$maxinger15-music:test`) enforces model/effort hygiene, so no action is needed on new releases.)_
6. **Report from MCP state**:
   - Health warnings (from step 1.5 — omit if ok):
     - Venv stale: "⚠️ Venv has N outdated package(s): pkg1 (1.0.0 → 1.1.0), ... Run: `~/.maxinger15-music/venv/bin/pip install -r .../requirements.txt`"
     - Skills stale: "⚠️ Codex plugin metadata is incomplete — repair `.codex-plugin/plugin.json` / `.agents/plugins/marketplace.json`, then restart Codex or reinstall with `codex plugin add maxinger15-music@maxinger15-local`"
   - Album ideas (from `get_ideas`)
   - In-progress albums (status: "In Progress", "Research Complete", "Complete")
   - Pending source verifications (from `get_pending_verifications(summary_only=True)`)
   - Last session context (from `get_session`)
7. **Show contextual tips** based on state:
   - No albums → suggest `$maxinger15-music:tutorial`
   - Ideas exist → suggest `$maxinger15-music:album-ideas list`
   - In-progress albums → suggest `$maxinger15-music:resume [album-name]`
   - Overrides loaded → note it; missing → suggest creating them (see `config/README.md` for override file reference)
   - Pending verifications → warn and suggest `$maxinger15-music:verify-sources`
   - One contextual tip from: resume, researcher, pronunciation, clipboard, mastering (pick based on most relevant album state)
8. **Ask**: "What would you like to work on?"

---

## Core Principles

**Be a collaborator, not a yes-man.** Push back when ideas don't work. The goal is good music, not agreement.

**Preserve exact casing and spelling.** "maxinger15" stays "maxinger15" — never auto-capitalize user-provided names, titles, or text.

**Ask when unsure.** Word choice, style, structure, Suno settings — don't guess.

**Pronunciation hard rule**: Suno CANNOT infer pronunciation from context. When any homograph is found (live, read, lead, wound, close, bass, tear, wind, etc.), **ASK** the user which pronunciation is intended — never assume. Fix with phonetic spelling in Suno lyrics only. See `/skills/lyric-writer/SKILL.md` and `/reference/suno/pronunciation-guide.md` for full rules.

**After writing or revising lyrics**, run the 13-point quality checklist from `/skills/lyric-writer/SKILL.md`. Report violations without being asked.

**When user says "let's work on [track]"**, scan full lyrics for issues BEFORE doing anything else: weak lines, prosody problems, POV/tense inconsistencies, twin verses, missing hook, factual errors, flow/pronunciation risks.

---

## Workflow Overview

Concept → Research → Write (+Suno Prompt) → [Refine] → QC/Verify → Generate → [Polish] → Master → Promo Videos (optional) → Promo Copy (optional) → **Release**

**Critical**: Research must complete before writing for source-based content. Human source verification is required before generation — never skip this gate.

### Key Routing Rules

- **Album mentioned** → `$maxinger15-music:resume`
- **"Make a new album"** → IMMEDIATELY use `$maxinger15-music:new-album` BEFORE any discussion
- **"Turn idea into album" / "promote [idea]"** → `$maxinger15-music:promote-idea "<idea title>"` (one-shot: creates album from a Pending idea, injects concept, updates status)
- **Writing lyrics** → apply `$maxinger15-music:lyric-writer` expertise (auto-invokes suno-engineer)
- **Refining/polishing lyrics** → `$maxinger15-music:lyric-refiner` (post-writing multi-pass refinement)
- **Planning album** → apply `$maxinger15-music:album-conceptualizer` (7 planning phases required)
- **Suno prompts** → apply `$maxinger15-music:suno-engineer` expertise (usually auto-invoked by lyric-writer; use directly only for re-prompting)
- **Research needed** → apply `$maxinger15-music:researcher` standards
- **Polishing audio / fixing Suno artifacts** → apply `$maxinger15-music:mix-engineer` expertise
- **Mastering audio** → polish first via `$maxinger15-music:mix-engineer`, then apply `$maxinger15-music:mastering-engineer` standards. Skip polish only if: (a) user says "master only", "skip polish", or "already polished"; or (b) polished audio already exists at `{audio_root}/artists/[artist]/albums/[genre]/[album]/polished/`. Applies equally to single-track and whole-album mastering.
- **Album art** → apply `$maxinger15-music:album-art-director`
- **Writing promo copy** → apply `$maxinger15-music:promo-writer` expertise
- **Releasing** → apply `$maxinger15-music:release-director`

- **Checking for plagiarism** → `$maxinger15-music:plagiarism-checker` (web search + LLM knowledge)
- **Checking voice/authenticity** → `$maxinger15-music:voice-checker` (detect AI-sounding patterns)
- **Verifying sources** → `$maxinger15-music:verify-sources` (human verification gate)
- **"What skills do X?"** → `list_skills` / `get_skill` MCP tools (not reading SKILL.md files)

Skills contain the deep expertise. See `/reference/SKILL_INDEX.md` for the full decision tree.

### Duration Planning

Album target duration set during Phase 3 (Sonic Direction). Tracks inherit unless overridden.
**Lookup**: Track `Target Duration` → Album `Target Duration` → Genre default (craft-reference.md)

### Source Verification Gate

1. Capture sources FIRST — every source must be a clickable markdown link `[Name](URL)`
2. Save RESEARCH.md and SOURCES.md to album directory (never cwd)
3. After adding sources → status: `❌ Pending` → human verifies via `$maxinger15-music:verify-sources` → `✅ Verified (DATE)`
4. Block generation if verification incomplete — `$maxinger15-music:pre-generation-check` enforces this

### Status Tracking

**Track statuses** (in order):
`Not Started` → `Sources Pending` → `Sources Verified` → `In Progress` → `Generated` → `Final`

- `Not Started`: No work begun on this track
- `Sources Pending`: Sources gathered, awaiting human verification
- `Sources Verified`: Human confirmed all sources via `$maxinger15-music:verify-sources`
- `In Progress`: Lyrics being written or revised
- `Generated`: Track generated on Suno, audio exists. User listens and either approves (mark ✓ in Generation Log → advance to `Final`) or rejects (see Regeneration Workflow below)
- `Final`: Approved and ready for mastering

**Album statuses** — two flows depending on album type:

**Documentary/true-story albums** (full flow):
`Concept` → `Research Complete` → `Sources Verified` → `In Progress` → `Complete` → `Released`

**Standard albums** (non-documentary, skip research statuses):
`Concept` → `In Progress` → `Complete` → `Released`

- `Concept`: Initial planning, album README created
- `Research Complete`: All research done, sources gathered (documentary albums only)
- `Sources Verified`: Human verified all track sources (documentary albums only)
- `In Progress`: Active writing/generation work
- `Complete`: All tracks Final, ready for mastering/release
- `Released`: Published to streaming platforms

**Transition rules**: Album status advances when ALL tracks reach the corresponding level. A single unverified track keeps the album from advancing past "Research Complete".

**Auto-advancement**: Skills that complete a phase should advance the album status automatically:
- `$maxinger15-music:verify-sources` → when all tracks verified, advance album to `Sources Verified`
- When all tracks are `Final` → album advances to `Complete`

**Batch operations**: To mark all Generated tracks as Final after QA, use `update_track_field(album_slug, track_slug, "status", "Final")` for each track via MCP, or ask Codex to batch-approve all tracks when all have ✓ in their Generation Logs.

### Regeneration Workflow

When a user rejects a generated track (doesn't like the result, wrong style, pronunciation issues, etc.):

1. **Log the rejection**: Add a row in the Generation Log with the reason (e.g., "wrong tempo", "vocal too high", "mispronounced name")
2. **Decide the fix path**:
   - **Style issue** (wrong genre, tempo, mood) → Revise Style Box via `$maxinger15-music:suno-engineer`, then regenerate on Suno
   - **Lyrics issue** (wrong words, pronunciation) → Fix lyrics via `$maxinger15-music:lyric-writer`, re-run `$maxinger15-music:pronunciation-specialist`, then regenerate
   - **Suno interpretation** (right prompt, wrong result) → Regenerate on Suno with same settings (Suno is non-deterministic)
3. **Regenerate**: Generate again on Suno, log the new attempt
4. **When satisfied**: Mark the keeper with ✓ in the Generation Log Rating column, then advance Status to `Final`

**Status stays `Generated`** during regeneration — no backward transition needed. The Generation Log tracks all attempts. A track is only `Final` when it has a ✓ in the Rating column.

**Quick reference**: `resume` and `next-step` detect Generated tracks without a ✓ rating and recommend the appropriate regeneration action.

See `/reference/workflows/error-recovery.md` for detailed recovery procedures.

See `/reference/state-schema.md` for the full state cache schema.

---

## Content Structure

Albums: `{content_root}/artists/[artist]/albums/[genre]/[album]/`
Templates: `{plugin_root}/templates/` — use for all new content
Research staging: `{content_root}/research/` (move to album directory once album exists)

**Album directory layout:**
```
{album}/
├── README.md
├── SOURCES.md        # (documentary albums)
├── RESEARCH.md       # (documentary albums)
├── tracks/
│   ├── 01-track-name.md
│   └── ...
└── promo/            # Social media copy
    ├── campaign.md
    ├── twitter.md
    ├── instagram.md
    ├── tiktok.md
    ├── facebook.md
    └── youtube.md
```

Track files: zero-padded (`01-`, `02-`). Import with `$maxinger15-music:import-track`, `$maxinger15-music:import-audio`.

`promo_videos/` in `{audio_root}` holds video files (unchanged). `promo/` in album directory holds social media copy (text).

Currently supports **Suno** (default). Service-specific template sections marked with `<!-- SERVICE: suno -->`.

---

## Versioning & Development

[Semantic Versioning](https://semver.org/) with [Conventional Commits](https://conventionalcommits.org/).

| Prefix | Version Bump |
|--------|--------------|
| `feat:` | MINOR |
| `fix:` | PATCH |
| `feat!:` | MAJOR |
| `docs:`, `chore:` | None |

**Co-author line**: `Co-Authored-By: Codex <noreply@openai.com>`

**Version file**: `.codex-plugin/plugin.json`; marketplace discovery lives in `.agents/plugins/marketplace.json`

**Release process**: Update CHANGELOG.md `[Unreleased]` → `[0.x.0 - DATE]`, update `.codex-plugin/plugin.json`, update README "What's New" table if notable. Commit: `chore: release 0.x.0`

**Development workflow**: Feature branch off `develop` → Conventional Commits → `$maxinger15-music:test all` → PR into `develop` → Release: merge `develop` → `main`. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

**Pre-push gate**: **ALWAYS run `make check` before `git push`.** This runs the same `ruff` + `bandit` + `mypy` + `pytest` suite that CI runs in the Lint and Tests jobs (see `Makefile` + `.github/workflows/test.yml`). `make lint` alone is fine for a quick type-check. Running targeted `pytest tests/unit/…` and file-scoped `ruff check` is NOT equivalent — `make` spins up `.venv` from `requirements.txt + requirements-test.txt` so mypy sees real (not stubbed) third-party types, which is what CI sees. If `make check` fails, fix the root cause; do not push and hope CI catches a different picture.

**External contributor PRs**: When the user mentions merging, reviewing, or having merged a PR from a non-maintainer (anyone other than @maxinger15-music), check the Contributors section of README.md. If the PR author is not listed, proactively offer to add them using the same `<a href>` avatar block format as existing entries. Do this without being asked.

---

## Mid-Session Rules

**Workflow file changes take effect immediately.** Re-read after any edit to AGENTS.md or templates.

**Lessons learned protocol**: When you discover a technical issue during production (pronunciation error, rhyme violation, wrong assumption):
1. Fix the immediate issue
2. Sweep the album for the same issue
3. Propose a rule to prevent recurrence: "I found [issue]. Here's a rule: [rule]. Should I add it to [location]?"

**Self-updating skills**: When a skill discovers something new, it adds to the relevant reference file. User-specific content (pronunciations) goes to `{overrides}/` directory.

---

## Skills Catalog

Every non-system skill, alphabetically. (System skills `help`, `about`, `configure`, `test` are covered in Session Start and invoked directly without a dedicated entry.)

- `$maxinger15-music:album-art-director` - Visual concepts and AI art prompts for album covers
- `$maxinger15-music:album-conceptualizer` - Album concepts and tracklist architecture (7 planning phases)
- `$maxinger15-music:album-dashboard` - Visual album progress dashboard
- `$maxinger15-music:album-ideas` - Track and manage album ideas
- `$maxinger15-music:clipboard` - Copy track lyrics/prompts to clipboard
- `$maxinger15-music:cloud-uploader` - Upload promo videos to Cloudflare R2 or AWS S3
- `$maxinger15-music:document-hunter` - Automated document search and download
- `$maxinger15-music:explicit-checker` - Verify explicit content flags on tracks
- `$maxinger15-music:genre-creator` - Create and document a new genre reference
- `$maxinger15-music:health-check` - Verify venv + skill registration health
- `$maxinger15-music:import-art` - Place album art in correct locations
- `$maxinger15-music:import-audio` - Move audio files to album location
- `$maxinger15-music:import-track` - Move track .md files to album location
- `$maxinger15-music:lyric-refiner` - Multi-pass lyric refinement and refactoring
- `$maxinger15-music:lyric-reviewer` - Pre-generation QC gate (14-point checklist)
- `$maxinger15-music:lyric-writer` - Write/review lyrics, fix prosody
- `$maxinger15-music:mastering-engineer` - Audio mastering guidance for streaming targets
- `$maxinger15-music:mix-engineer` - Per-stem audio polish (cleanup, EQ, compression)
- `$maxinger15-music:new-album` - Create new album with directory structure
- `$maxinger15-music:next-step` - Get recommended next action for current album
- `$maxinger15-music:plagiarism-checker` - Check lyrics for phrases matching existing songs
- `$maxinger15-music:pre-generation-check` - Final pre-generation checkpoint (6 gates)
- `$maxinger15-music:promo-director` - Generate promo videos for social media
- `$maxinger15-music:promo-reviewer` - Review and revise social media promo copy
- `$maxinger15-music:promo-writer` - Write platform-specific social promo copy
- `$maxinger15-music:promote-idea` - Convert a Pending idea into a full album (one-shot)
- `$maxinger15-music:pronunciation-specialist` - Scan lyrics for Suno pronunciation risks
- `$maxinger15-music:release-director` - Release coordination and distribution
- `$maxinger15-music:rename` - Rename album/track and update all mirrored paths
- `$maxinger15-music:researcher` - Main research coordinator and fact-checking
- `$maxinger15-music:researchers-biographical` - Personal backgrounds
- `$maxinger15-music:researchers-financial` - SEC filings and market data
- `$maxinger15-music:researchers-gov` - DOJ/FBI/SEC releases
- `$maxinger15-music:researchers-historical` - Archives and timelines
- `$maxinger15-music:researchers-journalism` - Investigative articles
- `$maxinger15-music:researchers-legal` - Court documents and indictments
- `$maxinger15-music:researchers-primary-source` - Tweets, blogs, forums
- `$maxinger15-music:researchers-security` - Malware analysis and CVEs
- `$maxinger15-music:researchers-tech` - Project histories and changelogs
- `$maxinger15-music:researchers-verifier` - Quality control and citation validation
- `$maxinger15-music:resume` - Find an album and see status/next steps
- `$maxinger15-music:session-start` - Run session startup procedure
- `$maxinger15-music:setup` - Dependency/venv environment check and setup
- `$maxinger15-music:sheet-music-publisher` - Convert audio to sheet music
- `$maxinger15-music:suno-engineer` - Technical Suno prompting and genre selection
- `$maxinger15-music:tutorial` - Interactive guided album creation
- `$maxinger15-music:validate-album` - Validate album structure and paths
- `$maxinger15-music:verify-sources` - Human source-verification gate before generation
- `$maxinger15-music:voice-checker` - Detect AI-written patterns in lyrics and prose

