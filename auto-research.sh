#!/bin/bash
# 自动调研脚本 - 追加调研日志
WORKSPACE="/root/.openclaw/workspace/aisoul-content"
LOGFILE="$WORKSPACE/CONTENT-RESEARCH.md"
DATE=$(date "+%Y-%m-%d %H:%M")
TMPFILE="/tmp/auto-research-$$.txt"

# 搜索小红书内容策略相关文章
SEARCHES=(
    "小红书情感类爆款笔记写法 2026"
    "AI测试类小红书内容运营"
    "灵魂伴侣 情感 小红书 万赞"
)

for q in "${SEARCHES[@]}"; do
    echo "=== 搜索: $q ===" >> "$TMPFILE"
    # 用ddg搜索（不会触发小红书拦截）
    curl -s "https://lite.duckduckgo.com/lite/?q=$(echo "$q" | sed 's/ /+/g')" 2>/dev/null | \
        grep -oP '(?<=<a href=")[^"]*' | grep -v "xiaohongshu.com" | head -5 >> "$TMPFILE" 2>/dev/null
done

# 如果有内容，更新日志
if [ -s "$TMPFILE" ]; then
    LINECOUNT=$(wc -l < "$TMPFILE")
    if [ "$LINECOUNT" -gt 3 ]; then
        echo "" >> "$LOGFILE"
        echo "### 自动调研: $DATE" >> "$LOGFILE"
        echo "采集样本 $LINECOUNT 条" >> "$LOGFILE"
        cat "$TMPFILE" >> "$LOGFILE"
    fi
fi

rm -f "$TMPFILE"
