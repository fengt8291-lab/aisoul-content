#!/bin/bash
# AISoul内容调研脚本 - 每小时自动运行
# 调研小红书/情感类AI测试内容规律

WORKSPACE="/root/.openclaw/workspace/aisoul-content"
LOGFILE="/root/.openclaw/workspace/aisoul-content/research-log.md"
DATE=$(date "+%Y-%m-%d %H:%M")

echo "=== 调研时间: $DATE ===" 

# 搜索相关话题
SEARCH_TERMS=(
    "小红书 AI灵魂测试 情感 帖子"
    "AI人格测试 恋爱 小红书"
    "ChatGPT DeepSeek 对比 情感"
    "MBTI 灵魂伴侣 小红书爆款"
    "AI分析 头像 朋友圈 玄学"
)

# 调研结果临时文件
TMPFILE="/tmp/xhs-research-$$.txt"

for term in "${SEARCH_TERMS[@]}"; do
    echo "搜索: $term"
    # 使用curl搜索，取前几条结果
    curl -s "https://www.bing.com/search?q=$(echo "$term" | sed 's/ /+/g')&count=5" 2>/dev/null | grep -oP '(?<=<h2>)[^<]+' | head -5 >> "$TMPFILE" 2>/dev/null
done

# 如果收集到新内容，更新调查报告
if [ -s "$TMPFILE" ] && [ $(wc -l < "$TMPFILE") -gt 5 ]; then
    echo "获取到内容样本，更新调查报告..."
    
    # 这里可以调用AI分析，但我先用简单的方式记录
    echo "" >> "$LOGFILE"
    echo "### 调研时刻: $DATE" >> "$LOGFILE"
    echo "采集到 $(wc -l < "$TMPFILE") 条内容线索" >> "$LOGFILE"
    echo '```' >> "$LOGFILE"
    head -10 "$TMPFILE" >> "$LOGFILE"
    echo '```' >> "$LOGFILE"
fi

rm -f "$TMPFILE"
echo "调研完成: $DATE"
