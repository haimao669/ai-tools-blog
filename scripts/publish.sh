#!/bin/bash
# AI工具社 - 自动发布脚本
# 生成文章 + 构建 + 提交到Git

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# 设置环境变量
source "$SCRIPT_DIR/set_env.sh"

echo "🚀 AI工具社 - 自动发布流程开始"
echo "================================"

# 生成指定数量的文章（默认5篇）
NUM_ARTICLES=${1:-5}

for i in $(seq 1 $NUM_ARTICLES); do
    echo ""
    echo "📝 生成第 $i/$NUM_ARTICLES 篇文章..."
    $PYTHON "$SCRIPT_DIR/generate_one.py"
    
    # 随机等待1-3秒，避免API限制
    sleep $((RANDOM % 3 + 1))
done

# 构建Hugo站点
echo ""
echo "🔨 构建Hugo站点..."
hugo --minify 2>&1

# Git提交
echo ""
echo "📦 提交到Git..."
git add -A
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "feat: 新增 $NUM_ARTICLES 篇AI工具文章 ($TIMESTAMP)" 2>&1 || echo "没有新的更改需要提交"

echo ""
echo "✅ 发布流程完成！共生成 $NUM_ARTICLES 篇文章"
echo "💡 如需推送到GitHub，请运行: git push"
