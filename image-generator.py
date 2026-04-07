#!/usr/bin/env python3
"""
AI对话截图生成器
生成逼真的AI聊天界面截图，用于小红书配图
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

class ChatScreenshotGenerator:
    """生成AI对话截图"""
    
    def __init__(self, width=800, height=None):
        self.width = width
        self.padding = 20
        self.line_height = 28
        self.avatar_size = 40
        self.message_spacing = 15
        
    def create_screenshot(self, messages, platform="chatgpt", theme="light"):
        """
        生成对话截图
        
        Args:
            messages: [{"role": "user"/"assistant", "content": "..."}, ...]
            platform: "chatgpt", "claude", "deepseek"
            theme: "light" or "dark"
        
        Returns:
            PIL Image对象
        """
        # 计算高度
        height = self._calculate_height(messages)
        
        # 创建画布
        if theme == "dark":
            bg_color = (32, 32, 32)
            user_bg = (52, 52, 52)
            ai_bg = (82, 82, 82)
            text_color = (255, 255, 255)
            header_color = (45, 45, 45)
        else:
            bg_color = (255, 255, 255)
            user_bg = (16, 163, 74)  # 绿色
            ai_bg = (245, 245, 245)
            text_color = (0, 0, 0)
            header_color = (255, 255, 255)
        
        img = Image.new('RGB', (self.width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # 绘制顶部栏
        draw.rectangle([(0, 0), (self.width, 50)], fill=header_color)
        
        # 平台标识和标题
        titles = {
            "chatgpt": "ChatGPT",
            "claude": "Claude", 
            "deepseek": "DeepSeek"
        }
        title = titles.get(platform, "AI Chat")
        
        # 字体大小
        title_size = 18
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", title_size)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
        except:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        # 绘制标题
        draw.text((20, 15), title, fill=text_color if theme == "dark" else (0, 0, 0), font=title_font)
        
        # 绘制消息
        y_offset = 60
        for msg in messages:
            y_offset = self._draw_message(draw, img, msg, y_offset, 
                                          user_bg if msg["role"] == "user" else ai_bg,
                                          text_color, body_font, theme, 
                                          msg["role"] == "user")
        
        return img
    
    def _calculate_height(self, messages):
        height = 60  # 顶部栏
        
        for msg in messages:
            content = msg["content"]
            # 计算文字换行后的行数
            chars_per_line = (self.width - 100) // 9  # 估算
            lines = len(content) // chars_per_line + content.count('\n') + 1
            height += self.message_spacing + self.avatar_size + (lines * self.line_height) + 15
        
        return height + 20
    
    def _draw_message(self, draw, img, msg, y_offset, bg_color, text_color, font, theme, is_user):
        """绘制单条消息"""
        content = msg["content"]
        lines = []
        
        # 换行处理
        for paragraph in content.split('\n'):
            if paragraph.strip():
                wrapped = textwrap.wrap(paragraph, width=45)
                lines.extend(wrapped if wrapped else [''])
            else:
                lines.append('')
        
        # 消息气泡高度
        bubble_height = len(lines) * self.line_height + 20
        bubble_width = self.width - 120
        
        # 头像位置
        avatar_x = 20 if not is_user else self.width - 60
        bubble_x = 70 if not is_user else self.width - bubble_width - 70
        
        # 绘制头像
        draw.ellipse([(avatar_x, y_offset), 
                     (avatar_x + self.avatar_size, y_offset + self.avatar_size)], 
                     fill=(100, 100, 100) if not is_user else (16, 163, 74))
        
        # 绘制头像文字
        avatar_text = "AI" if not is_user else "U"
        draw.text((avatar_x + 10, y_offset + 10), avatar_text, 
                  fill=(255, 255, 255), font=font)
        
        # 绘制消息气泡
        corner_radius = 15
        draw.rounded_rectangle(
            [(bubble_x, y_offset), 
             (bubble_x + bubble_width, y_offset + bubble_height)],
            radius=corner_radius,
            fill=bg_color
        )
        
        # 绘制文字
        text_y = y_offset + 10
        for line in lines:
            draw.text((bubble_x + 15, text_y), line, fill=text_color, font=font)
            text_y += self.line_height
        
        return y_offset + bubble_height + self.message_spacing

    def save(self, img, filepath):
        """保存图片"""
        img.save(filepath)
        print(f"✅ 已保存: {filepath}")

def demo():
    """演示"""
    generator = ChatScreenshotGenerator(width=750)
    
    # 示例对话
    messages = [
        {"role": "user", "content": "什么是灵魂伴侣？"},
        {"role": "assistant", "content": "灵魂伴侣不是找到的，是养成的。\n\n真正的亲密关系需要双方共同努力：\n\n1. 理解彼此的内心世界\n2. 在对方需要时给予支持\n3. 接受彼此的不完美"}
    ]
    
    # 生成三个平台的截图
    for platform in ["chatgpt", "claude", "deepseek"]:
        img = generator.create_screenshot(messages, platform=platform, theme="light")
        output_path = f"/root/.openclaw/workspace/aisoul-content/demo-{platform}.png"
        generator.save(img, output_path)

if __name__ == "__main__":
    demo()
