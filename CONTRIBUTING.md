# Contributing to chatgpt-ai-music-skills

Thank you for contributing! This document explains our development workflow.

## Branch Model

We use a **two-branch model** with `develop` as the integration branch and `main` as the stable release branch:

- **`develop`** — active development, receives feature branch PRs, version tagged with `-dev` suffix (e.g., `0.62.0-dev`)
- **`main`** — stable releases only, receives merges from `develop` when ready to release

CI runs on pushes to `develop` and on PRs into both branches. **PRs targeting `main` must come from `develop`** — PRs from feature branches or forks into `main` will be blocked by the "PR Target Gate" check. Always target `develop` for contributions.

**Plugin distribution channels** (both use `.agents/plugins/marketplace.json`, branch separation handles the split):
- Stable: `codex plugin marketplace add Maxinger15/chatgpt-ai-music-skills` (from `main`)
- Dev: `codex plugin marketplace add Maxinger15/chatgpt-ai-music-skills --ref develop`

## Development Workflow

We use a **PR-based workflow** with the following process:

### 1. Create a Feature Branch

```bash
# Create branch from develop
git checkout develop
git pull origin develop
git checkout -b feat/your-feature-name  # or fix/, docs/, chore/
```

**Branch naming conventions:**
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `chore/` - Maintenance tasks

### 2. Set Up Local Development

```bash
make test    # creates .venv, installs deps, runs tests with coverage
```

That's it. The Makefile handles venv creation and dependency installation automatically. Other useful targets:

```bash
make lint    # ruff + bandit + mypy
make check   # lint + test (full pre-PR check)
make clean   # remove venv and caches
```

### 3. Make Your Changes

Follow the existing code patterns and documentation style.

**Key files to update:**
- If adding a skill: Create `/skills/your-skill/SKILL.md`
- If changing workflow: Update `AGENTS.md`
- If user-facing: Update `README.md`
- Always: Update `CHANGELOG.md` under "Unreleased"

#### Adding a New Skill - Complete Checklist

When adding a new skill, you MUST update all of these files:

