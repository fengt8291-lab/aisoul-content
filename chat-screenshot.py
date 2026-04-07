#!/usr/bin/env python3
"""
AI对话截图生成器 v2 - 更逼真的界面
用于生成ChatGPT/Claude/DeepSeek风格的对话截图
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random

class RealisticChatGenerator:
    """生成逼真的AI对话截图"""
    
    def __init__(self, width=1080):
        self.width = width
        self.scale = width / 1080  # 响应式缩放
        
    def create_chatgpt_screenshot(self, messages):
        """生成ChatGPT风格截图"""
        return self._create_screenshot(
            messages,
            platform="chatgpt",
            header_color=(32, 33, 35),
            user_bubble=(0, 0, 0),
            ai_bubble=(58, 58, 58),
            bg_color=(32, 33, 35),
            user_text=(255, 255, 255),
            ai_text=(255, 255, 255),
            border_color=(68, 68, 68),
            header_text="ChatGPT",
            logo_color=(16, 163, 74),
            show_logo=True
        )
    
    def create_deepseek_screenshot(self, messages):
        """生成DeepSeek风格截图"""
        return self._create_screenshot(
            messages,
            platform="deepseek",
            header_color=(14, 14, 14),
            user_bubble=(0, 0, 0),
            ai_bubble=(38, 38, 38),
            bg_color=(14, 14, 14),
            user_text=(255, 255, 255),
            ai_text=(255, 255, 255),
            border_color=(48, 48, 48),
            header_text="DeepSeek",
            logo_color=(255, 189, 46),
            show_logo=True
        )
    
    def create_claude_screenshot(self, messages):
        """生成Claude风格截图"""
        return self._create_screenshot(
            messages,
            platform="claude",
            header_color=(255, 255, 255),
            user_bubble=(26, 26, 26),
            ai_bubble=(250, 250, 250),
            bg_color=(252, 252, 252),
            user_text=(255, 255, 255),
            ai_text=(0, 0, 0),
            border_color=(235, 235, 235),
            header_text="Claude",
            logo_color=(255, 189, 46),
            show_logo=True
        )
    
    def _create_screenshot(self, messages, **kwargs):
        """通用创建方法"""
        # 参数
        header_color = kwargs.get("header_color", (32, 33, 35))
        user_bubble = kwargs.get("user_bubble", (0, 0, 0))
        ai_bubble = kwargs.get("ai_bubble", (58, 58, 58))
        bg_color = kwargs.get("bg_color", (32, 33, 35))
        user_text_color = kwargs.get("user_text", (255, 255, 255))
        ai_text_color = kwargs.get("ai_text", (255, 255, 255))
        border_color = kwargs.get("border_color", (68, 68, 68))
        header_text = kwargs.get("header_text", "AI Chat")
        logo_color = kwargs.get("logo_color", (100, 100, 100))
        show_logo = kwargs.get("show_logo", True)
        
        # 计算高度
        height = 65 + self._calculate_content_height(messages) + 80
        
        # 创建图片
        img = Image.new('RGB', (self.width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # 加载字体
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(18 * self.scale))
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(16 * self.scale))
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(13 * self.scale))
        except:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # 顶部栏
        pad = int(20 * self.scale)
        header_height = int(55 * self.scale)
        
        # 顶部边框线
        draw.line([(0, header_height), (self.width, header_height)], fill=border_color, width=1)
        
        # Logo/标题
        if show_logo:
            # Logo圆点
            logo_x = pad
            logo_y = int(20 * self.scale)
            logo_size = int(16 * self.scale)
            draw.ellipse([(logo_x, logo_y), (logo_x + logo_size, logo_y + logo_size)], fill=logo_color)
            
            # 标题
            draw.text((logo_x + logo_size + 12, logo_y - 2), header_text, fill=(255, 255, 255), font=title_font)
        
        # 消息区域
        y_offset = header_height + pad
        
        for msg in messages:
            is_user = msg["role"] == "user"
            content = msg["content"]
            
            # 头像
            avatar_x = self.width - pad - int(36 * self.scale) if is_user else pad
            avatar_y = y_offset
            draw.ellipse([(avatar_x, avatar_y), 
                         (avatar_x + int(36 * self.scale), avatar_y + int(36 * self.scale))], 
                         fill=user_bubble if is_user else (100, 100, 100))
            
            # 头像文字
            avatar_char = "U" if is_user else "A"
            char_x = avatar_x + int(10 * self.scale)
            char_y = avatar_y + int(8 * self.scale)
            draw.text((char_x, char_y), avatar_char, fill=(255, 255, 255), font=body_font)
            
            # 消息气泡
            bubble_x = avatar_x + int(46 * self.scale) if not is_user else int(20 * self.scale)
            bubble_max_width = self.width - int(160 * self.scale)
            
            # 计算文字换行
            chars_per_line = int(bubble_max_width / (9 * self.scale))
            lines = []
            for para in content.split('\n'):
                if para.strip():
                    wrapped = textwrap.wrap(para, width=chars_per_line)
                    lines.extend(wrapped if wrapped else [''])
                else:
                    lines.append('')
            
            bubble_height = len(lines) * int(26 * self.scale) + int(20 * self.scale)
            
            # 气泡圆角矩形
            bubble_rect = [
                (bubble_x, y_offset),
                (bubble_x + bubble_max_width, y_offset + bubble_height)
            ]
            draw.rounded_rectangle(bubble_rect, radius=int(18 * self.scale), fill=ai_bubble if not is_user else user_bubble)
            
            # 文字
            text_x = bubble_x + int(16 * self.scale)
            text_y = y_offset + int(12 * self.scale)
            for line in lines:
                draw.text((text_x, text_y), line, fill=ai_text_color if not is_user else user_text_color, font=body_font)
                text_y += int(26 * self.scale)
            
            y_offset += bubble_height + int(20 * self.scale)
        
        # 底部输入框区域（装饰）
        input_y = height - int(60 * self.scale)
        input_height = int(48 * self.scale)
        draw.rounded_rectangle(
            [(pad, input_y), (self.width - pad, input_y + input_height)],
            radius=int(24 * self.scale),
            fill=border_color
        )
        draw.text((pad + int(20 * self.scale), input_y + int(14 * self.scale)), 
                 "输入消息...", fill=(128, 128, 128), font=body_font)
        
        return img
    
    def _calculate_content_height(self, messages):
        """计算消息内容总高度"""
        total = 0
        chars_per_line = 50
        
        for msg in messages:
            lines = 0
            for para in msg["content"].split('\n'):
                if para.strip():
                    lines += len(textwrap.wrap(para, width=chars_per_line))
                else:
                    lines += 1
            total += lines * 26 + 32
        
        return total

    def save(self, img, filepath):
        """保存图片"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, "PNG", quality=95)
        print(f"✅ 已保存: {filepath}")

