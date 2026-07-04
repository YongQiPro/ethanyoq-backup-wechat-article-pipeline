# Pipeline

## Phase 0: Topic Plan Gate

Create a plan and wait for user confirmation.

Plan must include:
- proposed title direction, not final title
- target reader
- core thesis
- source list and what must be verified
- visual inventory: cover, original evidence images, generated explanatory images
- risk notes
- expected output directory

After confirmation, enter Autopilot. Do not ask more preference questions unless blocked.

## Phase 1: Workspace

Create:

```text
docs/content-agent/topics/<slug>/
  sources/
  extracted/
  imgs/
    prompts/
  prompts/
```

Use `scripts/new_topic_workspace.py` when possible.

## Phase 2: Source Intake

Minimum source rules:
- Gmail topic: read the full email/thread, not only the snippet.
- GitHub repo: clone/read code or fetch repo files beyond README.
- Paper: download/read PDF or full HTML, not only abstract.
- News/company source: verify with primary or reputable source.

Write `source-ledger.md` or include source section in `evidence-register.md`.

## Phase 3: Evidence Register

Create `evidence-register.md`.

Every public claim must be one of:
- Verified
- Reasonable inference
- Unverified
- Do not publish

Separate facts from interpretations. If evidence is weak, rewrite the article angle instead of overstating.

## Phase 4: Draft

Create `wechat-draft.md` with frontmatter:

```yaml
---
title: ...
author: ...
description: ...
coverImage: imgs/<cover>.png
sourceUrl: ...
---
```

Draft requirements:
- clear opening hook
- reader problem first, source details second
- cite original paper/product charts when useful
- explain charts in Chinese
- avoid English jargon unless necessary
- avoid stale AI slogans
- do not turn proxy metrics into business value claims

## Phase 5: Humanization

Apply a Chinese humanization pass:
- remove generic AI phrasing
- reduce "不是 X，而是 Y" overuse
- vary paragraph rhythm
- keep evidence intact
- preserve author opinion

## Phase 6: Visuals

Read `visual-rules.md`.

Generate:
- cover image
- Baoyu body explanatory images
- original evidence images from paper/product/repo when applicable

Required files:
- `imgs/outline.md`
- `imgs/prompts/*.md`
- generated `imgs/*.png`

## Phase 7: QA

Read `quality-gates.md`.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File <plugin>/scripts/preflight.ps1 -ProjectRoot <root>
python <plugin>/scripts/validate_article_assets.py <article.md>
```

Fix failures before publishing.

## Phase 8: Publish

Prefer project wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File tools/github-to-wechat/publish-markdown-to-wechat.ps1 `
  -Article <article.md> `
  -Cover <cover.png> `
  -SourceUrl <url>
```

Fallback:

```powershell
powershell -ExecutionPolicy Bypass -File <plugin>/scripts/publish_wechat_draft.ps1 `
  -ProjectRoot <root> `
  -Article <article.md> `
  -Cover <cover.png> `
  -SourceUrl <url>
```

Capture `media_id`.

## Phase 9: Final Report

Report:
- title
- `media_id`
- article path
- cover path
- visual count and source/evidence images
- unverified conclusions or residual risks
- plugin artifacts used
