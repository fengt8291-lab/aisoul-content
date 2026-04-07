#!/usr/bin/env python3
"""
生成多AI对比图
在同一张图上展示多个AI的回答对比
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

class MultiAICompareGenerator:
    """生成多AI对比截图"""
    
    def __init__(self, width=1080):
        self.width = width
        self.scale = width / 1080
    
    def create_comparison(self, ai_responses):
        """
        生成对比图
        
        Args:
            ai_responses: [
                {"name": "ChatGPT", "color": (16, 163, 74), "header_bg": (32, 33, 35), "content": "..."},
                {"name": "DeepSeek", "color": (59, 130, 246), "header_bg": (1, 45, 86), "content": "..."},
                {"name": "Claude", "color": (255, 107, 53), "header_bg": (255, 247, 237), "content": "..."},
            ]
        """
        # 每列宽度
        col_width = (self.width - 60) // len(ai_responses)
        col_width = min(col_width, 350)  # 最大宽度
        
        # 计算高度
        max_lines = 0
        for resp in ai_responses:
            lines = self._count_lines(resp["content"])
            max_lines = max(max_lines, lines)
        
        height = int(70 + max_lines * 28 + 100) * self.scale
        
        # 创建画布
        img = Image.new('RGB', (self.width, int(height)), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # 加载字体
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(16 * self.scale))
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(14 * self.scale))
        except:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        # 绘制标题
        title_y = int(20 * self.scale)
        draw.text((self.width // 2 - 60, title_y), "多AI回答对比", fill=(50, 50, 50), font=title_font)
        
        # 绘制每列
        start_x = int(30 * self.scale)
        y_offset = int(60 * self.scale)
        
        for i, resp in enumerate(ai_responses):
            x = start_x + i * (col_width + int(15 * self.scale))
            
            # 列背景
            bg_color = resp.get("bg", (245, 245, 245))
            draw.rounded_rectangle(
                [(x, y_offset), (x + col_width, int(height) - int(20 * self.scale))],
                radius=int(15 * self.scale),
                fill=bg_color
            )
            
            # 头部
            header_height = int(45 * self.scale)
            # 头部圆角顶部
            draw.rounded_rectangle(
                [(x, y_offset), (x + col_width, y_offset + header_height)],
                radius=int(15 * self.scale),
                fill=resp["header_bg"]
            )
            # 底部遮盖
            draw.rectangle([(x, y_offset + header_height - 15), (x + col_width, y_offset + header_height)], fill=resp["header_bg"])
            
            # Logo圆点
            logo_x = x + int(15 * self.scale)
            logo_y = y_offset + int(12 * self.scale)
            draw.ellipse([(logo_x, logo_y), (logo_x + int(20 * self.scale), logo_y + int(20 * self.scale))], 
                         fill=resp["color"])
            
            # AI名称
            draw.text((logo_x + int(28 * self.scale), logo_y - 2), resp["name"], 
                     fill=(255, 255, 255) if resp["header_bg"][0] < 128 else (50, 50, 50),
                     font=title_font)
            
            # 内容
            content_y = y_offset + header_height + int(15 * self.scale)
            content_x = x + int(15 * self.scale)
            max_content_width = col_width - int(30 * self.scale)
            
            lines = self._wrap_text(resp["content"], int(max_content_width / (8 * self.scale)))
            for line in lines:
                draw.text((content_x, content_y), line, 
                         fill=(255, 255, 255) if resp["header_bg"][0] < 128 else (50, 50, 50),
                         font=body_font)
                content_y += int(24 * self.scale)
        
        return img
    
    def _count_lines(self, text):
        lines = 0
        for para in text.split('\n'):
            if para.strip():
                wrapped = textwrap.wrap(para, width=35)
                lines += len(wrapped) if wrapped else 1
            else:
                lines += 1
        return lines
    
    def _wrap_text(self, text, chars_per_line):
        lines = []
        for para in text.split('\n'):
            if para.strip():
                wrapped = textwrap.wrap(para, width=chars_per_line)
                lines.extend(wrapped if wrapped else [''])
            else:
                lines.append('')
        return lines
    
    def save(self, img, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, "PNG", quality=95)
        print(f"✅ 已保存: {filepath}")

def generate_samples():
    gen = MultiAICompareGenerator(width=1100)
    
    # 001 - 灵魂伴侣对比
    compare1 = [
        {
            "name": "ChatGPT",
            "color": (16, 163, 74),
            "header_bg": (32, 33, 35),
            "content": "灵魂伴侣不是找到的，是养成的。真正的亲密关系需要双方共同努力，理解彼此的内心世界。",
            "bg": (40, 40, 40)
        },
        {
            "name": "DeepSeek",
            "color": (59, 130, 246),
            "header_bg": (1, 45, 86),
            "content": "与其寻找灵魂伴侣，不如先成为自己的灵魂。真正的亲密关系不是找到完美的人，而是愿意彼此成长。",
            "bg": (10, 50, 100)
        },
        {
            "name": "Claude",
            "color": (255, 107, 53),
            "header_bg": (255, 247, 237),
            "content": "灵魂伴侣是那个能让你做真实的自己的人。不需要完美，但需要彼此理解和支持。",
            "bg": (255, 245, 238)
        }
    ]
    
    img = gen.create_comparison(compare1)
    gen.save(img, "/root/.openclaw/workspace/aisoul-content/001-AI人格测试/images/001-compare-3ai.png")
    
    # 003 - 出轨问题对比
    compare2 = [
        {
            "name": "ChatGPT",
            "color": (16, 163, 74),
            "header_bg": (32, 33, 35),
            "content": "建议沟通，表达感受，设立边界。先冷静下来，再处理问题。",
            "bg": (40, 40, 40)
        },
        {
            "name": "DeepSeek",
            "color": (59, 130, 246),
            "header_bg": (1, 45, 86),
            "content": "先确认是不是本人。有时候是小号互关好友手滑。先观察，别急着下结论。",
            "bg": (10, 50, 100)
        }
    ]
    
    img2 = gen.create_comparison(compare2)
    gen.save(img2, "/root/.openclaw/workspace/aisoul-content/003-不同AI聊出轨/images/003-compare-2ai.png")
    
    # 005 - 灵魂伴侣存在吗
    compare3 = [
        {
            "name": "DeepSeek",
            "color": (59, 130, 246),
            "header_bg": (1, 45, 86),
            "content": "你的灵魂类型是「探索者」。适合找「守护者」型。你需要能接住你情绪的人，他不一定多有趣，但崩溃时他能在。",
            "bg": (10, 50, 100)
        },
        {
            "name": "Claude",
            "color": (255, 107, 53),
            "header_bg": (255, 247, 237),
            "content": "存在的，但前提是你先搞清楚自己是谁。了解自己的灵魂，才能找到与之共鸣的人。",
            "bg": (255, 245, 238)
        }
    ]
    
    img3 = gen.create_comparison(compare3)
    gen.save(img3, "/root/.openclaw/workspace/aisoul-content/005-AI灵魂匹配测试/images/005-compare-2ai.png")
    
    print("\n✅ 多AI对比图生成完成！")

if __name__ == "__main__":
    generate_samples()
