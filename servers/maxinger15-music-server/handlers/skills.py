"""Skills listing tools — query and filter plugin skills."""

from __future__ import annotations

from typing import Any

from handlers import _shared
from handlers._shared import _normalize_slug, _safe_json


async def list_skills(
    complexity_filter: str = "",
    category: str = "",
    model_filter: str = "",
) -> str:
    """List all skills with optional filtering.

    Args:
        complexity_filter: Filter by advisory complexity tier ("opus", "sonnet", "haiku").
        category: Filter by keyword in description (case-insensitive substring match)
        model_filter: Deprecated alias for complexity_filter.

    Returns:
        JSON with skills list, count, and complexity_counts
    """
    state = _shared.cache.get_state()
    skills = state.get("skills", {})
    items = skills.get("items", {})

    result_items = []
    tier_filter = complexity_filter or model_filter
    for name, skill in sorted(items.items()):
        # Apply advisory complexity filter.
        if tier_filter and skill.get("complexity_tier", "").lower() != tier_filter.lower():
            continue

        # Apply category/description filter
        if category:
            description = skill.get("description", "").lower()
            if category.lower() not in description:
                continue

        result_items.append({
            "name": name,
            "description": skill.get("description", ""),
            "complexity_tier": skill.get("complexity_tier", "unknown"),
            "complexity_label": skill.get("complexity_label", ""),
            "complexity_effort": skill.get("complexity_effort"),
            "user_invocable": skill.get("user_invocable", True),
            "argument_hint": skill.get("argument_hint"),
        })

    return _safe_json({
        "skills": result_items,
        "count": len(result_items),
        "total": skills.get("count", 0),
        "complexity_counts": skills.get("complexity_counts", {}),
    })


async def get_skill(name: str) -> str:
    """Get full detail for a specific skill.

    Args:
        name: Skill name, slug, or partial match (e.g., "lyric-writer", "lyric")

    Returns:
        JSON with skill data, or error with available skills
    """
    state = _shared.cache.get_state()
    skills = state.get("skills", {})
    items = skills.get("items", {})

    if not items:
        return _safe_json({
            "found": False,
            "error": "No skills in state cache. Run rebuild_state first.",
        })

    normalized = _normalize_slug(name)

    # Exact match first
    if normalized in items:
        return _safe_json({
            "found": True,
            "name": normalized,
            "skill": items[normalized],
        })

    # Fuzzy match: substring match on skill names
    matches = {
        skill_name: data
        for skill_name, data in items.items()
        if normalized in skill_name or skill_name in normalized
    }

    if len(matches) == 1:
        skill_name = next(iter(matches))
        return _safe_json({
            "found": True,
            "name": skill_name,
            "skill": matches[skill_name],
        })
    elif len(matches) > 1:
        return _safe_json({
            "found": False,
            "multiple_matches": list(matches.keys()),
            "error": f"Multiple skills match '{name}': {', '.join(matches.keys())}",
        })
    else:
        return _safe_json({
            "found": False,
            "available_skills": sorted(items.keys()),
            "error": f"No skill found matching '{name}'",
        })


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register(mcp: Any) -> None:
    """Register skills listing tools with the MCP server."""
    mcp.tool()(list_skills)
    mcp.tool()(get_skill)
