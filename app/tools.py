from __future__ import annotations

import json
from typing import Any, Dict, List

from .skill_loader import load_skill_full, read_skill_relative_file
from .skills_types import SkillMeta

def tool_schemas() -> List[Dict[str, Any]]:
    """
    OpenAI tool schema: list of {"type":"function", "function": {...}}
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "load_skill",
                "description": "Load a skill's SKILL.md instructions by skill name.",
                "parameters": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_skill_file",
                "description": "Read a referenced file inside a skill folder (e.g., references/xxx.md, assets/template.txt).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"},
                    },
                    "required": ["name", "path"],
                },
            },
        },
    ]

class ToolRuntime:
    """
    Runtime that actually executes tool calls.
    Keep it deterministic & safe.
    """
    def __init__(self, metas: List[SkillMeta]):
        self.metas_by_name = {m.name: m for m in metas}

    def dispatch(self, tool_name: str, args: Dict[str, Any]) -> str:
        if tool_name == "load_skill":
            out = self.load_skill(args["name"])
        elif tool_name == "read_skill_file":
            out = self.read_skill_file(args["name"], args["path"])
        else:
            out = {"error": f"Unknown tool: {tool_name}"}
        return json.dumps(out, ensure_ascii=False)

    def load_skill(self, name: str) -> Dict[str, Any]:
        meta = self._get(name)
        full = load_skill_full(meta)
        # 你可以只返回 body_markdown；这里先返回 raw 方便调试
        return {"name": name, "skill_md": full.raw_markdown}

    def read_skill_file(self, name: str, path: str) -> Dict[str, Any]:
        meta = self._get(name)
        content = read_skill_relative_file(meta, path)
        return {"name": name, "path": path, "content": content}

    def _get(self, name: str) -> SkillMeta:
        if name not in self.metas_by_name:
            raise KeyError(f"Unknown skill: {name}")
        return self.metas_by_name[name]
