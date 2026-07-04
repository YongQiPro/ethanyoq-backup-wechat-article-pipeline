# WeChat Article Pipeline

[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-111827?logo=openai&logoColor=white)](#安装)
[![微信公众号](https://img.shields.io/badge/WeChat-Official%20Account-07C160?logo=wechat&logoColor=white)](#发布模式)
[![Baoyu 配图流程](https://img.shields.io/badge/Baoyu-Visual%20Workflow-2563EB)](#配图质量)
[![License: MIT](https://img.shields.io/badge/License-MIT-111827.svg)](LICENSE)

一个 Codex 插件：从选题确认开始，自动完成资料阅读、证据整理、公众号文章撰写、去 AI 味润色、Baoyu 风格配图、质量校验，并推送到微信公众号草稿箱。

English docs: [README.md](README.md)

## 它解决什么问题

公众号文章不是把资料总结一下就结束。尤其是科技、商业、AI 落地类文章，真正耗时间的是：

- 读完整材料，而不是只看摘要、README 或邮件片段
- 区分事实、推断和不能发布的结论
- 写出面向读者的角度，而不是论文复述
- 把原论文或产品里的关键图表提取出来，并用中文解释
- 生成符合文章内容的封面和正文配图，而不是泛泛的精美图片
- 最后把 Markdown、图片和封面推进微信公众号草稿箱

`wechat-article-pipeline` 把这些步骤固化成一个可复用的 Codex 插件。

## 适合谁

适合用 Codex 做中文公众号内容生产的人，尤其是：

- 从 Gmail 自动选题邮件里写文章
- 把 GitHub 仓库写成公众号文章
- 解读 arXiv 论文、PDF、技术报告
- 写 AI 落地、产品、商业分析类文章
- 需要稳定生成公众号封面和正文解释图

## 安装

克隆这个仓库后，把仓库根目录加入 Codex 插件市场：

```powershell
codex plugin marketplace add "<repo-root>"
codex plugin add wechat-article-pipeline@wechat-content-workflow
```

`<repo-root>` 是包含 `.agents/plugins/marketplace.json` 的目录。

安装后建议新开一个 Codex 线程，让插件和 skill 列表重新加载。

## 需要提前配置什么

不同发布模式需要的配置不一样。**服务器不是必需条件**。

| 能力 | 什么时候需要 | 配置 |
|---|---|---|
| Codex 插件运行环境 | 必须 | 安装并启用本插件 |
| Python | 本地辅助脚本 | 建议 Python 3.10+ |
| Node.js 或 Bun | 微信 API 发布脚本 | Node.js 18+ 或 Bun |
| 生图能力 | 封面和正文配图 | Codex 原生生图，或兼容的图片 API 后端 |
| 微信公众号 API | API 发布时 | `WECHAT_APP_ID`、`WECHAT_APP_SECRET` |
| 微信 IP 白名单 | API 发布时 | 把本机或服务器公网 IP 加入公众号后台白名单 |
| Gmail 授权 | 从 Gmail 选题雷达读取选题时 | Gmail Connector 或 OAuth 授权 |
| GitHub 授权 | 私有仓库时 | GitHub CLI 登录、Token 或 SSH Key |
| PDF 图表提取 | 论文/PDF 工作流 | Python 包 `pymupdf` |

## 发布模式

| 模式 | 需要微信 Key | 需要服务器 | 适合场景 |
|---|---:|---:|---|
| `browser` | 否 | 否 | 通过已登录浏览器半自动发布，可能需要扫码 |
| `api-local` | 是 | 否 | 本机公网 IP 可以加入微信 API 白名单 |
| `remote-api` | 是 | 是 | 通过固定公网 IP 的服务器稳定调用微信 API |

当前原始流程使用的是 `remote-api`，所以会涉及服务器 SSH Key。但这是你的本地选择，不是插件对所有人的强制要求。

## 环境变量

API 发布需要：

```env
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

远程发布还需要：

```yaml
default_publish_method: remote-api
remote_publish_host: your.server.example
remote_publish_user: root
remote_publish_port: 22
remote_publish_identity_file: C:/path/to/private-key.pem
```

不要把真实 `.env`、私钥、AppSecret 提交到 GitHub。

## 配图质量

这个插件的重点不是“用哪个模型生图”，而是**强制图片遵守 Baoyu 配图流程**：

- 生成图片前必须先写 `imgs/outline.md`
- 每张生成图必须有独立 prompt 文件
- prompt 必须包含布局、结构分区、标签、颜色、风格和比例
- 标签必须来自文章里的具体观点、指标、数字或概念
- 不能用只有质感、没有解释作用的装饰图糊弄过去

Codex 可以负责生成图片，但图片的规划、提示词和验收必须按 Baoyu 规则走。

## 基本用法

1. 让 Codex 使用 `wechat-article-pipeline`
2. 给出选题、Gmail 邮件、GitHub 仓库、论文、URL 或本地资料
3. Codex 先生成选题计划，等待你确认
4. 你确认后，后续自动运行到公众号草稿箱
5. 最终返回草稿 `media_id`、文章路径、封面路径和未证实结论

示例：

```text
用 wechat-article-pipeline 把今天 Gmail 里的选题一写成公众号文章，阅读论文后保留关键图表并推送草稿箱。
```

```text
用 wechat-article-pipeline 把这个 GitHub 仓库写成公众号文章，生成 Baoyu 风格封面和正文配图，并推送草稿箱。
```

## GitHub SEO 建议

建议仓库描述：

```text
Codex plugin for Chinese WeChat article writing, Baoyu-style visuals, evidence-based drafting, and Official Account draft publishing.
```

建议 Topics：

```text
codex-plugin, wechat, wechat-official-account, wechat-mp, ai-writing, content-automation, baoyu, chinese-writing, github-to-wechat, research-writing
```

不要写未经验证的流量、转化率、排名、成功率等承诺。

## 许可证

MIT
