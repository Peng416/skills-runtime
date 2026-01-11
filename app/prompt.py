from __future__ import annotations
from typing import List
from xml.sax.saxutils import escape

from .skills_types import SkillMeta

def build_available_skills_xml(metas: List[SkillMeta]) -> str:
    """
    Build an <available_skills> XML block containing each skill's name/description.

    Why XML?
    - It's structured, easy for models to parse.
    - Matches the common "skills registry" prompt pattern.
    """
    lines = ["<available_skills>"]
    for m in metas:
        lines.append("  <skill>")
        lines.append(f"    <name>{escape(m.name)}</name>")
        lines.append(f"    <description>{escape(m.description)}</description>")
        lines.append("  </skill>")
    lines.append("</available_skills>")
    print("\n".join(lines))
    return "\n".join(lines)

def build_system_prompt(metas):
    skills_xml = build_available_skills_xml(metas)
    return (
        "You are a helpful agent with access to Agent Skills.\n\n"
        "Workflow you MUST follow:\n"
        "1) Read <available_skills> and decide whether a skill is needed.\n"
        "2) If a skill is needed, call load_skill(name) with the chosen skill.\n"
        "   - Do NOT answer yet.\n"
        "3) After you receive the skill content, follow SKILL.md strictly.\n"
        "4) Do NOT invent instructions. Only use what you read.\n\n"
        f"{skills_xml}\n"
    )