**Required (skill won't work without these):**
- [ ] Create `/skills/your-skill/SKILL.md` with skill documentation
- [ ] Add entry to `AGENTS.md` skills table (alphabetically in correct category)
- [ ] Add entry to `skills/help/SKILL.md` in appropriate category
- [ ] Add entry to `skills/help/SKILL.md` Common Workflows section (if applicable)
- [ ] Update `CHANGELOG.md` under "Unreleased" → "Added"

**Recommended:**
- [ ] Add entry to `reference/SKILL_INDEX.md` (alphabetical table + decision tree + skill categories)
- [ ] Add entry to `reference/complexity-strategy.md` under appropriate complexity tier
- [ ] Add quick tip to `skills/help/SKILL.md` Quick Tips section (if relevant)
- [ ] Update workflow diagram in `AGENTS.md` (if part of main workflow)
- [ ] Add to Album Completion Checklist in `AGENTS.md` (if part of release)
- [ ] Add reference docs in `/reference/` if complex
- [ ] Update `README.md` Skills Reference tables (add to appropriate section: Core Production, Research, Quality Control, Release, or Setup & Maintenance)

**Testing:**
- [ ] Run `$maxinger15-music:test all` to ensure no regressions
- [ ] Test skill invocation: `$maxinger15-music:your-skill`
- [ ] Verify skill appears in `$maxinger15-music:help` output
- [ ] Check skill in skills table works as expected

**Common mistakes to avoid:**
- ❌ Forgetting to add skill to help system
- ❌ Not updating CHANGELOG.md
- ❌ Adding to AGENTS.md but not help/SKILL.md
- ❌ Inconsistent naming between files
- ❌ Breaking alphabetical order in lists

### 4. Test Your Changes

```bash
make test    # or: make check (lint + test)
```

All tests must pass before submitting PR.

### 5. Commit Your Changes

We use [Conventional Commits](https://conventionalcommits.org/).

**Format:**
```
<type>(<scope>): <description>

<body>

Co-Authored-By: Codex <noreply@openai.com>
```

**Examples:**
```bash
git commit -m "feat: add sheet-music-publisher skill

Add comprehensive sheet music generation workflow...

Co-Authored-By: Codex <noreply@openai.com>"

git commit -m "fix: correct audio path in import-audio skill

Was missing artist folder in path construction.

Co-Authored-By: Codex <noreply@openai.com>"
```

**Commit types:**
| Type | Version Bump | Example |
|------|--------------|---------|
| `feat:` | MINOR | New feature/skill |
| `fix:` | PATCH | Bug fix |
| `feat!:` | MAJOR | Breaking change |
| `docs:` | None | Documentation only |
| `chore:` | None | Maintenance |

### 6. Push and Create PR

```bash
git push origin feat/your-feature-name
```

Then create a PR targeting **`develop`** (not `main`).

### 7. PR Review Process

**Automated checks (run on GitHub Actions):**
- JSON/YAML validation
- Version sync check (plugin.json vs marketplace.json)
- SKILL.md structure validation

**Required before merge to `develop`:**
- [ ] All automated checks pass
- [ ] `$maxinger15-music:test all` passes locally (run before submitting PR)
- [ ] Follows Conventional Commits
- [ ] CHANGELOG.md updated under "Unreleased"
- [ ] Documentation updated
- [ ] No breaking changes (unless MAJOR bump)
- [ ] Migration note added if applicable (see below)

#### When to Add a Migration Note

If your PR introduces filesystem changes (new directories, moved files), dependency changes, template changes that affect existing albums, or config changes, add a migration file in `migrations/`:

1. Create `migrations/<version>.md` (use the version this will ship in)
2. Add YAML frontmatter with `version`, `summary`, `categories`, `actions`
3. Add markdown body with context
4. See `migrations/README.md` for format details and action types

### 8. Release to Stable

When `develop` is ready to release:

1. Create a PR from `develop` → `main`
2. Update `.codex-plugin/plugin.json` version (drop `-dev` suffix)
3. Move CHANGELOG.md entries from "Unreleased" to a versioned heading
4. Merge PR to `main`
5. After merge, bump `develop` to the next `-dev` version (e.g., `0.63.0-dev`)

**Version bumping:**
- `feat:` → Increment MINOR (0.3.0 → 0.4.0)
- `fix:` → Increment PATCH (0.3.0 → 0.3.1)
- `feat!:` → Increment MAJOR (0.3.0 → 1.0.0)

**Version file:**
- `.codex-plugin/plugin.json` — plugin version

## Testing

### Running Tests Locally

```bash
make test     # run tests with coverage (creates .venv if needed)
make lint     # ruff + bandit + mypy
make check    # lint + test (full pre-PR check)
make clean    # remove .venv and caches
```

The Makefile manages a `.venv/` directory automatically. If dependencies in `requirements.txt` or `requirements-test.txt` change, `make test` will reinstall them.

You can also use the `$maxinger15-music:test` skill inside a Codex session:

```bash
$maxinger15-music:test all         # all categories
$maxinger15-music:test skills      # skill structure tests
$maxinger15-music:test consistency # cross-reference checks
```

### Adding New Tests

When fixing bugs, add a regression test:

1. Open `skills/test/SKILL.md`
2. Find the appropriate category
3. Add a test that would have caught the bug
4. Verify it fails before your fix
5. Verify it passes after your fix

## Development Mode (Local Marketplace)

When developing locally, add this checkout as a Codex marketplace source and install `maxinger15-music` from that source. `run.py` derives the plugin root from its own path, so the MCP server runs from the local checkout.

**Before testing the local marketplace:**

```bash
# Option A: Remove the cached plugin
rm -rf ~/.codex/plugins/cache/maxinger15-music

# Option B: Uninstall first
codex plugin remove maxinger15-music
```

**Then install from the local checkout:**

```bash
codex plugin marketplace add /path/to/chatgpt-ai-music-skills
codex plugin add maxinger15-music@maxinger15-local
```

**After dev testing**, re-install the plugin normally to restore the cached version.

## Code Style

- **Python scripts:** Follow PEP 8
- **Markdown:** Use 2-space indentation for lists
- **YAML:** Use 2-space indentation
- **Line length:** 120 characters max for code, no limit for docs

## Questions?

- Check existing skills in `/skills/` for examples
- Read `AGENTS.md` for workflow documentation
- Open an issue for clarification

## License

By contributing, you agree to license your contribution under the CC0-1.0 license.
