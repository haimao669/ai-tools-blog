#!/usr/bin/env python3
"""
AI工具社 - 内容生成Pipeline
自动生成SEO优化的AI工具评测文章
"""
import json
import os
import sys
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

# DeepSeek API配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content" / "posts"
KEYWORDS_FILE = PROJECT_ROOT / "scripts" / "keywords.json"

# 文章模板
ARTICLE_TEMPLATES = {
    "review": {
        "name": "工具评测",
        "prompt": """你是一个专业的AI工具评测专家。请写一篇关于"{tool_name}"的详细评测文章。

要求：
1. 文章长度：2000-3000字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 工具简介（是什么、谁开发的、主要功能）
   - 核心功能详解（至少3个核心功能）
   - 使用体验（界面、易用性、速度）
   - 优缺点分析
   - 适用人群
   - 定价方案
   - 与竞品对比
   - 总结与推荐指数（1-10分）
5. 写作风格：专业但易懂，有个人观点
6. 自然融入关键词：{keywords}
7. 在文章末尾添加FAQ部分（3-5个常见问题）

请直接输出Markdown格式的文章内容，不要包含frontmatter。""",
    },
    "tutorial": {
        "name": "使用教程",
        "prompt": """你是一个AI工具教程专家。请写一篇关于"{tool_name}"的详细使用教程。

要求：
1. 文章长度：2000-3000字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 前言（为什么需要这个工具）
   - 注册与安装步骤
   - 基础功能使用（图文步骤）
   - 进阶技巧（至少3个实用技巧）
   - 常见问题解答
   - 总结
5. 写作风格：步骤清晰，有截图描述位置标记
6. 自然融入关键词：{keywords}
7. 使用编号列表描述步骤

请直接输出Markdown格式的文章内容，不要包含frontmatter。""",
    },
    "comparison": {
        "name": "对比分析",
        "prompt": """你是一个AI工具对比分析专家。请写一篇"{tool_a}" vs "{tool_b}"的详细对比文章。

要求：
1. 文章长度：2500-3500字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 引言（为什么需要对比这两个工具）
   - 工具概览（分别介绍）
   - 功能对比表格
   - 详细对比分析（至少5个维度）
   - 价格对比
   - 使用场景推荐
   - 最终选择建议
5. 写作风格：客观公正，有数据支撑
6. 自然融入关键词：{keywords}
7. 使用对比表格

请直接输出Markdown格式的文章内容，不要包含frontmatter。""",
    },
    "listicle": {
        "name": "推荐列表",
        "prompt": """你是一个AI工具推荐专家。请写一篇"{topic}"的推荐文章。

要求：
1. 文章长度：2500-3500字
2. 语言：中文
3. 结构清晰，使用H2/H3标题
4. 包含以下部分：
   - 引言（为什么需要这类工具）
   - 推荐工具列表（至少7个工具）
   - 每个工具包含：简介、核心功能、优缺点、适用场景、推荐指数
   - 选择指南（如何根据需求选择）
   - 总结
5. 写作风格：实用导向，有明确推荐
7. 自然融入关键词：{keywords}
8. 使用编号列表

请直接输出Markdown格式的文章内容，不要包含frontmatter。""",
    },
}

def load_keywords():
    """加载关键词库"""
    if KEYWORDS_FILE.exists():
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return generate_default_keywords()

def generate_default_keywords():
    """生成默认关键词库"""
    keywords = {
        "ai_writing": [
            "AI写作工具", "AI写作助手", "AI写作软件", "AI写文章",
            "AI文案生成", "AI内容创作", "AI写作免费", "AI写作哪个好",
        ],
        "ai_image": [
            "AI绘画工具", "AI绘画软件", "AI画图", "AI生成图片",
            "AI绘画免费", "AI绘画教程", "Midjourney替代", "Stable Diffusion教程",
        ],
        "ai_code": [
            "AI编程工具", "AI编程助手", "AI写代码", "AI代码生成",
            "GitHub Copilot替代", "AI编程免费", "Cursor IDE", "AI代码补全",
        ],
        "ai_video": [
            "AI视频工具", "AI视频生成", "AI视频编辑", "AI视频制作",
            "Sora替代", "AI视频免费", "AI视频教程", "AI生成短视频",
        ],
        "ai_office": [
            "AI办公工具", "AI效率工具", "AI做PPT", "AI表格处理",
            "AI会议记录", "AI翻译工具", "AI总结工具", "AI办公自动化",
        ],
        "tools_general": [
            "AI工具推荐", "AI工具大全", "免费AI工具", "最好用的AI工具",
            "AI工具对比", "2026年AI工具", "AI工具评测", "AI工具排行榜",
        ],
    }
    
    # 保存到文件
    KEYWORDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)
    
    return keywords

def generate_article(prompt, max_tokens=4000):
    """调用DeepSeek API生成文章"""
    import urllib.request
    import urllib.error
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }
    
    data = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的AI工具评测和教程作者。你的文章专业、详细、易读，适合SEO优化。"},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9,
    }).encode("utf-8")
    
    req = urllib.request.Request(DEEPSEEK_API_URL, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API调用失败: {e}", file=sys.stderr)
        return None

def create_slug(title):
    """生成URL友好的slug"""
    # 移除特殊字符，保留中文和英文
    slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title)
    slug = re.sub(r'[\s]+', '-', slug)
    return slug.lower().strip('-')

