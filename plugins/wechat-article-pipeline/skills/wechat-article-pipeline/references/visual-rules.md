# Visual Rules

## Visual Inventory

Before image generation, write `imgs/outline.md`.

Each entry must include:
- position in article
- purpose
- visual content
- type application
- style
- palette
- filename

## Cover Defaults

Use `baoyu-cover-image` logic:
- type: `metaphor`, `conceptual`, or `typography`, selected by article tension
- palette: `macaron`, `elegant`, or `mono`, selected by topic
- rendering: `hand-drawn`, `flat-vector`, or `screen-print`
- text: `none` or `title-only`; prefer `none` when Chinese text may distort
- aspect: `2.35:1` for WeChat cover

The cover must communicate the article promise or tension. It must not be generic AI decoration.

## Body Illustration Defaults

Use `baoyu-article-illustrator` logic. Prefer these presets:

- Research/data summary: `hand-drawn-edu` (`infographic + sketch-notes + macaron`)
- Before/after or old/new comparison: `ink-notes-compare` (`comparison + ink-notes + mono-ink`)
- Organizational mechanism/framework: `ink-notes-framework` (`framework + ink-notes + mono-ink`)
- Workflow/process: `hand-drawn-edu-flow` or `ink-notes-flow`
- Technical architecture: `system-design` or `tech-explainer`

## Required Prompt Shape

Each generated body image prompt must include:

```text
LAYOUT or STRUCTURE:
ZONES / STEPS / NODES:
LABELS:
COLORS:
STYLE:
ASPECT:
Avoid:
```

`LABELS` must contain actual article-specific terms, numbers, metrics, or short claims.

Bad:
- "show adoption, retention, cost"

Good:
- "+216% 尝试信号"
- "+24.0% 不是业务价值"
- "Token / 返工 / 合规"

## Original Evidence Images

When the source is a paper, report, product, or repo UI:
- preserve important original charts/screenshots
- crop for readability
- explain in Chinese immediately below the image
- do not replace evidence charts with generated illustrations

## Rejection Criteria

Reject and regenerate if:
- the image is only glossy or decorative
- the image could fit any AI article
- the central claim is not visually explained
- text is unreadable or garbled beyond quick scanning
- composition is cropped or crowded
- fake UI replaces a real UI screenshot
- every image uses the same layout/palette

## Backend Rule

Codex native `image_gen` is the preferred renderer when available. It is only the renderer; Baoyu compliance is measured by outline, prompt structure, placement, and review.
