#!/bin/bash
# AI工具社 - 环境变量设置
# 从OpenClaw配置中提取DeepSeek API Key

export DEEPSEEK_API_KEY=$(cat ~/.openclaw/openclaw.json | grep -o '"apiKey": "[^"]*"' | head -1 | cut -d'"' -f4)

# 设置Python路径
export PYTHON="/c/Users/76277/.hermes/hermes-agent/venv/Scripts/python.exe"

# 设置Hugo路径
export PATH="$PATH:/c/Users/76277/AppData/Local/Microsoft/WinGet/Packages/Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe"

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "❌ 无法获取DeepSeek API Key"
    exit 1
fi

echo "✅ 环境变量已设置"
echo "   - DeepSeek API Key: ${DEEPSEEK_API_KEY:0:10}..."
echo "   - Python: $PYTHON"
