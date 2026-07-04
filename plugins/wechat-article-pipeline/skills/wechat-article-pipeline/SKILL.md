---
name: wechat-article-pipeline
description: End-to-end WeChat Official Account article production pipeline. Use when the user wants Codex to turn a confirmed topic, Gmail topic radar email, GitHub repository, paper, URL, or local materials into a researched WeChat article with evidence, Baoyu-style cover/body visuals, humanized polish, QA, and publishing to the WeChat Official Account draft box. Trigger for Chinese requests such as 公众号文章自动撰写到发布, 选题确认后自动执行, 推送到公众号草稿箱, 微信公众号文章配图, 从 Gmail 选题写文章, or GitHub 仓库转公众号.
---

# WeChat Article Pipeline

This skill runs a reusable WeChat article production pipeline. Its control rule is:

> The user confirms the topic plan once. After that, continue autonomously until the WeChat draft is created, unless a hard blocker appears.

Hard blockers only:
- missing credentials or unusable publishing config
- missing source access that cannot be reconstructed
- insufficient evidence for the article's main claim
- image generation or publishing tools unavailable after one retry
- user asks to pause or change direction

## Required References

Read these only when executing the corresponding phase:

- `references/pipeline.md` for the full phase checklist and artifacts.
- `references/visual-rules.md` before any cover/body image work.
- `references/quality-gates.md` before publishing.

## Autopilot Contract

1. Produce a concise topic plan first: angle, audience, source list, expected visuals, risk notes.
2. Ask the user to confirm or revise that plan.
3. Once confirmed, do not ask for style, image preset, title, density, or publishing method again. Choose defaults using this skill.
4. Keep short progress updates, but do not stop after intermediate artifacts.
5. Publish to WeChat draft box when quality gates pass.
6. Final response must include draft `media_id`, article path, cover path, skills/tools used, and any unverified conclusions.

## Default Pipeline Choices

- Article language: Simplified Chinese.
- Writing voice: clear, human, business/technology WeChat essay.
- Evidence standard: claims must be marked as verified, reasonable inference, unverified, or do not publish.
- Title standard: choose a title with either depth or clear open-rate pull; avoid stale AI slogans.
- Cover: Baoyu-style cover image; no dense text by default.
- Body visuals: Baoyu-style explanatory illustrations plus original paper/product screenshots when relevant.
- Publishing: use project wrapper if available: `tools/github-to-wechat/publish-markdown-to-wechat.ps1`; otherwise call the bundled `scripts/publish_wechat_draft.ps1`.

## Baoyu Visual Compliance

For every generated body illustration:

- Create `{topic_dir}/imgs/outline.md` before generation.
- Create one prompt file per image under `{topic_dir}/imgs/prompts/`.
- Each prompt must contain `LAYOUT`, `ZONES` or `STRUCTURE`, `LABELS`, `COLORS`, `STYLE`, and `ASPECT`.
- `LABELS` must include article-specific terms, numbers, metrics, or short claims.
- Do not publish if generated illustrations are merely glossy/decorative and do not explain the article.

Codex native `image_gen` is allowed and preferred as the image backend. That does not replace Baoyu compliance; the prompt and artifacts must still follow the Baoyu workflow above.

## Helper Scripts

Scripts live in this plugin's `scripts/` directory:

- `preflight.ps1` checks runtime, credentials, known project skills, and publishing config.
- `new_topic_workspace.py` creates a standard topic directory.
- `extract_pdf_assets.py` extracts PDF text and selected chart/page crops.
- `validate_article_assets.py` checks markdown image paths and required visual artifacts.
- `publish_wechat_draft.ps1` publishes markdown to the WeChat draft box via local project wrappers or Baoyu API scripts.

Prefer these scripts over retyping equivalent checks.

## Completion Bar

Do not claim completion until:

- source material was read beyond summaries/readme when applicable
- evidence register exists
- article draft exists
- humanization pass was applied
- Baoyu outline and prompt files exist for generated visuals
- image paths validate
- publishing returns success and `media_id`