def generate_for_content(content_num, messages):
    """为指定内容生成配图"""
    gen = RealisticChatGenerator(width=1080)
    
    results = {}
    
    # DeepSeek风格（最适合我们的内容主题）
    if "灵魂伴侣" in str(messages):
        img = gen.create_deepseek_screenshot(messages)
        path = f"/root/.openclaw/workspace/aisoul-content/{content_num}/images/deepseek-demo.png"
        gen.save(img, path)
        results["deepseek"] = path
    
    # ChatGPT风格
    img = gen.create_chatgpt_screenshot(messages)
    path = f"/root/.openclaw/workspace/aisoul-content/{content_num}/images/chatgpt-demo.png"
    gen.save(img, path)
    results["chatgpt"] = path
    
    return results

def demo():
    """演示"""
    gen = RealisticChatGenerator(width=1080)
    
    # 示例1：灵魂伴侣问题
    messages1 = [
        {"role": "user", "content": "什么是灵魂伴侣？"},
        {"role": "assistant", "content": "与其寻找灵魂伴侣，不如先成为自己的灵魂。\n\n真正的亲密关系不是找到完美的人，而是与一个不完美的人相处时，仍愿意彼此成长。"}
    ]
    
    print("生成示例截图...")
    img = gen.create_deepseek_screenshot(messages1)
    gen.save(img, "/root/.openclaw/workspace/aisoul-content/demo-screenshot.png")
    
    # 同时生成一个对比图（多AI回答）
    messages2 = [
        {"role": "assistant", "content": "ChatGPT：灵魂伴侣不是找到的，是养成的。两个人在一起需要不断磨合。"},
        {"role": "assistant", "content": "DeepSeek：与其寻找灵魂伴侣，不如先成为自己的灵魂。"},
        {"role": "assistant", "content": "Claude：真正的亲密是理解对方的内心世界，在需要时给予支持。"}
    ]
    
    img2 = gen.create_deepseek_screenshot(messages2)
    gen.save(img2, "/root/.openclaw/workspace/aisoul-content/demo-multi-ai.png")
    
    print("\n演示完成！")

if __name__ == "__main__":
    demo()
