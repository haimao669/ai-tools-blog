#!/usr/bin/env python3
"""
AI工具社 - 单篇文章生成器
每次生成一篇高质量的AI工具文章
"""
import json
import os
import sys
import re
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content" / "posts"

# AI工具数据库
AI_TOOLS = {
    "AI写作": [
        {"name": "ChatGPT", "desc": "OpenAI开发的AI对话助手", "category": "AI写作"},
        {"name": "Claude", "desc": "Anthropic开发的AI助手", "category": "AI写作"},
        {"name": "文心一言", "desc": "百度开发的AI对话工具", "category": "AI写作"},
        {"name": "通义千问", "desc": "阿里巴巴的AI助手", "category": "AI写作"},
        {"name": "Kimi", "desc": "月之暗面的AI助手", "category": "AI写作"},
        {"name": "秘塔写作猫", "desc": "秘塔科技的AI写作工具", "category": "AI写作"},
    ],
    "AI绘画": [
        {"name": "Midjourney", "desc": "最受欢迎的AI绘画工具", "category": "AI绘画"},
        {"name": "DALL-E", "desc": "OpenAI的AI图像生成器", "category": "AI绘画"},
        {"name": "Stable Diffusion", "desc": "开源的AI绘画模型", "category": "AI绘画"},
        {"name": "通义万相", "desc": "阿里巴巴的AI绘画工具", "category": "AI绘画"},
        {"name": "文心一格", "desc": "百度的AI绘画工具", "category": "AI绘画"},
    ],
    "AI编程": [
        {"name": "GitHub Copilot", "desc": "GitHub的AI编程助手", "category": "AI编程"},
        {"name": "Cursor", "desc": "AI原生的代码编辑器", "category": "AI编程"},
        {"name": "通义灵码", "desc": "阿里巴巴的AI编程助手", "category": "AI编程"},
        {"name": "CodeGeeX", "desc": "智谱AI的编程助手", "category": "AI编程"},
    ],
    "AI视频": [
        {"name": "Sora", "desc": "OpenAI的AI视频生成器", "category": "AI视频"},
        {"name": "Runway", "desc": "专业的AI视频编辑工具", "category": "AI视频"},
        {"name": "Pika", "desc": "简单易用的AI视频生成", "category": "AI视频"},
        {"name": "可灵", "desc": "快手的AI视频生成器", "category": "AI视频"},
    ],
    "AI办公": [
        {"name": "Notion AI", "desc": "Notion的AI增强功能", "category": "AI办公"},
        {"name": "Gamma", "desc": "AI生成PPT工具", "category": "AI办公"},
        {"name": "秘塔AI搜索", "desc": "AI搜索引擎", "category": "AI办公"},
        {"name": "Perplexity", "desc": "AI搜索引擎", "category": "AI办公"},
    ],
}

# 文章类型
ARTICLE_TYPES = ["review", "tutorial", "comparison", "listicle"]

