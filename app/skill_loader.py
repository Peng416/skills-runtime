from __future__ import annotations

import os
import re
from typing import List, Tuple, Optional

import yaml

from .skills_types import SkillMeta, SkillFull

#skills规范要求，必须有YAML frontmatter,  name 有命名约束且要和目录名称一致

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")  # 简化版：避免 --，避免首尾 -

def _split_frontmatter(markdown: str) -> Tuple[dict, str]:
    #检查提取YAML frontmatter
    m = _FRONTMATTER_RE.match(markdown)
    if not m:
        raise ValueError("Missing YAML frontmatter. Expect '---\\n...\\n---' at top of SKILL.md")
    fm_text, body = m.group(1), m.group(2)
    frontmatter = yaml.safe_load(fm_text) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must be a YAML mapping/object.")
    return frontmatter, body

def _validate_name(name: str, folder_name: str) -> None:
    #验证skill名称是否符合命名规范
    if not name or not isinstance(name, str):
        raise ValueError("Frontmatter 'name' must be a non-empty string.")
    if len(name) > 64:
        raise ValueError("Frontmatter 'name' too long (max 64).")
    if not _NAME_RE.match(name):
        raise ValueError("Frontmatter 'name' must be lowercase letters/numbers/hyphens only.")
    if name != folder_name:
        raise ValueError(f"Skill name '{name}' must match folder name '{folder_name}'.")

def discover_skills(skills_root: str) -> List[SkillMeta]:
    #发现skills并返回元数据
    metas: List[SkillMeta] = []
    if not os.path.isdir(skills_root):
        return metas

    for entry in sorted(os.listdir(skills_root)):
        skill_dir = os.path.join(skills_root, entry)
        if not os.path.isdir(skill_dir):
            continue
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue

        raw = open(skill_md, "r", encoding="utf-8").read()
        fm, _body = _split_frontmatter(raw)

        name = fm.get("name")
        desc = fm.get("description")
        _validate_name(name, entry)

        if not desc or not isinstance(desc, str) or len(desc) > 1024:
            raise ValueError(f"Skill '{name}' has invalid description (1-1024 chars).")

        metas.append(
            SkillMeta(
                name=name,
                description=desc,
                path=skill_dir,
                skill_md_path=skill_md,
                license=fm.get("license"),
                compatibility=fm.get("compatibility"),
                metadata=fm.get("metadata"),
            )
        )
    return metas

def load_skill_full(meta: SkillMeta) -> SkillFull:
    #加载完整的skill
    print(f'加载skill, 元数据: {meta}')
    raw = open(meta.skill_md_path, "r", encoding="utf-8").read()
    _fm, body = _split_frontmatter(raw)
    return SkillFull(meta=meta, body_markdown=body, raw_markdown=raw)

def read_skill_relative_file(meta: SkillMeta, relative_path: str) -> str:
    #读取skill内的相对路径文件
    # 安全：限制只能读取 skill 内的一层相对路径（符合规范建议）:contentReference[oaicite:8]{index=8}
    if relative_path.startswith("/") or ".." in relative_path.replace("\\", "/"):
        raise ValueError("Invalid relative path.")
    full = os.path.normpath(os.path.join(meta.path, relative_path))
    if not full.startswith(os.path.normpath(meta.path)):
        raise ValueError("Path escapes skill directory.")
    if not os.path.isfile(full):
        raise FileNotFoundError(relative_path)
    return open(full, "r", encoding="utf-8").read()
