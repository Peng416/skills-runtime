import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    skills_dir: str = os.environ.get("SKILLS_DIR", "./skills")
    openai_model: str = os.environ.get("OPENAI_MODEL", "deepseek-v3.2")
    openai_token: str = os.environ.get("OPENAI_TOKEN", "")
    openai_url: str = os.environ.get("OPENAI_URL", "https://api.deepseek.com/v1/chat/completions") 
    max_turns: int = int(os.environ.get("MAX_TURNS", "8")) #最大对话轮数

settings = Settings()
