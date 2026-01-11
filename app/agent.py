from __future__ import annotations

import json
import requests
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .conf import settings
from .skill_loader import load_skill_full
from .skills_types import SkillMeta
from .tools import ToolRuntime, tool_schemas
from .prompt import build_system_prompt

@dataclass
class ChatTurn:
    role: str
    content: str

class SkillAgent:
    def __init__(self, metas: List[SkillMeta]):
        self.api_url = settings.openai_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.openai_token}'
        }
        self.metas = metas
        self.runtime = ToolRuntime(metas)
        self.system_prompt = build_system_prompt(metas)
        self.max_turns = settings.max_turns

    def run(self, user_text: str, history: Optional[List[ChatTurn]] = None) -> str:
        """
        使用 HTTP 请求实现的对话功能，支持工具调用
        """
        if history is None:
            history = []

        # 构建消息列表
        messages: List[Dict[str, Any]] = [{"role": "system", "content": self.system_prompt}]
        for t in history:
            messages.append({"role": t.role, "content": t.content})
        messages.append({"role": "user", "content": user_text})

        tools = tool_schemas()

        for _ in range(self.max_turns):
            # 构建请求载荷
            payload = {
                'model': settings.openai_model,
                'messages': messages,
                'tools': tools
            }

            try:
                # 发送 HTTP 请求
                response = requests.post(
                    self.api_url, 
                    headers=self.headers, 
                    data=json.dumps(payload)
                )
                
                # 检查响应状态
                if response.status_code != 200:
                    return f"API Error: {response.status_code} - {response.text}"

                # 解析响应
                result = response.json()
                
                # 检查是否有工具调用
                tool_calls = self._extract_tool_calls(result)
                if tool_calls:
                    # 添加助手消息（包含工具调用）
                    assistant_message = {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": tool_calls
                    }
                    messages.append(assistant_message)

                    # 逐个工具调用执行并回填结果
                    for call in tool_calls:
                        tool_name = call["function"]["name"]
                        args = json.loads(call["function"]["arguments"])

                        # 执行工具
                        tool_result = self.runtime.dispatch(tool_name, args)

                        # 回填 tool 消息
                        messages.append({
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "content": tool_result,
                        })
                    
                    # 执行完工具，继续下一轮
                    continue

                # 没有工具调用，返回模型文本
                text = self._extract_text(result)
                if text:
                    return text

                # 兜底：有时模型既没 tool call 也没文本
                return "No output from model."
                
            except requests.RequestException as e:
                return f"Request failed: {str(e)}"
            except json.JSONDecodeError as e:
                return f"JSON decode error: {str(e)}"
            except Exception as e:
                return f"Unexpected error: {str(e)}"

        return "Stopped: too many tool iterations."

    def _extract_text(self, result: Dict[str, Any]) -> str:
        """从 HTTP 响应中提取文本内容"""
        try:
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message'].get('content')
                if content:
                    return content.strip()
            return ""
        except Exception:
            return ""

    def _extract_tool_calls(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """从 HTTP 响应中提取工具调用"""
        try:
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0]['message']
                if 'tool_calls' in message and message['tool_calls']:
                    return message['tool_calls']
            return []
        except Exception:
            return []
