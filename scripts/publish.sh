#!/bin/bash
# AI工具社 - 自动发布脚本（含GitHub推送）
# 生成文章 + 构建 + 提交到Git + 推送到GitHub

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
git commit -m "feat: 自动生成 $NUM_ARTICLES 篇AI工具文章 ($TIMESTAMP)" 2>&1 || echo "没有新的更改需要提交"

# 推送到GitHub
echo ""
echo "☁️ 推送到GitHub..."
git push origin master:main 2>&1 || echo "推送失败，请检查GitHub配置"

echo ""
echo "========================================"
echo "✅ 发布流程完成！"
echo "📊 共生成 $NUM_ARTICLES 篇文章"
echo "🌐 GitHub: https://github.com/haimao669/ai-tools-blog"
echo "☁️ Cloudflare Pages: https://ai-tools-blog.pages.dev"
echo "========================================"
