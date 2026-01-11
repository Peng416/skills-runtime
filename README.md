# Skills Runtime

一个基于技能的模块化 AI Agent 框架，支持通过 Markdown 文件零代码扩展功能。

## ✨ 特性

- 🎯 **零代码扩展**：通过 `SKILL.md` 文件添加新功能，无需修改核心代码
- 📦 **标准化规范**：YAML frontmatter + Markdown 内容格式
- 🔧 **工具调用支持**：完整实现 OpenAI Function Calling 协议
- 🔒 **安全设计**：路径遍历防护、输入验证、内容转义
- 💬 **交互式 CLI**：便于开发测试和演示
- 🪶 **轻量级依赖**：仅依赖 3 个核心库

## 📋 快速开始

### 1. 环境要求

- Python >= 3.13
- UV 包管理器（推荐）或 pip

### 2. 安装依赖

```bash
# 使用 UV（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Token
export OPENAI_TOKEN="your-api-token-here"
export OPENAI_URL="https://api.deepseek.com/v1/chat/completions"
export OPENAI_MODEL="deepseek-v3.2"
```

### 4. 运行

```bash
python main.py
```

## 🎓 使用示例

```
=== AI Agent 已启动 ===
输入消息与 AI 对话，输入 'quit' 退出

用户: hello
AI: Hi there! 👋 Welcome to Skills Runtime!

To get started:
1. Tell me what you want to build
2. I'll help you plan the steps
3. We'll execute together

What would you like to work on today?
```

## 📚 技能系统

### 技能结构

```
skills/
└── your-skill-name/
    ├── SKILL.md          # 技能定义文件（必需）
    ├── templates/        # 模板文件（可选）
    └── data/             # 数据文件（可选）
```

### 创建自定义技能

创建 `skills/my-skill/SKILL.md`：

```markdown
---
name: my-skill
description: 简短描述你的技能功能（1-1024 字符）
license: MIT
---

# My Skill

## What to do
1. 步骤 1：描述具体操作
2. 步骤 2：...
3. 步骤 3：...

## Output format
- 指定期望的输出格式

## Examples
### Example 1
Input: 示例输入
Output: 示例输出
```

### 技能命名规范

- ✅ 仅使用小写字母、数字和连字符
- ✅ 正则表达式：`^[a-z0-9]+(?:-[a-z0-9]+)*$`
- ✅ 示例：`hello-skills`, `financial-analysis`, `report-generator-v2`

## 🏗️ 项目结构

```
skills-runtime/
├── app/                    # 核心应用
│   ├── agent.py           # Agent 核心逻辑
│   ├── conf.py            # 配置管理
│   ├── prompt.py          # 提示词构建
│   ├── skill_loader.py    # 技能加载器
│   ├── skills_types.py    # 数据类型定义
│   └── tools.py           # 工具运行时
├── skills/                 # 技能目录
│   └── hello-skills/      # 示例技能
├── main.py                # 主入口
├── requirements.txt       # 依赖列表
├── pyproject.toml         # 项目配置
└── README.md              # 本文件
```

## 🔧 配置说明

### 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `OPENAI_TOKEN` | ✅ | - | API 认证 Token |
| `OPENAI_URL` | ❌ | https://api.deepseek.com/v1/chat/completions | API 端点 |
| `OPENAI_MODEL` | ❌ | deepseek-v3.2 | 使用的模型 |
| `SKILLS_DIR` | ❌ | ./skills | 技能目录路径 |
| `MAX_TURNS` | ❌ | 8 | 最大对话轮数 |

## 📖 技术文档

详细的技术文档请参考 [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md)，包含：

- 完整的架构设计
- API 接口说明
- 开发指南
- 部署运维
- 安全规范

## 🔒 安全注意事项

- ⚠️ 不要将 `.env` 文件提交到版本控制
- ⚠️ 生产环境请定期轮换 API Token
- ⚠️ 技能目录权限设置为只读（755）
- ⚠️ 定期更新依赖版本以修复安全漏洞

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📝 开发规范

- 遵循 PEP 8 代码风格
- 使用类型注解（Type Hints）
- 添加必要的文档字符串
- 确保安全编码（参考技术文档中的安全规范）

## 📄 许可证

本项目采用 MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙋 FAQ

### Q: 如何添加新技能？

A: 在 `skills/` 目录创建新文件夹，编写 `SKILL.md` 文件，重启即可自动加载。

### Q: 支持哪些 AI 模型？

A: 支持所有兼容 OpenAI API 的模型，包括 DeepSeek、GPT-4、Claude 等（需确保支持 Function Calling）。

### Q: 技能不生效怎么办？

A: 检查技能名称是否符合命名规范，SKILL.md 的 frontmatter 是否正确，以及目录名是否与 name 字段一致。

## 📮 联系方式

- 问题反馈：[Issues](https://github.com/Peng416/skills-runtime/issues)
- 技术讨论：[Discussions](https://github.com/Peng416/skills-runtime/discussions)

---

**Made with ❤️ by Skills Runtime Team**
