# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## GitHub

- **账号**: fengt8291-lab
- **Token**: `[REDACTED-GH-TOKEN]` (public_repo)
- **已Star项目**: unclecode/crawl4ai

## 服务器

- **SSH**: root@47.250.37.93 (密码 Typhoon2026@Aliyun)
- **crawl4ai**: v0.8.6 已安装 ✅

## 阿里云

- **域名管理**: nihaofengzi.top (15701025472 / tf020243)

## API Keys & Tokens

### Tavily搜索
- **Key**: `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`
- **Skill**: `~/.openclaw/skills/tavily-search-1.0.0/`
- **测试命令**: `node ~/.openclaw/skills/tavily-search-1.0.0/scripts/search.mjs "query"`

### Notion
- **Token**: `[REDACTED-NOTION-TOKEN]`
- **Bot名**: OpenClaw
- **限制**: 仅可访问手动分享给OpenClaw Integration的页面
- **授权方法**: Notion页面 → ... → Add connections → 添加OpenClaw
- **已接入页面**: Typhoon工作台 `345b6365-e6f4-8062-b5ad-d5794494cf8d`（含：关于我/项目/周复盘/人生规划/Notion使用规划/当前困境记录）
- **页面结构**：5大模块——人生规划/项目管理体系/点子库/学业追踪/云图工作流

### Telegram
- **Bot**: @CloudMap243bot
- **Token**: `8668458845:AAH25eYi36YAy7se8TK-4hxbJ1OCOwKzw9o`
- **代理**: http://127.0.0.1:7897（Clash Verge HTTP）

## 浏览器自动化

### agent-browser
- **安装**: `npm install -g agent-browser && agent-browser install`
- **Chrome路径**: `~/.agent-browser/browsers/chrome-147.0.7727.56/`
- **使用代理**: `agent-browser open <url> --proxy http://127.0.0.1:7897`
- **显示窗口**: `agent-browser open <url> --headed`
- **常用命令**:
  - `agent-browser open <url>` - 打开页面
  - `agent-browser snapshot -i` - 获取可交互元素
  - `agent-browser click @e1` - 点击元素
  - `agent-browser fill @e1 "text"` - 填写表单
  - `agent-browser close` - 关闭浏览器

## 小红书

### 创作者平台
- **网址**: https://creator.xiaohongshu.com
- **账号**: AI徕风灵魂实验室
- **问题**: 需要保持登录状态，session容易丢

### MCP调研结论
- **推荐**: RedNote-MCP（MIT授权），但Mac mini内存不够跑Playwright
- **替代方案**: agent-browser直接访问创作者平台
- **调研数据源**: B站API（api.bilibili.com）可搜索热门视频

## SBTI蹭热度内容

- **仓库**: fengt8291-lab/aisoul-content
- **路径**: `007-SBTI玩梗测试/`
- **推送方式**: GitHub API（git push超时）

Add whatever helps you do your job. This is your cheat sheet.