def call_deepseek_api(prompt, max_tokens=4000):
    """调用DeepSeek API"""
    import urllib.request
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }
    
    data = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的AI工具评测和教程作者。你的文章专业、详细、易读，适合SEO优化。文章要自然流畅，有个人观点和见解。"},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }).encode("utf-8")
    
    req = urllib.request.Request(DEEPSEEK_API_URL, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API调用失败: {e}", file=sys.stderr)
        return None

def generate_review(tool):
    """生成工具评测文章"""
    prompt = f"""请写一篇关于"{tool['name']}"的详细评测文章。

工具简介：{tool['desc']}

要求：
1. 文章长度：2000-3000字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 工具简介（是什么、谁开发的、主要功能）
   - 核心功能详解（至少3个核心功能，每个功能详细说明）
   - 使用体验（界面设计、易用性、响应速度）
   - 优缺点分析（至少3个优点和2个缺点）
   - 适用人群（哪些人最适合使用）
   - 定价方案（免费版、付费版对比）
   - 与竞品对比（和2-3个同类工具对比）
   - 总结与推荐指数（1-10分，给出明确推荐理由）
5. 写作风格：专业但易读，有个人观点，不要过于广告化
6. 自然融入关键词：{tool['name']}、{tool['category']}、AI工具推荐
7. 在文章末尾添加FAQ部分（3-5个常见问题及解答）

请直接输出Markdown格式的文章内容，不要包含frontmatter。"""

    return call_deepseek_api(prompt)

def generate_tutorial(tool):
    """生成使用教程文章"""
    prompt = f"""请写一篇关于"{tool['name']}"的详细使用教程。

工具简介：{tool['desc']}

要求：
1. 文章长度：2000-3000字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 前言（为什么推荐这个工具，适合什么场景）
   - 注册与安装步骤（详细图文步骤）
   - 基础功能使用（至少3个基础功能的使用方法）
   - 进阶技巧（至少3个实用的高级技巧）
   - 常见问题解答（5个以上常见问题）
   - 总结（使用心得和建议）
5. 写作风格：步骤清晰，实用导向，有操作截图位置标记
6. 自然融入关键词：{tool['name']}教程、{tool['name']}使用方法、{tool['category']}

请直接输出Markdown格式的文章内容，不要包含frontmatter。"""

    return call_deepseek_api(prompt)

def generate_comparison(tool_a, tool_b):
    """生成对比文章"""
    prompt = f"""请写一篇"{tool_a['name']}" vs "{tool_b['name']}"的详细对比文章。

{tool_a['name']}简介：{tool_a['desc']}
{tool_b['name']}简介：{tool_b['desc']}

要求：
1. 文章长度：2500-3500字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 引言（为什么需要对比这两个工具）
   - 工具概览（分别详细介绍）
   - 功能对比表格（至少5个维度的对比）
   - 详细对比分析（每个维度深入分析）
   - 价格对比（各版本价格对比）
   - 使用场景推荐（什么情况选A，什么情况选B）
   - 最终选择建议（给出明确的推荐）
5. 写作风格：客观公正，有数据支撑，有个人见解
6. 自然融入关键词：{tool_a['name']} vs {tool_b['name']}、{tool_a['name']}对比

请直接输出Markdown格式的文章内容，不要包含frontmatter。"""

    return call_deepseek_api(prompt)

def generate_listicle(category, tools):
    """生成推荐列表文章"""
    tools_desc = "\n".join([f"- {t['name']}: {t['desc']}" for t in tools[:8]])
    
    prompt = f"""请写一篇"2026年最佳{category}推荐"的文章。

推荐的工具列表：
{tools_desc}

要求：
1. 文章长度：2500-3500字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 引言（为什么需要{category}，这类工具的发展趋势）
   - 每个工具的详细介绍（包含：简介、核心功能、优缺点、适用场景、推荐指数1-10分）
   - 对比表格（所有工具的核心功能对比）
   - 选择指南（如何根据自己的需求选择）
   - 总结（给出明确的Top 3推荐）
5. 写作风格：实用导向，有明确推荐理由
6. 自然融入关键词：{category}推荐、{category}排行、2026年AI工具

请直接输出Markdown格式的文章内容，不要包含frontmatter。"""

    return call_deepseek_api(prompt)

def create_slug(title):
    """生成URL友好的slug"""
    # 移除中文标点和特殊字符
    slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title)
    # 将空格替换为连字符
    slug = re.sub(r'[\s]+', '-', slug)
    return slug.lower().strip('-')

def create_frontmatter(title, description, categories, tags, keywords):
    """生成Hugo frontmatter"""
    slug = create_slug(title)
    now = datetime.now(timezone(timedelta(hours=8)))
    
    return f"""---
title: "{title}"
date: {now.strftime('%Y-%m-%dT%H:%M:%S+08:00')}
lastmod: {now.strftime('%Y-%m-%dT%H:%M:%S+08:00')}
slug: "{slug}"
description: "{description}"
categories: {json.dumps(categories, ensure_ascii=False)}
tags: {json.dumps(tags, ensure_ascii=False)}
keywords: {json.dumps(keywords, ensure_ascii=False)}
draft: false
ShowToc: true
TocOpen: true
cover:
  image: ""
  alt: "{title}"
  caption: "{title}"
summary: "{description}"
---

"""

