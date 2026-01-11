from app.skill_loader import discover_skills
from app.agent import SkillAgent
from app.conf import settings

def main():
    # 发现技能
    print(f"从目录加载技能: {settings.skills_dir}")
    metas = discover_skills(settings.skills_dir)
    print(f"发现 {len(metas)} 个技能:")
    for meta in metas:
        print(f"  - {meta.name}: {meta.description}")
    
    # 创建 agent
    agent = SkillAgent(metas)
    
    # 交互式运行
    print("\n=== AI Agent 已启动 ===")
    print("输入消息与 AI 对话，输入 'quit' 退出")
    
    while True:
        try:
            user_input = input("\n用户: ").strip()
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            
            if user_input:
                print("AI: ", end="")
                result = agent.run(user_input)
                print(result)
                
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    # 添加绝对导入用于测试
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 调用 main() 函数
    main()