def create_frontmatter(title, description, categories, tags, keywords, article_type):
    """生成Hugo frontmatter"""
    slug = create_slug(title)
    now = datetime.now(timezone(timedelta(hours=8)))
    
    frontmatter = f"""---
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
    return frontmatter

def generate_review_article(tool_name, keywords):
    """生成工具评测文章"""
    template = ARTICLE_TEMPLATES["review"]
    prompt = template["prompt"].format(
        tool_name=tool_name,
        keywords=", ".join(keywords[:5]),
    )
    
    content = generate_article(prompt)
    if not content:
        return None
    
    title = f"{tool_name} 详细评测：功能、优缺点与使用体验全解析"
    description = f"本文详细评测{tool_name}，包括核心功能、使用体验、优缺点分析、定价方案和竞品对比，帮你判断是否值得使用。"
    
    categories = ["工具评测", "AI工具"]
    tags = [tool_name, "AI评测", "工具推荐"]
    
    frontmatter = create_frontmatter(title, description, categories, tags, keywords, "review")
    return frontmatter + content

def generate_tutorial_article(tool_name, keywords):
    """生成使用教程文章"""
    template = ARTICLE_TEMPLATES["tutorial"]
    prompt = template["prompt"].format(
        tool_name=tool_name,
        keywords=", ".join(keywords[:5]),
    )
    
    content = generate_article(prompt)
    if not content:
        return None
    
    title = f"{tool_name} 使用教程：从入门到精通完整指南"
    description = f"手把手教你使用{tool_name}，包含注册安装、基础功能、进阶技巧和常见问题解答，适合新手快速上手。"
    
    categories = ["使用教程", "AI教程"]
    tags = [tool_name, "AI教程", "使用指南"]
    
    frontmatter = create_frontmatter(title, description, categories, tags, keywords, "tutorial")
    return frontmatter + content

def generate_comparison_article(tool_a, tool_b, keywords):
    """生成对比文章"""
    template = ARTICLE_TEMPLATES["comparison"]
    prompt = template["prompt"].format(
        tool_a=tool_a,
        tool_b=tool_b,
        keywords=", ".join(keywords[:5]),
    )
    
    content = generate_article(prompt)
    if not content:
        return None
    
    title = f"{tool_a} vs {tool_b}：哪个更适合你？深度对比分析"
    description = f"详细对比{tool_a}和{tool_b}，从功能、价格、易用性等多个维度分析，帮你做出最佳选择。"
    
    categories = ["对比分析", "AI工具"]
    tags = [tool_a, tool_b, "工具对比"]
    
    frontmatter = create_frontmatter(title, description, categories, tags, keywords, "comparison")
    return frontmatter + content

def generate_listicle_article(topic, keywords):
    """生成推荐列表文章"""
    template = ARTICLE_TEMPLATES["listicle"]
    prompt = template["prompt"].format(
        topic=topic,
        keywords=", ".join(keywords[:5]),
    )
    
    content = generate_article(prompt)
    if not content:
        return None
    
    title = f"{topic}：2026年最值得使用的工具推荐"
    description = f"精选{topic}，详细介绍每个工具的特点、优缺点和适用场景，帮你快速找到最适合的工具。"
    
    categories = ["工具推荐", "AI工具"]
    tags = [topic, "工具推荐", "2026"]
    
    frontmatter = create_frontmatter(title, description, categories, tags, keywords, "listicle")
    return frontmatter + content

def save_article(content, title):
    """保存文章到content/posts目录"""
    slug = create_slug(title)
    filename = f"{slug}.md"
    filepath = CONTENT_DIR / filename
    
    # 确保目录存在
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 文章已保存: {filepath}")
    return filepath

def main():
    """主函数：生成一批文章"""
    if not DEEPSEEK_API_KEY:
        print("❌ 请设置DEEPSEEK_API_KEY环境变量", file=sys.stderr)
        sys.exit(1)
    
    # 加载关键词
    keywords = load_keywords()
    all_keywords = []
    for category_keywords in keywords.values():
        all_keywords.extend(category_keywords)
    
    # 要评测的AI工具列表
    tools_to_review = [
        "ChatGPT",
        "Claude",
        "Midjourney",
        "Cursor",
        "Notion AI",
        "Gamma",
        "Perplexity",
        "秘塔AI搜索",
    ]
    
    # 生成文章
    articles_generated = 0
    
    for tool in tools_to_review:
        print(f"\n📝 正在生成: {tool} 评测文章...")
        content = generate_review_article(tool, all_keywords)
        if content:
            save_article(content, f"{tool} 详细评测")
            articles_generated += 1
        
        print(f"📝 正在生成: {tool} 教程文章...")
        content = generate_tutorial_article(tool, all_keywords)
        if content:
            save_article(content, f"{tool} 使用教程")
            articles_generated += 1
    
    # 生成对比文章
    comparisons = [
        ("ChatGPT", "Claude"),
        ("Midjourney", "DALL-E"),
        ("Cursor", "GitHub Copilot"),
    ]
    
    for tool_a, tool_b in comparisons:
        print(f"\n📝 正在生成: {tool_a} vs {tool_b}...")
        content = generate_comparison_article(tool_a, tool_b, all_keywords)
        if content:
            save_article(content, f"{tool_a} vs {tool_b}")
            articles_generated += 1
    
    # 生成推荐列表
    listicle_topics = [
        "2026年最佳AI写作工具",
        "2026年最佳AI绘画工具",
        "2026年最佳AI编程助手",
    ]
    
    for topic in listicle_topics:
        print(f"\n📝 正在生成: {topic}...")
        content = generate_listicle_article(topic, all_keywords)
        if content:
            save_article(content, topic)
            articles_generated += 1
    
    print(f"\n✅ 本次生成完成：共生成 {articles_generated} 篇文章")
    return articles_generated

if __name__ == "__main__":
    main()