def save_article(content, title):
    """保存文章"""
    slug = create_slug(title)
    filename = f"{slug}.md"
    filepath = CONTENT_DIR / filename
    
    # 如果文件已存在，添加时间戳
    if filepath.exists():
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        filename = f"{slug}-{timestamp}.md"
        filepath = CONTENT_DIR / filename
    
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已保存: {filepath.name}")
    return filepath

def main():
    """主函数：随机生成一篇文章"""
    if not DEEPSEEK_API_KEY:
        print("❌ 请设置DEEPSEEK_API_KEY环境变量", file=sys.stderr)
        sys.exit(1)
    
    # 随机选择文章类型和工具
    article_type = random.choice(ARTICLE_TYPES)
    
    if article_type == "review":
        category = random.choice(list(AI_TOOLS.keys()))
        tool = random.choice(AI_TOOLS[category])
        print(f"📝 正在生成: {tool['name']} 评测...")
        content = generate_review(tool)
        title = f"{tool['name']} 详细评测：功能、优缺点与使用体验全解析"
        desc = f"本文详细评测{tool['name']}，包括核心功能、使用体验、优缺点分析、定价方案和竞品对比，帮你判断是否值得使用。"
        cats = ["工具评测", tool['category']]
        tags = [tool['name'], "AI评测", "工具推荐"]
        
    elif article_type == "tutorial":
        category = random.choice(list(AI_TOOLS.keys()))
        tool = random.choice(AI_TOOLS[category])
        print(f"📝 正在生成: {tool['name']} 教程...")
        content = generate_tutorial(tool)
        title = f"{tool['name']} 使用教程：从入门到精通完整指南"
        desc = f"手把手教你使用{tool['name']}，包含注册安装、基础功能、进阶技巧和常见问题解答，适合新手快速上手。"
        cats = ["使用教程", tool['category']]
        tags = [tool['name'], "AI教程", "使用指南"]
        
    elif article_type == "comparison":
        category = random.choice(list(AI_TOOLS.keys()))
        if len(AI_TOOLS[category]) >= 2:
            tool_a, tool_b = random.sample(AI_TOOLS[category], 2)
        else:
            tool_a = AI_TOOLS[category][0]
            tool_b = AI_TOOLS["AI写作"][0]
        print(f"📝 正在生成: {tool_a['name']} vs {tool_b['name']}...")
        content = generate_comparison(tool_a, tool_b)
        title = f"{tool_a['name']} vs {tool_b['name']}：哪个更适合你？深度对比分析"
        desc = f"详细对比{tool_a['name']}和{tool_b['name']}，从功能、价格、易用性等多个维度分析，帮你做出最佳选择。"
        cats = ["对比分析", category]
        tags = [tool_a['name'], tool_b['name'], "工具对比"]
        
    else:  # listicle
        category = random.choice(list(AI_TOOLS.keys()))
        tools = AI_TOOLS[category]
        print(f"📝 正在生成: {category}推荐列表...")
        content = generate_listicle(category, tools)
        title = f"2026年最佳{category}推荐：{len(tools)}款工具深度评测"
        desc = f"精选2026年最值得使用的{category}，详细介绍每个工具的特点、优缺点和适用场景，帮你快速找到最适合的工具。"
        cats = ["工具推荐", category]
        tags = [category, "工具推荐", "2026"]
    
    if not content:
        print("❌ 文章生成失败", file=sys.stderr)
        sys.exit(1)
    
    # 组装完整文章
    full_content = create_frontmatter(title, desc, cats, tags, [title, category, "AI工具"])
    full_content += content
    
    # 保存
    save_article(full_content, title)
    print(f"✅ 文章生成完成: {title}")

if __name__ == "__main__":
    main()
