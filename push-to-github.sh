#!/bin/bash

# Skills Runtime - GitHub 推送脚本
# 使用方法: bash push-to-github.sh

echo "🚀 开始推送到 GitHub..."

# 进入项目目录
cd /data/project/skills-runtime

# 配置 Git 用户信息
git config user.name "Peng416"
git config user.email "peng416@users.noreply.github.com"

# 添加所有文件
echo "📦 添加文件到 Git..."
git add .

# 查看将要提交的文件
echo "📋 将要提交的文件:"
git status --short

# 提交
echo "💾 提交更改..."
git commit -m "Initial commit: Skills Runtime AI Agent Framework

- Modular AI Agent framework with skill-based architecture
- Zero-code skill extensions via SKILL.md files  
- OpenAI Function Calling support
- Security hardened (path traversal protection, input validation)
- Lightweight dependencies (openai, pyyaml, requests)
- Complete documentation and examples"

# 重命名分支为 main
echo "🌿 切换到 main 分支..."
git branch -M main

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote add origin https://github.com/Peng416/skills-runtime.git

# 推送到 GitHub
echo "⬆️  推送到 GitHub..."
git push -u origin main

echo "✅ 完成！访问: https://github.com/Peng416/skills-runtime"
