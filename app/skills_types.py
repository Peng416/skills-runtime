from dataclasses import dataclass
from typing import Optional,Dict,Any

@dataclass(frozen=True)
class SkillMeta:
    name: str
    description: str
    path: str
    skill_md_path: str
    license: Optional[str] = None
    compatibility: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass(frozen=True)
class SkillFull:
    meta: SkillMeta
    body_markdown: str
    raw_markdown: str