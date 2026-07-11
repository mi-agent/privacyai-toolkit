# GitHub 推送指南 - 请按以下步骤操作

## 方法1：GitHub CLI（推荐，2分钟）

在你的终端运行：

```bash
# 1. 登录 GitHub（浏览器弹窗认证）
gh auth login --web

# 2. 创建仓库并推送
cd ~/Projects
gh repo create privacyai-toolkit --public --source=. --push

# 3. 创建内容站仓库
cd ~/Projects/ai-tools-guide
gh repo create ai-tools-guide --public --source=. --push
```

## 方法2：手动 GitHub Web 上传

1. 打开 https://github.com/new
2. 输入仓库名：`privacyai-toolkit`，选 Public，点击 Create
3. 在新仓库页面点击 "uploading an existing file"
4. 拖入 `~/Projects` 下的所有文件（除了 .git 目录）
5. 点击 Commit changes

## 立即操作

请在浏览器中打开 https://github.com 并登录（或注册），然后：

1. 创建 `privacyai-toolkit` 仓库
2. 创建 `ai-tools-guide` 仓库

创建完成后告诉我仓库 URL，我会自动推送代码。

---

## GitHub Pages 开启（在仓库 Settings 中）

创建 `ai-tools-guide` 仓库后：
- Settings → Pages → Source: Deploy from branch → main → Save
- 等待 2 分钟，网站上线

## 下一步变现操作

创建仓库后告诉我，我会帮你：
1. 推送所有代码
2. 开启 GitHub Pages
3. 注册 Gumroad 销售数字产品
4. 申请联盟链接