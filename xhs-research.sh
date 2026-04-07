#!/bin/bash
# 小红书内容调研脚本 - 使用MCP自动搜索
# 用法: ./xhs-research.sh [关键词]

WORKSPACE="/root/.openclaw/workspace/aisoul-content"
LOGFILE="$WORKSPACE/CONTENT-RESEARCH.md"
MCP_URL="http://47.250.37.93:18060"
KEYWORDS=("AI灵魂测试" "AI人格测试 恋爱" "灵魂伴侣 MBTI" "AI看内心" "DeepSeek 情感")
SESSION_ID="research-$(date +%s)"

# Initialize MCP session
init_result=$(curl -s -X POST "$MCP_URL/mcp" \
    -H 'Content-Type: application/json' \
    -H "MCPSessionId: $SESSION_ID" \
    -d '[{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"research","version":"1.0"}}}]' 2>&1)

if echo "$init_result" | grep -q "serverInfo"; then
    echo "[$(date '+%Y-%m-%d %H:%M')] MCP初始化成功" >> "$WORKSPACE/research-log.txt"
    
    # 搜索几个关键词
    for kw in "${KEYWORDS[@]}"; do
        echo "[$(date '+%Y-%m-%d %H:%M')] 搜索: $kw" >> "$WORKSPACE/research-log.txt"
        
        result=$(curl -s -X POST "$MCP_URL/mcp" \
            -H 'Content-Type: application/json' \
            -H "MCPSessionId: $SESSION_ID" \
            -d "[{\"jsonrpc\":\"2.0\",\"id\":99,\"method\":\"tools/call\",\"params\":{\"name\":\"search_feeds\",\"arguments\":{\"keyword\":\"$kw\"}}}]" 2>&1)
        
        if echo "$result" | grep -q "notes"; then
            count=$(echo "$result" | grep -o '"likedCount":"[^"]*"' | head -5)
            echo "  热门笔记: $count" >> "$WORKSPACE/research-log.txt"
        fi
        
        sleep 2
    done
else
    echo "[$(date '+%Y-%m-%d %H:%M')] MCP初始化失败" >> "$WORKSPACE/research-log.txt"
fi
