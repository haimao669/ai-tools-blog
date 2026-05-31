# 🚀 部署指南 - AI工具社

## 前置条件

1. GitHub账号（免费）
2. Cloudflare账号（免费）

## 步骤1：创建GitHub Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 名称：`hermes-agent`
4. 勾选权限：
   - ✅ `repo` (完整仓库访问)
   - ✅ `workflow` (GitHub Actions)
5. 点击 "Generate token"
6. **复制token**（只显示一次）

## 步骤2：配置Git认证

在终端运行：

```bash
# 设置GitHub用户名和邮箱
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的邮箱@example.com"

# 存储凭据
git config --global credential.helper store

# 测试认证
cd /c/Users/76277/ai-tools-blog
git remote add origin https://github.com/你的用户名/ai-tools-blog.git
git push -u origin master
# 输入用户名和token（不是密码）
```

## 步骤3：创建GitHub仓库

1. 访问：https://github.com/new
2. 仓库名：`ai-tools-blog`
3. 设为 **Public**（免费使用Cloudflare Pages）
4. 不要初始化README
5. 点击 "Create repository"

## 步骤4：推送代码

```bash
cd /c/Users/76277/ai-tools-blog
git remote add origin https://github.com/你的用户名/ai-tools-blog.git
git push -u origin master
```

## 步骤5：配置Cloudflare Pages

1. 访问：https://dash.cloudflare.com/
2. 登录/注册Cloudflare账号
3. 左侧菜单：Workers & Pages
4. 点击 "Create Application"
5. 选择 "Pages"
6. 连接GitHub
7. 选择仓库：`ai-tools-blog`
8. 配置：
   - **Production branch**: `master`
   - **Framework preset**: `Hugo`
   - **Build command**: `hugo --minify`
   - **Build output directory**: `public`
   - **Environment variables**:
     - `HUGO_VERSION`: `0.162.1`
9. 点击 "Save and Deploy"

## 步骤6：访问网站

部署完成后，Cloudflare会分配一个域名：
```
https://ai-tools-blog.pages.dev
```

## 自动化部署

配置完成后，每次 `git push` 都会自动部署！

## 常用命令

```bash
# 生成5篇文章并提交
./scripts/publish.sh 5

# 生成单篇文章
source scripts/set_env.sh
$PYTHON scripts/generate_one.py

# 本地预览
hugo server -D

# 构建并提交
hugo --minify && git add -A && git commit -m "更新内容" && git push
```

## 故障排除

### Git push失败
- 检查token是否正确
- 检查仓库权限
- 运行 `git credential reject` 清除缓存

### Cloudflare构建失败
- 检查Hugo版本设置
- 查看构建日志
- 确保build output是 `public`

### 文章不显示
- 检查 `draft: false`
- 检查日期格式
- 运行 `hugo --minify` 本地测试
