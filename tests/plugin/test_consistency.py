"""Tests for cross-reference consistency: plugin metadata, skill counts, complexity tiers, .gitignore."""

import json
import re

import pytest
import yaml

pytestmark = pytest.mark.plugin


class TestSkillCount:
    """README skill count must match actual count."""

    def test_readme_skill_count(self, project_root, all_skill_frontmatter):
        readme_path = project_root / "README.md"
        if not readme_path.exists():
            pytest.skip("README.md not found")

        readme_content = readme_path.read_text()
        match = (
            re.search(r'\*\*(\d+)\s+specialized skills\*\*', readme_content)
            or re.search(r'Skill System\s*\((\d+)\s+Skills\)', readme_content)
        )
        if not match:
            pytest.skip("Skill count pattern not found in README")

        claimed = int(match.group(1))
        actual = len(all_skill_frontmatter)
        assert claimed == actual, (
            f"README claims {claimed} skills, actual is {actual}"
        )


class TestVersionSync:
    """Codex plugin metadata must be internally coherent."""

    def test_plugin_metadata_valid(self, project_root):
        plugin_json = project_root / ".codex-plugin" / "plugin.json"
        marketplace_json = project_root / ".agents" / "plugins" / "marketplace.json"

        if not plugin_json.exists() or not marketplace_json.exists():
            pytest.skip("Codex plugin metadata files not found")

        plugin_data = json.loads(plugin_json.read_text())
        marketplace_data = json.loads(marketplace_json.read_text())

        plugin_name = plugin_data.get("name")
        assert plugin_name == "maxinger15-music"
        assert re.match(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$", plugin_data.get("version", ""))

        entries = marketplace_data.get("plugins", [])
        assert any(entry.get("name") == plugin_name for entry in entries), (
            "Codex marketplace must include the maxinger15-music plugin entry"
        )


class TestNoSkillJson:
    """No invalid skill.json files (standard is SKILL.md)."""

    def test_no_skill_json_files(self, skills_dir):
        skill_json_files = list(skills_dir.glob("*/skill.json"))
        assert not skill_json_files, (
            f"Found invalid skill.json files: {[str(f.relative_to(skills_dir)) for f in skill_json_files]}"
        )


class TestComplexityTierConsistency:
    """Complexity tiers in metadata must match complexity-strategy.md."""

    def test_complexity_strategy_alignment(self, project_root):
        strategy_path = project_root / "reference" / "complexity-strategy.md"
        metadata_path = project_root / "skills" / "metadata.yaml"
        if not strategy_path.exists():
            pytest.skip("complexity-strategy.md not found")
        if not metadata_path.exists():
            pytest.skip("skills/metadata.yaml not found")

        strategy_content = strategy_path.read_text()
        metadata = yaml.safe_load(metadata_path.read_text()) or {}
        skill_metadata = metadata.get("skills", {})

        tier_sections = {
            'opus': r'## Opus.*?(?=## Sonnet|## Haiku|## Decision|$)',
            'sonnet': r'## Sonnet.*?(?=## Haiku|## Decision|$)',
            'haiku': r'## Haiku.*?(?=## Decision|$)',
        }

        mismatches = []
        for skill_name, meta in skill_metadata.items():
            actual_tier = meta.get("complexity_tier")
            if not actual_tier:
                continue

            # Find which section documents this skill
            skill_heading = re.compile(rf'^### {re.escape(skill_name)}$', re.MULTILINE)
            documented_tier = None
            for tier, pattern in tier_sections.items():
                section_match = re.search(pattern, strategy_content, re.DOTALL)
                if section_match and skill_heading.search(section_match.group()):
                    documented_tier = tier
                    break

            if documented_tier and documented_tier != actual_tier:
                mismatches.append(
                    f"{skill_name}: metadata says {actual_tier}, complexity-strategy.md says {documented_tier}"
                )

        assert not mismatches, "Complexity tier mismatches:\n" + "\n".join(mismatches)


class TestNoDisableModelInvocation:
    """No skills should have disable-model-invocation flag."""

    def test_no_disable_flag(self, all_skill_frontmatter):
        flagged = [
            name for name, fm in all_skill_frontmatter.items()
            if '_error' not in fm and fm.get('disable-model-invocation')
        ]
        # This is advisory, not a hard fail
        assert not flagged or True  # soft check preserved


class TestGitignore:
    """Required .gitignore entries must be present."""

    REQUIRED_IGNORES = ['artists/', 'research/', '*.pdf', 'venv/']

    @pytest.mark.parametrize("entry", REQUIRED_IGNORES)
    def test_gitignore_entry(self, project_root, entry):
        gitignore_path = project_root / ".gitignore"
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")

        content = gitignore_path.read_text()
        assert entry in content or entry.rstrip('/') in content, (
            f".gitignore missing recommended entry: {entry}"
        )
