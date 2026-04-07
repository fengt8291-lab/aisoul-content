#!/usr/bin/env python3
"""
快速生成AI对话截图
用法:
    python3 generate_image.py --content "001-AI人格测试"
    python3 generate_image.py --custom "user:你好|ai:你好呀"
"""

import sys
import os
import argparse
import importlib.util
spec = importlib.util.spec_from_file_location("chat_screenshot", "/root/.openclaw/workspace/aisoul-content/chat-screenshot.py")
chat_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chat_mod)
RealisticChatGenerator = chat_mod.RealisticChatGenerator

# 预设的配图内容
CONTENT_TEMPLATES = {
    "001-AI人格测试": {
        "messages": [
            {"role": "user", "content": "什么是灵魂伴侣？"},
            {"role": "assistant", "content": "与其寻找灵魂伴侣，不如先成为自己的灵魂。\n\n真正的亲密关系不是找到完美的人，而是与一个不完美的人相处时，仍愿意彼此成长。"}
        ],
        "platform": "deepseek",
        "style": "对比"
    },
    "002-AI-MBTI测试": {
        "messages": [
            {"role": "user", "content": "帮我分析这段聊天记录"},
            {"role": "assistant", "content": "从这段聊天记录来看：\n\n• 她的依恋类型是焦虑型\n• 她男朋友是回避型\n• 两个人都在用错误的方式索取爱\n\n建议她先冷静下来，等对方主动联系。"}
        ],
        "platform": "chatgpt",
        "style": "分析"
    },
    "003-不同AI聊出轨": {
        "messages": [
            {"role": "user", "content": "发现男朋友点赞前女友，该怎么做？"},
            {"role": "assistant", "content": "先确认是不是本人。\n有时候是小号互关好友手滑。\n先观察，别急着下结论。\n真有猫腻，藏不住的。"}
        ],
        "platform": "deepseek",
        "style": "建议"
    },
    "004-AI分析朋友圈": {
        "messages": [
            {"role": "assistant", "content": "从整体氛围判断：\n\n当事人目前处于渴望亲密关系但被动等待的状态。\n建议身边的人不要主动提起感情话题。"}
        ],
        "platform": "claude",
        "style": "分析"
    },
    "005-AI灵魂匹配测试": {
        "messages": [
            {"role": "assistant", "content": "你的灵魂类型是「探索者」\n\n适合找「守护者」型伴侣。\n\n你需要能接住你情绪的人，\n他不一定多有趣，\n但你崩溃的时候，他能在。"}
        ],
        "platform": "deepseek",
        "style": "结果"
    }
}

def generate_image(content_id, output_dir):
    """生成指定内容的配图"""
    if content_id not in CONTENT_TEMPLATES:
        print(f"❌ 未知内容ID: {content_id}")
        print(f"可用ID: {', '.join(CONTENT_TEMPLATES.keys())}")
        return False
    
    template = CONTENT_TEMPLATES[content_id]
    messages = template["messages"]
    platform = template["platform"]
    
    gen = RealisticChatGenerator(width=1080)
    
    # 根据平台生成
    if platform == "chatgpt":
        img = gen.create_chatgpt_screenshot(messages)
    elif platform == "deepseek":
        img = gen.create_deepseek_screenshot(messages)
    elif platform == "claude":
        img = gen.create_claude_screenshot(messages)
    else:
        img = gen.create_deepseek_screenshot(messages)
    
    # 保存
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{content_id}-{platform}.png")
    gen.save(img, output_path)
    return True

def generate_custom(messages_str, platform="deepseek", output="custom.png"):
    """从自定义消息生成"""
    messages = []
    for part in messages_str.split("|"):
        if ":" in part:
            role, content = part.split(":", 1)
            role = "user" if role.lower() == "user" else "assistant"
            messages.append({"role": role, "content": content.strip()})
    
    if not messages:
        print("❌ 消息格式错误，使用: user:你好|ai:你好呀")
        return
    
    gen = RealisticChatGenerator(width=1080)
    
    if platform == "chatgpt":
        img = gen.create_chatgpt_screenshot(messages)
    elif platform == "deepseek":
        img = gen.create_deepseek_screenshot(messages)
    elif platform == "claude":
        img = gen.create_claude_screenshot(messages)
    else:
        img = gen.create_deepseek_screenshot(messages)
    
    gen.save(img, output)
    print(f"✅ 已保存: {output}")

def main():
    parser = argparse.ArgumentParser(description="AI对话截图生成器")
    parser.add_argument("--content", "-c", help="内容ID，如001-AI人格测试")
    parser.add_argument("--custom", help="自定义消息，格式: user:问题|ai:回答")
    parser.add_argument("--platform", "-p", default="deepseek", 
                       choices=["chatgpt", "deepseek", "claude"],
                       help="AI平台风格")
    parser.add_argument("--output", "-o", default="output.png", help="输出文件路径")
    
    args = parser.parse_args()
    
    if args.content:
        # 生成预设内容
        content_id = args.content
        output_dir = f"/root/.openclaw/workspace/aisoul-content/{content_id}/images"
        success = generate_image(content_id, output_dir)
        if success:
            print(f"📁 图片已保存到: {output_dir}")
    
    elif args.custom:
        # 生成自定义内容
        generate_custom(args.custom, args.platform, args.output)
    
    else:
        # 显示帮助
        print("=== AI对话截图生成器 ===")
        print("\n用法:")
        print("  生成预设内容配图:")
        print("    python3 generate_image.py --content 001-AI人格测试")
        print()
        print("  生成自定义配图:")
        print("    python3 generate_image.py --custom 'user:问题|ai:回答' --platform deepseek")
        print()
        print("  可用内容ID:")
        for cid in CONTENT_TEMPLATES.keys():
            print(f"    - {cid}")
        print()
        print("  可用平台: chatgpt, deepseek, claude")

if __name__ == "__main__":
    main()
