# WeChat Article Pipeline

[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-111827?logo=openai&logoColor=white)](#installation)
[![WeChat Official Account](https://img.shields.io/badge/WeChat-Official%20Account-07C160?logo=wechat&logoColor=white)](#publishing-modes)
[![Baoyu Visual Workflow](https://img.shields.io/badge/Baoyu-Visual%20Workflow-2563EB)](#visual-quality)
[![License: MIT](https://img.shields.io/badge/License-MIT-111827.svg)](LICENSE)

A Codex plugin that turns a confirmed topic into a researched, illustrated, human-polished WeChat Official Account article and pushes it to the WeChat draft box.

It is built for Chinese technology and business writing workflows where the article needs more than a summary: source reading, evidence control, title strategy, Baoyu-style visuals, original paper chart extraction, humanized Chinese editing, and final WeChat draft publishing.

中文文档：[README.zh-CN.md](README.zh-CN.md)

## What It Does

- Reads source material beyond summaries, abstracts, or README files.
- Builds an evidence register before writing.
- Drafts a Chinese WeChat article with a clear reader angle and business insight.
- Applies a humanized Chinese writing pass.
- Forces Baoyu-style cover and article illustration planning before image generation.
- Preserves and explains important original charts from papers or product materials.
- Validates article images and visual prompt artifacts before publishing.
- Publishes the finished article to the WeChat Official Account draft box.

## Who It Is For

This plugin is for creators, researchers, developers, and content operators who use Codex to produce Chinese WeChat Official Account articles from:

- Gmail topic radar emails
- GitHub repositories
- arXiv papers and PDFs
- product documentation
- URLs, reports, and local research materials

## Installation

Clone this repository, then add its local marketplace root to Codex:

```powershell
codex plugin marketplace add "<repo-root>"
codex plugin add wechat-article-pipeline@wechat-content-workflow
```

The marketplace root is the directory that contains `.agents/plugins/marketplace.json`.

After installation, start a new Codex thread so the plugin skill list is reloaded.

## Required Setup

The exact setup depends on how you want to publish.

| Capability | Required For | Configuration |
|---|---|---|
| Codex plugin runtime | All usage | Codex with this plugin installed |
| Python | Workspace helpers | Python 3.10+ recommended |
| Node.js or Bun | WeChat API scripts | Node.js 18+ or Bun |
| Image generation | Cover and body visuals | Codex native image generation, or a compatible image API backend |
| WeChat Official Account API | API publishing | `WECHAT_APP_ID`, `WECHAT_APP_SECRET` |
| WeChat IP whitelist | API publishing | Local or server public IP added in WeChat Official Account backend |
| Gmail access | Gmail topic radar workflow | Gmail connector or OAuth access |
| GitHub access | Private repositories | GitHub CLI login, token, or SSH key |
| PDF extraction | Paper workflows | `pymupdf` Python package |

## Publishing Modes

You do not need a server for every setup.

| Mode | Needs WeChat API Key | Needs Server | Best For |
|---|---:|---:|---|
| `browser` | No | No | Manual or semi-automated publishing through a logged-in browser |
| `api-local` | Yes | No | Users whose local public IP can be added to the WeChat API whitelist |
| `remote-api` | Yes | Yes | Stable publishing through a server with an allowlisted public IP |

The original local workflow uses `remote-api`, but reusable installations can choose `browser` or `api-local` when no server is available.

## Environment Variables

For API publishing:

```env
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

For remote publishing, also configure:

```yaml
default_publish_method: remote-api
remote_publish_host: your.server.example
remote_publish_user: root
remote_publish_port: 22
remote_publish_identity_file: C:/path/to/private-key.pem
```

Do not commit real credentials, private keys, or `.env` files.

## Visual Quality

This plugin intentionally separates image backend from visual direction.

Codex may generate the image, but the article must still follow the Baoyu visual workflow:

- create an image outline before generation
- create one prompt file per generated image
- include layout, zones or structure, labels, color, style, and aspect ratio
- use article-specific claims, metrics, or concepts in the labels
- reject decorative images that do not explain the article

This is designed to prevent generic, glossy images that look polished but do not fit the article.

## Basic Workflow

1. Ask Codex to use `wechat-article-pipeline`.
2. Provide a topic, Gmail radar email, GitHub repository, paper, URL, or local source folder.
3. Codex creates a topic plan and waits for confirmation.
4. After confirmation, Codex runs the pipeline automatically.
5. The final output is a WeChat draft box entry plus local article and image artifacts.

Example prompts:

```text
用 wechat-article-pipeline 把今天 Gmail 里的选题一写成公众号文章，阅读论文后保留关键图表并推送草稿箱。
```

```text
Use wechat-article-pipeline to turn this GitHub repository into a Chinese WeChat article draft with Baoyu-style cover and article visuals.
```

## Repository SEO Notes

Suggested GitHub repository metadata:

- Description: `Codex plugin for Chinese WeChat article writing, Baoyu-style visuals, evidence-based drafting, and Official Account draft publishing.`
- Topics: `codex-plugin`, `wechat`, `wechat-official-account`, `wechat-mp`, `ai-writing`, `content-automation`, `baoyu`, `chinese-writing`, `github-to-wechat`, `research-writing`

Avoid unsupported claims about traffic, conversion, ranking, or publishing success rate unless you have measured evidence.

## License

MIT
