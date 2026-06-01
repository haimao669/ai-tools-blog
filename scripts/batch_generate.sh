#!/bin/bash
# 批量生成文章脚本
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

source "$SCRIPT_DIR/set_env.sh"

NUM=${1:-35}
echo "🚀 开始批量生成 $NUM 篇文章..."
echo "================================"

SUCCESS=0
FAIL=0

for i in $(seq 1 $NUM); do
    echo ""
    echo "[$i/$NUM] 生成中..."
    if $PYTHON "$SCRIPT_DIR/generate_one.py" 2>&1; then
        SUCCESS=$((SUCCESS + 1))
    else
        FAIL=$((FAIL + 1))
        echo "⚠️ 第 $i 篇生成失败，继续..."
    fi
    # 短暂间隔避免API过载
    sleep 1
done

echo ""
echo "================================"
echo "✅ 批量生成完成！"
echo "   成功: $SUCCESS 篇"
echo "   失败: $FAIL 篇"
echo "================================"
